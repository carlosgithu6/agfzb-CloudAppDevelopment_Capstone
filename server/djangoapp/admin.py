from django.contrib import admin
from .models import CarModel,CarMake



admin.site.register(CarModel)

# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

class CarMakeAdmin(admin.ModelAdmin):
    fields = ['Name',  'Description']
    inlines=[CarModelInline]

admin.site.register(CarMake,CarMakeAdmin)
