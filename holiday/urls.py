from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import views as myapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp_views.login_view, name='home'),
    path('', include('myapp.urls')),
    path('<str:username>/movie/', include('movie.urls', namespace='movie')),
    path('<str:username>/photo/', include('photo.urls')),
    path('home/', myapp_views.index_redirect, name='index_redirect'),
    path('<str:owner_name>/memo/', include('memo.urls', namespace='memo')),
    path('summernote/', include('django_summernote.urls')),
    path('<str:username>/now/', include('now.urls', namespace='now')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.THUMBNAIL_URL, document_root=settings.THUMBNAIL_ROOT)
