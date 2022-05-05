import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")
django.setup()

from apps.menu.models import Menu
from apps.restaurants.models import Group, Restaurant
from apps.sales.models import Pos


class UploadAll:
    """
    Assignee : 김수빈
    Reviewer : -
    """
    def __init__(self, filename: str):
        self.upload_groups()
        self.use_csv(filename, "self.upload_restaurants")
        self.upload_menu()
        self.use_csv(filename, "self.upload_pos")
        
    def use_csv(self, filename: str, func: str):
        path = os.path.join(os.getcwd(), filename)
        f = open(path, newline='')
        csvs = csv.DictReader(f)
        eval(func)(csvs)
        f.close()

    def upload_groups(self):
        Group.objects.create(
        name = "CJ푸드빌"
        )
        print(f"{'='*25} GROUP DATA UPLOADED SUCCESSFULLY {'='*25}")

    def upload_restaurants(self, csvs):
        restaurant_id = set(map(lambda x: x.get('restaurant'), csvs))
        restaurant_id = sorted(list(restaurant_id))
        restaurant_name = ['비비고', '빕스버거', '제일제면소', '뚜레쥬르']  # 예시에 사용된 브랜드는 CJ푸드빌 프랜자이즈여서 21, 22, 31, 32 순으로 임의 지정
        
        # restaurant_id가 자동 생성되지만,, 제공된 파일을 사용해야하기에 다음의 과정을 거침
        restaurants = [
            Restaurant(
                id = _id,
                group = 1,
                name = _name,
                city = "서울",
            ) for _id, _name in zip(restaurant_id, restaurant_name)
        ]
        Restaurant.objects.bulk_create(restaurants)
        print(f"{'='*25} RESTAURANT DATA UPLOADED SUCCESSFULLY {'='*25}")

    def upload_menu(self):
        menus = [
            Menu(
                restaurant = 21,
                name = "갈비비빔밥",
                price = 15000,
            ),
            Menu(
                restaurant = 21,
                name = "제육덮밥",
                price = 10000,
            ),
            Menu(
                restaurant = 22,
                name = "버거",
                price = 10000,
            ),
            Menu(
                restaurant = 22,
                name = "불고기버거",
                price = 10000,
            ),
            Menu(
                restaurant = 31,
                name = "수제주먹밥",
                price = 2500,
            ),
            Menu(
                restaurant = 31,
                name = "차돌박이 우동",
                price = 10000,
            ),
            Menu(
                restaurant = 31,
                name = "삼겹살 부추볶음",
                price = 15000,
            ),
            Menu(
                restaurant = 32,
                name = "식빵",
                price = 3000,
            ),
            Menu(
                restaurant = 32,
                name = "마늘빵",
                price = 3500,
            ),
            Menu(
                restaurant = 32,
                name = "앙버터빵",
                price = 5000,
            ),
            Menu(
                restaurant = 32,
                name = "케잌 1호",
                price = 20000,
            ),
        ]
        Menu.objects.bulk_create(menus)
        print(f"{'='*25} MENU DATA UPLOADED SUCCESSFULLY {'='*25}")

    def upload_pos(self, csvs):
        pos = [
            Pos(
                created_datetime = _d,
                restaurant = _r,
                number_of_party = _n,
                payment = _p,
            ) for (_d, _r, _n, _p) in zip
            (
                csvs.get('timestamp'),
                csvs.get('restaurant'), 
                csvs.get('number_of_party'), 
                csvs.get('payment')
            )
        ]
        Pos.objects.bulk_create(pos)
        print(f"{'='*25} POS DATA UPLOADED SUCCESSFULLY {'='*25}")

if __name__=="__main__":
    UploadAll("pos_example.csv")
