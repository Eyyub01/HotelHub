from django.urls import path

from hotels.views.hotel_views import(
    HotelListCreateAPIView, HotelRetrieveUpdateDestroy,
    WishlistView, HotelReviewListCreateView, HotelElasticSearchAPIView
)


urlpatterns = [
    path(
        'hotels/', 
        HotelListCreateAPIView.as_view(), 
        name='hotels'
    ),
    path(
        'hotels/search/', 
        HotelElasticSearchAPIView.as_view(), 
        name='hotel-search'
    ),
    path(
        'hotels/<int:pk>/', 
        HotelRetrieveUpdateDestroy.as_view(),
        name='hotel-detail'
    ),
    path(
        'hotels/<int:hotel_id>/reviews/', 
        HotelReviewListCreateView.as_view(), 
        name='hotel-reviews'
    ),
    path(
        'profile/<int:user_id>/wishlist/', 
        WishlistView.as_view(), 
        name='wishlist'
    ),
    path(
        'profile/<int:user_id>/wishlist/<int:hotel_id>/', 
        WishlistView.as_view(), 
        name='wishlist-remove'
    ),
]
