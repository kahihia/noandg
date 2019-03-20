from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.engineering import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'create/project', views.CreateProjectViewSet)
router.register(r'files', views.ProjectFileViewSet)
router.register(r'create/file', views.CreateProjectFileViewSet)
router.register(r'equipments', views.ProjectEquipmentViewSet)
router.register(r'create/equipment', views.CreateProjectEquipmentViewSet)
router.register(r'budgets', views.ProjectBudgetViewSet)
router.register(r'create/budget', views.CreateProjectBudgetViewSet)
router.register(r'bids', views.ProjectBidViewSet)
router.register(r'create/bid', views.CreateProjectBidViewSet)
router.register(r'quotes', views.ProjectQuoteViewSet)
router.register(r'create/quote', views.CreateProjectQuoteViewSet)
router.register(r'quoteitems', views.ProjectQuoteItemViewSet)
router.register(r'create/quoteitem', views.CreateProjectQuoteItemViewSet)
router.register(r'designs', views.ProjectDesignViewSet)
router.register(r'create/design', views.CreateProjectDesignViewSet)

urlpatterns = [
    path('api/v1/engineering/forms/leads/', views.ProjectLeadsViewSet.as_view()),
    path('api/v1/engineering/forms/equipments/', views.ProjectEquipmentsViewSet.as_view()),
    path('api/v1/engineering/', include(router.urls)),
]
