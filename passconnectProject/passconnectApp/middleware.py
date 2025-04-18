#Benjamin2404-AB-PASSCONNECT--ADMinBackend--TRY-FIX-1
# middleware.py - Add this file to your Django app

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class SessionHeaderMiddleware(MiddlewareMixin):
    """
    Middleware that authenticates using a session ID in the X-Session-ID header
    This works alongside regular cookie-based authentication
    """
    
    def process_request(self, request):
        # Skip if user is already authenticated via cookies
        if request.user.is_authenticated:
            return None
            
        # Try to get session ID from header
        session_id = request.headers.get('X-Session-ID')
        
        if not session_id:
            return None
            
        try:
            # Get session from database
            session = Session.objects.get(session_key=session_id)
            session_data = session.get_decoded()
            
            # Get user ID from session
            user_id = session_data.get('_auth_user_id')
            
            if user_id:
                # Get user model
                UserModel = request.user.__class__
                try:
                    user = UserModel.objects.get(pk=user_id)
                    # Attach user to request
                    request.user = user
                    logger.info(f"Authenticated via X-Session-ID header: {user.username}")
                except UserModel.DoesNotExist:
                    logger.warning(f"User ID {user_id} from session not found")
            
        except Session.DoesNotExist:
            logger.warning(f"Session ID {session_id} not found")
        except Exception as e:
            logger.error(f"Error in SessionHeaderMiddleware: {str(e)}")
            
        return None
