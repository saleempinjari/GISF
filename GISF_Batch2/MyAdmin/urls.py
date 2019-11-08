from django.urls import path
from MyAdmin.views import NewUserCreate
from django.contrib.auth.decorators import login_required
from MyAdmin.views import register,about,\
    loginView,logout_view,mainmenu,homepage
app_name = 'MyAdmin'

urlpatterns = [
    path('CSignup/', NewUserCreate , name='Signup'),
    path('', homepage, name='homepage'),
    path('About/', about, name='About'),
    path('clogin/', loginView, name='clogin'),
    path('log-out/', logout_view, name='logout'),
    path("Newregister/", register, name="register"),
    path('mainmenu/', mainmenu, name='mainmenu'),
     ]