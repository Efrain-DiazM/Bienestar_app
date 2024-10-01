from apps.base.api import GeneralListApiView
from apps.activities.api.serializers.general_serializers import DimensionSerializer, ProgramDimensionSerializer, SubprogramDimensionSerializer

class DimensionListAPIView(GeneralListApiView):
    serializer_class = DimensionSerializer

class ProgramDimensionListAPIView(GeneralListApiView):
    serializer_class = ProgramDimensionSerializer

class SubprogramDimensionListAPIView(GeneralListApiView):
    serializer_class = SubprogramDimensionSerializer
