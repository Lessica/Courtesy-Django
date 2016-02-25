"""qr_gift_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()

from django.views.generic.base import RedirectView
from qr_gift import views as qr_gift_views

#  import qr_gift

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^qrstyles/upload$', qr_gift_views.qr_style_upload),
    url(r'^user/upload$', qr_gift_views.user_avatar_upload),
    url(r'^qrcode/arrise$', qr_gift_views.qr_arrise),
    url(r'^upload/(\w+)$', qr_gift_views.common_upload),
    #  url(r'^accounts/register$', qr_gift_views.register),
    #  url(r'^accounts/login$',qr_gift_views.login),
    #  url(r'^accounts/logout/$',qr_gift_views.logout),

    url(r'^api/courtesy', qr_gift_views.api),
    #  url(r'^accounts/test$',qr_gift_views.test),
]
