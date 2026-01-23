from django.utils.deprecation import MiddlewareMixin 
from django.shortcuts import redirect 
from django.utils.timezone import now 
from django.contrib.auth import logout 
from datetime import datetime

class SessionTimeoutMiddleware(MiddlewareMixin): 
    def process_request(self, request): 
        if request.user.is_authenticated: 
            current_time = now() 
            last_activity_raw = request.session.get('last_activity') 
        
       
            try:
             if last_activity_raw: 
              if isinstance(last_activity_raw, str): 
                 last_activity = datetime.fromisoformat(last_activity_raw) 
                 
             else: 
              last_activity = last_activity_raw 
              elapsed = (current_time - last_activity_raw).total_seconds() 
              
              if elapsed > 600: # 10 minutes logout(request) 
                  logout(request)
                  return redirect('sign_up') 
              
            except Exception as e:
                request.session['last_activity'] = current_time 
                
            else: 
             request.session['last_activity'] = current_time 
             
            request.session['last_activity'] = current_time.isoformat()