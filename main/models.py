from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

STATES = (
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming")
)


class PROFILE(models.Model):
    user = models.ForeignKey(User, blank=False, null=False,
                             on_delete=models.CASCADE)
    city = models.TextField(max_length=25, blank=True)
    state = models.CharField(choices=STATES, max_length=2, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    first_name = models.TextField(max_length=20, blank=True)
    last_name = models.TextField(max_length=20, blank=True)
    email = models.EmailField(blank=True)


class BREWERY(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    city = models.TextField(max_length=50, null=True)
    state = models.TextField(choices=STATES, null=True)
    country = models.TextField(max_length=50, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class BEER(models.Model):
    name = models.TextField(max_length=40)
    description = models.TextField(max_length=500)
    brewery = models.ForeignKey(BREWERY, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class FAVORITE(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(BEER, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)


class TAG(models.Model):
    beer = models.ForeignKey(BEER, on_delete=models.CASCADE)
    tag = models.TextField(max_length=20)
    likes = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
