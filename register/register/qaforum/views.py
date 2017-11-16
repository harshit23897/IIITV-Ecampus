import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, UpdateView, View
from hitcount.views import HitCountDetailView
from register.qaforum.models import (QaAnswer, QaAnswerComment, QaQuestion,
                       QaQuestionComment)
from taggit.models import Tag, TaggedItem

from .forms import QaQuestionForm
from .mixins import AuthorRequiredMixin, LoginRequired
from .utils import question_score
from django.contrib.auth.models import User

try:
    qaforum_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and\
        settings.QAFORUM_SETTINGS['qaforum_messages']

except AttributeError:  # pragma: no cover
    qaforum_messages = False

if qaforum_messages:
    from django.contrib import messages


"""Dear maintainer:

Once you are done trying to 'optimize' this routine, and have realized what a
terrible mistake that was, please increment the following counter as a warning
to the next guy:

total_hours_wasted_here = 2
"""


class QaAnswerQuestionView(LoginRequired, View):
    """
    View to select an answer as the satisfying answer to the question,
    validating than the user who created que
    question is the only one allowed to make those changes.
    """
    model = QaAnswer

    def post(self, request, answer_id):
        answer = get_object_or_404(self.model, pk=answer_id)
        if answer.question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question.")

        else:
            answer.question.answer_set.update(answer=False)
            answer.answer = True
            answer.save()


        next_url = request.POST.get('next', '')
        if next_url is not '':
            return redirect(next_url)

        else:
            return reverse('qaforum:qaforum_index')


class QaCloseQuestionView(LoginRequired, View):
    """View to
    mark the question as closed, validating than the user who created que
    question is the only one allowed to make those changes.
    """
    model = QaQuestion

    def post(self, request, question_id):
        question = get_object_or_404(self.model, pk=question_id)
        if question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question.")
        else:
            if not question.closed:
                question.closed = True

            else:
                raise ValidationError("Sorry, this question is already closed")

            question.save()

        next_url = request.POST.get('next', '')
        if next_url is not '':
            return redirect(next_url)

        else:
            return reverse('qaforum:qaforum_index')


class QaQuestionIndexView(ListView):
    """CBV to render the index view
    """
    model = QaQuestion
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qaforum/index.html'
    ordering = '-pub_date'

    def get_context_data(self, *args, **kwargs):
        context = super(
            QaQuestionIndexView, self).get_context_data(*args, **kwargs)
        noans = QaQuestion.objects.order_by('-pub_date').filter(
            qaanswer__isnull=True).select_related('user')\
            .annotate(num_answers=Count('qaanswer', distinct=True),
                      num_question_comments=Count('qaquestioncomment',
                      distinct=True))
        context['totalcount'] = QaQuestion.objects.count()
        context['anscount'] = QaAnswer.objects.count()
        paginator = Paginator(noans, 10)
        page = self.request.GET.get('noans_page')
        context['active_tab'] = self.request.GET.get('active_tab', 'latest')
        tabs = ['latest', 'unans']
        context['active_tab'] = 'latest' if context['active_tab'] not in\
            tabs else context['active_tab']
        try:
            noans = paginator.page(page)

        except PageNotAnInteger:
            noans = paginator.page(1)

        except EmptyPage:  # pragma: no cover
            noans = paginator.page(paginator.num_pages)

        context['totalnoans'] = paginator.count
        context['noans'] = noans

        question_contenttype = ContentType.objects.get_for_model(QaQuestion)
        items = TaggedItem.objects.filter(content_type=question_contenttype)
        context['tags'] = Tag.objects.filter(
            taggit_taggeditem_items__in=items).order_by('-id').distinct()[:10]

        return context

    def get_queryset(self):
        queryset = super(QaQuestionIndexView, self).get_queryset()\
            .select_related('user')\
            .annotate(num_answers=Count('qaanswer', distinct=True),
                      num_question_comments=Count('qaquestioncomment',
                      distinct=True))
        return queryset


class QaQuestionsSearchView(QaQuestionIndexView):
    """
    Display a ListView page inherithed from the QuestionIndexView filtered by
    the search query and sorted by the different elements aggregated.
    """

    def get_queryset(self):
        result = super(QaQuestionsSearchView, self).get_queryset()
        query = self.request.GET.get('word', '')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)))

        return result

    def get_context_data(self, *args, **kwargs):
        context = super(
            QaQuestionsSearchView, self).get_context_data(*args, **kwargs)
        context['totalcount'] = QaQuestion.objects.count
        context['anscount'] = QaAnswer.objects.count
        context['noans'] = QaQuestion.objects.order_by('-pub_date').filter(
            qaanswer__isnull=True)[:10]

        return context


class QaQuestionsByTagView(ListView):
    """View to call all the questions clasiffied under one specific tag.
    """
    model = QaQuestion
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qaforum/index.html'

    def get_queryset(self, **kwargs):
        return QaQuestion.objects.filter(tags__slug=self.kwargs['tag'])

    def get_context_data(self, *args, **kwargs):
        context = super(
            QaQuestionsByTagView, self).get_context_data(*args, **kwargs)
        context['active_tab'] = self.request.GET.get('active_tab', 'latest')
        tabs = ['latest', 'unans']
        context['active_tab'] = 'latest' if context['active_tab'] not in\
            tabs else context['active_tab']
        context['totalcount'] = QaQuestion.objects.count
        context['anscount'] = QaAnswer.objects.count
        context['noans'] = QaQuestion.objects.order_by('-pub_date').filter(
            tags__name__contains=self.kwargs['tag'], qaanswer__isnull=True)[:10]


        context['totalnoans'] = len(context['noans'])
        return context


class QaCreateQuestionView(LoginRequired, CreateView):
    """
    View to handle the creation of a new question
    """
    template_name = 'qaforum/create_question.html'
    message = _('Thank you! your question has been created.')
    form_class = QaQuestionForm

    def form_valid(self, form):
        """
        Create the required relation
        """
        form.instance.user = self.request.user
        return super(QaCreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qaforum_messages:
            messages.success(self.request, self.message)

        return reverse('qaforum:qaforum_index')


class QaUpdateQuestionView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question
    """
    template_name = 'qaforum/update_question.html'
    model = QaQuestion
    pk_url_kwarg = 'question_id'
    fields = ['title', 'description', 'tags']

    def get_success_url(self):
        question = self.get_object()
        return reverse('qaforum:qaforum_detail', kwargs={'pk': question.pk})


class QaCreateAnswerView(LoginRequired, CreateView):
    """
    View to create new answers for a given question
    """
    template_name = 'qaforum/create_answer.html'
    model = QaAnswer
    fields = ['answer_text']
    message = _('Thank you! your answer has been posted.')

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(QaCreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        if qaforum_messages:
            messages.success(self.request, self.message)

        return reverse('qaforum:qaforum_detail', kwargs={'pk': self.kwargs['question_id']})


class QaUpdateAnswerView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question answer
    """
    template_name = 'qaforum/update_answer.html'
    model = QaAnswer
    pk_url_kwarg = 'answer_id'
    fields = ['answer_text']

    def get_success_url(self):
        answer = self.get_object()
        return reverse('qaforum:qaforum_detail', kwargs={'pk': answer.question.pk})


class QaCreateAnswerCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given answer
    """
    template_name = 'qaforum/create_comment.html'
    model = QaAnswerComment
    fields = ['comment_text']
    message = _('Thank you! your comment has been posted.')

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.answer_id = self.kwargs['answer_id']
        return super(QaCreateAnswerCommentView, self).form_valid(form)

    def get_success_url(self):
        if qaforum_messages:
            messages.success(self.request, self.message)

        question_pk = QaAnswer.objects.get(
            id=self.kwargs['answer_id']).question.pk
        return reverse('qaforum:qaforum_detail', kwargs={'pk': question_pk})


class QaCreateQuestionCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given question
    """
    template_name = 'qaforum/create_comment.html'
    model = QaQuestionComment
    fields = ['comment_text']
    message = _('Thank you! your comment has been posted.')

    def form_valid(self, form):
        """
        Creates the required relationship between question
        and user/comment
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(QaCreateQuestionCommentView, self).form_valid(form)

    def get_success_url(self):
        if qaforum_messages:
            messages.success(self.request, self.message)

        return reverse('qaforum:qaforum_detail', kwargs={'pk': self.kwargs['question_id']})


class QaUpdateQuestionCommentView(LoginRequired,
                                AuthorRequiredMixin, UpdateView):
    """
    Updates the comment question
    """
    template_name = 'qaforum/create_comment.html'
    model = QaQuestionComment
    pk_url_kwarg = 'comment_id'
    fields = ['comment_text']

    def get_success_url(self):
        question_comment = self.get_object()
        return reverse('qaforum:qaforum_detail',
                       kwargs={'pk': question_comment.question.pk})


class QaUpdateAnswerCommentView(QaUpdateQuestionCommentView):
    """
    Updates the comment answer
    """
    model = QaAnswerComment

    def get_success_url(self):
        answer_comment = self.get_object()
        return reverse('qaforum:qaforum_detail',
                       kwargs={'pk': answer_comment.answer.question.pk})


class QaQuestionDetailView(HitCountDetailView):
    """
    View to call a question and to render all the details about that question.
    """
    model = QaQuestion
    template_name = 'qaforum/detail_question.html'
    context_object_name = 'question'
    slug_field = 'slug'
    try:
        count_hit = settings.QA_SETTINGS['count_hits']

    except KeyError:
        count_hit = True

    def get_context_data(self, **kwargs):
        answers = self.object.qaanswer_set.all().order_by('pub_date')
        context = super(QaQuestionDetailView, self).get_context_data(**kwargs)
        context['last_comments'] = self.object.qaquestioncomment_set.order_by(
            'pub_date')[:5]
        context['answers'] = list(answers.select_related(
            'user').select_related(
            'user__userprofile')
            .annotate(qaanswercomment_count=Count('qaanswercomment')))
        return context

    def get(self, request, **kwargs):
        my_object = self.get_object()
        slug = kwargs.get('slug', '')
        if slug != my_object.slug:
            kwargs['slug'] = my_object.slug
            return redirect(reverse('qaforum:qaforum_detail', kwargs=kwargs))

        else:
            return super(QaQuestionDetailView, self).get(request, **kwargs)

    def get_object(self):
        question = super(QaQuestionDetailView, self).get_object()
        return question
