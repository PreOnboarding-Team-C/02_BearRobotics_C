from django.urls import path

from apps.sales.views import PosListAPIView, PosDetailAPIView

urlpatterns = [
    path('', PosListAPIView.as_view()),
    path('/<int:pk>', PosDetailAPIView.as_view()),
]