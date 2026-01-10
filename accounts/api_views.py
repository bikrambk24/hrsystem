from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.password_validation import validate_password

class ForceChangePasswordAPI(APIView):
   permission_classes = [permissions.IsAuthenticated]

   def post(self, request):
       new_password = request.data.get("new_password")
       confirm = request.data.get("confirm_password")

       if not request.user.must_change_password:
           return Response({"detail": "Not required."}, status=status.HTTP_400_BAD_REQUEST)

       if not new_password or not confirm:
           return Response({"detail": "new_password and confirm_password required."}, status=status.HTTP_400_BAD_REQUEST)

       if new_password != confirm:
           return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

       validate_password(new_password)
       request.user.set_password(new_password)
       request.user.must_change_password = False
       request.user.save(update_fields=["must_change_password"])
       return Response({"detail": "Password changed."})
