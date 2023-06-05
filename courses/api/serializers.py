from rest_framework import serializers
from courses.models import Subject,Course,Module,Content

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model=Subject
		fields=['id','title','slug']

class ModuleSerializer(serializers.ModelSerializer):
	class Meta:
		model=Module
		fields=['order','title','description']

class CourseSerializer(serializers.ModelSerializer):
	modules=ModuleSerializer(many=True,read_only=True)
	class Meta:
		model=Course
		fields=['id','subject','title','slug','created','owner','modules']



class ContentObjectSerializer(serializers.ModelSerializer):
	def to_representation(self,value):
		return render.value()
class ContentSerializer(serializers.ModelSerializer):
	content_object=ContentObjectSerializer(read_only=True)
	class Meta:
		model=Content
		fields=['order','content_object']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
	course=ContentSerializer(many=True)
	class Meta:
		model=Module
		fields=['contents','title','description','order']
class CourseWithContentsSerializer(serializers.ModelSerializer):
	modules=ModuleWithContentsSerializer(many=True)
	class Meta:
		model=Course
		fields=['id','subject','title','slug','created','owner','modules']