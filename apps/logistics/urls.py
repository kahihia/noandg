from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.logistics import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'create/project', views.CreateProjectViewSet)
router.register(r'bids', views.ProjectBidViewSet)
router.register(r'create/bid', views.CreateProjectBidViewSet)
router.register(r'quotes', views.ProjectQuoteViewSet)
router.register(r'create/quote', views.CreateProjectQuoteViewSet)
router.register(r'quoteitems', views.ProjectQuoteItemViewSet)
router.register(r'create/quoteitem', views.CreateProjectQuoteItemViewSet)

urlpatterns = [
    path('api/v1/logistics/forms/equipments/', views.ProjectEquipmentsViewSet.as_view()),
    path('api/v1/logistics/', include(router.urls)),
]
