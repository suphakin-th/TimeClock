import datetime
import logging

from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework import status

from account.caches import cached_account_profile
from account.models import Account, Session
from account.serializers import AccountSerializer
from log.models import Log


def login_web(request, data, code, is_web, group='ACCOUNT_LOGIN'):
    logger = logging.getLogger('LOGIN')
    if not data['password']:
        Log.push(request, group, code, None,
                 'Hacking!! password is None', status.HTTP_401_UNAUTHORIZED)
        logger.info('401 Unauthorized (%s) Password not entered' % data['username'])
        return {'detail': 'error_email_pass_fail'}, status.HTTP_401_UNAUTHORIZED

    account = Account.pull_account(data['username'])
    if not account:
        return {'detail': 'error_email_pass_fail'}, status.HTTP_401_UNAUTHORIZED

    account = authenticate(username=account.username, password=data['password'])
    if account is None:
        _account = Account.pull_account(data['username'].strip().lower())
        if _account:
            Log.push(request, group, code, _account,
                     'Password incorrect', status.HTTP_401_UNAUTHORIZED)
            logger.info('401 Unauthorized (%s) Password Incorrect' % data['username'])
        else:
            Log.push(request, group, code, None,
                     'Username incorrect', status.HTTP_401_UNAUTHORIZED, payload={'username': data['username']})
            logger.info('401 Unauthorized (%s) Username Incorrect' % data['username'])
        return {'detail': 'error_email_pass_fail'}, status.HTTP_401_UNAUTHORIZED

    if not account.is_active:
        Log.push(request, group, code, account, 'User is inactive',
                 status.HTTP_406_NOT_ACCEPTABLE)
        logger.info('406 Not Acceptable (%s) User is inactive' % data['username'])
        return {'detail': 'error_account_inactive'}, status.HTTP_406_NOT_ACCEPTABLE

    # account.language = data['language']
    login(request, account)

    account.last_login = timezone.now()
    account.save(update_fields=["last_login", "datetime_update"])


    session_key = request.session.session_key
    if session_key is None:
        request.session.save()
        session_key = request.session.session_key
    Session.push(request.user, session_key)

    request.session.set_expiry(86400 * 365)  # 1 year

    Log.push(request, group, code, account, 'Login success', status.HTTP_200_OK)
    logger.info('200 OK (%s) Login Success' % data['username'])
    result = AccountSerializer(account).data

    return result, status.HTTP_200_OK
