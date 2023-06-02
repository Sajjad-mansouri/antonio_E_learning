from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm


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
		return reverse('courses')
