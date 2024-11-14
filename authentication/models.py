from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class LawyerActive(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        # …
        permissions = (("Lawyer_Active", "Lawyer Active"),)