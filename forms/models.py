from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Project_Form_Meta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_name = models.CharField(max_length=80)
    form_description = models.CharField(max_length=160)
    form_country = models.CharField(max_length=40)
    form_field = models.CharField(max_length=80) # Where the form will be used
    created_date = models.DateField(null=True)
    updated_date = models.DateField(null=True)
    user = models.ForeignKey(User,        
                            models.SET_NULL,
                            blank=True,
                            null=True,
                        ) 
    #form_url = models.CharField(max_length=80)

    F_STATUS = (
        ('deployed', 'Deployed'),
        ('draft', 'Draft'),
        ('arquived', 'Arquived'),
    )
    form_status = models.CharField(max_length=100, choices=F_STATUS)

    def save(self, *args, **kwargs):
        #self.form_url = (self.id).replace('-', '')
        super().save(*args, **kwargs)


class Project_Form(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    field_name = models.CharField(max_length=80)
    field_description = models.CharField(max_length=160)
    field_type = models.CharField(max_length=160)
    field_size = models.IntegerField()
    created_date = models.DateField()
    updated_date = models.DateField()  
    form_meta = models.ForeignKey(Project_Form_Meta,  models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)


class Form_Sql_Query_Db(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sql_query = models.TextField()
    created_date = models.DateField()
    updated_date = models.DateField()  
    form_meta = models.ForeignKey(Project_Form_Meta,  models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)


class FieldwithChoiceOptions(models.Model):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4, editable=False)
    option_name = models.CharField(max_length=160)
    option_label = models.CharField(max_length=160)
    created_date = models.DateField()
    updated_date = models.DateField()  
    project_form = models.ForeignKey(Project_Form,  models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)