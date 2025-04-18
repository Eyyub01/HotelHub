from .city_urls import urlpatterns as city_urlpatterns
from .hotel_urls import urlpatterns as hotel_urlpatterns

urlpatterns = city_urlpatterns + hotel_urlpatterns
from .city_urls import urlpatterns as city_urlpatterns
from .hotel_urls import urlpatterns as hotel_urlpatterns

urlpatterns = city_urlpatterns + hotel_urlpatterns