from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .forms import CourseEnrollForm
from courses.models import Course


class StudentRegistrationView(CreateView):
	template_name='students/student/register.html'
	success_url=reverse_lazy('student-course-list') 
	form_class=UserCreationForm

	def form_valid(self,form):
		result=super().form_valid(form)
		cd=form.cleaned_data
		user=authenticate(username=cd['username'],password=cd['password1'])
		login(self.request,user)

		return result


class StudentEnrollCourseView(LoginRequiredMixin,FormView):

	form_class=CourseEnrollForm

	def form_valid(self,form):
		if form.is_valid():
			course=form.cleaned_data['course']
			course.students.add(self.request.user)
			return super().form_valid(form)

		return super().form_valid(form)

	def get_success_url(self):
		return reverse('student-course-list')



class StudentCourseListView(LoginRequiredMixin,ListView):
	model=Course
	template_name='students/student/course-list.html'

	def get_queryset(self):
		qs=super().get_queryset()
		return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin,DetailView):
	model=Course
	template_name='students/student/course-detail.html'

	def get_queryset(self):
		qs=super().get_queryset()
		return qs.filter(students__in=[self.request.user])		

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*args,**kwargs)
		course=self.get_object()
		if 'module_id' in self.kwargs:
			context['module']=course.modules.get(id=self.kwargs['module_id'])

		else:
			context['module']=course.modules.all()[0]

		return context