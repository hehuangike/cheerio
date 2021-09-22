from django.urls import path

from IKEdata import views

app_name = 'IKEdata'

urlpatterns = [
    path('loginto/', views.loginto, name='login'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('collect/', views.collect, name='collect'),
    path('clean/', views.clean, name='clean'),
    path('analysis/', views.analysis, name='analysis'),
    path('analysis_test/', views.analysis_test, name='analysis_test'),
    path('mining/', views.mining, name='mining'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wordnet/', views.wordnet, name='wordnet'),
    path('', views.dashboard, name='home'),
]
