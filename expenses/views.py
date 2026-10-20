from django.contrib import messages
from django.db.models import Sum
from .models import Budget
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CustomUserCreationForm, UserForm,editProfileForm,addCategoryForm,addIncomeForm,addExpenseForm
from django.contrib.auth.decorators import login_required

from.models import Profile,Category,Income,Expense


@login_required(login_url='login')
def dashboard(request):

    profile = request.user.profile

    total_income = (
        Income.objects
        .filter(owner=profile)
        .aggregate(total=Sum('amount'))
        ['total']
        or 0
    )

    total_expense = (
        Expense.objects
        .filter(owner=profile)
        .aggregate(total=Sum('amount'))
        ['total']
        or 0
    )

    budget = (
    Budget.objects
    .filter(owner=profile)
    .aggregate(total=Sum('amount'))
    ['total']
    or 0
)

    budget_used = 0

    if budget > 0:
      budget_used = round((total_expense / budget) * 100, 2)

    recent_transactions = (
    Expense.objects
    .filter(owner=profile)
    .select_related('category')
    .order_by('-date')[:5]
)

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'budget':budget,
        'recent_transactions':recent_transactions
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profile(request):

    profile = request.user.profile


    context = {
        'profile': profile
    }
    return render(request,'account/profile.html',context )


def signupUser(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    form = CustomUserCreationForm()

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,"New account created successfully!")

            return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request,'account/signup.html',context)
 

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
    
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request,'user loged in successfully!')

            return redirect('dashboard')

    return render(
        request,
        'account/login.html'
    )


def logoutUser(request):

    logout(request)
    messages.success(request,'user loged out successfully!')

    return redirect('login')

@login_required(login_url='login')
def editUser(request):
    user = request.user
    profile= request.user.profile
    user_form=UserForm(instance=user)
    profile_form=editProfileForm(instance=profile)
    if request.method == 'POST':
        user_form=UserForm(request.POST, instance=user)
        profile_form=editProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request,'user edited successfully!')
            return redirect('profile')
        
    context={
        'user_form': user_form, 'profile_form': profile_form}
    return render(request,'account/edit-profile.html',context)

@login_required
def deleteProfile(request):

    profile = request.user.profile

    if request.method == 'POST':

        profile.delete()

        messages.warning(
            request,
            'Profile deleted successfully.'
        )

        return redirect('login')

    context = {
        'object_name': 'Profile',
        'object_display': request.user.username,
        'cancel_url': reverse('profile')
    }

    return render(
        request,
        'delete.html',
        context
    )

@login_required(login_url='login')
def category(request):
    profile=request.user.profile
    categories = profile.category_set.all()
    context={
        'categories': categories}
    return render(request,'category/category_list.html',context)

def addCategory(request):
    form = addCategoryForm()

    if request.method == 'POST':

        form = addCategoryForm(request.POST)

        if form.is_valid():

            category = form.save(commit=False)
            # assign to the model's ForeignKey field `owner`
            category.owner = request.user.profile
            messages.success(request,'Category added successfully successfully!')
            category.save()

            return redirect('categories')

    context = {
        'form': form,
        'is_edit': False,
    }

    return render(request,'category/category_form.html',context)

def editCategory(request,pk):
    profile=request.user.profile
    category=profile.category_set.get(id=pk)

    # instantiate form with the existing category so template knows it's an edit
    form = addCategoryForm(instance=category)

    if request.method=='POST':
        form=addCategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()

            messages.success(request,'Category edited successfully!')
            return redirect('categories')
        

    context={'form':form, 'is_edit': True}
    return render(request,'category/category_form.html',context)

def deleteCategory(request, pk):

    category = Category.objects.get(id=pk)

    if request.method == 'POST':

        category.delete()

        messages.warning(request,'Category deleted successfully!')


        return redirect('categories')

    context = {
        'object_name': 'Category',
        'object_display': category.name,
        'cancel_url': reverse('categories')
    }

    return render(
        request,
        'delete.html',
        context
    )


def income(request):
    profile=request.user.profile
    incomes=profile.income_set.all()
    context={'incomes':incomes,}
    return render(request,'income/income.html',context)

def addIncome(request):
    form=addIncomeForm()
    
    if request.method=='POST':
        form=addIncomeForm(request.POST)
        if form.is_valid():
            income=form.save(commit=False)
            income.owner=request.user.profile
            income.save()
            messages.success(request,'Income added successfully!')
            return redirect('income')
        
    context={'form':form}
    return render(request,'income/income_form.html',context)

def editIncome(request,pk):
    profile=request.user.profile
    income=profile.income_set.get(id=pk)

    form=addIncomeForm(instance=income)

    if request.method=='POST':
      form=addIncomeForm(request.POST,instance=income)
      if form.is_valid():
          form.save()
          messages.success(request,'Income edited successfully!')
          return redirect('income')
    
    context={'form':form}

    return render(request,'income/income_form.html',context)

def deleteIncome(request, pk):

    income = Income.objects.get(id=pk)

    if request.method == 'POST':

        messages.warning(request,'Income deleted successfully!')

        income.delete()



        return redirect('income')

    context = {
        'object_name': 'Income',
        'object_display': f'₹{income.amount}',
        'cancel_url': reverse('income')
    }

    return render(
        request,
        'delete.html',
        context
    )


def expense(request):
    profile=request.user.profile
    expenses=profile.expense_set.all()
    context={'expenses':expenses}
    return render(request,'expense/expense.html',context)

def addexpense(request):
    form=addExpenseForm()

    if request.method=='POST':
        form=addExpenseForm(request.POST)
        if form.is_valid():
            expense=form.save(commit=False)
            expense.owner=request.user.profile
            expense.save()
            messages.success(request,'expense added successfully!')
            return redirect('expense')
       

    profile=request.user.profile
    categories=profile.category_set.all()
    context={'form':form,'categories':categories}
    return render(request,'expense/expense_form.html',context)

def editexpense(request,pk):
    profile=request.user.profile
    expenses=profile.expense_set.get(id=pk)
    form=addExpenseForm(instance=expenses)
    if request.method=='POST':
        form=addExpenseForm(request.POST,instance=expenses)
        
        if form.is_valid():
            form.save()
            messages.success(request,'Expense edited successfully!')
            return redirect('expense')
    
    categories = profile.category_set.all()

    context={'form':form,'categories': categories}
    return render(request,'expense/expense_form.html',context)

def deleteExpense(request, pk):

    expense = Expense.objects.get(id=pk)

    if request.method == 'POST':

        messages.warning(request,'Expense deleted successfully!')

        expense.delete()

        

        return redirect('expense')

    context = {
        'object_name': 'Expense',
        'object_display': f'₹{expense.amount}',
        'cancel_url': reverse('expense')
    }

    return render(
        request,
        'delete.html',
        context
    )



        
    


    

