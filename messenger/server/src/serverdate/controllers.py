"""Controllers for serverdate module"""
from datetime import datetime

from src.decorators import logged
from src.protocol import make_response


@logged
def server_date_controller(request):
    """Make response based on current date."""
    return make_response(request, 200, datetime.now().timestamp())
