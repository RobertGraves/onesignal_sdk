
class OneSignalHTTPError(Exception):
    """
    Exception raised for errors in the response of REST API calls to One Signal.
    """

    def __init__(self, response):
        
        if hasattr(response,'status_code'):
            self.status = response.status_code
        elif hasattr(response,'status'):
            self.status = response.status

        self.http_response = response
        self.message = self._get_message(response)
        

    def _get_message(self, response) -> str:
        if hasattr(response,'status_code'):
            status = response.status_code
        elif hasattr(response,'status'):
            status = response.status
        message = f'Unexpected http status code {status}.'
        response_body = response.json()
        if response_body and 'errors' in response_body and len(response_body['errors']) > 0:
            message = response_body['errors'][0]
        return message
