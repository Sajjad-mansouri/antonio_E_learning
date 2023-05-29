from django.urls import path
from . import views

urlpatterns=[
	path('',views.CourseListView.as_view(),name='course-list'),
	path('create/',views.CourseCreateView.as_view(),name='course-create'),
	path('<pk>/update/',views.CourseUpdateView.as_view(),name='course-update'),
	path('<pk>/delete/',views.CourseDeleteView.as_view(),name='course-delete'),
	path('<pk>/module/',views.CourseModule.as_view(),name='course-module')



]