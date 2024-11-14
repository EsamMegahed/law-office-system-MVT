from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from cases.models import Client,CasesFiles, Cases, CaseSessions, CasePayment, CasesCategory
from .forms import CasesCategoryForm
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from decimal import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,user_passes_test
from authentication.forms import UserCreateForm,UserEditForm,UserPasswordChangeForm
from django.contrib.auth.models import User, Permission
from django.contrib import messages



# Create your views here.

# ------------ Start Home ------------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_home(request):
    today = date.today()
    last_week = today - timedelta(days=7)
    sessions = CaseSessions.objects.filter(created_at__gte=last_week).order_by(
        "-created_at"
    )
    num_clients = Client.objects.all().count()
    num_cases = Cases.objects.all().count()
    num_sessions = CaseSessions.objects.all().count()
    pays = CasePayment.objects.all()
    sum_pay = 0
    for pay in pays:
        sum_pay += pay.paid

    context = {
        "num_clients": num_clients,
        "num_cases": num_cases,
        "num_sessions": num_sessions,
        "sum_pay": sum_pay,
        "sessions": sessions,
    }
    return render(request, "dashboard_home.html", context)


# ------------ End Home ------------


# ------------ Start Case Section ------------


# ++++ Start Category Section ++++
@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_case_category(request):
    categories = CasesCategory.objects.all()
    if request.method == "POST":
        category_form = CasesCategoryForm(request.POST)
        if category_form.is_valid():
            name = category_form.cleaned_data["name"]
            if CasesCategory.objects.filter(name=name).exists():
                pass
            else:
                category_form.save()

            return redirect(reverse("dashboard:dashboard_case_category"))
    else:
        category_form = CasesCategoryForm()
    context = {
        "category_form": category_form,
        "categories": categories,
    }
    return render(request, "dashboard_case_category.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_case_category_delete(request, id):
    category = CasesCategory.objects.get(id=id)
    category.delete()
    return HttpResponseRedirect(reverse("dashboard:dashboard_case_category"))


# ++++ End Category Section ++++


# ++++ Start Client Section ++++

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_clients(request):
    clients_data = Client.objects.all()
    client = Client.objects.all()

    if request.method == "POST":
        client_search = request.POST.get("client_search_field")
        client = Client.objects.filter(name__icontains=client_search)
    else:
        client = Client.objects.all()

    paginator = Paginator(client, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "clients": page_obj,
        "clients_data": clients_data,
        # "client": client,
    }

    return render(request, "dashboard_clients.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_clients_delete(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return HttpResponseRedirect(reverse("dashboard:dashboard_clients"))


# ++++ End Client Section ++++


# ++++ Start Cases Section ++++

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_cases(request):
    cases_data = Cases.objects.all()
    cases = Cases.objects.all()
    if request.method == "POST":
        case_search = request.POST.get("case_number_search_field")
        cases = Cases.objects.filter(case_id__icontains=case_search)
    else:
        cases = Cases.objects.all()

    paginator = Paginator(cases, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "cases": page_obj,
        "cases_data": cases_data,
    }

    return render(request, "dashboard_cases.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_cases_delete(request, id):
    cases = Cases.objects.get(id=id)
    cases.delete()
    return HttpResponseRedirect(reverse("dashboard:dashboard_cases"))


# ++++ End Cases Section ++++

# ++++ Start Cases Sessions Section ++++
@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_sessions(request):
    cases_data = Cases.objects.all()
    cases = Cases.objects.all()
    if request.method == "POST":
        case_search = request.POST.get("case_number_search_field")
        cases = Cases.objects.filter(case_id__icontains=case_search)
    else:
        cases = Cases.objects.all()

    paginator = Paginator(cases, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "cases": page_obj,
        "cases_data": cases_data,
    }

    return render(request, "dashboard_sessions.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_sessions_view(request,id):
    cases = Cases.objects.get(id=id)
    sessions = CaseSessions.objects.filter(cases=cases).order_by("-created_at")
    context = {
        'sessions':sessions,
        'cases':cases,
    }

    return render(request, "dashboard_sessions_view.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_sessions_delete(request, id):
    session = CaseSessions.objects.get(id=id)
    session.delete()
    return HttpResponseRedirect(reverse("dashboard:dashboard_sessions_view",args=[session.cases.id]))


# ++++ End Cases Sessions Section ++++


# ++++ Start Cases Files Section ++++
@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_files(request):
    cases_data = Cases.objects.all()
    cases = Cases.objects.all()
    if request.method == "POST":
        case_search = request.POST.get("case_number_search_field")
        cases = Cases.objects.filter(case_id__icontains=case_search)
    else:
        cases = Cases.objects.all()
    paginator = Paginator(cases, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "cases": page_obj,
        "cases_data": cases_data,
    }

    return render(request, "dashboard_files.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_files_view(request,id):
    cases = Cases.objects.get(id=id)
    files = CasesFiles.objects.filter(cases=cases).order_by("-created_at")
    context = {
        'files':files,
        'cases':cases,
    }

    return render(request, "dashboard_files_view.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_file_delete(request, id):
    file = CasesFiles.objects.get(id=id)
    file.delete()
    return HttpResponseRedirect(reverse("dashboard:dashboard_files_view",args=[file.cases.id]))


# ++++ End Cases Files Section ++++



# ++++ Start Cases Charts Section ++++

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_cases_charts(request):
    # Category Charts
    Category_madni = Cases.objects.filter(category__name="مدنى").count()
    Category_genaey = Cases.objects.filter(category__name="جنائى").count()
    Category_osra = Cases.objects.filter(category__name="اسرة").count()
    Category_gonah = Cases.objects.filter(category__name="جنح").count()
    Category_3kod = Cases.objects.filter(category__name="صياغة عقود").count()
    Category_tra5es = Cases.objects.filter(category__name="تراخيص").count()
    others = Cases.objects.all().count() - (
        Category_madni
        + Category_genaey
        + Category_osra
        + Category_gonah
        + Category_3kod
        + Category_tra5es
    )
    # Sessions and cases Charts in monthis

    first_day_in_the_year = date(date.today().year, 1, 1)
    last_day_in_the_year = date(date.today().year, 12, 31)
    year = date.today().year
    sessions_data_months = []
    cases_data_months = []

    for i, x in enumerate(range(12)):
        session_month = CaseSessions.objects.filter(
            created_at__month=x,
        ).count()
        sessions_data_months.append(session_month)

        case_month = Cases.objects.filter(
            created_at__month=x,
        ).count()
        cases_data_months.append(case_month)

    context = {
        "Category_madni": Category_madni,
        "Category_genaey": Category_genaey,
        "Category_osra": Category_osra,
        "Category_gonah": Category_gonah,
        "Category_3kod": Category_3kod,
        "Category_tra5es": Category_tra5es,
        "others": others,
        "sessions": sessions_data_months,
        "cases": cases_data_months,
    }

    return render(request, "dashboard_cases_charts.html", context)


# ++++ End Cases Charts Section ++++

# ------------ End Case Section ------------


# ------------ Start Sales Section ------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_sales(request):
    cases_data = Cases.objects.all()
    cases = Cases.objects.all()
    if request.method == "POST":
        case_search = request.POST.get("case_number_search_field")
        cases = Cases.objects.filter(case_number__icontains=case_search)
    else:
        cases = Cases.objects.all()
    paginator = Paginator(cases, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "cases": page_obj,
        "cases_data": cases_data,
    }

    return render(request, "dashboard_sales.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_sales_view(request, id):
    cases = Cases.objects.get(id=id)
    payments = CasePayment.objects.filter(cases=cases).order_by("-created_at")
    sum_cash = 0
    for payment in payments:
        sum_cash += payment.paid
    context = {
        "paymets": payments,
        "case": cases,
        "sum_cash": sum_cash,
    }
    return render(request, "dashboard_sales_view.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_payment_delete(request, id):
    payment = CasePayment.objects.get(id=id)
    payment.delete()
    return HttpResponseRedirect(
        reverse("dashboard:dashboard_sales_view", args=[payment.cases.id])
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_sales_charts(request):
    # Sales Category

    # 1------ 'مدنى'
    Category_madni = Cases.objects.filter(category__name="مدنى")
    Category_madni_sum = 0
    for Category in Category_madni:
        for a in Category.cases_payment.all():
            Category_madni_sum += a.paid

    # 2------ 'جنائى'
    Category_genaey = Cases.objects.filter(category__name="جنائى")
    Category_genaey_sum = 0
    for Category in Category_genaey:
        for a in Category.cases_payment.all():
            Category_genaey_sum += a.paid

    # 3------ 'اسرة'
    Category_osra = Cases.objects.filter(category__name="اسرة")
    Category_osra_sum = 0
    for Category in Category_osra:
        for a in Category.cases_payment.all():
            Category_osra_sum += a.paid

    # 4------ 'جنح'
    Category_gonah = Cases.objects.filter(category__name="جنح")
    Category_gonah_sum = 0
    for Category in Category_gonah:
        for a in Category.cases_payment.all():
            Category_gonah_sum += a.paid

    # 5------ 'صياغة عقود'
    Category_3kod = Cases.objects.filter(category__name="صياغة عقود")
    Category_3kod_sum = 0
    for Category in Category_3kod:
        for a in Category.cases_payment.all():
            Category_3kod_sum += a.paid
    # 6------ 'تراخيص'
    Category_tra5es = Cases.objects.filter(category__name="تراخيص")
    Category_tra5es_sum = 0
    for Category in Category_tra5es:
        for a in Category.cases_payment.all():
            Category_tra5es_sum += a.paid

    # 6------ 'others'
    Category_all = Cases.objects.all()
    Category_all_sum = 0
    for Category in Category_all:
        for a in Category.cases_payment.all():
            Category_all_sum += a.paid

    other_category = Category_all_sum - (
        Category_madni_sum
        + Category_genaey_sum
        + Category_osra_sum
        + Category_gonah_sum
        + Category_3kod_sum
        + Category_tra5es_sum
    )

    # --------------- Sales Months---------------

    sales_data_months = []
    cases_data_months = []

    for i, x in enumerate(range(12)):
        # Sales Cash
        sales_month = CasePayment.objects.filter(
            created_at__month=x,
        )
        paid_sum = 0
        for sale in sales_month:
            paid_sum += sale.paid
        sales_data_months.append(paid_sum)

        # Cases Cash
        case_month = Cases.objects.filter(
            created_at__month=x,
        )
        cases_sum = 0
        for cases in case_month:
            cases_sum += cases.case_price
        cases_data_months.append(cases_sum)

    context = {
        "sales_data_months": sales_data_months,
        "cases_data_months": cases_data_months,
        # Category sales
        "Category_madni_sum": Category_madni_sum,
        "Category_genaey_sum": Category_genaey_sum,
        "Category_osra_sum": Category_osra_sum,
        "Category_gonah_sum": Category_gonah_sum,
        "Category_3kod_sum": Category_3kod_sum,
        "Category_tra5es_sum": Category_tra5es_sum,
        "other_category": other_category,
    }
    return render(request, "dashboard_sales_charts.html", context)


# ------------ End Sales Section ------------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_create(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            return redirect(reverse("dashboard:dashboard_user_details", args=[user.id]))
    else:
        user_form = UserCreateForm()

    context ={'user_form':user_form}
    return render(request, "auth/dashboard_user_create.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_list(request):
    users = User.objects.all()
    context ={'users':users}
    return render(request, "auth/dashboard_user_list.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_details(request,id):
    user = User.objects.get(id=id)
    if user.has_perm('authentication.Lawyer_Active') == True:
        perm = True
    else:
        perm = False
    context ={'user':user,
              'perm':perm}
    return render(request, "auth/dashboard_user_details.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_edit(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse("dashboard:dashboard_user_details", args=[user.id]))
    else:
        user_form = UserEditForm(instance=user)

    context ={'user_form':user_form,
              'user':user}
    return render(request, "auth/dashboard_user_edit.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(
        reverse("dashboard:dashboard_user_list")
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_password_change(request,id):

    user = User.objects.get(id=id)

    if request.method == 'POST':
        user_form = UserPasswordChangeForm(request.POST)
        if user_form.is_valid():
            password = user_form.cleaned_data['new_password']
            password_confirm = user_form.cleaned_data['confirm_password']
            
            if password == password_confirm :
                user.set_password(password)
                user.save()
                return redirect(reverse("dashboard:dashboard_user_details", args=[user.id]))
            else:
                messages.error(request, 'Wrong password Matching')
                return redirect(request.path)
    else:
        user_form = UserPasswordChangeForm()

    context ={
        'user_form':user_form,
        'user':user,
    }
    return render(request, "auth/dashboard_user_password_change.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_add_permission(request, id):
    
    user = User.objects.get(id=id)
    permission = Permission.objects.get(codename='Lawyer_Active')
    
    user.user_permissions.add(permission)
    

    
    return HttpResponseRedirect(
        reverse("dashboard:dashboard_user_details",args=[user.id])
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_user_remove_permission(request, id):
    
    user = User.objects.get(id=id)
    permission = Permission.objects.get(codename='Lawyer_Active')
    user.user_permissions.remove(permission)
    return HttpResponseRedirect(
        reverse("dashboard:dashboard_user_details",args=[user.id])
    )