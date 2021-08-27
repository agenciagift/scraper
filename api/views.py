from api.scrape.request import get_page_data
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def scrape(request):
    url = request.query_params.get('url')

    content = get_page_data(url)

    return Response(content)
