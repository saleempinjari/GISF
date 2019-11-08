from django.urls import path
from .views import (ProductsMaster,ProductRisk)

app_name = 'Masters'

urlpatterns = [
    path('ProductsMaster/', ProductsMaster, name='ProductsMaster'),
    path('ProductRisk/', ProductRisk, name='ProductRisk'),  # modelformset_factory table format

   ]