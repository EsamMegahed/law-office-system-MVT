from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Client)
admin.site.register(CasesCategory)
admin.site.register(CasesFiles)
admin.site.register(CaseSessions)
admin.site.register(Cases)
admin.site.register(CasePayment)
admin.site.register(CasesEvents)