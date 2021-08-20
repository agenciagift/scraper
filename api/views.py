from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def scrape(request):
    content = {
        "foo": "bar"
    }

    return Response(content)
