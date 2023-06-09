from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.template.loader import render_to_string
from .fields import OrderField


class Subject(models.Model):
	title=models.CharField(max_length=100)
	slug=models.SlugField(max_length=100)
	

	class Meta:
		ordering=['title']

	def __str__(self):
		return self.title


class Course(models.Model):
	owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='courses')
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='courses')
	title=models.CharField(max_length=100)
	slug=models.SlugField(max_length=100,unique=True)
	overview=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	students=models.ManyToManyField(User,blank=True,related_name='courses_joined')

	class Meta:
		ordering=['-created']

	def __str__(self):
		return self.title



class Module(models.Model):
	course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='modules')
	title=models.CharField(max_length=100)
	description=models.TextField(blank=True)
	order=OrderField(blank=True,null=True,for_fields=['course'])

	def __str__(self):
		return f'{self.order}.{self.title}'


class Content(models.Model):
	module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name='contents')
	content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':(
'text',
'video',
'image',
'file')})
	object_id=models.PositiveIntegerField()
	content_object=GenericForeignKey('content_type','object_id')
	order=OrderField(blank=True,for_fields=['module'])


class BaseItem(models.Model):
	owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related')
	title=models.CharField(max_length=100)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	def render(self):
		return render_to_string(f'courses/content/{self._meta.model_name}.html',{'item':self})

	class Meta:
		abstract=True

	def __str__(self):
		return self.title


class Text(BaseItem):
	content=models.TextField()


class File(BaseItem):
	file=models.FileField(upload_to='files')

class  Image(BaseItem):
	file=models.FileField(upload_to='images')

class Video(BaseItem):
	url=models.URLField()