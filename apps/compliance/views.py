from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.compliance.models import Survey, SurveyQuestion, SurveyQuestionAnswer, HelpIssue
from apps.compliance.serializers import SurveySerializer, CreateSurveySerializer, SurveyQuestionSerializer, \
    SurveyQuestionAnswerSerializer, CreateSurveyQuestionAnswerSerializer, HelpSerializer, CreateHelpSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()

    def get_queryset(self):
        if self.request.GET.get('type'):
            return Survey.objects.filter(survey_type=self.request.GET.get('type'))
        else:
            return self.queryset

    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateSurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = CreateSurveySerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()

    def get_queryset(self):
        if self.request.GET.get('survey'):
            survey = get_object_or_404(Survey, slug=self.request.GET.get('survey'))
            return SurveyQuestion.objects.filter(survey=survey)
        else:
            return self.queryset

    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class SurveyQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = SurveyQuestionAnswerSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateSurveyQuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestionAnswer.objects.all()
    serializer_class = CreateSurveyQuestionAnswerSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class HelpViewSet(viewsets.ModelViewSet):
    queryset = HelpIssue.objects.all()
    serializer_class = HelpSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class CreateHelpViewSet(viewsets.ModelViewSet):
    queryset = HelpIssue.objects.all()
    serializer_class = CreateHelpSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'
