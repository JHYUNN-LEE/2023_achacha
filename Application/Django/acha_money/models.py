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


class Posts(models.Model):
    posts_id = models.AutoField(primary_key=True)
    users_fk = models.CharField(max_length=45)
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    acha_money = models.IntegerField(blank=True, null=True)
    delivery_way = models.CharField(max_length=45, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    lost_items_fk = models.IntegerField()
    image_src = models.CharField(max_length=150, blank=True, null=True)
    pickup_center = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class AchachaDeals(models.Model):
    achacha_deals_id = models.AutoField(primary_key=True)
    users_fk = models.CharField(max_length=45)
    posts_fk = models.IntegerField()
    role = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'achacha_deals'