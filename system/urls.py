from django.urls import path
from django.conf.urls import url,include
from .views import index_view
urlpatterns = [
    path('', index_view),

]