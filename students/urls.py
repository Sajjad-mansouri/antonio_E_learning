from django.urls import path
from django.views.decorators.cache import cache_page
from . import views


urlpatterns=[
	path('register/',views.StudentRegistrationView.as_view(),name='student-register'),
	path('enroll/',views.StudentEnrollCourseView.as_view(),name='enroll-course'),
	path('courses/',views.StudentCourseListView.as_view(),name='student-course-list'),
	path('course/<pk>',cache_page(60*50)(views.StudentCourseDetailView.as_view()),name='student-course-detail'),
	path('course/<pk>/<module_id>',cache_page(60*50)(views.StudentCourseDetailView.as_view()),name='student-course_detail-module')
]

