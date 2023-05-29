from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.apps import app
from django.urls import reverse_lazy,reverse
from .forms import Modul_Formset
from .models import Course,Content



class OwnerMixin:
	def get_queryset(self):
		query=super().get_queryset()
		return query.filter(owner=self.request.user)

class OwnerEditMixin:
	def form_valid(self,form):
		form.instance.owner=self.request.user
		return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
	model=Course
	fields=['title','subject','slug','overview']
	success_url=reverse_lazy('course-list')

class OwnerCourseEditMix(OwnerCourseMixin,OwnerEditMixin):
	template_name='courses/course/course-form.html'




class CourseListView(OwnerCourseMixin,ListView):
	template_name='courses/course/course-list.html'
	permission_required='courses.view_course'

class CourseCreateView(OwnerCourseEditMix,CreateView):
		permission_required='courses.add_course'

class CourseUpdateView(OwnerCourseEditMix,UpdateView):
		permission_required='courses.change_course'


class CourseDeleteView(OwnerCourseMixin,DeleteView):
		template_name='courses/course/course-delete.html'
		permission_required='courses.delete_course'



class CourseModule(UpdateView):
	template_name='courses/module/formset.html'
	# success_url=reverse_lazy('course-list')

	def get_form(self):
		return Modul_Formset(**self.get_form_kwargs())

	def get_form_kwargs(self):
		kwargs={}
		if self.request.method in ("POST", "PUT"):
			kwargs.update(
				{
					"data": self.request.POST,
					"files": self.request.FILES,
				}
			)
		object=self.get_object()
		kwargs.update({'instance':object})
		return kwargs
	def get_object(self):
		pk = self.kwargs.get(self.pk_url_kwarg)
		obj=get_object_or_404(Course,pk=pk)
		return obj

	def get_success_url(self):
		return reverse('course-list')


class CourseContent(TemplateResponseMixin,View):
	template_name='courses/content/content.html'

	def get_model(self,model_name):
		if model_name in ['text', 'video', 'image', 'file']:
			return apps.get_model(app_label='courses',model_name=model_name)

		else:
			return None
	def dispatch(self,request,module_id,model_name,id=None):
		self.module=get_object_or_404(Module,id=module_id,course__owner=request.user)
		self.model=self.get_model(model_name)
		if id:
			self.obj=get_object_or_404(self.model,id=id,owner=request.user)
		return super().dispatch(request,module_id,model_name,id)

	def get_form(self,model,*args,**kwargs):
		form=modelformset_factory(model,exclude=['owner','created','updated','order'])
		return form(*args,**kwargs)

	def get(self,request,module_id,model_name,id=None):
		form=self.get_form(self.model,instance=self.obj)
		return self.render_to_response({'form':form,'object':self.obj})

	def post(self,request,module_id,model_name,id=None):
		form=self.get_form(self.model,instance=self.obj,data=request.POST,files=request.FILES)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.owner=request.user
			obj.save()
			if not id:
				Content.objects.create(module=self.module,content_object=obj)

			return redirect('content-list',self.module_id)
		else:
			return self.render_to_response({'form':form,'object':self.obj})

