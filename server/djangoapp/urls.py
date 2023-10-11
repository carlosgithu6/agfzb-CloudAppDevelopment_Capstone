from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='static',view=views.get_static,name='get_static'),
    path(route='about', view=views.get_about, name='get_about'),
    path(route='contact', view=views.get_contact_us, name='get_contact_us'),
    path(route='login', view=views.login_request, name='login'),
    path(route='registration', view=views.registration, name='registration'),
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)