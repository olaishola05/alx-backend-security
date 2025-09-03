from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='ALL', block=True)
@login_required
def my_view(request):
    return HttpResponse("This is a rate-limited view.")

@ratelimit(key='user_or_ip', rate='10/m', block=True)
def limited_authenticated_view(request):
    """
    This view is rate-limited to 10 requests per minute for both authenticated and anonymous users.
    """
    return HttpResponse("This is a limited view. You get 10 requests/minute.")

@ratelimit(key='ip', rate='5/m', block=True)
def limited_anonymous_view(request):
    """
    This view is rate-limited to 5 requests per minute for all requests based on IP.
    """
    return HttpResponse("This is a limited view for anonymous users. You get 5 requests/minute.")

@ratelimit(key='user', rate='10/m')
@ratelimit(key='ip', rate='5/m')
def login_view(request):
    """
    This view combines two rate limits.
    - An anonymous user gets 5 requests/minute (based on IP).
    - An authenticated user gets 10 requests/minute (based on user ID).
    """
    return HttpResponse("Welcome to the login page.")

