from django.urls import path

from .views import KPIPerRestaurantAPIView, RestaurantListAPIView, RestaurantDetailAPIView, RestaurantPaymentKPIView


urlpatterns = [
    path('', RestaurantListAPIView.as_view()),  # Restaurant 생성 및 전체 리스트 조회
    path('/<int:pk>', RestaurantDetailAPIView.as_view()),   # Restaurant 상세 정보 조회, 수정 및 삭제
    path('/kpi/number-of-party', KPIPerRestaurantAPIView.as_view()),   # Restaurant별 인원별 KPI 조회
    path('/kpi/payment', RestaurantPaymentKPIView.as_view()),   # Restaurant별 payment별 KPI 조회
]
