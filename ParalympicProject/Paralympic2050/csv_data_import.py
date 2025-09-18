import csv
import os
import django
import sys

##### Add the path
sys.path.append(r"C:\Users\ACE\OneDrive\Studio3_FinalProj")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ParalympicProject.settings")  
django.setup()

from Paralympic2050.models import Athletes

#### For inserting single data, this is the postgreSQL command
'''
INSERT INTO athletes
(bid, country, firstName, lastName, gender, dateOfBirth, classification, imgProfile, email)
VALUES
(101, 'CAM', 'Jake', 'Phillip', 'Men', '2005-11-08', 'T62', NULL, NULL);
'''


##### I recommend to upload data through calling py manage.py shell
'''
py manage.py shell

In [1]: from Paralympic2050.csv_data_import import upload_data

In [2]: upload_data("C:/Users/ACE/OneDrive/Studio3_FinalProj/ParalympicProject/Paralympic2050/csv_files/Athlests.member
   ...: .csv")
UPLOADING: 100

'''

def upload_data(path):
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        athletes_ls = []

        for i in reader:
            ###### this method will check for id, same id will skip, (prevent duplicates)
            if Athletes.objects.filter(bid=int(i["id"])).exists():
                continue

            if i["dateOfBirth"]:
                dob = i["dateOfBirth"]
            else:
                dob = None

            if i["imgProfile"]:
                img = i["imgProfile"]
            else:
                img = None

            if i["email"]:
                email = i["email"]
            else:
                email = None

            athlete = Athletes(
                bid = int(i["id"]),
                country = i["country"],
                firstName = i["firstName"],
                lastName = i["lastName"],
                gender = i["gender"],
                dateOfBirth = dob,
                classification = i["classification"],
                imgProfile = img,
                email= email
            )
            athletes_ls.append(athlete)
        Athletes.objects.bulk_create(athletes_ls)

    print(f"UPLOADING: {len(athletes_ls)}")

if __name__ == "__main__":
    path_csv = "C:/Users/ACE/OneDrive/Studio3_FinalProj/ParalympicProject/Paralympic2050/csv_files/Athlests.member.csv"
    upload_data(path=path_csv)

    #upload_data("C:/Users/ACE/OneDrive/Studio3_FinalProj/ParalympicProject/Paralympic2050/csv_files/Athlests.member.csv")