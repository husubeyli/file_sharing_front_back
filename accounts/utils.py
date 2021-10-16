def get_ip_adress(request):
    ip=''
    x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forward:
        ip = x_forward.split(",")[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip