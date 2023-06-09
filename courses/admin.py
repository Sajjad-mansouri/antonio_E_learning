from django.contrib import admin
from .models import Subject,Course,Module

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display=['title','slug']
	prepopulated_fields={'slug':('title',)}


class ModuleInline(admin.StackedInline):
	model=Module
	extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display=['pk','title','subject','owner','created']
	list_filter=['created','subject']
	search_fields=['title','Subject','owner','overview']
	inlines=[ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
	list_display=['pk','title']