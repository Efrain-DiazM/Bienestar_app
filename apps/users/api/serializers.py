from rest_framework import serializers
from apps.users.models import User, Estudiante, UsuarioBienestar, AcademicProgram, Gender, DocumentType

from django.contrib.auth.tokens import  PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

# class UserTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'last_name', 'identification', 'gender', 'password', 'role', 'image', 'is_active', 'is_staff']

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
        fields = ['id', 'username', 'email', 'name', 'last_name', 'identification', 'is_active']

class AcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicProgram
        fields = ['id', 'name', 'code']

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'code', 'name']

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'code', 'name']

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=16, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    
    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El link de restablecimiento es invalido', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('El link de restablecimiento es invalido', 401)        
        return super().validate(attrs)