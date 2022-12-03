from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Q, F
from django.http import HttpResponse, FileResponse
from django_celery_results.models import TaskResult

from rest_framework import viewsets, mixins

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_api_key.permissions import HasAPIKey

from mainapp.tasks import get_and_save_report
from mainapp.models import Discipline, Direction, Group, Student, User
from mainapp.permissions import HasGroupPermission
from mainapp.serializers import DirectionSerializer, DisciplineSerializer, GroupSerializer, StudentSerializer, \
    UserSerializer, DirectionListSerializer, ReportGroupSerializer, \
    ReportDirectionSerializer


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects
    serializer_class = DirectionSerializer
    permission_classes = [IsAdminUser, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return DirectionListSerializer
        else:
            return DirectionSerializer


class ReportDirectionViewSet(mixins.ListModelMixin,
                   GenericViewSet):

     queryset = Direction.objects.prefetch_related('disciplines').select_related('tutor')
     serializer_class = ReportDirectionSerializer
     permission_classes = [IsAdminUser|HasAPIKey]


class ReportGroupViewSet(mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Group.objects.prefetch_related('students').annotate(
        men = Count('id', filter = Q(students__gender = Student.Genders.MALE)),
        women = Count('students') - F('men'),
        seats_available = Group.MAX_STUDENTS_COUNT - F('men') - F('women'),
    )
    serializer_class = ReportGroupSerializer
    permission_classes = [IsAdminUser | HasAPIKey]


class GetReportView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        get_and_save_report.delay()
        return Response({'message': 'Попытка генерации отчета.'})


class GetReportStatusView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        res_obj = TaskResult.objects.first()
        data = {'task_result': res_obj.status, 'result': res_obj.result}
        return Response(data)


class DownloadReportView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        response = FileResponse(open('report.xlsx', 'rb'), as_attachment=True,  filename="report.xlsx")
        return response


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects
    serializer_class = DisciplineSerializer
    permission_classes = [IsAdminUser, ]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects
    serializer_class = GroupSerializer
    permission_classes = [HasGroupPermission,]
    required_groups = ['tutors',]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects
    serializer_class = StudentSerializer
    permission_classes = [HasGroupPermission,]
    required_groups = ['tutors',]


class TutorViewSet(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    permission_classes = [HasGroupPermission,]
    required_groups = ['tutors',]
