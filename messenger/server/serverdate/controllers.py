"""Controllers for serverdate module"""
from datetime import datetime

from decorators import logged
from protocol import make_response


@logged
def server_date_controller(request):
    """Make response based on current date."""
    return make_response(request, 200, datetime.now().timestamp())
