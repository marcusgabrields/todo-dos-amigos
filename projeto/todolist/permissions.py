from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    message = 'Só usuários administradores podem acessar essa área.'

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser
