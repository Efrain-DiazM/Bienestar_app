from rest_framework import serializers
from apps.activities.models import Activity
from apps.activities.api.serializers.general_serializers import DimensionSerializer, ProgramDimensionSerializer, SubprogramDimensionSerializer

class ActivitySerializer(serializers.ModelSerializer):
    # dimension = serializers.StringRelatedField()
    # program_dimension = serializers.StringRelatedField()
    # subprogram_dimension = serializers.StringRelatedField()
    # responsible = serializers.StringRelatedField()

    class Meta:
        model = Activity
        exclude = ('created_date','modified_date','deleted_date',)

    # def to representation
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'state': instance.state,
            'name': instance.name,
            'description': instance.description,
            'dimension': instance.dimension.name,
            'program_dimension': instance.program_dimension.name,
            'subprogram_dimension': instance.subprogram_dimension.name,
            'responsible': instance.responsible.username,
            'date': instance.date,
            'start_hour': instance.start_hour,
            'end_hour': instance.end_hour,
            'count_hours': instance.count_hours,
        }