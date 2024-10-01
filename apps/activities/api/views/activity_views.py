from  rest_framework import generics
from rest_framework import status
from rest_framework.response import Response


from apps.base.api import GeneralListApiView
from apps.activities.api.serializers.activity_serializers import ActivitySerializer

class ActivityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    queryset = ActivitySerializer.Meta.model.objects.filter(state=True)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Actividad creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state=True)
    
    def patch(self, request, pk=None):
        activity = self.get_queryset().filter(id = pk).first()
        if activity:
            activity_serializer = self.serializer_class(activity)
            return Response(activity_serializer.data, status = status.HTTP_200_OK)
        return Response({'message': 'Actividad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        activity = self.get_queryset().filter(id = pk).first()
        if activity:
            activity_serializer = self.serializer_class(activity, data=request.data)
            if activity_serializer.is_valid():
                activity_serializer.save()
                return Response(activity_serializer.data, status=status.HTTP_200_OK)
                # return Response({'message': 'Actividad actualizada correctamente'}, status=status.HTTP_200_OK)
            return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Actividad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        activity = self.get_queryset().filter(id = pk).first()
        if  activity:
            activity.state = False
            activity.save()
            return Response({'message': 'Actividad eliminada correctamente'}, status=status.HTTP_200_OK)
        return Response({'message': 'Actividad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)