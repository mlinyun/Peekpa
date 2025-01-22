from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


@require_http_methods(["GET"])
def home(request):
    return HttpResponse("Welcome to PeekpaBackend!")
