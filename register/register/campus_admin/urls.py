from django.conf.urls import url
from . import views

app_name = 'campus_admin'

# For char .+ whereas for integer \d+
urlpatterns=[

    url(r'^$',views.index, name='index'),


    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/course_list/$',views.course_list,name='course_list'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/$',views.result_view,name='result_view'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/(?P<pk3>.+)/result_add/$',views.result_add,name='result_add'),
    url(r'^result/(?P<pk4>.+)/(?P<pk1>.+)/(?P<pk>\d+)/$', views.sem_view_result, name='sem_view_result'),
    url(r'^result/(?P<pk4>.+)/(?P<pk>.+)/$',views.result_base,name='result_base'),
    url(r'^result/$', views.result, name='result'),


    url(r'^fee_receipt/CS/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/$', views.fee_receipt_view, name='fee_receipt_view'),
    url(r'^fee_receipt/CS/(?P<pk1>.+)/(?P<pk>\d+)/(?P<pk2>\d+)/fee_receipt_add/$', views.fee_receipt_add,
        name='fee_receipt_add'),
    url(r'^fee_receipt/CS/(?P<pk1>.+)/(?P<pk>\d+)/$', views.sem_view_fee, name='sem_view_fee'),
    url(r'^fee_receipt/CS/(?P<pk>.+)/$', views.fee_receipt_base, name='fee_receipt_base'),
    url(r'^fee_receipt/$', views.result, name='fee_receipt'),

]