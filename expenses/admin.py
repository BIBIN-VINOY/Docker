from django.contrib import admin

# Register your models here.
from .models import Category, Income, Expense,Profile

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Income) 
admin.site.register(Expense)

