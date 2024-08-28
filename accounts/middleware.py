from django.utils import timezone
from  django.conf import settings
from django.contrib.auth import logout
from datetime import timedelta,datetime



class LogoutMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity= request.session.get('last_activity')
            if last_activity:
                last_activity= datetime.fromisoformat(last_activity)
                time= timezone.now()- last_activity
                if time > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    del request.session['last_activity']
                    logout(request)
            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
    
  