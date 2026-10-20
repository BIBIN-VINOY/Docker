from django.http import HttpResponse
from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signupUser, name='signup'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('edit-profile/', views.editUser, name='edit-profile'),
    path('delete-profile/', views.deleteProfile, name='delete-profile'),
    path('categories/', views.category, name='categories'),

    path('add-category/', views.addCategory, name='add-category'),

    path('edit-category/<str:pk>/', views.editCategory,name='edit-category'),

    path('delete-category/<str:pk>/', views.deleteCategory, name='delete-category'),
    path('income/', views.income, name='income'),
    path('add-income/', views.addIncome, name='add-income'),
    path('edit-income/<str:pk>', views.editIncome, name='edit-income'),
    path('delete-income/<str:pk>', views.deleteIncome, name='delete-income'),
    path('expense/', views.expense, name='expense'),
    path('addexpense/', views.addexpense, name='add-expense'),
    path('editexpense/<str:pk>', views.editexpense, name='edit-expense'),
    path('deleteexpense/<str:pk>', views.deleteExpense, name='delete-expense'),

]