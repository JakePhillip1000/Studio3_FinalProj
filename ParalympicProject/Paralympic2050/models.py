from django.db import models

#### This model is already connect to postgreSQL db
## I rename this model to athletes (you will see it in postgreSQL)
class Athletes(models.Model):
    bid = models.IntegerField()
    country = models.CharField(max_length=5)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dateOfBirth = models.DateField(null=True, blank=True)
    classification = models.CharField(max_length=50)
    imgProfile = models.URLField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table  = "athletes" ###### I will rename the database table to athletes
        verbose_name = "Athlete"
        verbose_name_plural = "Athletes"