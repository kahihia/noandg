from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.engineering.forms import ProjectForm, ProjectFileForm
from apps.engineering.models import Project, ProjectFile, ProjectEquipment, ProjectBudget, ProjectBid, ProjectQuote, \
    ProjectQuoteItem, ProjectDesign, ProjectFabrication, ProjectStage
from apps.engineering.serializers import CreateProjectSerializer, ProjectSerializer, CreateProjectFileSerializer, \
    ProjectFileSerializer, CreateProjectEquipmentSerializer, ProjectEquipmentSerializer, CreateProjectBudgetSerializer, \
    ProjectBudgetSerializer, ProjectBidSerializer, CreateProjectBidSerializer, CreateProjectQuoteSerializer, \
    ProjectQuoteSerializer, CreateProjectQuoteItemSerializer, ProjectQuoteItemSerializer, ProjectDesignSerializer, \
    CreateProjectDesignSerializer, ProjectFabricationSerializer, CreateProjectFabricationSerializer, \
    ProjectStageSerializer
from configs import day_min, day_max, daterange


class ProjectsView(LoginRequiredMixin, View):
    template_name = 'engineering/index.html'
    context = {}

    def get(self, request):
        project_form = ProjectForm

        self.context['projects'] = Project.objects.all()
        self.context['form'] = project_form

        return render(request, self.template_name, self.context)

    def post(self, request):
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project = project_form.save(commit=True)
            messages.success(request, 'Project successfully created.')
            return redirect(reverse('projects_directory'))

        else:
            messages.warning(request, project_form.errors)
            self.context['profile_form'] = project_form
            return render(request, self.template_name, self.context)


class ProjectView(LoginRequiredMixin, View):
    template_name = 'engineering/project.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_form = ProjectForm(instance=project)

        self.context['project'] = project
        self.context['form'] = project_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_form = ProjectForm(request.POST, instance=project)

        if project_form.is_valid():
            project = project_form.save(commit=True)
            messages.success(request, 'Changes successfully saved.')
            return redirect(reverse('project_overview', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_form.errors)
            self.context['profile_form'] = project_form
            return render(request, self.template_name, self.context)


class ProjectFilesView(LoginRequiredMixin, View):
    template_name = 'engineering/files/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_files = ProjectFile.objects.filter(project=project)
        project_file_form = ProjectFileForm

        self.context['project'] = project
        self.context['project_files'] = project_files
        self.context['form'] = project_file_form

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_file_form = ProjectFileForm(request.POST, request.FILES)

        if project_file_form.is_valid():
            project_data = project_file_form.save(commit=False)
            project_data.project = project
            project_data.save()

            messages.success(request, 'Document successfully uploaded.')
            return redirect(reverse('project_documents', kwargs={'slug': project.slug}))

        else:
            messages.warning(request, project_file_form.errors)
            self.context['form'] = project_file_form
            return render(request, self.template_name, self.context)


class ProjectFileDeleteView(LoginRequiredMixin, View):
    context = {}

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs['slug'])
        project_file = get_object_or_404(ProjectFile, slug=kwargs['file_slug'])
        project_file.delete()

        messages.success(request, 'Document deleted successfully.')

        return redirect(reverse('project_documents', kwargs={'slug': project.slug}))


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
        elif self.request.GET.get('start_date') and self.request.GET.get('end_date'):

            start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

            return self.queryset.filter(
                created_at__range=[day_min(start_date.strftime("%Y-%m-%d")), day_max(end_date.strftime("%Y-%m-%d"))])
        else:
            return self.queryset


class ProjectStageViewSet(viewsets.ModelViewSet):
    queryset = ProjectStage.objects.all()

    def get_queryset(self):
        if self.request.GET.get('project'):
            project = get_object_or_404(Project, slug=self.request.GET.get('project'))
            return ProjectStage.objects.filter(project=project)
        else:
            return self.queryset

    serializer_class = ProjectStageSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


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
        elif self.request.GET.get('start_date') and self.request.GET.get('end_date'):

            start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

            return self.queryset.filter(
                created_at__range=[day_min(start_date.strftime("%Y-%m-%d")), day_max(end_date.strftime("%Y-%m-%d"))])
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
        elif self.request.GET.get('start_date') and self.request.GET.get('end_date'):

            start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d')

            return self.queryset.filter(
                created_at__range=[day_min(start_date.strftime("%Y-%m-%d")), day_max(end_date.strftime("%Y-%m-%d"))])
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


class ProjectFabricationViewSet(viewsets.ModelViewSet):
    queryset = ProjectFabrication.objects.all()
    serializer_class = ProjectFabricationSerializer
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


class CreateProjectFabricationViewSet(viewsets.ModelViewSet):
    queryset = ProjectFabrication.objects.all()
    serializer_class = CreateProjectFabricationSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    lookup_field = 'slug'


class ProjectTeamViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        project = get_object_or_404(Project, id=self.request.GET.get('project'))
        all_teams = project.members.all()

        teams = []
        for team in all_teams:
            team_object = {'value': team.id,
                           'label': team.first_name + ' ' + team.last_name}

            # append groups
            teams.append(team_object)

        return Response({'results': teams})


class ProjectFormViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = Project.objects.all()

        projects_obj = []
        for project in projects:
            project_object = {'value': project.id, 'label': project.name}

            projects_obj.append(project_object)

        return Response({'results': projects_obj})
