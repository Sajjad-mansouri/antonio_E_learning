from django.urls import path
from . import views

urlpatterns=[
	path('',views.CourseManageView.as_view(),name='course-list'),
	path('subject/<slug:subject>/',views.CourseListView.as_view(),name='subject-course-list'),
	path('<slug>/',views.CourseDetailView.as_view(),name='course-detail'),
	path('create/',views.CourseCreateView.as_view(),name='course-create'),
	path('<pk>/update/',views.CourseUpdateView.as_view(),name='course-update'),
	path('<pk>/delete/',views.CourseDeleteView.as_view(),name='course-delete'),
	path('<pk>/module/',views.CourseModule.as_view(),name='course-module'),
	path('module/<int:module_id>/',views.ModuleContentListView.as_view(),name='content-list'),
	path('module/<int:module_id>/content/<model_name>/',views.CourseContent.as_view(),name='content-create'),
	path('module/<int:module_id>/content/<model_name>/<id>/',views.CourseContent.as_view(),name='content-update'),
	path('content/<int:id>/delete',views.CourseContentDeleteView.as_view(),name='content-delete')




]