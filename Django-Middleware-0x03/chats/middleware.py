import datetime
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("RequestLoggingMiddleware: Processing request...")
        now = datetime.datetime.now()


        #Getting the user information
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            username = user.username

        else:
            username = 'Anonymous'

        # Log the request details
        log_message = f"{now} - User: {username} - Path: {request.path}\n"
        with open('requests.log', 'a') as log_file:
            log_file.write(log_message)

        response = self.get_response(request)
        return response
    

# Restrict Chat Access by time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.datetime.now().time()
        # Allow access only between 16:00 (6PM) and 21:00 (9PM)
        if not (datetime.time(16, 0) <= now <= datetime.time(21, 0)):
            return HttpResponseForbidden("Access to chats is only allowed between 4PM and 9PM.")
        return self.get_response(request)
    

#Detect and Block offensive Language Section
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        #This store timestamps of messages per IP
        self.ip_message_times = {}  
        # List of banned words
        self.banned_words = ['suicide', 'kill', 'offensive']  


    def __call__(self, request):
        # Only limit POST requests
        if request.method == "POST":
            #This is where we check for offensive language and rate limiting
            message = ""
            if hasattr(request, "POST"):
                message = request.POST.get("message", "")
            elif hasattr(request, "body"):
                try:
                    import json
                    data = json.loads(request.body.decode())
                    message = data.get("message", "")
                except Exception:
                    pass

            for word in self.banned_words:
                if word.lower() in message.lower():
                    return HttpResponseForbidden("Offensive language detected.")


            #limit the number of messages per IP address
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute in seconds
            limit = 5    # max messages per window

            # Get or create the list of timestamps for this IP
            timestamps = self.ip_message_times.get(ip, [])
            # Remove timestamps older than 1 minute
            timestamps = [t for t in timestamps if now - t < window]
            if len(timestamps) >= limit:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")
            timestamps.append(now)
            self.ip_message_times[ip] = timestamps

        return self.get_response(request)


    def get_client_ip(self, request):
        # This will get the client's IP address from the request
        # It checks for the 'X-Forwarded-For' header first, which is common in proxied requests
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

#Enforce chat user Role Permissions
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This middleware checks if the user is authenticated and has the required permissions
        # It allows access to admin and staff users, and blocks access for others
        excluded_paths = ['/admin/login/', '/accounts/login/', '/login/', '/logout/', '/admin/logout/']
        if request.path in excluded_paths:
            return self.get_response(request)
        

        # Only check for authenticated users
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            # Check if user is admin (superuser)
            if not (user.is_superuser or user.is_staff):
                return HttpResponseForbidden("You do not have permission to perform this action.")
        else:
            # If not authenticated, block access
            return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)