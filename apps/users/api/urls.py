from django.urls import path
from apps.users.api.api import user_api_view, user_detail_api_view, activate_account, create_student_api_view, create_collaborator_api_view, academic_programs_api_view

urlpatterns = [
    path('user/', user_api_view, name='user_api'),
    path('create-student/', create_student_api_view, name='create_student'),
    path('create-collaborator/', create_collaborator_api_view, name='create_collaborator'),
    path('user/<int:pk>/', user_detail_api_view, name='user_detail_api_view'),

    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('academic-programs/', academic_programs_api_view, name='academic_programs')
]