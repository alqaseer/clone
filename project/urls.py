from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^convert/$', 'main.views.convert'),
    url(r'^upload/$', 'main.views.upload'),
    url(r'^video/(?P<pk>[0-9]+)/$', 'main.views.displayvideo'),
    url(r'^myvideos/$', 'main.views.myvideos'),

    #user managment below
    url(r'^signup/$', 'main.views.signup'),
    url(r'^logout/$', 'main.views.logout_view'),
    url(r'^login/$', 'main.views.login_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
