from django.urls import path

from apps.sales.views import PosListAPIView, PosDetailAPIView, PosSearchAPIView

urlpatterns = [
    path('', PosListAPIView.as_view()),
    path('/kpi', PosSearchAPIView.as_view()),
    path('/<int:pk>', PosDetailAPIView.as_view()),
]