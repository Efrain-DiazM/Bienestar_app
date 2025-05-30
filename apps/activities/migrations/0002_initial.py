# Generated by Django 5.1 on 2025-05-03 09:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.usuariobienestar'),
        ),
        migrations.AddField(
            model_name='attendanceactivity',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='activities.activity'),
        ),
        migrations.AddField(
            model_name='attendanceactivity',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.estudiante'),
        ),
        migrations.AddField(
            model_name='activity',
            name='dimension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.dimension'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='dimension',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activities.dimension'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='responsible',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.usuariobienestar'),
        ),
        migrations.AddField(
            model_name='historicalattendanceactivity',
            name='activity',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activities.activity'),
        ),
        migrations.AddField(
            model_name='historicalattendanceactivity',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalattendanceactivity',
            name='student',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.estudiante'),
        ),
        migrations.AddField(
            model_name='historicaldimension',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalprogramdimension',
            name='dimension',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activities.dimension'),
        ),
        migrations.AddField(
            model_name='historicalprogramdimension',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsubprogramdimension',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='programdimension',
            name='dimension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.dimension'),
        ),
        migrations.AddField(
            model_name='historicalsubprogramdimension',
            name='program_dimension',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activities.programdimension'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='program_dimension',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activities.programdimension'),
        ),
        migrations.AddField(
            model_name='activity',
            name='program_dimension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.programdimension'),
        ),
        migrations.AddField(
            model_name='subprogramdimension',
            name='program_dimension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.programdimension'),
        ),
        migrations.AddField(
            model_name='historicalactivity',
            name='subprogram_dimension',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='activities.subprogramdimension'),
        ),
        migrations.AddField(
            model_name='activity',
            name='subprogram_dimension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.subprogramdimension'),
        ),
        migrations.AlterUniqueTogether(
            name='attendanceactivity',
            unique_together={('activity', 'student')},
        ),
    ]
