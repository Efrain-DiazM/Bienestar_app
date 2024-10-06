from django.urls import path
from apps.activities.api.views.general_views import DimensionListAPIView, ProgramDimensionListAPIView, SubprogramDimensionListAPIView

urlpatterns = [
    path('dimension/', DimensionListAPIView.as_view(), name='dimension'),
    path('program_dimension/', ProgramDimensionListAPIView.as_view(), name='program_dimension'),
    path('subprogram_dimension/', SubprogramDimensionListAPIView.as_view(), name='subprogram_dimension'),
]