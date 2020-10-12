from rest_framework import permissions
from django.contrib.auth import get_user_model # If used custom user model

# logger = logging.getLogger(__name__)

User = get_user_model()


class IsOwner(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     #### can write custom code
    #     print(view.kwargs)
    #     user = User.objects.get(pk=view.kwargs['id'])
    #     if request.user == user:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Instance must have an attribute named `owner`.
        print("Im here", obj)
        return obj.owner == request.user or request.user.is_admin