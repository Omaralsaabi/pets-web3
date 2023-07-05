from django.db import models

# Create your models here.


class ContractAddress(models.Model):
    contract_address = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.contract_address
