import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from apps.restaurants.models import Restaurant
from apps.sales.models import Pos


ROBOTICS_PATH = 'BearRobotics_pos_example.csv'


def insert_pos_data():
    with open(ROBOTICS_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        pos_list = []
        for row in data_reader:
            restaurant_id = int(row[2])
            number_of_party = int(row[4])
            payment = row[5]
            
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            pos_list.append(
                Pos(
                    restaurant_id = restaurant.id,
                    number_of_party = number_of_party,
                    payment = payment
                )
            )
        Pos.objects.bulk_create(pos_list)
    print('Pos data was uploaded!')
    

insert_pos_data()
