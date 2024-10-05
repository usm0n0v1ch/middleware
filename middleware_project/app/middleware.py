import os
import logging
from django.utils.timezone import now

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        url = request.build_absolute_uri()
        ip = request.META.get('REMOTE_ADDR')
        username = request.user.username if request.user.is_authenticated else ip
        log_file_name = f'logs/{username}.log'
        os.makedirs(os.path.dirname(log_file_name), exist_ok=True)

        log_message = f"{now()} - {method} {url} - IP: {ip}"
        with open(log_file_name, 'a') as log_file:
            log_file.write(log_message + '\n')

        response = self.get_response(request)

        log_message = f"{now()} - Response status: {response.status_code}"
        with open(log_file_name, 'a') as log_file:
            log_file.write(log_message + '\n')

        return response
