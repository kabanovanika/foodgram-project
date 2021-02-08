from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('', include('recipe.urls')),
    path('foodgram-page/', views.flatpage, name='foodgram'),
    path('about-author/', views.flatpage, {'url': '/about-us/'},
         name='about_author'),
    path('technologies-page/', views.flatpage, name='technologies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
