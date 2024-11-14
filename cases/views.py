from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib import messages
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.template.loader import get_template
# from weasyprint import HTML, CSS
from xhtml2pdf import pisa
from .gen_pdf import link_callback
import re
from pathlib import Path
import shutil
import tempfile


# Create your views here.


# ======== Start Home Page ========

def home_page(request):
   
    
    context = {}
    return render(request, "home_page.html", context)


# ======== End Home Page ========


# ======== Start Client Create,Edit,Details,view ========
@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def client_create(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client = client_form.save()
            return redirect(reverse("cases:client_details", args=[client.id]))
    else:
        client_form = ClientForm()

    context = {
        "client_form": client_form,
    }
    return render(request, "create_client.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_edit(request, id):
    client = Client.objects.get(id=id)
    if request.method == "POST":
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            return redirect(reverse("cases:client_details", args=[client.id]))
    else:
        client_form = ClientForm(instance=client)

    context = {
        "client_form": client_form,
    }
    return render(request, "edit_client.html", context)

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def client_details(request, id):
    client = Client.objects.get(id=id)
    cases = Cases.objects.filter(client=client).order_by('-created_at')
    context = {
        "client_details": client,
        "cases": cases,
    }
    return render(request, "client_details.html", context)


@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def clients_view(request):
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
       
    }
    return render(request, "clients_view.html", context)


# ======== End Client Create,Edit,Details,view ========

# ======== Start Case Create,Edit,Details ========

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_create(request, id):
    client = Client.objects.get(id=id)
    if request.method == "POST":
        case_form = CaseForm(request.POST)
        if case_form.is_valid():
            form = case_form.save(commit=False)
            form.client = client
            form.save()
            return redirect(reverse("cases:case_details", args=[form.id]))
    else:
        case_form = CaseForm()

    context = {
        "case_form": case_form,
    }
    return render(request, "case_create.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def case_edit(request, id):
    case = Cases.objects.get(id=id)
    if request.method == "POST":
        case_form = CaseForm(request.POST, instance=case)
        if case_form.is_valid():
            form = case_form.save()
            return redirect(reverse("cases:case_details", args=[form.id]))
    else:
        case_form = CaseForm(instance=case)
    context = {
        "case_form": case_form,
    }
    return render(request, "case_edit.html", context)

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_details(request, id):
    case = Cases.objects.get(id=id)
    files = Cases.objects.prefetch_related("cases_files").all()
    sessions = CaseSessions.objects.all().filter(cases=case).all()

    context = {
        "case": case,
        "files": files,
        "sessions": sessions,
    }
    return render(request, "case_details.html", context)

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_text_field_edit(request, id):
    case = Cases.objects.get(id=id)
    if request.method == "POST":
        case_form = CasePart2Form(request.POST, instance=case)
        if case_form.is_valid():
            case_form.save()
            return redirect(reverse("cases:case_details", args=[case.id]))
    else:
        case_form = CasePart2Form(instance=case)

    context = {
        "case_form": case_form,
        "case": case,
    }
    return render(request, "case_text_field_edit.html", context)


# ======== End Case Create,Edit,Details ========


# ======== Start Case Files Create,Edit ========
@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_file_create(request, id):
    cases = Cases.objects.get(id=id)

    if request.method == "POST":
        case_file_form = CaseFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        
        for file in files:
            CasesFiles.objects.create(
                file=file,
                cases=cases,
            )
        return redirect(reverse("cases:case_details", args=[cases.id]))
    else:
        case_file_form = CaseFileForm()

    context = {
        "case_file_form": case_file_form,
        "cases": cases,
    }
    return render(request, "case_file_create.html", context)

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_file_edit(request, id):
    file = CasesFiles.objects.get(id=id)
    case_id = file.cases.id
    cases = Cases.objects.get(id=case_id)
    if request.method == "POST":
        case_file_form = CaseFileUpdateForm(request.POST, request.FILES, instance=file)
        if case_file_form.is_valid():
            case_file_form.save()
            return redirect(reverse("cases:case_details", args=[cases.id]))
    else:
        case_file_form = CaseFileForm(instance=file)

    context = {
        "case_file_form": case_file_form,
        "file": file,
    }
    return render(request, "case_file_update.html", context)



# ======== End Case Files Create,Edit ========


# ======== Start Case Sessions Create,Edit,Details ========
@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_sessions_create(request, id):

    case = Cases.objects.get(id=id)
    if request.method == "POST":
        session_form = CaseSessionsForm(request.POST)
        if session_form.is_valid():
            form = session_form.save(commit=False)
            form.cases = case
            form.save()
            return redirect(reverse("cases:case_details", args=[case.id]))
    else:
        session_form = CaseSessionsForm()
    context = {
        "session_form": session_form,
        "case": case,
    }
    return render(request, "case_sessions_create.html", context)

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_sessions_edit(request, id):
    session = CaseSessions.objects.get(id=id)
    if request.method == "POST":
        session_form = CaseSessionsForm(request.POST, instance=session)
        if session_form.is_valid():
            session_form.save()
            return redirect(reverse("cases:case_details", args=[session.cases.id]))

    else:
        session_form = CaseSessionsForm(instance=session)
    context = {
        "session_form": session_form,
        "session": session,
    }
    return render(request, "case_sessions_update.html", context)

@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_sessions_details(request, id):
    session = CaseSessions.objects.get(id=id)

    context = {
        "session": session,
    }
    return render(request, "case_sessions_details.html", context)

@login_required
def case_sessions_list(request):
    sessions = CaseSessions.objects.all()
    today = date.today()
    date_to_next_month = today + relativedelta(months=+1)
    sessions_for_next_month = []
    for session in sessions:
        if session.date >= today:
            if session.date <= date_to_next_month:
                sessions_for_next_month.append(session)
        else:
            pass

    context = {
        "sessions_for_next_month": sessions_for_next_month,
        "today": today,
        "date_to_next_month": date_to_next_month,
    }

    return render(request, "case_sessions_list.html", context)


# ======== End Case Sessions Create,Edit,Details ========


# ======== Start Case Payment Create ========
@login_required
@user_passes_test(lambda u: u.is_superuser)
def case_payment_create(request, id):
    cases = Cases.objects.get(id=id)
   
   
    if request.method == "POST":
        payment_form = CasePaymentForm(request.POST)
        if payment_form.is_valid():
            if payment_form.cleaned_data["paid"] <= 0:
                messages.error(request, "Error : You Cant Inter Nigtive value")

            else:
                form = payment_form.save(commit=False)
                form.cases = cases
                form.save()
                return redirect(reverse("cases:case_payment_create", args=[cases.id]))
    else:
        payment_form = CasePaymentForm()

    old_payments = CasePayment.objects.filter(cases=cases)

    old_payments_sum = 0

    for payment in old_payments:
        old_payments_sum += payment.paid

    not_paid = cases.case_price - old_payments_sum

    context = {
        "payment_form": payment_form,
        "old_payments": old_payments,
        "old_payments_sum": old_payments_sum,
        "not_paid": not_paid,
        "cases": cases,
    }
    return render(request, "case_payment_create.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_paymen_total(request, id):
    client = Client.objects.get(id=id)
    context= {"client":client,}
    return render(request, "client_paymen_total.html", context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def case_payment_delete(request, id):
    old_payments = CasePayment.objects.get(id=id)
    redirect_id = old_payments.cases.id
    old_payments.delete()
    return HttpResponseRedirect(
        reverse("cases:case_payment_create", args=[redirect_id])
    )


# ======== End Case Payment Create,Delete ========


# ======== Start Cases Events Create,Delete,View ========
@login_required
def case_event_view(request):
    
    if request.method == 'POST':
        date_form = CaseEventsForm(request.POST)
        value = date_form['date'].value()
        today = datetime.now().date()
        if date_form.is_valid():
            date_list = []
            date_list.extend(str(value).split('-')) 
            events = CasesEvents.objects.filter(start_date__year=date_list[0],
                                        start_date__month=date_list[1],
                                        start_date__day=date_list[2],
                                        ).order_by('start_date')
        
    else:
        date_form = CaseEventsForm()
        today = datetime.now().date()
        date_list = []
        date_list.extend(str(today).split('-')) 
        
        events = CasesEvents.objects.filter(start_date__year=date_list[0],
                                        start_date__month=date_list[1],
                                        start_date__day=date_list[2],
                                        ).order_by('start_date')
        

    events_id = []
    for a in events:
        events_id.append(int(a.id))
    
    context = {"date_form":date_form,
               'events':events,
               "today":today,
               "events_id":events_id,}
    return render(request, "case_event_view.html", context)


@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_event_create(request,id):
    cases = Cases.objects.get(id=id)
    
    if request.method == 'POST':
        event_form = CaseEventsCreateForm(request.POST)
        if event_form.is_valid():
            form = event_form.save(commit=False)
            form.cases=cases
            form.save()
            return redirect(reverse("cases:case_details", args=[cases.id]))
    else:
        event_form = CaseEventsCreateForm()
    context = {'event_form':event_form,
               'cases':cases}
    return render(request, "case_event_create.html", context)



@login_required
@permission_required('authentication.Lawyer_Active',raise_exception=True)
def case_event_delete(request, id):
    event = CasesEvents.objects.get(id=id)
    event.delete()
    return HttpResponseRedirect(
        reverse("cases:case_event_create", args=[event.cases.id])
    )
# ======== End Cases Events Create,Delete,View ========




# Genrate Pdf 

def events_pdf_view(request):
    template_path = 'pdf/events_pdf.html'


    events = "".join(request.GET.getlist('events_id'))
    events_id = re.findall(r'\d+',events)
    obj = []
    for i in events_id:
        obj.append(int(i))

    ev = CasesEvents.objects.filter(id__in=obj).order_by('start_date')

    context = {'events':ev}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if want to download 
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #  if want to open it
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    
  

    
   
    # create a pdf
    
    pisa_status = pisa.CreatePDF(
       html, dest=response,
       link_callback=link_callback)
    
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

