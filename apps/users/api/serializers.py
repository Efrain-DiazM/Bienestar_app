from rest_framework import serializers
from apps.users.models import User, Estudiante, UsuarioBienestar, AcademicProgram

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'last_name', 'identification', 'gender', 'phone_number', 'password', 'role', 'image', 'is_active', 'is_staff']

    def validate_email(self, value):
        print('validacion de correo')
        print(value)
    # Validacion personalizada
        if value == "":
            raise serializers.ValidationError("Error, el email no puede estar vacio")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Error, el correo ya existe")
        if not value.endswith('@campusucc.edu.co') and not value.endswith('@ucc.edu.co'):
            print('Error, el correo debe ser institucional')
            raise serializers.ValidationError("Error, el correo debe ser institucional")
        # if self.validate_name(self.context['name']) in value:
        #     raise serializers.ValidationError("Error, el nombre no puede estar en el email")
        return value

    def create(self, validated_data):
        print(validated_data)
        role = validated_data.get('role')
        email = validated_data.get('email')
        username = email.split('@')[0]
        print(username)
        validated_data['username'] = username
        if role == 'Estudiante':
            validated_data['username'] = username
            user = Estudiante(**validated_data)
        elif role == 'Usuario_Bienestar':
            validated_data['username'] = username
            user = UsuarioBienestar(**validated_data)
        else:
            user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        return super().update(instance, validated_data)

class EstudianteSerializer(UserSerializer):
    email = serializers.EmailField()
    class Meta(UserSerializer.Meta):
        model = Estudiante
        fields = UserSerializer.Meta.fields + ['semester', 'academic_program', 'accumulated_hours']

class UsuarioBienestarSerializer(UserSerializer):
    email = serializers.EmailField()
    class Meta(UserSerializer.Meta):
        model = UsuarioBienestar
        fields = UserSerializer.Meta.fields + ['dimension']

class EditUsuarioBienestarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioBienestar
        fields = ['id', 'username', 'email', 'name', 'last_name', 'identification', 'phone_number', 'is_active']

class AcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicProgram
        fields = ['id', 'name', 'code']
