def check_role(request):
    is_counselor = False
    if request.user.is_authenticated:
        is_counselor = request.user.groups.filter(name="Counselor").exists()
    return {"is_counselor": is_counselor}