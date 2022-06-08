from typing import Any, Dict

import aiohttp
import asyncio
import requests

from .error import OneSignalHTTPError
from .response import OneSignalResponse


def _build_request_kwargs(token: str = None,
                          payload: Dict[str, Any] = None,
                          params: Dict[str, Any] = None) -> Dict[str, Any]:
    request_kwargs = {}
    if token is not None:
        request_kwargs['headers'] = {'Authorization': 'Basic {0}'.format(token)}
    if payload is not None:
        request_kwargs['json'] = payload
    if params is not None:
        request_kwargs['params'] = params
    return request_kwargs


def _handle_response(response) -> OneSignalResponse:
    """Given an httpx.Response either raise an Exception or return final Response object."""
    
    if hasattr(response,'status_code'):
        status_code = response.status_code
    elif hasattr(response,'status'):
        status_code = response.status
    if status_code >= 300:
        raise OneSignalHTTPError(response)
    return OneSignalResponse(response)


def basic_auth_request(method: str,
                       url: str,
                       token: str = None,
                       payload: Dict[str, Any] = None,
                       params: Dict[str, Any] = None) -> OneSignalResponse:
    """Make a request using basic authorization."""
    request_kwargs = _build_request_kwargs(token, payload, params)
    
    return _handle_response(requests.request(method,url,**request_kwargs))


async def async_basic_auth_request(method: str,
                                   url: str,
                                   token: str = None,
                                   payload: Dict[str, Any] = None,
                                   params: Dict[str, Any] = None) -> OneSignalResponse:
    """Make an async request using basic authorization."""
    request_kwargs = _build_request_kwargs(token, payload, params)
    async with aiohttp.ClientSession() as client:
        response = await client.request(method, url, **request_kwargs)
        return _handle_response(response)