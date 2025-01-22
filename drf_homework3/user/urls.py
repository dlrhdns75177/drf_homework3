from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path("api/signup/",views.SignupView.as_view(),name="signup"),
    path("profile/",views.ProfileIntro.as_view(),name="profile"),
]

if settings.DEBUG:  # 개발 환경에서만 media 파일에 이미지 저장
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)