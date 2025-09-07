from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for admin, auth pages, and static files
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/') or
            request.path in ['/', '/logout/']):
            return None
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Check if user has a profile
        if not hasattr(request.user, 'userprofile'):
            messages.error(request, 'User profile not found. Please contact administrator.')
            return redirect('login')
        
        user_type = request.user.userprofile.user_type
        
        # Define role-based access rules
        # Admin can access everything
        if user_type == 'admin':
            return None
        
        # Teacher access rules
        if user_type == 'teacher':
            if any(request.path.startswith(path) for path in ['/students/', '/results/']):
                return None
            if any(request.path.startswith(path) for path in ['/teachers/', '/classes/', '/subjects/', '/reports/']):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
        
        # Student access rules
        if user_type == 'student':
            if request.path.startswith('/results/my-results/'):
                return None
            if any(request.path.startswith(path) for path in ['/students/', '/teachers/', '/classes/', '/subjects/', '/results/', '/reports/']):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
        
        return None