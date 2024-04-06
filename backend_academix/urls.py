from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    # re_path(r'(posts|comments|club|general|course).*', include('PostApp.urls'), name='post-related-routes'),
    path('user/', include('UserApp.urls'), name='user-routes'),
    path('postapi/', include('PostApp.urls'), name='Post-routes'),
    path('community/', include('CommunityApp.urls'), name='community-route')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)