"""Analytics views that are served from the same domain as the docs."""
from functools import lru_cache
from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from readthedocs.analytics.models import PageView
from readthedocs.api.v2.permissions import IsAuthorizedToViewVersion
from readthedocs.core.unresolver import unresolve
from readthedocs.core.utils.extend import SettingsOverrideObject
from readthedocs.projects.models import Project


class BaseAnalyticsView(APIView):

    """
    Track page views.

    Query parameters:

    - project
    - version
    - absolute_uri: Full path with domain.
    """

    http_method_names = ['get']
    permission_classes = [IsAuthorizedToViewVersion]

    @lru_cache(maxsize=1)
    def _get_project(self):
        project_slug = self.request.GET.get('project')
        project = get_object_or_404(Project, slug=project_slug)
        return project

    @lru_cache(maxsize=1)
    def _get_version(self):
        version_slug = self.request.GET.get('version')
        project = self._get_project()
        version = get_object_or_404(
            project.versions.all(),
            slug=version_slug,
        )
        return version

    # pylint: disable=unused-argument
    def get(self, request, *args, **kwargs):
        project = self._get_project()
        version = self._get_version()
        absolute_uri = self.request.GET.get('absolute_uri')
        self.increase_page_view_count(
            request=request,
            project=project,
            version=version,
            absolute_uri=absolute_uri,
        )
        return Response(status=200)

    # pylint: disable=no-self-use
    def increase_page_view_count(self, request, project, version, absolute_uri):
        """Increase the page view count for the given project."""
        unresolved = unresolve(absolute_uri)
        if not unresolved or not unresolved.file:
            return

        path = unresolved.file
        full_path = urlparse(absolute_uri).path

        PageView.objects.register_page_view(
            project=project,
            version=version,
            path=path,
            full_path=full_path,
            status=200,
        )


class AnalyticsView(SettingsOverrideObject):

    _default_class = BaseAnalyticsView
