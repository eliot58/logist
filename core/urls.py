from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path, re_path as url

urlpatterns = [
    path("", index, name = "index"),
    path("login/", login_view, name = "login_view"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name = "auth/password_reset_form.html",email_template_name = "auth/password_reset_email.html", form_class = ResetPassForm), name = "password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name = "auth/password_reset_done.html"), name = "password_reset_done"),
    url(r"^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$", auth_views.PasswordResetConfirmView.as_view(template_name = "auth/password_reset_confirm.html",form_class = PassSetForm), name = "password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name = "auth/password_reset_complete.html"), name = "password_reset_complete"),
    path("logout/", logout_view, name = "logout_core_view"),
    path("routes/", routes, name = "routes"),
    path("route/<int:id>", route, name = "route"),
    path("create-route/", create_route, name = "create_route"),
    path("route/delete/<int:id>", route_delete, name = "route_delete"),

]
