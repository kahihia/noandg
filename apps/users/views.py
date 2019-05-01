from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import AllowedPermission
from apps.users.serializers import GroupSerializer, PermissionSerializer, UserSerializer, CreateGroupSerializer, \
    CreateUserSerializer


class UsersView(LoginRequiredMixin, View):
    template_name = 'users/index.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)


class UserViewSet(viewsets.ModelViewSet):
    """
    Users viewset automatically provides `list` and `crud` actions.
    """
    queryset = User.objects.all()

    def get_queryset(self):
        users = User.objects.filter(is_staff=False)
        if self.request.GET.get('q'):
            return users.filter(
                Q(first_name__icontains=self.request.GET.get('q')) |
                Q(last_name__icontains=self.request.GET.get('q')))
        elif self.request.GET.get('f'):
            group_users = users.filter(groups__name=self.request.GET.get('f'))
            if self.request.GET.get('fq'):
                return group_users.filter(
                    Q(first_name__icontains=self.request.GET.get('fq')) |
                    Q(last_name__icontains=self.request.GET.get('fq')))
            return group_users
        else:
            return users

    serializer_class = UserSerializer
    lookup_field = 'id'


class CreateUserViewSet(viewsets.ModelViewSet):
    """
    Create users
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    View user groups
    """
    queryset = Group.objects.all()

    def get_queryset(self):

        if self.request.GET.get('q'):
            return self.queryset.filter(
                Q(name__icontains=self.request.GET.get('q')))
        else:
            return self.queryset

    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class CreateGroupViewSet(viewsets.ModelViewSet):
    """
    Create user groups
    """
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class PermissionViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        allowed_permissions = AllowedPermission.objects.all()

        permissions = []
        """
        get permission details for each model
        """
        for allowed_permission in allowed_permissions:
            model_permissions_object = {'model': allowed_permission.name, 'title': allowed_permission.title,
                                        'summary': allowed_permission.summary}
            permission_models = allowed_permission.models.all()
            model_perms = []
            for permission_model in permission_models:
                content_type = get_object_or_404(ContentType, model=permission_model.name,
                                                 app_label=allowed_permission.name)
                model_permissions = Permission.objects.filter(content_type=content_type)
                serializer = PermissionSerializer(model_permissions, many=True)
                model_perms.append(serializer.data)

            model_permissions_object['permissions'] = model_perms

            # append permissions
            permissions.append(model_permissions_object)

        return Response({'results': permissions})


class GroupsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_groups = Group.objects.all()

        groups = []
        """
        get form employee groups
        """
        for group in all_groups:
            group_object = {'value': group.id, 'label': group.name}

            # append groups
            groups.append(group_object)

        return Response({'results': groups})


class UsersOptionViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_users = User.objects.all()

        users = []
        """
        get user options
        """
        for user in all_users:
            user_object = {'value': user.id, 'label': f'{user.first_name} {user.last_name}'}

            # append users
            users.append(user_object)

        return Response({'results': users})


class DeleteGroupUserViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        group_name = request.GET.get('group')
        user_id = request.GET.get('user')
        g = get_object_or_404(Group, name=group_name)
        g.user_set.remove(user_id)

        return Response({'results': True})
