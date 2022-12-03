from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField, SlugRelatedField

from mainapp.models import Direction, Discipline, Group, Student, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'groups')


# class TutorRelatedField(serializers.StringRelatedField):
#     def get_queryset(self):
#         queryset = User.objects.filter(groups_name = 'tutors')
#         return queryset
#

class DirectionSerializer(serializers.ModelSerializer):
    tutor = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.filter(groups__name = 'tutors'))

    class Meta:
        model = Direction
        fields = ('name', 'tutor', 'disciplines')


class DirectionListSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField(many=False)

    class Meta:
        model = Direction
        fields = ('name', 'tutor', 'disciplines')


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('name', 'directions')


class ReportDirectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direction
        fields = ('name', 'tutor', 'disciplines')

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'disciplines': ', '.join(list(map(str, instance.disciplines.all()))),
            'tutor_username': instance.tutor.username,
            'tutor_fullname': ' '.join([instance.tutor.first_name, instance.tutor.last_name]),
            'tutor_email': instance.tutor.email,
        }


class ReportGroupSerializer(serializers.ModelSerializer):
    students = SerializerMethodField()
    men = serializers.IntegerField()
    women = serializers.IntegerField()
    seats_available = serializers.IntegerField()

    def get_students(self, obj):
        return ', '.join(list(map(str, obj.students.all())))

    class Meta:
        model = Group
        fields = ('name', 'students', 'men', 'women', 'seats_available')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'direction')



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('fio', 'group', 'gender')

    def validate_group(self, group):
        seats_available = Group.MAX_STUDENTS_COUNT - group.students.count()
        if (not self.instance or self.instance and self.instance.group != group) and seats_available <= 0:
            raise serializers.ValidationError('В группе нет свободных мест')
        return group