from rest_framework import viewsets, status
from rest_framework.response import Response

from log.models import Log
from log.serializers import MiniLogSerializer, LogSerializer
from rest_framework.permissions import AllowAny


class LogDeviceView(viewsets.GenericViewSet):
    queryset = Log.objects.all()
    serializer_class = MiniLogSerializer
    permission_classes = (AllowAny,)

    app = 'log'
    model = 'log'

    def create(self, request, *args, **kwargs):
        serializer = MiniLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        log = Log.objects.create(
            group='EXTERNAL_LOG',
            code='DEVICE_EXTERNAL_LOG',
            payload=data['payload'],
            status='This data sent from external device',
            status_code=status.HTTP_201_CREATED
        )
        result = MiniLogSerializer(log).data
        return Response(result, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        queryset = Log.objects.filter(group='EXTERNAL_LOG', code='DEVICE_EXTERNAL_LOG')
        serializer = LogSerializer(queryset, many=True)
        return Response(serializer.data)
