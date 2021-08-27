from django.urls import path

from . import views

urlpatterns = [
    # User admin browser endpoints
    #path("gencal/login", views.login_view, name="login"),
    #path("gencal/register", views.register, name="register"),
    #path("gencal/logout", views.logout_view, name="logout"),

    # Browser endpoints
    path("gencal", views.index, name='index'),
    path("gencal/goals", views.goals, name='goals'),
    path("gencal/calendar", views.calendar, name='calendar')


    # API and form endpoints

]