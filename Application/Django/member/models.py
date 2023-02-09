from django.db import models

class Users(models.Model):
    users_id = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=150, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    mail_address = models.CharField(max_length=45, blank=True, null=True)
    user_group = models.CharField(max_length=45, blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'