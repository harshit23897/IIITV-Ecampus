from django.conf.urls import url
from . import views

app_name = 'campus_admin'

# For char .+ whereas for integer \d+
urlpatterns=[

    url(r'^$', views.index, name='index'),

    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/(?P<pk3>.+)/success/$', views.success_result,
        name='success_result'),
    url(r'^fee_receipt/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/success/$', views.success_fee_receipt,
        name='success_fee_receipt'),

    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/course_list/$', views.course_list,
        name='course_list'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/$', views.result_view, name='result_view'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/view/$', views.final_result_view, name='final_result_view'),

    # url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/add_grade/$',views.add_grade,name='add_grade'),
    # url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/(?P<pk3>.+)/result_update/$', views.result_update,
    #   name='result_update'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/(?P<pk3>.+)/result_add/$', views.result_add,
        name='result_add'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/$', views.sem_view_result, name='sem_view_result'),
    url(r'^result/(?P<pk4>.+)/(?P<pk>.+)/$', views.result_base, name='result_base'),
    url(r'^result/add_course/$', views.add_course, name='add_course'),
    url(r'^add_faculty/$', views.add_faculty, name='add_faculty'),
    url(r'^success/$', views.success, name='success'),
    # url(r'^result/(?P<pk5>.+)/add_semester/$',views.add_semester,name='add_semester'),
    url(r'^result/$', views.result, name='result'),
    url(r'^registration/', views.registration, name='registration'),

    url(r'^fee_receipt/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/$', views.fee_receipt_view,
        name='fee_receipt_view'),
    url(r'^fee_receipt/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/view/$', views.final_fee_receipt_view,
        name='final_fee_receipt_view'),
    url(r'^fee_receipt/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/fee_receipt_add/$', views.fee_receipt_add,
        name='fee_receipt_add'),
    url(r'^fee_receipt/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/$', views.sem_view_fee, name='sem_view_fee'),
    url(r'^fee_receipt/(?P<pk4>.+)/(?P<pk>.+)/$', views.fee_receipt_base, name='fee_receipt_base'),
    url(r'^fee_receipt/$', views.fee_receipt, name='fee_receipt'),

]