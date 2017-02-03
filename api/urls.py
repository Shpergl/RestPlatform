from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from api import views
from api.views import UserPostList, UserRegister, UserProfile
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

router = DefaultRouter()
router.register(r'user', views.UserViewSet, 'user')
router.register(r'post', views.PostViewSet, 'post')

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/register/$', UserRegister.as_view(), name='user-register'),
    url(r'^v1/profile/$', UserProfile.as_view(), name='user-profile'),
    url(r'^v1/get-token/', obtain_jwt_token, name='get-token'),
    url(r'^v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/(?P<userId>[0-9a-zA-Z_-]+)/post/$', UserPostList.as_view(), name='user-post'),
    url(r'^v1/docs/$', schema_view),
]
