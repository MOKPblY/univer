from django.contrib.auth.models import Group
from rest_framework import permissions

def is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists() #get???
    except Group.DoesNotExist:
        return None

class HasGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups = getattr(view, "required_groups", [])

        # # Determine the required groups for this particular request method.
        # required_groups = required_groups_mapping.get(request.method, [])

        # Return True if the user has all the required groups or is staff.
        return all(
            [
                is_in_group(request.user, group_name)
                for group_name in required_groups
            ]
        )