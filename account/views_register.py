from django.contrib.auth import login
from django.core.validators import validate_email, ValidationError
from django.utils import timezone
from rest_framework import mixins
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from log.models import Log
from .models import Account, Session
from .serializers import RegisterSerializer, AccountSerializer


def register(request, data, is_web):
    config_register_value = {
        'field_list': [
            {
                'key': 'username',
                'name': 'username',
                'placeholder': 'username',
                'type': 5,
                'max_length': 255,
                'min_length': 4,
                'is_optional': False
            }, {
                'key': 'email',
                'name': 'email',
                'placeholder': 'email',
                'type': 5,
                'max_length': 255,
                'is_optional': False
            }, {
                'key': 'password',
                'name': 'password',
                'placeholder': 'password',
                'type': 5,
                'is_optional': False
            }, {
                'key': 'confirm_password',
                'name': 'confirm_password',
                'placeholder': 'confirm_password',
                'type': 5,
                'is_optional': False
            }]}

    all_field = config_register_value['field_list']

    database_standard_field = {'username', 'email', 'password', 'confirm_password'}
    param_extra_field = {}

    # Check Empty Field
    for field in all_field:
        if not field['is_optional']:
            if field['key'] not in data:
                return {'detail': '%s_is_required' % field['key']}, status.HTTP_428_PRECONDITION_REQUIRED

        value = data.get(field['key'], None)

        if field['key'] in data and value and field['key'] not in str(database_standard_field):
            param_extra_field[field['key']] = value

        min_length = field.get('min_length', None)
        max_length = field.get('max_length', None)
        if min_length and value and len(value) < int(min_length) and max_length is None:
            return {'detail': '%s_length_error' % field['key']}, status.HTTP_400_BAD_REQUEST
        if max_length and value and len(value) > int(max_length) and min_length is None:
            return {'detail': '%s_length_error' % field['key']}, status.HTTP_400_BAD_REQUEST
        if max_length and value and len(value) > int(max_length) or min_length and value and len(value) < int(
                min_length):
            return {'detail': '%s_length_error' % field['key']}, status.HTTP_400_BAD_REQUEST

    username = Account.objects.filter(username__iexact=data['username'].strip()).first()
    if username:
        return {'detail': 'username_has_been_already_use'}, status.HTTP_409_CONFLICT
    email = Account.objects.filter(email__iexact=data['email'].strip()).first()
    if email:
        return {'detail': 'email_has_been_already_use'}, status.HTTP_409_CONFLICT
    try:
        validate_email(data['email'])
    except ValidationError:
        return {'detail': 'error_email_format'}, status.HTTP_400_BAD_REQUEST

    if data['password'] != data['confirm_password']:
        return {'detail': 'password_not_match'}, status.HTTP_400_BAD_REQUEST

    _account = Account.objects.create(
        username=data['username'].strip().lower(),
        email=data['email'].strip().lower() if data['email'] else None,
    )

    _account.set_password(data['password'])
    _account.last_active = datetime.datetime.now()
    _account.is_admin = True
    _account.save()

    login(request, _account, backend='django.contrib.auth.backends.ModelBackend')
    session_key = request.session.session_key
    if session_key is None:
        request.session.save()
        session_key = request.session.session_key
    Session.push(request.user, session_key)
    request.session.set_expiry(86400 * 365)  # 1 year expire
    Log.push(request, 'ACCOUNT_REGISTER', 'Login', _account, 'Register Successful', status.HTTP_201_CREATED)
    return AccountSerializer(_account).data, status.HTTP_201_CREATED


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Account.objects.all()
    allow_redirects = True
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data, status_response = register(request, request.data, False)
        return Response(data=response_data, status=status_response)
