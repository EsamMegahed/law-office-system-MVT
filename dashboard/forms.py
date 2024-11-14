from django import forms
from cases.models import CasesCategory
from django.utils.translation import gettext_lazy as _

class CasesCategoryForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Category Name'),
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-group"}),
    )
    
    class Meta:
        model = CasesCategory
        fields = ["name"]

