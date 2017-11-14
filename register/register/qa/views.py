import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render,HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, UpdateView, View
from hitcount.views import HitCountDetailView
from .models import (Answer, AnswerComment,  Question,
                       QuestionComment)
from taggit.models import Tag, TaggedItem

from .forms import QuestionForm
from .mixins import AuthorRequiredMixin, LoginRequired
from .utils import question_score
from django.contrib.auth.models import User
from register.student.models import course

try:
    qa_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and\
        settings.QA_SETTINGS['qa_messages']

except AttributeError:  # pragma: no cover
    qa_messages = False

if qa_messages:
    from django.contrib import messages


"""Dear maintainer:

Once you are done trying to 'optimize' this routine, and have realized what a
terrible mistake that was, please increment the following counter as a warning
to the next guy:

total_hours_wasted_here = 2
"""


class AnswerQuestionView(LoginRequired, View):
    """
    View to select an answer as the satisfying answer to the question,
    validating than the user who created que
    question is the only one allowed to make those changes.
    """
    model = Answer

    def post(self, request, course_no, answer_id):
        print("1oooooooo")
        answer = get_object_or_404(self.model, pk=answer_id)
        if answer.question.user != request.user:
            raise ValidationError(
                "Sorry, you're not allowed to close this question.")

        else:
            answer.question.answer_set.update(answer=False)
            answer.answer = True
            answer.save()
            try:
                points = settings.QA_SETTINGS['reputation']['ACCEPT_ANSWER']

            except KeyError:
                points = 0

            qa_user = UserProfile.objects.get(user=answer.user)
            qa_user.modify_reputation(points)

        next_url = request.POST.get('next', '')
        if next_url is not '':
            return redirect(next_url)

        else:
            url = reverse('qa_index', kwargs={'course_no': self.kwargs['course_no']})
            return url



class CloseQuestionView(LoginRequired, View):
    """View to
    mark the question as closed, validating than the user who created que
    question is the only one allowed to make those changes.
    """
    model = Question

    def post(self, request,course_no, question_id):
        print("2oooooooo")
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
            url = reverse('qa_index', kwargs={'course_no': self.kwargs['course_no']})
            return url


class QuestionIndexView(ListView):
    """CBV to render the index view
    """
    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/index.html'
    ordering = '-pub_date'

    def get_context_data(self, *args, **kwargs):
        context = super(
            QuestionIndexView, self).get_context_data(*args, **kwargs)
        noans = Question.objects.order_by('-pub_date').filter(
            answer__isnull=True, courseNo__courseNo=self.kwargs['course_no']).select_related('user')\
            .annotate(num_answers=Count('answer', distinct=True),
                      num_question_comments=Count('questioncomment',
                      distinct=True))
        context['course_no'] = self.kwargs['course_no']
        context['totalcount'] = Question.objects.filter(courseNo=self.kwargs['course_no']).count()
        context['anscount'] = Answer.objects.count()
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

        question_contenttype = ContentType.objects.get_for_model(model = Question)
        items = TaggedItem.objects.filter(content_type=question_contenttype)
        context['tags'] = Tag.objects.filter(
             taggit_taggeditem_items__in=items).order_by('-id').distinct()[:10]



        return context

    def get_queryset(self):
        print(self.kwargs)
        queryset = super(QuestionIndexView, self).get_queryset().filter(courseNo__courseNo__exact=self.kwargs['course_no'])\
            .select_related('user')\
            .annotate(num_answers=Count('answer', distinct=True),
                      num_question_comments=Count('questioncomment',
                      distinct=True))
        return queryset


class QuestionsSearchView(QuestionIndexView):
    """
    Display a ListView page inherithed from the QuestionIndexView filtered by
    the search query and sorted by the different elements aggregated.
    """

    def get_queryset(self):
        print("4oooooooo")
        result = super(QuestionsSearchView, self).get_queryset()
        query = self.request.GET.get('word', '')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)))

            result = result.filter(courseNo = self.kwargs['course_no'])

        return result

    def get_context_data(self, *args, **kwargs):
        context = super(
            QuestionsSearchView, self).get_context_data(*args, **kwargs)
        context['totalcount'] = Question.objects.count
        context['anscount'] = Answer.objects.count
        context['noans'] = Question.objects.order_by('-pub_date').filter(
            answer__isnull=True, courseNo = self.kwargs['course_no'])[:10]
        context['course_No'] = self.kwargs['course_no']
        return context


class QuestionsByTagView(ListView):
    """View to call all the questions clasiffied under one specific tag.
    """
    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'qa/index.html'

    def get_queryset(self, **kwargs):
        print("5oooooooo")
        return Question.objects.filter(tags__slug=self.kwargs['tag'], courseNo=self.kwargs['course_no'])

    def get_context_data(self, *args, **kwargs):
        context = super(
            QuestionsByTagView, self).get_context_data(*args, **kwargs)
        context['active_tab'] = self.request.GET.get('active_tab', 'latest')
        tabs = ['latest', 'unans']
        context['active_tab'] = 'latest' if context['active_tab'] not in\
            tabs else context['active_tab']
        context['totalcount'] = Question.objects.count
        context['anscount'] = Answer.objects.count
        context['noans'] = Question.objects.order_by('-pub_date').filter(
            tags__name__contains=self.kwargs['tag'], answer__isnull=True)[:10]

        context['course_no'] = self.kwargs['course_no']
        context['totalnoans'] = len(context['noans'])
        return context


class CreateQuestionView(LoginRequired, CreateView):
    """
    View to handle the creation of a new question
    """

    template_name = 'qa/create_question.html'
    message = _('Thank you! your question has been created.')
    form_class = QuestionForm
    model = Question
    def get_context_data(self, *args, **kwargs):
        context = super(
            CreateQuestionView, self).get_context_data(*args, **kwargs)
        context['course_no'] = self.kwargs['course_no']
        return context

    def form_valid(self, form):
        """
        Create the required relation
        """
        print("Helo asdlkalsdk")
        form.instance.courseNo = course.objects.get(courseNo=self.kwargs['course_no'])
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        if qa_messages:
            def get_success_url(self):
                messages.success(self.request, self.message)
        url = reverse('qa:qa_index', kwargs={'course_no': self.kwargs['course_no']})
        return url





class UpdateQuestionView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question
    """
    template_name = 'qa/update_question.html'
    model = Question
    pk_url_kwarg = 'question_id'
    fields = ['title', 'description', 'tags']

    def get_context_data(self, *args, **kwargs):
        context = super(
            UpdateQuestionView, self).get_context_data(*args, **kwargs)
        context['course_no'] = self.kwargs['course_no']
        return context

    def get_success_url(self):
        print("7oooooooo")
        question = self.get_object()
        url = reverse('qa:qa_detail', kwargs={'course_no': self.kwargs['course_no'],'pk': question.pk})
        return url



class CreateAnswerView(LoginRequired, CreateView):
    """
    View to create new answers for a given question
    """
    template_name = 'qa/create_answer.html'
    model = Answer
    fields = ['answer_text']
    message = _('Thank you! your answer has been posted.')
    def get_context_data(self, *args, **kwargs):
        context = super(
            CreateAnswerView, self).get_context_data(*args, **kwargs)
        context['course_no'] = self.kwargs['course_no']
        return context

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        print("8oooooooo")
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        print("8oooooooo")
        if qa_messages:
            def get_success_url(self, course_no):
                messages.success(self.request, self.message)

        url = reverse('qa:qa_detail', kwargs={'course_no': self.kwargs['course_no'],'pk': self.kwargs['question_id']})
        return url


class UpdateAnswerView(LoginRequired, AuthorRequiredMixin, UpdateView):
    """
    Updates the question answer
    """
    template_name = 'qa/update_answer.html'
    model = Answer
    pk_url_kwarg = 'answer_id'
    fields = ['answer_text']

    def get_context_data(self, *args, **kwargs):
        context = super(
            UpdateAnswerView, self).get_context_data(*args, **kwargs)
        context['course_no'] = self.kwargs['course_no']
        return context

    def get_success_url(self):
        print("9oooooooo")
        answer = self.get_object()
        url = reverse('qa:qa_detail', kwargs={'course_no': self.kwargs['course_no'],'pk': answer.question.pk})
        return url



class CreateAnswerCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given answer
    """
    template_name = 'qa/create_comment.html'
    model = AnswerComment
    fields = ['comment_text']
    message = _('Thank you! your comment has been posted.')

    def get_context_data(self, *args, **kwargs):
        context = super(
            CreateAnswerCommentView, self).get_context_data(*args, **kwargs)
        context['course_no'] = self.kwargs['course_no']
        return context

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/comment
        """
        print("11oooooooo")
        form.instance.user = self.request.user
        form.instance.answer_id = self.kwargs['answer_id']
        return super(CreateAnswerCommentView, self).form_valid(form)

    def get_success_url(self):
        print("11oooooooo")
        if qa_messages:
            messages.success(self.request, self.message)

        question_pk = Answer.objects.get(
            id=self.kwargs['answer_id']).question.pk

        url = reverse('qa:qa_detail', kwargs={'course_no': self.kwargs['course_no'],'pk': question_pk})
        return url


class CreateQuestionCommentView(LoginRequired, CreateView):
    """
    View to create new comments for a given question
    """
    template_name = 'qa/create_comment.html'
    model = QuestionComment
    fields = ['comment_text']
    message = _('Thank you! your comment has been posted.')

    def get_context_data(self, *args, **kwargs):
        context = super(
            CreateQuestionCommentView, self).get_context_data(*args, **kwargs)
        context['course_no'] = self.kwargs['course_no']
        return context

    def form_valid(self, form):
        """
        Creates the required relationship between question
        and user/comment
        """
        print("12oooooooo")
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateQuestionCommentView, self).form_valid(form)

    def get_success_url(self):
        print("12oooooooo")
        if qa_messages:
            messages.success(self.request, self.message)

        url = reverse('qa:qa_detail', kwargs={'course_no':self.kwargs['course_no'], 'pk': self.kwargs['question_id']})
        return url


class UpdateQuestionCommentView(LoginRequired,
                                AuthorRequiredMixin, UpdateView):
    """
    Updates the comment question
    """
    template_name = 'qa/create_comment.html'
    model = QuestionComment
    pk_url_kwarg = 'comment_id'
    fields = ['comment_text']


    def get_success_url(self):
        print("13oooooooo")
        question_comment = self.get_object()
        url = reverse('qa:qa_detail', kwargs={'course_no': self.kwargs['course_no'], 'pk': question_comment.question.pk})
        return url



class UpdateAnswerCommentView(UpdateQuestionCommentView):
    """
    Updates the comment answer
    """
    model = AnswerComment


    def get_success_url(self):
        answer_comment = self.get_object()
        print("14oooooooo")
        url = reverse('qa:qa_detail', kwargs={'course_no': self.kwargs['course_no'], 'pk': answer_comment.answer.question.pk})
        return url



class QuestionDetailView(HitCountDetailView):
    """
    View to call a question and to render all the details about that question.
    """

    model = Question
    template_name = 'qa/detail_question.html'
    context_object_name = 'question'
    slug_field = 'slug'
    try:
        count_hit = settings.QA_SETTINGS['count_hits']

    except KeyError:
        count_hit = True

    def get_context_data(self, **kwargs):

        answers = self.object.answer_set.all().order_by('pub_date')
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['last_comments'] = self.object.questioncomment_set.order_by(
            'pub_date')[:5]
        context['answers'] = list(answers.select_related(
            'user').select_related(
            'user__userprofile')
            .annotate(answercomment_count=Count('answercomment')))

        context['course_no'] = self.kwargs['course_no']

        return context


    def get(self, request, **kwargs):
        print("15oooooooo")

        my_object = self.get_object()

        slug = kwargs.get('slug', '')

        if slug != my_object.slug:

            kwargs['course_no'] = self.kwargs['course_no']
            kwargs['pk'] = self.kwargs['pk']
            kwargs['slug'] = my_object.slug
            url = reverse('qa:qa_detail', kwargs=kwargs)
            return url

        else:

            return super(QuestionDetailView, self).get(request,**kwargs)

    def get_object(self):

        question = super(QuestionDetailView, self).get_object()
        return question
