from django.db import models


class Smartphone(models.Model):
    title = models.CharField(max_length=80)
    storage = models.IntegerField()
    brand = models.CharField(max_length=80)
    cost = models.IntegerField()
    img = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)

    def __str__(self):
        return self.title


class Sale(models.Model):
    smartphone = models.ForeignKey('Smartphone', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
