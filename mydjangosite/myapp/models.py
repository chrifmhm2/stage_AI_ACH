# from django.db import models
#
# class User(models.Model):
#     uid = models.CharField(primary_key=True, max_length=20)
#     uname = models.CharField(max_length=100)
#     uemail = models.EmailField()
#     ucontact = models.CharField(max_length=15)
#
#     class Meta:
#         db_table = 'user'

from django.db import models

# class Account(models.Model):
#     account_id = models.CharField(max_length=100, primary_key=True)
#     account_name = models.CharField(max_length=100)
#     balance = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return self.account_name

class Bank(models.Model):
    bank_id = models.CharField(max_length=100, primary_key=True)
    bank_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.bank_name

class MsgIDSeq(models.Model):
    msg_id_seq = models.IntegerField()

    def __str__(self):
        return str(self.msg_id_seq)

from django.db import models

class Account(models.Model):
    old_acnt_num = models.CharField(max_length=100, default='default_old_acnt_num')
    acnt_num = models.CharField(max_length=100, default='default_acnt_num')
    account_name = models.CharField(max_length=255, default='default_account_name')
    curr = models.CharField(max_length=100, default='MRU')
    old_rib = models.CharField(max_length=100, default='default_old_rib')
    new_rib = models.CharField(max_length=100, default='default_new_rib')

    def __str__(self):
        return self.account_name
