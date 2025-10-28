from django.db import models

#### This model is already connect to postgreSQL db
## I rename this model to athletes (you will see it in postgreSQL)
class Athletes(models.Model):
    bid = models.IntegerField()
    country = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(blank=True, null=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    classification = models.CharField(max_length=50)
    imgProfile = models.URLField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table  = "athletes" ###### I will rename the database table to athletes
        verbose_name = "Athlete"
        verbose_name_plural = "Athletes"

#### This is for the register sign up username and email storage
class UserData(models.Model):  #### This one will automatically turns into the form field (<input> in HTML)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128) 

    class Meta:
        db_table  = "userdatas"
        verbose_name = "userdata"
        verbose_name_plural = "userdatas" 

##### IN the event management I will use each model to represent
#### each event hosted... These will be put into the postgreSQL database
class Event(models.Model):
    date_time = models.DateTimeField(verbose_name="Date and Time")
    number = models.CharField(max_length=10, verbose_name="Event No.")
    gender = models.CharField(max_length=10)
    sport = models.CharField(max_length=100)
    classification = models.CharField(max_length=10)
    phrase = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=255, null=True, blank=True) # <-- เพิ่มบรรทัดนี้

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date_time"]
        db_table  = "sport_events"
        verbose_name = "sport_event"
        verbose_name_plural = "sport_events"

##### THis one is the Medals model which collects the data of team name
#### gold, silver and bronze medal
class Medal(models.Model):
    team = models.CharField(max_length=100)
    gold = models.PositiveIntegerField(default=0)
    silver = models.PositiveIntegerField(default=0)
    bronze = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "medal_summary"   
        verbose_name = "medal"      
        verbose_name_plural = "medals"  

##### The ticket class, when user buys the ticket
class Ticket(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=[("A", "Category A"), ("B", "Category B")])
    ticket_type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    visa_last_four = models.CharField(max_length=4, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ticket"   
        verbose_name = "tickets"      
        verbose_name_plural = "ticket_value"  