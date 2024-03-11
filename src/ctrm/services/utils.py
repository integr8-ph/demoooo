import json
import requests

from src.ctrm.helpers.constants import ForwarderError, WorkbenchError
from src.ctrm.helpers.exceptions import NotFound, Conflict


class ClientNotFound(NotFound):
    DETAIL = ForwarderError.CLIENT_NOT_FOUND


class BaseUrlError(NotFound):
    DETAIL = ForwarderError.BASE_URL_NOT_FOUND


class WorkbenchConflict(Conflict):
    DETAIL = WorkbenchError.ALREADY_EXISTS


async def requests_get(url, headers=None):
    data = None
    if not headers:
        data = requests.get(url)
    else:
        data = requests.get(url, headers=headers)
    json_response = data.json()["data"]
    return json_response


async def requests_put(url, headers=None):
    data = None
    if not headers:
        data = requests.put(url)
    else:
        data = requests.put(url, headers=headers)
    return data


async def requests_post(url, data, headers=None):
    response_data = None
    if not headers:
        response_data = requests.post(url, data=json.dumps(data))
    else:
        response_data = requests.post(url, headers, data=json.dumps(data))
    json_response = response_data.json()
    return json_response
