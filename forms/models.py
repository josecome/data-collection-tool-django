from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class SharedFields(models.Model):
    created_date = models.DateField(null=True)
    updated_date = models.DateField(null=True)

    class Meta:
        abstract = True


class Project_Form_Meta(SharedFields):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_name = models.CharField(max_length=80)
    form_description = models.CharField(max_length=160)
    form_country = models.CharField(max_length=40)
    form_field = models.CharField(max_length=80) # Where the form will be used
    user = models.ForeignKey(User,        
                            models.SET_NULL,
                            blank=True,
                            null=True,
                        ) 
    #form_url = models.CharField(max_length=80)

    F_STATUS = (
        ('deployed', 'Deployed'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    )
    form_status = models.CharField(max_length=100, default='draft', choices=F_STATUS)

    def save(self, *args, **kwargs):
        #self.form_url = (self.id).replace('-', '')
        super().save(*args, **kwargs)


class Project_Form(SharedFields):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    field_name = models.CharField(max_length=80)
    field_label = models.CharField(max_length=80, default='Label')
    field_description = models.CharField(max_length=160)
    field_type = models.CharField(max_length=160)
    field_size = models.IntegerField()
    form_meta = models.ForeignKey(Project_Form_Meta,  models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)


class Form_Sql_Query_Db(SharedFields):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sql_query = models.TextField()
    form_meta = models.ForeignKey(Project_Form_Meta,  models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)


class FieldwithChoiceOptions(SharedFields):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4, editable=False)
    option_name = models.CharField(max_length=160)
    option_label = models.CharField(max_length=160)
    project_form = models.ForeignKey(Project_Form,  models.SET_NULL, blank=True, null=True) 
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)

class Project_Form_Shared(SharedFields):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4, editable=False)
    form_id = models.ForeignKey(Project_Form_Meta,  models.SET_NULL, blank=True, null=True)
    shared_with_user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True) 
    view_form = models.BooleanField(default=False)
    edit_form = models.BooleanField(default=False)