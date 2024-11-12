from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('Administrador', 'Administrador'),
        ('Usuario_Bienestar', 'Usuario Bienestar'),
        ('Estudiante', 'Estudiante'),
    )

    TYPODOC =(
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
    )

    GENDERS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True)
    name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    type_document = models.CharField('Tipo de documento', max_length=2, choices=TYPODOC, default='CC')
    identification = models.CharField('Documento', max_length=20, blank=True, null=True, unique=True)
    phone_number = models.CharField('Celular', max_length=15, blank=True, null=True)
    gender = models.CharField('Género', max_length=1, choices=GENDERS)
    image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField('Rol', max_length=20, choices=ROLES, default='Estudiante')
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name', 'role']

    def __str__(self):
        return f'{self.name} {self.last_name} {self.role}'
    
class AcademicProgram(models.Model):
    name = models.CharField('Nombre', max_length=255, blank=False, null=False)
    code = models.CharField('Código', max_length=10, unique=True)

    class Meta:
        verbose_name = 'Programa Académico'
        verbose_name_plural = 'Programas Académicos'

    def __str__(self):
        return self.name


class Estudiante(User):
    semester = models.IntegerField('Semestre')
    academic_program = models.ForeignKey(AcademicProgram, on_delete=models.PROTECT)
    accumulated_hours = models.DecimalField('Horas Acumuladas', max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def create(self, validated_data):
        print("Datos recibidos desde el frontend:", validated_data)


class UsuarioBienestar(User):
    dimension = models.CharField('Dimensión Académica', max_length=255)

    class Meta:
        verbose_name = 'Usuario Bienestar'
        verbose_name_plural = 'Usuarios Bienestar'
    
    def __str__(self):
        return f'{self.name} {self.last_name}'
