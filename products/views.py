from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ListProductSerializer, UpdateTotalStockSerializer
from django.db import DatabaseError
from .models import Products
from . import utils


class CreateProductAPIView(APIView):
    def post(self, request):
        data = utils.preprocess_request_data(dict(request.data))

        print("Processed Data:", data)
        serializer = ProductSerializer(data=data, context={"request": request})
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Product created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
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


class ListProductViewSet(generics.ListAPIView):
    queryset = Products.objects.filter(Active=True)
    serializer_class = ListProductSerializer
    permission_classes = [IsAuthenticated]

class EditStockView(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = UpdateTotalStockSerializer
    lookup_field = 'id'
    
    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
