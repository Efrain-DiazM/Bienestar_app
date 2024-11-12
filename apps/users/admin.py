from django.contrib import admin
from apps.users.models import User, Estudiante, UsuarioBienestar, AcademicProgram

admin.site.register(User)
admin.site.register(Estudiante)
admin.site.register(UsuarioBienestar)
admin.site.register(AcademicProgram)
