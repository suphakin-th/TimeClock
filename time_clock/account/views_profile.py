from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .caches import cached_account_profile, cache_account_delete
from .models import Account
from .serializers import AccountSerializer, AccountListSerializer


class ProfileView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Account.objects.none()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    permission_classes_action = {
        'list': [IsAuthenticated],
        'profile_patch': [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return Account.objects.filter(id=self.request.user.id)
        else:
            return self.queryset

    def get_object(self, queryset=None):
        account = Account.objects.filter(pk=self.request.user.id).first()
        return account

    def list(self, request, *args, **kwargs):
        result = AccountSerializer(Account.objects.get(id=request.user.id)).data
        return Response(data=result, status=status.HTTP_200_OK)

    def profile_patch(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = AccountListSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache_account_delete(account.id)
        return Response(self.get_serializer(account).data)
