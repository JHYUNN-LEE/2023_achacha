from django.db import models

# Create your models here.
class LostItems(models.Model):
    lost_items_id = models.AutoField(primary_key=True)
    lost_item = models.CharField(max_length=150, blank=True, null=True)
    find_place = models.CharField(max_length=45, blank=True, null=True)
    find_date = models.DateField(blank=True, null=True)
    loster = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    images_fk = models.CharField(max_length=45)
    center_name = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    pickup_center_number = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lost_items'
    
class Images(models.Model):
    images_id = models.CharField(primary_key=True, max_length=45)
    images_src = models.CharField(max_length=150, blank=True, null=True)
    yolo_category = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'

class Alarms(models.Model):
    alarms_id = models.AutoField(primary_key=True)
    users_fk = models.CharField(max_length=45)
    category = models.CharField(max_length=45, blank=True, null=True)
    image_src = models.CharField(max_length=150, blank=True, null=True)
    alarm_check = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alarms'