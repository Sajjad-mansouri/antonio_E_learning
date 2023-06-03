from django.urls import path
from . import views


urlpatterns=[
	path('register/',views.StudentRegistrationView.as_view(),name='student-register'),
	path('enroll/',views.StudentEnrollCourseView.as_view(),name='enroll-course'),
	path('courses/',views.StudentCourseListView.as_view(),name='student-course-list'),
	path('course/<pk>',views.StudentCourseDetailView.as_view(),name='student-course-detail'),
	path('course/<pk>/<module_id>',views.StudentCourseDetailView.as_view(),name='student-course_detail-module')
]

