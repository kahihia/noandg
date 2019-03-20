from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.engineering.models import Project, ProjectFile, ProjectEquipment, ProjectBudget, ProjectBid, ProjectQuote, \
    ProjectQuoteItem, ProjectDesign
from apps.engineering.serializers import CreateProjectSerializer, ProjectSerializer, CreateProjectFileSerializer, \
    ProjectFileSerializer, CreateProjectEquipmentSerializer, ProjectEquipmentSerializer, CreateProjectBudgetSerializer, \
    ProjectBudgetSerializer, ProjectBidSerializer, CreateProjectBidSerializer, CreateProjectQuoteSerializer, \
    ProjectQuoteSerializer, CreateProjectQuoteItemSerializer, ProjectQuoteItemSerializer, ProjectDesignSerializer, \
    CreateProjectDesignSerializer


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


class ProjectLeadsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_leads = User.objects.filter(groups__name='Project Lead')

        leads = []
        for lead in all_leads:
            lead_object = {'value': lead.id, 'label': lead.first_name + ' ' + lead.last_name}

            # append groups
            leads.append(lead_object)

        return Response({'results': leads})


class CreateProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = CreateProjectFileSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectDesignViewSet(viewsets.ModelViewSet):
    queryset = ProjectDesign.objects.all()
    serializer_class = CreateProjectDesignSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectDesignViewSet(viewsets.ModelViewSet):
    queryset = ProjectDesign.objects.all()
    serializer_class = ProjectDesignSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectEquipmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectEquipment.objects.all()
    serializer_class = CreateProjectEquipmentSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectEquipmentViewSet(viewsets.ModelViewSet):
    queryset = ProjectEquipment.objects.all()
    serializer_class = ProjectEquipmentSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectBudgetViewSet(viewsets.ModelViewSet):
    queryset = ProjectBudget.objects.all()
    serializer_class = CreateProjectBudgetSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectBudgetViewSet(viewsets.ModelViewSet):
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset


class CreateProjectBidViewSet(viewsets.ModelViewSet):
    queryset = ProjectBid.objects.all()
    serializer_class = CreateProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectBidViewSet(viewsets.ModelViewSet):
    queryset = ProjectBid.objects.all()
    serializer_class = ProjectBidSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectBid.objects.filter(vendor=self.request.user, project=project)
        else:
            return self.queryset


class CreateProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuote.objects.all()
    serializer_class = CreateProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectQuoteViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuote.objects.all()
    serializer_class = ProjectQuoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectQuote.objects.filter(vendor=self.request.user, project=project)
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
    queryset = ProjectQuoteItem.objects.all()
    serializer_class = ProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        self.queryset = self.queryset.filter(project=project)

        if self.request.GET.get('e'):
            return ProjectQuoteItem.objects.filter(vendor=self.request.user, project=project)
        elif self.request.GET.get('item'):
            if self.request.GET.get('item') == '':
                return []
            else:
                equipment = get_object_or_404(ProjectEquipment, id=self.request.GET.get('item'))
                return ProjectQuoteItem.objects.filter(project=project, equipment=equipment)
        elif self.request.GET.get('vendor'):
            vendor = get_object_or_404(User, id=self.request.GET.get('vendor'))
            return ProjectQuoteItem.objects.filter(project=project, vendor=vendor)
        else:
            return self.queryset


class CreateProjectQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = ProjectQuoteItem.objects.all()
    serializer_class = CreateProjectQuoteItemSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'
