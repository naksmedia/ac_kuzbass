from django.contrib import admin
from .models import OrderService, OrderEmailTemplate
# Register your models here.
admin.site.register(OrderService)
admin.site.register(OrderEmailTemplate)