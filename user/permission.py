from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    edit_methods = ("POST", "DELETE",)

    def has_permission(self, request, view):
        if request.user.role=='admin':
            return True