from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from smartphones.models import Smartphone, Sale
from django.db.models.functions import TruncMonth
import datetime


@login_required(login_url='/login/')
def index(request):
    top_brands = Smartphone.objects.values('brand').annotate(num_sales=Count('sale')).order_by('-num_sales')[:3]
    overall_sales = Sale.objects.count()
    brands = list(top['brand'] for top in top_brands)
    brands.append('other')
    sales = list(top['num_sales'] for top in top_brands)
    sales.append(overall_sales - sum(sales))
    today = datetime.datetime.now()
    sales_current_year = Sale.objects.filter(created_at__year=today.year)
    sales_by_month = sales_current_year.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
    total_sales = []
    j = 0
    smartphones = Smartphone.objects.all()
    storages = list(set(smartphone.storage for smartphone in smartphones))
    top_storages = Smartphone.objects.values('storage').annotate(num_sales=Count('sale')).order_by('storage')
    for i in range(1, 13):
        if len(sales_by_month) > 0:
            if sales_by_month[j]['month'].month == i:
                total_sales.append(sales_by_month[j]['total'])
                j += 1
            else:
                total_sales.append(0)
    context = {
        'brands': brands,
        'sales': sales,
        'total_sales': total_sales,
        'storages': sorted(storages),
        'top_storages': list(top['num_sales'] for top in top_storages),
        'overall_sales': overall_sales,
        'in_stock': smartphones.count(),
    }
    return render(request, 'smartphones/home.html', context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.warning(request, "Invalid username or password.")
                return render(request=request, template_name="smartphones/login_new.html", context={"form": form})

        else:
            messages.warning(request, "Invalid username or password.")
            return render(request=request, template_name="smartphones/login_new.html", context={"form": form})
    form = AuthenticationForm()
    return render(request=request, template_name="smartphones/login_new.html", context={"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        messages.warning(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name="smartphones/register_new.html", context={"form": form})
    form = UserCreationForm
    return render(request=request, template_name="smartphones/register_new.html", context={"form": form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def smartphones_view(request):
    smartphones = Smartphone.objects.all()
    brands = set(smartphone.brand for smartphone in smartphones)
    storages = set(smartphone.storage for smartphone in smartphones)
    context = {
        'smartphones': smartphones,
        'brands': sorted(brands),
        'storages': sorted(storages),
    }
    return render(request, 'smartphones/smartphones_list.html', context)


@login_required(login_url='/login/')
def filter_view(request):
    if request.method == 'POST':
        checked_brands = request.POST.getlist('brands')
        checked_storages = request.POST.getlist('storages')
        smartphones = Smartphone.objects.all()
        brands = set(smartphone.brand for smartphone in smartphones)
        storages = set(smartphone.storage for smartphone in smartphones)
        if len(checked_brands) != 0:
            smartphones = smartphones.filter(brand__in=checked_brands)
        if len(checked_storages) != 0:
            smartphones = smartphones.filter(storage__in=checked_storages)
        context = {
            'smartphones': smartphones,
            'brands': sorted(brands),
            'checked_brands': checked_brands,
            'checked_storages': list(map(int, checked_storages)),
            'storages': sorted(storages),
        }
        return render(request, 'smartphones/smartphones_list_filtered.html', context)


@login_required(login_url='/login/')
def sales_view(request):
    sales = Sale.objects.all()
    context = {
        'sales': sales
    }
    return render(request, 'smartphones/tables.html', context)
