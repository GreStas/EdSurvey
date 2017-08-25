# clients.context_processors
# from clients.admin import RolePermissionAdmin


def person(request):
    """
    Returns context variables required by apps that use personalization system.

    If there is no 'person' attribute in the request, uses None.
    """
    if hasattr(request, 'person'):
        person = request.person
        # role_permission = RolePermissionAdmin.objects.filter(role=person.role)
    else:
        person = None

    return {
        'person': person,
        # 'role_permission': role_permission,
    }
