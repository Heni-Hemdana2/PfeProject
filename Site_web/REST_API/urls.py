from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('detections/', DetectionListView.as_view(), name='detection-list'),
    path('latest-detection/', LatestDetectionView.as_view(), name='latest-detection'),
    path('latest-detection/<str:camera_name>/', LatestDetectionView.as_view(), name='latest-camera-detection'),
    path('latest-yolo-image/', LatestYoloImageView.as_view(), name='latest-yolo-image'),
]