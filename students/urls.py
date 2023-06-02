from django.urls import path
from . import views


urlpatterns=[
	path('register/',views.StudentRegistrationView.as_view(),name='student-register'),
	path('enroll/',views.StudentEnrollCourseView.as_view(),name='enroll-course')
]

