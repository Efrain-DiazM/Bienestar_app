from django.urls import path
from apps.activities.api.views.general_views import DimensionListAPIView, ProgramDimensionListAPIView, SubprogramDimensionListAPIView
from apps.activities.api.views.activity_views import ActivityListCreateAPIView, ActivityRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('dimension/', DimensionListAPIView.as_view(), name='dimension'),
    path('program_dimension/', ProgramDimensionListAPIView.as_view(), name='program_dimension'),
    path('subprogram_dimension/', SubprogramDimensionListAPIView.as_view(), name='subprogram_dimension'),
    path('activity/', ActivityListCreateAPIView.as_view(), name='activity_create'),
    path('activity/retrieve-update-destroy/<int:pk>', ActivityRetrieveUpdateDestroyAPIView.as_view(), name='activity_retrieve_update_destroy'),
]