import os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

SHARED_ROOT = "/srv/shared"


class RenameFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        source = os.path.join(SHARED_ROOT, request.data["from"])
        destination = os.path.join(SHARED_ROOT, request.data["to"])
        if not os.path.exists(source):
            return Response({"detail": "missing"}, status=status.HTTP_404_NOT_FOUND)
        os.rename(source, destination)
        return Response({"renamed": request.data["to"]})
