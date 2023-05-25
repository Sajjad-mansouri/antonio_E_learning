from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Course



class OwnerMixin:
	def get_queryset(self):
		query=super().get_queryset()
		return query.filter(owner=self.request.user)

class OwnerEditMixin:
	def form_valid(self,form):
		form.instanc.owner=self.request.user
		return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin):
	model=Course
	field=['title','subject','slug','overview']
	success_url=reverse_lazy('course-list')

class OwnerCourseEditMix(OwnerCourseMixin,OwnerEditMixin):
	template_name='courses/course/course-form.html'




class CourseListView(OwnerCourseMixin,ListView):
	template_name='courses/course/list.html'

class CourseCreateView(OwnerCourseEditMix,CreateView):
	pass
class CourseUpdateView(OwnerCourseEditMix,UpdateView):
	pass

class CourseDeleteView(OwnerCourseMixin,DeleteView):
		template_name='courses/course/course-delete.html'

