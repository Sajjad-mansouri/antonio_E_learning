from django.shortcuts import render
from django.views.generic import ListView
from .models import Course

class CourseListView(ListView):
	model=Course
	template_name='courses/course/list.html'
	def get_queryset(self):
		query=super().get_queryset()
		return query.filter(owner=self.request.user)
