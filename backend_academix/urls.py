from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    # re_path(r'(posts|comments|club|general|course).*', include('PostApp.urls'), name='post-related-routes'),
    re_path('student/', include('UserApp.urls'), name='user-routes')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)