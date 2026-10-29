from django.db import models

# Create your models here.

class Catagory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    TYPE_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]
    title = models.CharField(max_length=100)
    catagory = models.ForeignKey(Catagory,on_delete=models.PROTECT)
    description = models.TextField(max_length=300)
    picture = models.ImageField(upload_to='item_pics/', blank=True, null=True)
    color = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    location = models.CharField(max_length=80)
    incident_d_t = models.DateTimeField()
    # status
    created_at = models.DateTimeField(auto_now_add=True)
    itemtype = models.CharField(max_length=5, choices=TYPE_CHOICES, default='LOST')

    def __str__(self):
        return f'{self.itemtype}_{self.title}'