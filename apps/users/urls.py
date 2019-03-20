from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users import views

router = DefaultRouter()
router.register(r'list', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'create/group', views.CreateGroupViewSet)
router.register(r'create/employee', views.CreateUserViewSet)

urlpatterns = [
    path('api/v1/users/permissions/', views.PermissionViewSet.as_view()),
    path('api/v1/users/forms/groups/', views.GroupsViewSet.as_view()),
    path('api/v1/users/forms/users/', views.UsersOptionViewSet.as_view()),
    path('api/v1/users/', include(router.urls))
]
