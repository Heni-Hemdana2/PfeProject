from django.urls    import path 
from .views         import  *

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]