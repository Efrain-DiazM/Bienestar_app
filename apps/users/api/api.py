# crear APIView del modelo
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdmin, IsCollaborator
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, EstudianteSerializer, UsuarioBienestarSerializer

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

from django.shortcuts import get_object_or_404

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = f'{request.scheme}://{request.get_host()}{activation_link}'

    subject = 'Activa tu cuenta'
    message = (
        f'Hola {user.username},\n\n'
        'Gracias por registrarte en nuestro sitio. Por favor, activa tu cuenta haciendo clic en el siguiente enlace:\n\n'
        f'{activation_url}\n\n'
        'Si no solicitaste este registro, ignora este correo.\n\n'
        'Saludos,\n'
        'El equipo de soporte'
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

# @api_view(['GET'])
# def activate_account(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return Response({'message': 'Cuenta activada correctamente'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'Token de activación inválido'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'message': 'El enlace de activación es inválido o el usuario no existe.'}, status=status.HTTP_400_BAD_REQUEST)

    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({'message': 'Cuenta activada correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'La cuenta ya está activada.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Token de activación inválido.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def user_api_view(request):

    if request.method == 'GET':
        # Queryset
        users = User.objects.all()
        # Serializer
        users_serializer = UserSerializer(users, many=True)

        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    # elif request.method == 'POST':
    #     role = request.data.get('role')
    #     if role == 'Estudiante':
    #         print(request.data)
    #         user_serializer = EstudianteSerializer(data=request.data)
    #     elif role == 'Usuario_Bienestar':
    #         user_serializer = UsuarioBienestarSerializer(data=request.data)
    #     else:
    #         user_serializer = UserSerializer(data=request.data)

    #     if user_serializer.is_valid():
    #         print("el usuario el valido")
    #         user = user_serializer.save()

    #         user.is_active = False  # Desactiva la cuenta hasta la activación
    #         user.save()

    #         # Enviar correo de activación
    #         send_activation_email(user, request)
    #         return Response({'message': 'Usuario creado correctamente, Revisa tu correo para activar la cuenta.'}, status=status.HTTP_201_CREATED)
    #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdmin])
def create_student_api_view(request):
    if request.method == 'POST':
        estudiante_serializer = EstudianteSerializer(data=request.data)

        if estudiante_serializer.is_valid():
            estudiante = estudiante_serializer.save()
            estudiante.is_active = False  # Desactiva la cuenta hasta que sea activada
            estudiante.save()

            # Enviar correo de activación
            send_activation_email(estudiante, request)

            return Response({
                'message': 'Estudiante creado correctamente. Revisa tu correo para activar la cuenta.'
            }, status=status.HTTP_201_CREATED)

        return Response(estudiante_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_collaborator_api_view(request):
    if request.method == 'POST':
        bienestar_serializer = UsuarioBienestarSerializer(data=request.data)

        if bienestar_serializer.is_valid():
            bienestar = bienestar_serializer.save()

            # Si no requiere activación por correo
            return Response({
                'message': 'Usuario Bienestar creado correctamente.'
            }, status=status.HTTP_201_CREATED)

        return Response(bienestar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    # Queryset
    user = User.objects.filter(id=pk).first()

    if user:

        if request.method == 'GET':
            # Serializer
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST) 