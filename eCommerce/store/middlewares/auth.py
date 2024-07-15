from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        if not request.session.get('customer'):
            return_url = request.path_info
            return redirect(f'/login/?return_url={return_url}')
        response = get_response(request)
        return response

    return middleware
