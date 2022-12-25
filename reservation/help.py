def time_in_range(start, end, current):
    return start <= current <= end


def convert_12_format(hour, min):
    from datetime import datetime
    d = datetime.strptime(str(hour)+":"+str(min), "%H:%M")
    return d.strftime("%I:%M %p")


def get_role(request):
    from user.models import User
    import jwt
    from rest_framework.exceptions import AuthenticationFailed
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('unauthenticated!')

    user = User.objects.get(pk=payload['id'])
    return user.role