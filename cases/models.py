import os
import random
import uuid
from django.db import models
from django.core.validators import FileExtensionValidator
from random import randrange ,randint
from project import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
# Create your models here.


class Client(models.Model):
    name = models.CharField(_("name"),max_length=300)
    phone = models.CharField(_("phone"),max_length=20)
    whatsapp = models.CharField(_("whatsapp"),max_length=20, blank=True, null=True)
    adress = models.CharField(_("adress"),max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
    
    def sum_cases_payment(self):
        total_cases = 0
        cases = self.client_cases.all()
        for single_case in cases:
            total_cases += single_case.case_price
        return total_cases
    
    def sum_cases_payment_paid(self):
        
        total_sum_paid = 0
        cases = self.client_cases.all()
        for single_case in cases:
            payments = single_case.cases_payment.all()
            for payment in payments:
                total_sum_paid += payment.paid
        return total_sum_paid
    
    def sum_cases_payment_unpiad(self):
        total_sum_unpaid = self.sum_cases_payment() - self.sum_cases_payment_paid()
        return total_sum_unpaid
    


class CasesCategory(models.Model):
    name = models.CharField(_("name"),max_length=300)

    def __str__(self) -> str:
        return str(self.name)


class CasesFiles(models.Model):
    file = models.FileField(_("file"),upload_to="cases_Files")
    created_at = models.DateTimeField(auto_now_add=True)

    cases = models.ForeignKey(
        "Cases",verbose_name=_('Case Files'), on_delete=models.CASCADE, related_name="cases_files"
    )

    def __str__(self) -> str:
        return str(self.file)

    @property
    def relative_path(self):
        return os.path.relpath(self.file.url, settings.MEDIA_ROOT)


class CaseSessions(models.Model):
    date = models.DateField(_("date"),)
    session_description = models.TextField(_("session description"),blank=True, null=True)
    active = models.BooleanField(_("active"),default=False)
    cases = models.ForeignKey(
        "Cases",verbose_name=_('Case Sessions'), on_delete=models.CASCADE, related_name="cases_sessions"
    )
    created_at = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)


class CasePayment(models.Model):
    cases = models.ForeignKey(
        "Cases",verbose_name=_('Case Payment'), on_delete=models.CASCADE, related_name="cases_payment"
    )
    paid = models.DecimalField(_("paid"),decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)


class Cases(models.Model):

    def random_number():
        a = random.randint(1000000, 9999999)
        b = Cases.objects.values_list('case_id')
        for num in b:
            if a == b:
                a = random.randint(1000000, 9999999)
        return a

    client = models.ForeignKey(
        Client,verbose_name=_('Client'), on_delete=models.CASCADE, related_name="client_cases", null=True
    )
    category = models.ForeignKey(
        CasesCategory,
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        related_name="cases_category",
        null=True,
    )
    case_name = models.CharField(_("case name"),max_length=300)
    case_description = models.TextField(_("case description"),blank=True, null=True)
    case_number = models.CharField(_("case number"),max_length=300)
    case_plan = models.TextField(_("case plan"),blank=True, null=True)
    Case_loopholes = models.TextField(_("Case loopholes"),blank=True, null=True)
    case_price = models.DecimalField(_("case price"),
        decimal_places=2,
        max_digits=12,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    case_id = models.CharField(_("case id"),
        max_length=10, blank=True, editable=False, unique=True, default=random_number
    )
    updated = models.DateTimeField(auto_now=True)

    def sum_paid_money(self):
        total = 0
        case_paid = self.cases_payment.all()
        for payment in case_paid:
            total += payment.paid
        return total
    
    def sum_not_paid_money(self):
        case_price = self.case_price
        paid = self.sum_paid_money()
        total =  case_price - paid 
        return total


class CasesEvents(models.Model):
    cases = models.ForeignKey(
        Cases,
        verbose_name=_('Case Events'),
        on_delete=models.SET_NULL,
        related_name="cases_events",
        null=True,
        blank=True
    )
    location = models.CharField(_("location"),max_length=600)
    task = models.TextField(_("task"),blank=True, null=True)
    start_date = models.DateTimeField(_("start_date"),)
    End_date = models.DateTimeField(_("End_date"),blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
