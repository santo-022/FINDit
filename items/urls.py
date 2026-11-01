from django.urls import path
from . import views

urlpatterns = [
    path('report/<str:item_type>/', views.report_item, name='report_item'),

    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    path('update/<int:item_id>/', views.update_item, name='update_item'),

    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
