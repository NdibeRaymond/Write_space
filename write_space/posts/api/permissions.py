from rest_framework.permissions import BasePermission

class  IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object to perform this function"
    my_safe_methods = ["PUT","GET"]
    def has_object_permission(self,request,view,objects):
        if request.method in self.my_safe_methods:
            return True
        return objects.author == request.user
