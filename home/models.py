from django.db import models
from django.contrib.auth.models import User

class LoginInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fails = models.PositiveSmallIntegerField(default=0)
    login_link = models.CharField(unique=True, blank=True, null=True, max_length=225)
    reset_link = models.CharField(unique=True, blank=True, null=True, max_length=225)
    
    # passwordone = models.CharField(max_length=225)
    # passwordtwo = models.CharField(max_length=225)

    def __str__(self):
        return self.user.username

# class Secondpass(models.Model):
#     name= models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class secondfpassInfo(models.Model):
#     secondpass = models.ForeignKey(User, on_delete=models.CASCADE)
#     passwordone = models.CharField(unique=False, blank=False, null=False, max_length=225)

#     def __str__(self):
#         return self.secondpass.passowrdone

# class Thirdpass(models.Model):
#     name= models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class thirdpassInfo(models.Model):
#     thirdpass = models.ForeignKey(User, on_delete=models.CASCADE) 
#     passwordtwo = models.CharField(unique=False, blank=False, null=False, max_length=225)

#     def __str__(self):
#         return self.thirdpass.passwordtwo
