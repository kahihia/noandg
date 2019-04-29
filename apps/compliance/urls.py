from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.compliance import views

router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'create/survey', views.CreateSurveyViewSet)
router.register(r'questions', views.SurveyQuestionViewSet)
router.register(r'answers', views.SurveyQuestionAnswerViewSet)
router.register(r'create/answer', views.CreateSurveyQuestionAnswerViewSet)
router.register(r'help', views.HelpViewSet)
router.register(r'create/help', views.CreateHelpViewSet)

urlpatterns = [
    path('api/v1/compliance/', include(router.urls))
]
