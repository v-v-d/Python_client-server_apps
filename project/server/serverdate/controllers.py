from datetime import datetime

from decorators import logged
from protocol import make_response


@logged
def server_date_controller(request):
    return make_response(request, 200, datetime.now().timestamp())
