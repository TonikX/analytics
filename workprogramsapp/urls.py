from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path, re_path
from .views import WorkProgramsList, WorkProgramsPost, WorkProgramsPostUpdate, WorkProgramsListApi, WorkProgramView
from .views import EvaluationToolList, EvaluationToolPost, EvaluationToolPostUpdate
from .views import DisciplineSectionList, DiscplineSectionPost, DisciplineSectionPostUpdate
from .views import TopicList, TopicPost, TopicPostUpdate
from .views import PrerequisitesUpdate, OutcomesUpdate, upload_file



urlpatterns = [
    path('workprogramslist/', WorkProgramsList.as_view(), name='workprograms'),
    url(r'^workprogram/(?P<pk>\d+)/$', WorkProgramView.as_view(), name='workprogram'),
    path('workprograms/newbinding', WorkProgramsPost.as_view(), name='author_update'),
    url(r'^uploadcsv/$', upload_file, name = 'uploadcsv'),
    #ToDo: сделать нормально.
    #re_path(r'^workprograms/(?P<pk>)/update/', WorkProgramsPostUpdate.as_view(), name='workprograms_update'),
    url(r'^workprograms/(?P<pk>\d+)/update/$', WorkProgramsPostUpdate.as_view(), name='workprograms_update'),
    path('api/wplist/', WorkProgramsListApi.as_view()),
    #url for prerequisites
    url(r'^prerequisites/(?P<pk>\d+)/update/$', PrerequisitesUpdate.as_view(), name='prereq_update'),
    #url for outcomes
    url(r'^outcomes/(?P<pk>\d+)/update/$', OutcomesUpdate.as_view(), name='outcome_update'),
    #url for evaluation tools
    path('evaluationlist/', EvaluationToolList.as_view(), name='evaluation'),
    path('evaluation/new', EvaluationToolPost.as_view(), name='eval_post'),
    url(r'^evaluation/(?P<pk>\d+)/update/$', EvaluationToolPostUpdate.as_view(), name='eval_update'),
    #url for sections 
    path('sectionlist/', DisciplineSectionList.as_view(), name='section'),
    path('section/new', DiscplineSectionPost.as_view(), name='sec_post'),
    url(r'^section/(?P<pk>\d+)/update/$', DisciplineSectionPostUpdate.as_view(), name='sec_update'),
    #url for topics
    path('topiclist/', TopicList.as_view(), name='topic'),
    path('topic/new', TopicPost.as_view(), name='topic_post'),
    url(r'^topic/(?P<pk>\d+)/update/$', TopicPostUpdate.as_view(), name='topic_update'),


]
