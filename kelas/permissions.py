from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission untuk memastikan hanya pemilik kelas yang dapat mengedit.
    """
    
    def has_permission(self, request, view):
        # Read permissions untuk semua request (termasuk anonymous)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions hanya untuk authenticated users
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permissions untuk semua request (termasuk anonymous)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions hanya untuk pemilik kelas
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'kelas'):
            return obj.kelas.author == request.user
        elif hasattr(obj, 'nama') and hasattr(obj.nama, 'kelas'):
            return obj.nama.kelas.author == request.user
        
        return False