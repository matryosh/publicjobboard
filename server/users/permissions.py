from rest_framework import permissions

class IsCompany(permissions.BasePermission):
    """
        Custom Permission to allow only users
        with Company flags to use it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'CM'


class IsProperCompany(permissions.BasePermission):
    """
        Custom Permission to allow only a company
        with associated ID to use this API
    """

    def has_object_permission(self, request, view, obj):
        if request.user.user_number == obj.user.user_number and request.user.user_type=='CM':
            return True


class IsJobseeker(permissions.BasePermission):
    """
        Custom Permission to determine if the user 
        is flagged as a Jobseeker and not a Company
    """
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'JB'


class IsProperJobseeker(permissions.BasePermission):
    """
        Custom Permission to allow only users
        that have the Jobseeker flag and
        are the owner/creator to modify
        the given view.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.user_number == obj.user.user_number and request.user.user_type=='JB':
            return True
        elif(request.methods in permissions.SAFE_METHODS):
            return True
        
        return False