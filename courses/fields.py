from django.db import models

class OrderField(models.PositiveIntegerField):
	def __init__(self,for_fields=None,*args,**kwargs):
		self.for_fields=for_fields
		super().__init__(*args,**kwargs)


	def pre_save(self,model_instance,add):
		if getattr(model_instance,self.attname) is None:
			try:
				qs=self.models.objects.all()
				if self.for_fields:
					query={field:getattr(model_instance,field) for field in for_fields}
					qs=qs.filter(**query)
				last_item=qs.last(self.attname)
				value=last_item.value+1
			except ObjectDoesNotExist:
				value=0

			setattr(model_instance,self.attname,value)
			return value


		else:
			super().pre_save(model_instance,add)