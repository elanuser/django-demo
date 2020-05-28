from django.db import models

# Create your models here.
class manager(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=50, null=False)

    phone_number = models.CharField(max_length=12)