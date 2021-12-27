from django.urls import path
from .views import GeneralView, LibraryView, AdminSignup, AdminSignin, user_logout

# Library Urls...

urlpatterns = [
    path('', GeneralView.as_view(), name='libraryMS'),
    path('adminops/', LibraryView.as_view(), name='adminops'),
    path('adminops/<int:id>/', LibraryView.as_view(), name='adminops_update'),
    path('signup/', AdminSignup.as_view(), name='signup'),
    path('signin/', AdminSignin.as_view(), name='signin'),
    path('signout/', user_logout, name='signout'),
]