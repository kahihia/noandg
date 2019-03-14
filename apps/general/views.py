from django.views.generic import TemplateView
from rest_framework import pagination
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


# Home view
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# Login API
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        full_name = '%s %s' % (user.first_name, user.last_name)
        user_groups = user.groups.all()
        user_group = None
        for ug in user_groups:
            user_group = ug.name

        perms = user.get_all_permissions()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'data': {
            'token': token.key,
            'full_name': full_name,
            'user_id': user.pk,
            'username': user.username,
            'user_group': user_group,
            'email': user.email,
            'permissions': perms
        }})


class APIPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
