from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from graphene_django.views import GraphQLView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
import os

from django.core import management


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


class DownloadGraphQlSchema(LoginRequiredMixin, View):

    def get(self, request):
        management.call_command('graphql_schema')
        file_path = os.path.join(settings.BASE_DIR, 'schema.json')
        if request.user.is_superuser and os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(),
                    content_type='application/json'
                )
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
            return response
        else:
            raise Http404
