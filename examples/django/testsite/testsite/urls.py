from django.conf.urls import include, url
from django.contrib import admin
from testsite.views import Home

urlpatterns = [
    # Examples:
    url(r'^$', Home.as_view()),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
