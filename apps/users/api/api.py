# crear APIView del modelo
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, EstudianteSerializer, UsuarioBienestarSerializer

@api_view(['GET', 'POST'])
def user_api_view(request):

    if request.method == 'GET':
        # Queryset
        users = User.objects.all()
        # Serializer
        users_serializer = UserSerializer(users, many=True)

        # test_data = {
        #     'name': 'Test1',
        #     'email': 'Test@gmail.com'
        # }

        # test_user = TestUserSerialezer(data=test_data, context = test_data)
        # if test_user.is_valid():
        #     user_instance = test_user.save()
        #     print(user_instance)
        # else:
        #     print(test_user.errors)

        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        role = request.data.get('role')
        if role == 'Estudiante':
            user_serializer = EstudianteSerializer(data=request.data)
        elif role == 'Usuario_Bienestar':
            user_serializer = UsuarioBienestarSerializer(data=request.data)
        else:
            user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'POST':
    #     user_serializer = UserSerializer(data=request.data)
    #     if user_serializer.is_valid():
    #         user_serializer.save()
    #         return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
    #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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