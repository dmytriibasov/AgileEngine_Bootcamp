from django.db import transaction
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status


class CreateModelTransactionMixin(mixins.CreateModelMixin):
    """
    Custom Create Model Mixin with extended database transaction functionality
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
