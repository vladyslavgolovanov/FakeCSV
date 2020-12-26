from django.contrib.auth.models import User
from django.db import models


class Schemas(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_of_characters = (
        (',', 'Comma "," '),
        (';', 'Semicolon ";"'),
        ('/', 'Slush "/"'),
        ('"', 'Double quotes """'),
        ('|', 'Pipe "|"'))
    column_separators = models.CharField(max_length=1,
                                         choices=list_of_characters,
                                         default=',')
    string_chapter = models.CharField(max_length=1,
                                      choices=list_of_characters,
                                      default='"')
    data = models.DateField(auto_now_add=True)
    rows = models.IntegerField()


class Column(models.Model):
    column_name = models.CharField(max_length=30)
    schemas = models.ForeignKey(Schemas, on_delete=models.CASCADE)
    column_choices = (
        ('Full Name', 'Full Name'),
        ('Integer', 'Integer'),
        ('Email', 'Email'),
        ('Job', 'Job'),
        ('Phone', 'Phone')
    )
    type = models.CharField(max_length=254, choices=column_choices)


class File(models.Model):
    csv = models.FileField(db_index=True, upload_to='not_used')

#
# class Range(models.Model):
#     column = models.ForeignKey(Column, on_delete=models.CASCADE)
#     begin = models.PositiveIntegerField()
#     end = models.PositiveIntegerField()
#
#     @property
#     def age(self):
#         if self.begin < self.end:
#             age = "Good"
#         else:
#             age = 'No matter'
#         return age


# class File(models.Model):
#     csv = models.FileField(db_index=True, upload_to='not_used')
