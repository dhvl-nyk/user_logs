from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from phonenumber_field.modelfields import PhoneNumberField

class user(models.Model):
    user_name =  models.TextField(max_length=1000, blank=True)
    def __str__(self):
        return self.user_name

class user_log(models.Model):
    call_timestamp = models.DateTimeField()
    call_duration =  models.IntegerField()
    call_type =  models.TextField(max_length=100, blank=True)
    phone_number =  models.TextField(max_length=15, blank=True)
    # phone_number = PhoneNumberField(null=True, blank=True, unique=False)

    user = models.ForeignKey(user, on_delete=models.CASCADE)#, related_name='tags')
    def __str__(self):
        return self.call_type

class user_app(models.Model):
    app_name = models.TextField(max_length=100, blank=True)
    app_id =  models.TextField(max_length=100, blank=True)
    app_category =  models.TextField(max_length=100, blank=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.app_name

    # Created At  Call Date   Call Duration   Call Type   Phone Number

    # def __str__(self):
    #     return self.message_type

    # def clean(self):
    #     error_dict = {}
    #     for field in self._meta.get_fields():
    #         if field.name != "id":
    #             field_value =  getattr(self, field.name)
    #             if not field_value:
    #                 msg =  field.name + " should not be blank"
    #                 error_dict[field.name] = msg
    #     raise ValidationError(error_dict)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super().save(*args, **kwargs)