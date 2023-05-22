from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "You are not owner of this selection!"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "author"):
            owner = obj.author
        else:
            raise Exception("permission error")

        if request.user == owner:
            return True


class IsStaff(BasePermission):
    message = "You are not admin/moderator"

    def has_object_permission(self, request, view, obj):
        if request.user.role in ["moderator", "admin"]:
            return True
