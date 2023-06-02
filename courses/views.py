from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.views import View
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404,redirect
from django.apps import apps
from django.urls import reverse_lazy,reverse
from django.db.models import Count
from .forms import Modul_Formset
from .models import Course,Content,Module,Subject
from students.forms import CourseEnrollForm


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
	template_name='courses/course/manage/course-form.html'




class CourseManageView(OwnerCourseMixin,ListView):
	template_name='courses/course/manage/course-list.html'
	permission_required='courses.view_course'

class CourseCreateView(OwnerCourseEditMix,CreateView):
		permission_required='courses.add_course'

class CourseUpdateView(OwnerCourseEditMix,UpdateView):
		permission_required='courses.change_course'


class CourseDeleteView(OwnerCourseMixin,DeleteView):
		template_name='courses/course/manage/course-delete.html'
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
	obj=None
	module=None
	model=None
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
		Form=modelform_factory(model,exclude=['owner','created','updated','order'])
		return Form(*args,**kwargs)

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

			return redirect('content-list',self.module.id)
		else:
			return self.render_to_response({'form':form,'object':self.obj})


class CourseContentDeleteView(View):
	def post(self,request,id):
		content=get_object_or_404(Content,id=id,module__course__owner=request.user)
		module=content.module
		content.delete()
		return redirect('content-list',module.id)


class ModuleContentListView(TemplateResponseMixin,View):
	template_name='courses/module/content-list.html'
	def get(self,request,module_id):
		module=get_object_or_404(Module,id=module_id,course__owner=request.user)
		return self.render_to_response({'module':module})



class CourseListView(TemplateResponseMixin,View):
	template_name='courses/course/list.html'

	def get(self,request,subject=None):
		subjects=Subject.objects.annotate(total_courses=Count('courses'))
		courses=Course.objects.annotate(total_module=Count('modules'))

		if subject:
			subject=get_object_or_404(Subject,slug=subject)
			courses=Course.objects.filter(subject=subject)

		return self.render_to_response({'subjects':subjects,'courses':courses,'subject':subject})


class CourseDetailView(DetailView):
	model=Course
	template_name='courses/course/detail.html'
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['form']=CourseEnrollForm(initial={'course':self.object})
		return context
