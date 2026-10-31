from django.urls import path
from . import views

urlpatterns = [
    path('report/<str:item_type>/', views.report_item, name='report_item'),
]