from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.engineering import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'create/project', views.CreateProjectViewSet)
router.register(r'projectstage', views.ProjectStageViewSet)
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
router.register(r'fabrications', views.ProjectFabricationViewSet)
router.register(r'create/fabrication', views.CreateProjectFabricationViewSet)

urlpatterns = [
    path('engineering/directory/', views.ProjectsView.as_view(), name='projects_directory'),
    path('engineering/project/<slug>/overview/', views.ProjectView.as_view(), name='project_overview'),
    path('engineering/project/<slug>/documents/', views.ProjectFilesView.as_view(), name='project_documents'),
    path('engineering/project/<slug>/documents/<file_slug>/delete/', views.ProjectFileDeleteView.as_view(),
         name='project_document_delete'),

    path('api/v1/engineering/forms/leads/', views.ProjectLeadsViewSet.as_view()),
    path('api/v1/engineering/forms/teams/', views.ProjectTeamViewSet.as_view()),
    path('api/v1/engineering/forms/equipments/', views.ProjectEquipmentsViewSet.as_view()),
    path('api/v1/engineering/forms/projects/', views.ProjectFormViewSet.as_view()),
    path('api/v1/engineering/', include(router.urls)),
]
