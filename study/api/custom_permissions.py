from rest_framework.permissions import BasePermission


class NotStudent(BasePermission):
    '''
    Allows access only to users who are admin or teacher.
    '''
    def has_permission(self, request, view):
        return request.user.profile.type != 3 if request.user.is_authenticated else False
