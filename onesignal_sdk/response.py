
class OneSignalResponse:
    """
    Designates a successful response from OneSignal with body.
    """

    def __init__(self, response):

        if hasattr(response,'status_code'):
            self.status = response.status_code
        elif hasattr(response,'status'):
            self.status = response.status

        self.http_response = response
        self.body = response.json()
