from rest_framework import serializers
from apps.users.models import User, Estudiante, UsuarioBienestar

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'last_name', 'phone_number', 'password', 'role', 'image', 'is_active', 'is_staff']

    # def to_representation(self, instance):
    #     if instance.role == 'Estudiante':
    #         return EstudianteSerializer(instance).data
    #     elif instance.role == 'Usuario_Bienestar':
    #         return UsuarioBienestarSerializer(instance).data
    #     else:
    #         return super().to_representation(instance)
    # calidar que el correo sea @campusucc.edu.co o @ucc.edu.co

    def validate_email(self, value):
    # Validacion personalizada
        if value == "":
            raise serializers.ValidationError("Error, el email no puede estar vacio")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Error, el correo ya existe")
        if not value.endswith('@campusucc.edu.co') and not value.endswith('@ucc.edu.co'):
            raise serializers.ValidationError("Error, el correo debe ser institucional")
        # if self.validate_name(self.context['name']) in value:
        #     raise serializers.ValidationError("Error, el nombre no puede estar en el email")
        return value
    
    

    def create(self, validated_data):
        role = validated_data.get('role')
        email = validated_data.get('email')
        username = email.split('@')[0]
        validated_data['username'] = username
        if role == 'Estudiante':
            # validated_data['username'] = username
            user = Estudiante(**validated_data)
        elif role == 'Usuario_Bienestar':
            # validated_data['username'] = username
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
    class Meta(UserSerializer.Meta):
        model = Estudiante
        fields = UserSerializer.Meta.fields + ['semester', 'accumulated_hours']

class UsuarioBienestarSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UsuarioBienestar
        fields = UserSerializer.Meta.fields + ['dimension']
