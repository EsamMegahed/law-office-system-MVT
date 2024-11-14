from typing import Any
from django import forms
from .models import Client, Cases, CasesFiles, CaseSessions, CasePayment,CasesEvents
from django.contrib.admin import widgets
from django.utils.translation import gettext_lazy as _

# User Forms ---------------------


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["style"] = "text-align: right; direction: rtl;"

    class Meta:
        model = Client
        fields = ["name", "phone", "whatsapp", "adress"]


class CaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["style"] = "text-align: right; direction: rtl;"

    class Meta:
        model = Cases
        fields = [
            "category",
            "case_name",
            "case_description",
            "case_number",
            "case_price",
        ]


class CasePart2Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["style"] = "text-align: right; direction: rtl;"

    class Meta:
        model = Cases
        fields = ["case_description", "case_plan", "Case_loopholes"]


class CaseFileForm(forms.ModelForm):
    file = forms.FileField(label= _('file'),
        widget=forms.TextInput(
            attrs={
                "name": "file",
                "type": "File",
                "class": "form-control",
                "multiple": "True",
            }
        ),
    )

    class Meta:
        
        model = CasesFiles
        fields = ["file"]


class CaseFileUpdateForm(forms.ModelForm):
    class Meta:
        model = CasesFiles
        fields = ["file"]


class CaseSessionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["style"] = "text-align: right; direction: rtl;"
        
    date = forms.DateField(
        label=_('Date of Sessions'),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    # widgets = {
    #         'released_at':forms.TextInput(attrs={'type':'datetime-local'}),
    #     }

    class Meta:
        model = CaseSessions
        fields = ["date", "session_description"]


class CasePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["style"] = "text-align: right; direction: rtl;"
    class Meta:
        model = CasePayment
        fields = ["paid"]



class CaseEventsForm(forms.Form):
    date = forms.DateField(
            label=_('Event Day'),
            required=True,
            widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"],
        )   

# %Y-%m-%d %H:%M:%S


class CaseEventsCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["style"] = "text-align: right; direction: rtl;"
        
    start_date = forms.CharField(
        label=_('Start Time'),
        required=True,
        widget=forms.TextInput(attrs={"type": "datetime-local"}),
        
        
    )
    End_date = forms.CharField(
        label=_('ُEnd Time'),
        required=True,
        widget=forms.TextInput(attrs={"type": "datetime-local"}),
    )
    class Meta:
        model = CasesEvents
        fields = ["location", "task","start_date","End_date"]
