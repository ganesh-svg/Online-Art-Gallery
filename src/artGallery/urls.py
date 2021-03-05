from django.urls import path
from .views import home, add_to_cart, art_detail
app_name = "artGallery"
urlpatterns = [
    path("", home, name="home"),
    path("add-to-cart", add_to_cart, name="add-to-cart"),
    path("art-detail/<int:art_id>", art_detail, name="art-detail")

]
