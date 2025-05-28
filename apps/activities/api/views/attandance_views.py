from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import uuid
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from datetime import datetime
from django.db import IntegrityError

from apps.activities.models import Activity, AttendanceActivity
from apps.users.models import Estudiante
from apps.activities.api.serializers.attandance_serializers import AttendanceSerializer, AttandenceActivitySerializer

class QRCodeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, activity_id):
        print(activity_id)
        # Aquí puedes verificar si el usuario está autenticado
        # user = request.user
        # if user.is_authenticated:
        #     return Response({"message": "User is authenticated"})
        # else:
        #     return Response({"message": "User is not authenticated"})
        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            return Response({"message": "Activity not found"}, status=404)

        print('activity', activity)
        
         # Validar que el QR solo se genere en la fecha y horario de la actividad
        current_time = now()
        activity_date = activity.date
        activity_start_time = datetime.combine(activity_date, activity.start_hour)
        activity_end_time = datetime.combine(activity_date, activity.end_hour) + timedelta(minutes=20)

        if not (activity_start_time <= current_time <= activity_end_time):
            return Response(
                {"error": "El código QR se genera en el horario de la actividad."},
                status=400
            )
        
        # Generar el QR si está dentro del horario permitido
        activity.qr_code_identifier = uuid.uuid4()
        print('qr_code_identifier', activity.qr_code_identifier)
        activity.save()
        return Response({"qr_code_identifier": activity.qr_code_identifier}, status=200)

class ActivityByQRAPIView(APIView):
    def get(self, request, qr_code_identifier):
        print(qr_code_identifier)
        try:
            activity = Activity.objects.get(qr_code_identifier=qr_code_identifier)
            return Response({'activity_id': activity.id}, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({'error': 'Actividad no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
from datetime import datetime, timedelta
from django.utils.timezone import now

class RegisterAttandenceApiView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            qr_code_identifier = request.data.get("qr_code_identifier")
            student_id = request.data.get("student")

            # Buscar al estudiante
            try:
                student = Estudiante.objects.get(id=student_id)
            except Estudiante.DoesNotExist:
                return Response({"error": "Estudiante no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # Buscar la actividad
            try:
                activity = Activity.objects.get(qr_code_identifier=qr_code_identifier)
            except Activity.DoesNotExist:
                return Response({"error": "Actividad no encontrada."}, status=status.HTTP_404_NOT_FOUND)

            # Validar que la actividad no haya caducado
            if activity.date < datetime.now().date():
                return Response({"error": "La actividad ha caducado."}, status=status.HTTP_400_BAD_REQUEST)

            # Validar que el estudiante no haya registrado asistencia previamente
            if AttendanceActivity.objects.filter(activity=activity, student=student).exists():
                return Response({"error": "El estudiante ya ha registrado asistencia para esta actividad."}, status=status.HTTP_400_BAD_REQUEST)

            # Validar que el qr pertenezca a la actividad
            if str(activity.qr_code_identifier) != qr_code_identifier:
                return Response({"error": "El código QR no corresponde a la actividad."}, status=status.HTTP_400_BAD_REQUEST)

            # Validar que la asistencia esté dentro de la fecha y horario permitido
            current_time = now()
            activity_date = activity.date
            activity_start_time = datetime.combine(activity_date, activity.start_hour)
            activity_end_time = datetime.combine(activity_date, activity.end_hour) + timedelta(minutes=20)

            if not (activity_start_time <= current_time <= activity_end_time):
                return Response(
                    {"error": "La asistencia solo puede registrarse en la fecha y horario de la actividad o hasta 20 minutos después de que termine."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Registrar la asistencia
            try:
                student.accumulated_hours += activity.count_hours
                student.save()

                attandence_activity = AttendanceActivity(activity=activity, student=student)
                attandence_activity.attendance_date = current_time
                attandence_activity.save()
            except IntegrityError:
                # Captura cualquier error de unicidad por si acaso
                return Response({"error": "El estudiante ya ha registrado asistencia para esta actividad."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Asistencia registrada exitosamente"}, status=status.HTTP_200_OK)

        # Si el serializer no es válido, muestra un mensaje claro
        error_msg = serializer.errors.get('non_field_errors', serializer.errors)
        return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

class AttandenceListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = AttendanceActivity.objects.all()
        serializer_class = AttendanceSerializer(queryset, many=True)
        return Response(serializer_class.data, status=200)
    
# listar los estudiantes que asistieron a cierta actividad
class AttandenceListByActivityAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, activity_id):
        activity = Activity.objects.get(id=activity_id)
        attandence_activity = AttendanceActivity.objects.filter(activity=activity)
        serializer = AttandenceActivitySerializer(attandence_activity, many=True)
        return Response(serializer.data, status=200)
    
