from rest_framework.permissions import BasePermission
class IsAuthorOrReadOnly (BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', 'GET', 'OPTIONS', 'HEAD']:
            return True
        return obj.user_id == request.user