from django.urls import path
from GoToMarketApplication.views import *

urlpatterns = [
    path('generate-plan/', generate_marketing_plan, name='generate_marketing_plan'),
    path("api/register/", register_user, name="register_user"),
]
