from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from django.db import DatabaseError

class CreateProductAPIView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product created successfully."}, status=status.HTTP_201_CREATED)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as db_error:
            return Response(
                {"error": "Database error occurred.", "details": str(db_error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
