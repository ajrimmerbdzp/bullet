from competitions.views import register
from django.urls import path

urlpatterns = [
    path(
        "register/",
        register.CategorySelectView.as_view(),
        name="team_register",
    ),
    path(
        "register/venue/",
        register.VenueSelectView.as_view(),
        name="team_register_venue",
    ),
]
