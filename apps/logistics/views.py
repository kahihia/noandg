from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.engineering.models import Project, ProjectEquipment
from apps.engineering.serializers import CreateProjectSerializer, ProjectSerializer
from apps.logistics.models import LogisticsBid, LogisticsQuote, LogisticsQuoteItem
from apps.logistics.serializers import CreateProjectBidSerializer, ProjectBidSerializer, CreateProjectQuoteSerializer, \
    ProjectQuoteSerializer, ProjectQuoteItemSerializer, CreateProjectQuoteItemSerializer


class UsersView(LoginRequiredMixin, View):
    template_name = 'users/index.html'
    context = {}

    def get(self, request):
        self.context['users'] = User.objects.all()
        return render(request, self.template_name, self.context)


class CreateProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = CreateProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectBidViewSet(viewsets.ModelViewSet):
    queryset = LogisticsBid.objects.all()
    serializer_class = CreateProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectBidViewSet(viewsets.ModelViewSet):
    queryset = LogisticsBid.objects.all()
    serializer_class = ProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return LogisticsBid.objects.filter(vendor=self.request.user, project=project)
        else:
            return self.queryset


class CreateProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuote.objects.all()
    serializer_class = CreateProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuote.objects.all()
    serializer_class = ProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return LogisticsQuote.objects.filter(vendor=self.request.user, project=project)
        else:
            return self.queryset


class ProjectEquipmentsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        project = request.GET.get('project')
        project_equipments = ProjectEquipment.objects.filter(project=project)

        equipments = []
        for equipment in project_equipments:
            equipment_object = {'value': equipment.id, 'label': equipment.name}

            equipments.append(equipment_object)

        return Response({'results': equipments})


class ProjectQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuoteItem.objects.all()
    serializer_class = ProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return LogisticsQuoteItem.objects.filter(vendor=self.request.user, project=project)
        elif self.request.GET.get('item'):
            if self.request.GET.get('item') == '':
                return []
            else:
                equipment = get_object_or_404(ProjectEquipment, id=self.request.GET.get('item'))
                return LogisticsQuoteItem.objects.filter(project=project, equipment=equipment)
        elif self.request.GET.get('vendor'):
            vendor = get_object_or_404(User, id=self.request.GET.get('vendor'))
            return LogisticsQuoteItem.objects.filter(project=project, vendor=vendor)
        else:
            return self.queryset


class CreateProjectQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = LogisticsQuoteItem.objects.all()
    serializer_class = CreateProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'
