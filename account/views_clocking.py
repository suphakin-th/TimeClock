from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Account, Clocking
from .serializers import AccountSerializer


class ClockingView(viewsets.GenericViewSet):
    queryset = Clocking.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    permission_classes_action = {
        'clockIn': [IsAuthenticated],
        'profile_patch': [IsAuthenticated],
    }

    @action(methods=['GET'], detail=False)
    def clockIn(self, request, *args, **kwargs):
        clocking = Clocking.check_in(request.user.id)
        if not clocking:
            return Response(
                data={'You already checkIn today or Have something wrong, Please contact your admin'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(AccountSerializer(clocking.account).data)

    @action(methods=['GET'], detail=False)
    def clockOut(self, request, *args, **kwargs):
        clocking = Clocking.check_out(request.user.id)
        if not clocking:
            return Response(data={'Please ClockIn first'}, status=status.HTTP_404_NOT_FOUND)
        return Response(AccountSerializer(clocking.account).data)
