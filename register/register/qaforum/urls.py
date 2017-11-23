from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.QaQuestionIndexView.as_view(), name='qaforum_index'),

    url(r'^question/(?P<pk>\d+)/$',
        views.QaQuestionDetailView.as_view(), name='qaforum_detail'),

    url(r'^question/(?P<pk>\d+)/(?P<slug>[-_\w]+)/$',
        views.QaQuestionDetailView.as_view(), name='qaforum_detail'),

    url(r'^question/answer/(?P<answer_id>\d+)/$',
        views.QaAnswerQuestionView.as_view(), name='qaforum_answer_question'),

    url(r'^question/close/(?P<question_id>\d+)/$',
        views.QaCloseQuestionView.as_view(), name='qaforum_close_question'),

    url(r'^new-question/$', views.QaCreateQuestionView.as_view(),
        name='qaforum_create_question'),

    url(r'^edit-question/(?P<question_id>\d+)/$',
        views.QaUpdateQuestionView.as_view(),
        name='qaforum_update_question'),

    url(r'^answer/(?P<question_id>\d+)/$',
        views.QaCreateAnswerView.as_view(), name='qaforum_create_answer'),

    url(r'^answer/edit/(?P<answer_id>\d+)/$',
        views.QaUpdateAnswerView.as_view(), name='qaforum_update_answer'),



    url(r'^comment-answer/(?P<answer_id>\d+)/$',
        views.QaCreateAnswerCommentView.as_view(),
        name='qaforum_create_answer_comment'),

    url(r'^comment-question/(?P<question_id>\d+)/$',
        views.QaCreateQuestionCommentView.as_view(),
        name='qaforum_create_question_comment'),

    url(r'^comment-question/edit/(?P<comment_id>\d+)/$',
        views.QaUpdateQuestionCommentView.as_view(),
        name='qaforum_update_question_comment'),

    url(r'^comment-answer/edit/(?P<comment_id>\d+)/$',
        views.QaUpdateAnswerCommentView.as_view(),
        name='qaforum_update_answer_comment'),

    url(r'^search/$', views.QaQuestionsSearchView.as_view(), name='qaforum_search'),

    url(r'^tag/(?P<tag>[-\w]+)/$',
        views.QaQuestionsByTagView.as_view(), name='qaforum_tag'),

    url(r'hitcount/', include('hitcount.urls', namespace='qahitcount')),

]
