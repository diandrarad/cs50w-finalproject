from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "get_listings/<str:type>/<str:country>/<str:tag>/<str:title>/<str:location>/<int:page>/<str:results_per_page>/<str:what_and>/<str:what_phrase>/<str:what_or>/<str:what_exclude>/<str:title_only>/<str:distance>/<str:location0>/<str:location1>/<str:location2>/<str:location3>/<str:location4>/<str:location5>/<str:location6>/<str:location7>/<str:max_days_old>/<str:sort_dir>/<str:sort_by>/<str:salary_min>/<str:salary_max>/<str:salary_include_unknown>/<str:full_time>/<str:part_time>/<str:contract>/<str:permanent>/<str:company>/",
        views.get_listings,
        name="get_listings"
        ),
    path(
        "save_listing/<str:listing_id>/<str:category>/<str:title>/<str:salary_max>/<str:company>/<str:location>/<str:description>/",
        views.save_listing,
        name="save_listing"
        ),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
