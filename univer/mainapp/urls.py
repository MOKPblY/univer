from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from mainapp.views import StudentViewSet, GroupViewSet, DisciplineViewSet, DirectionViewSet, TutorViewSet, \
    ReportDirectionViewSet, ReportGroupViewSet, GetReportView, GetReportStatusView, DownloadReportView

direction_router = routers.SimpleRouter()
discipline_router = routers.SimpleRouter()
group_router = routers.SimpleRouter()
student_router = routers.SimpleRouter()
tutor_router = routers.SimpleRouter()
report_direction_router = routers.SimpleRouter()
report_group_router = routers.SimpleRouter()

direction_router.register(r'directions', DirectionViewSet)
discipline_router.register(r'disciplines', DisciplineViewSet)
group_router.register(r'groups', GroupViewSet)
student_router.register(r'students', StudentViewSet)
tutor_router.register(r'tutors', TutorViewSet)
report_direction_router.register(r'report_dirs', ReportDirectionViewSet)
report_group_router.register(r'report_groups', ReportGroupViewSet)

urlpatterns = [
    path('', include(direction_router.urls)),
    path('', include(discipline_router.urls)),
    path('', include(group_router.urls)),
    path('', include(student_router.urls)),
    path('', include(tutor_router.urls)),
    path('', include(report_direction_router.urls)),
    path('', include(report_group_router.urls)),
    path('getreport/', GetReportView.as_view()),
    path('getrepstat/', GetReportStatusView.as_view()),
    path('downloadreport/', DownloadReportView.as_view()),
    path('auth/', include('rest_framework.urls')),
    #path('report/', get_report),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ]