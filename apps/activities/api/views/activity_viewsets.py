from  rest_framework import generics
from datetime import datetime
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.decorators import action
from django.db.models import Q

from apps.base.api import GeneralListApiView
from apps.users.authentication_mixins import Authentication
from apps.activities.models import AttendanceActivity, Activity

from apps.users.permissions import IsAdmin, IsCollaborator, IsStudent
from apps.activities.api.serializers.activity_serializers import ActivitySerializer, EditActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):

    serializer_class = ActivitySerializer
    print(serializer_class)

    # def get_permissions(self):
        # Define permisos según la acción (action)
        # if self.action in ['list']:
            # permission_classes = [IsAuthenticated]  # Solo autenticados pueden listar
        # else:
            # permission_classes = [IsAuthenticated, IsAdmin]  # Solo admin para otras acciones
            # permission_classes = [IsAuthenticated]  # Solo admin para otras acciones
        # return [permission() for permission in permission_classes]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    def list(self, request):
        activity_serializer = self.get_serializer(self.get_queryset(), many=True)
        # print(activity_serializer.data)
        return Response(activity_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = EditActivitySerializer(data=request.data)
        request.data['count_hours'] = 0
        # start_hour = datetime.strptime(request.data['start_hour'], '%H:%M')
        # end_hour = datetime.strptime(request.data['end_hour'], '%H:%M')
        # # calcular la resta de las horas que de resultado en entero aproximado hacia arriba
        # duration = (end_hour - start_hour).total_seconds() / 3600
        # if duration - int(duration) >= 0.5:
        #     request.data['count_hours'] = int(duration) + 1
        # else:
        #     request.data['count_hours'] = int(duration)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Actividad creada correctamente'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            activity_serializer = EditActivitySerializer(self.get_queryset(pk), data=request.data)
            # print(request.data)
            if activity_serializer.is_valid():
                # print('entro')
                activity_serializer.save()
                return Response(activity_serializer.data, status=status.HTTP_200_OK)
            return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        activity = self.get_queryset().filter(id = pk).first()
        if activity:
            activity.state = False
            activity.save()
            return Response({'message': 'Actividad eliminada correctamente'}, status=status.HTTP_200_OK)
        return Response({'message': 'Actividad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsStudent])
    def student_activities(self, request):
        """
        Consulta las actividades en las que está registrado el estudiante autenticado.
        """
        user = request.user

        # Obtener las actividades en las que está registrado el estudiante
        student = user.estudiante
        activities = self.get_serializer().Meta.model.objects.filter(
            attendanceactivity__student=student,
            state=True
        ).distinct()

        total_activities = activities.count()

        # Serializar las actividades
        serializer = self.get_serializer(activities, many=True)
        return Response({
            "count_activities": total_activities,
            "activities": serializer.data
        }, status=status.HTTP_200_OK)
    
# class ActivityViewSet(viewsets.ModelViewSet):
#     serializer_class = ActivitySerializer

#     def get_queryset(self, pk=None):
#         if pk is None:
#             return self.get_serializer().Meta.model.objects.filter(state=True)
#         return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

    # @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    # def filtered_activities(self, request):
    #     """
    #     Filtra actividades basadas en los parámetros proporcionados y en los estudiantes registrados.
    #     """
    #     print('Usuario autenticado:', request.user)
    #     print('Parámetros recibidos:', request.query_params)

    #     # Obtener parámetros de la solicitud
    #     # start_date = request.query_params.get('start_date')
    #     # end_date = request.query_params.get('end_date')
    #     program_id = request.query_params.get('program_id')
    #     gender_id = request.query_params.get('gender_id')
    #     dimension_id = request.query_params.get('dimension_id')

    #     print(program_id)

    #     # Construir el queryset base desde AttendanceActivity
    #     queryset = AttendanceActivity.objects.filter(activity__state=True)

    #     # Aplicar filtros según los parámetros
    #     # if start_date:
    #     #     queryset = queryset.filter(activity__date__gte=start_date)
    #     # if end_date:
    #     #     queryset = queryset.filter(activity__date__lte=end_date)
    #     if program_id:
    #         queryset = queryset.filter(activity__program_dimension_id=program_id)
    #     if gender_id:
    #         queryset = queryset.filter(activity__responsible__gender_id=gender_id)
    #     if dimension_id:
    #         queryset = queryset.filter(activity__dimension_id=dimension_id)

    #     # Obtener las actividades únicas
    #     activities = queryset.values_list('activity', flat=True).distinct()

    #     # Serializar y devolver los resultados
    #     activity_queryset = self.get_serializer().Meta.model.objects.filter(id__in=activities)
    #     serializer = self.get_serializer(activity_queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
class FilteredActivitiesAPIView(APIView):
    """
    API para filtrar actividades basadas en parámetros proporcionados.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Parámetros recibidos:", request.query_params)

        # Obtener parámetros de la solicitud
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        program_id = request.query_params.get('program_id')
        gender_id = request.query_params.get('gender_id')
        dimension_id = request.query_params.get('dimension_id')

        print("Parámetros procesados:", start_date, end_date, program_id, gender_id, dimension_id)

        # Construir el queryset base desde AttendanceActivity
        queryset = AttendanceActivity.objects.filter(activity__state=True)

        # Aplicar filtros según los parámetros
        if start_date:
            queryset = queryset.filter(activity__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(activity__date__lte=end_date)
        if program_id:
            queryset = queryset.filter(student__academic_program_id=program_id)
        if gender_id:
            queryset = queryset.filter(activity__responsible__gender_id=gender_id)
        if dimension_id:
            queryset = queryset.filter(activity__dimension_id=dimension_id)

        # Obtener las actividades únicas
        activity_ids = queryset.values_list('activity', flat=True).distinct()

        # Filtrar actividades por los IDs obtenidos
        activities = Activity.objects.filter(id__in=activity_ids, state=True)

        # Serializar y devolver los resultados
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)