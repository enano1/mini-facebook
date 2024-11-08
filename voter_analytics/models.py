# Create your models here.
import csv
from django.db import models

class Voter(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.IntegerField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.street_name}, {self.zip_code})"


def load_data():
    from voter_analytics.models import Voter
    import csv

    Voter.objects.all().delete()

    filename = '/Users/enano/Desktop/newton_voters.csv'
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                precinct_number = int(row['Precinct Number'])  # Attempt to convert to integer
            except ValueError:
                print(f"Skipping voter {row['First Name']} {row['Last Name']} due to invalid precinct: {row['Precinct Number']}")
                continue

            voter = Voter(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'] or None,
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=row['Date of Birth'],
                date_of_registration=row['Date of Registration'],
                party_affiliation=row['Party Affiliation'],
                precinct_number=precinct_number,
                v20state=row['v20state'].strip().upper() == 'TRUE',
                v21town=row['v21town'].strip().upper() == 'TRUE',
                v21primary=row['v21primary'].strip().upper() == 'TRUE',
                v22general=row['v22general'].strip().upper() == 'TRUE',
                v23town=row['v23town'].strip().upper() == 'TRUE',
                voter_score=int(row['voter_score']),
            )
            voter.save()

    print(f"Done. Created {Voter.objects.count()} voters.")
