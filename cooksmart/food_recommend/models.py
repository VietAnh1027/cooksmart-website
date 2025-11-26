# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class FoodMetadata(models.Model):
    index = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    directions = models.TextField(blank=True, null=True)
    ner = models.TextField(db_column='NER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False # Django không tạo bảng mới trong postgres, dùng khi database đã có sẵn bảng
        db_table = 'food_metadata'

class FoodAdding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    directions = models.TextField(blank=True, null=True)
    ner = models.TextField(db_column='NER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'food_adding'