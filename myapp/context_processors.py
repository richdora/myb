from django.contrib.auth import get_user_model

def owner(request):
    User = get_user_model()
    if request.user.is_authenticated:
        owner_user = User.objects.get(username=request.user.username)
        return {'owner': owner_user}
    else:
        return {'owner': None}
