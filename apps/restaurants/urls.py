from django.urls import path

from .views import RestaurantListAPIView, RestaurantDetailAPIView


urlpatterns = [
    path('', RestaurantListAPIView.as_view()),  # Restaurant 생성 및 전체 리스트 조회
    path('/<int:pk>', RestaurantDetailAPIView.as_view()),   # Restaurant 상세 정보 조회, 수정 및 삭제
]
