from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from cars.views import (
    carsListView, newCarCreateView, carDetailView, carUpdateView, carDeleteView,
    myCarsListView,
)
from accounts.views import registerView, loginView, logoutView, ProfileUpdateView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='cars_list', permanent=False)),
    path('admin/', admin.site.urls),
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('cars/', carsListView.as_view(), name='cars_list'),
    path('meus-anuncios/', myCarsListView.as_view(), name='my_cars'),
    path('newCar/', newCarCreateView.as_view(), name='new_car'),
    path('car/<int:pk>/', carDetailView.as_view(), name='car_detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('car/<int:pk>/update/', carUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', carDeleteView.as_view(), name='car_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # django.conf.urls.static.static() retorna [] quando DEBUG=False, o que
    # deixava todas as fotos de carro com 404 em producao. Servir por aqui
    # funciona, mas e ineficiente: o ideal e um alias /media/ no nginx ou um
    # storage externo (S3). Mantido como fallback para nao quebrar o site.
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
