import datetime

import six
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from account.caches import cache_account_delete
from utils.datetime import convert_to_local
from utils.rounder import hour_rounder


def generate_username():
    import random
    import string
    return ''.join(random.sample(string.ascii_lowercase, 6))


class AccountManager(BaseUserManager):

    def create_user(self, username, password):
        if username is None:
            raise ValueError('The given username must be set')

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, is_accepted_active_consent=True):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(username, password)
        user.is_admin = True
        user.is_superuser = True
        user.type = 1
        user.is_accepted_active_consent = is_accepted_active_consent
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        db_index=True,
        null=True,
        blank=True
    )
    is_admin = models.BooleanField(default=False)
    datetime_update = models.DateTimeField(auto_now=True, null=True)
    objects = AccountManager()

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['-id']

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def today(self):
        clocking = Clocking.checking_today(self.id)
        if clocking and clocking.clock_in and not clocking.clock_out:
            return round(abs(clocking.clock_in - timezone.now()).total_seconds() / 3600.0)
        else:
            return 0

    @property
    def currentWeek(self):
        date = datetime.datetime.now()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        clocking = Clocking.objects.filter(
            account_id=self.id,
            datetime_create__range=[start_week, end_week]
        ).aggregate(Sum('count_time'))

        return round(clocking['count_time__sum'] if clocking and 'count_time__sum' in clocking else 0)

    @property
    def currentMonth(self):
        clocking = Clocking.objects.filter(
            account_id=self.id,
            datetime_create__year=datetime.datetime.now().year,
            datetime_create__month=datetime.datetime.now().month
        ).aggregate(Sum('count_time'))
        return round(clocking['count_time__sum'] if clocking and 'count_time__sum' in clocking else 0)

    @staticmethod
    def pull_account(username_or_email):
        _account = Account.objects.filter(username=username_or_email).first()
        if _account is None:
            _account = Account.objects.filter(email=username_or_email).exclude(
                email__isnull=True).first()
        return _account


class Clocking(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)
    count_time = models.IntegerField(default=0)
    clock_in = models.DateTimeField(blank=True, null=True)
    clock_out = models.DateTimeField(blank=True, null=True)

    datetime_update = models.DateTimeField(auto_now_add=True, db_index=True)
    datetime_create = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-id']

    @staticmethod
    def checking_today(account_id):
        print('q: %s - %s - %s' % (datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day))
        print(Clocking.objects.values())
        clocking = Clocking.objects.filter(
            account_id=account_id,
            datetime_create__year=datetime.datetime.now().year,
            datetime_create__month=datetime.datetime.now().month,
            datetime_create__day=datetime.datetime.now().day
        ).order_by('-datetime_create').first()

        return clocking if clocking else None

    @staticmethod
    def check_in(account_id):
        clocking = Clocking.checking_today(account_id)

        if not clocking:
            return Clocking.objects.create(
                account_id=account_id,
                clock_in=datetime.datetime.now()
            )
        elif clocking and clocking.clock_in and (timezone.now().day - clocking.clock_in.day) >= 1:
            clocking.count_time += (24 - int(hour_rounder(clocking.clock_in).hour))
            clocking.clock_out = datetime.datetime(
                day=datetime.datetime.now().day + 1,
                month=datetime.datetime.now().month,
                year=datetime.datetime.now().year
            )
            clocking.save()
            return Clocking.objects.create(
                account_id=account_id,
                clock_in=datetime.datetime.now()
            )
        elif clocking and not clocking.clock_in:
            clocking.clock_in = datetime.datetime.now()
            clocking.count_time = 0
            clocking.save()
            return clocking

        elif clocking and clocking.clock_in and clocking.clock_out:
            return Clocking.objects.create(
                account_id=account_id,
                clock_in=datetime.datetime.now()
            )
        else:
            return None

    @staticmethod
    def check_out(account_id):
        clocking = Clocking.checking_today(account_id)
        if not clocking:
            return None
        elif clocking and clocking.clock_in and (timezone.now().day - clocking.clock_in.day) >= 1:
            clocking.count_time += (24 - int(hour_rounder(clocking.clock_in).hour))
            clocking.clock_out = datetime.datetime(
                day=datetime.datetime.now().day + 1,
                month=datetime.datetime.now().month,
                year=datetime.datetime.now().year
            )
            clocking.save()
            return Clocking.objects.create(
                account_id=account_id,
                clock_in=datetime.datetime(
                    day=datetime.datetime.now().day,
                    month=datetime.datetime.now().month,
                    year=datetime.datetime.now().year
                ),
                clock_out=datetime.datetime.now(),
                count_time=hour_rounder(datetime.datetime.now())
            )
        elif clocking and clocking.clock_in and not clocking.clock_out:
            clocking.count_time += round(abs(clocking.clock_in - timezone.now()).total_seconds() / 3600.0)
            clocking.clock_out = datetime.datetime.now()
            clocking.save()
            return clocking


class Session(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, db_index=True)
    token = models.TextField(null=True, blank=True)
    datetime_create = models.DateTimeField(auto_now_add=True, db_index=True)

    @staticmethod
    def push(account, session_key, token=None):
        from importlib import import_module
        from django.conf import settings

        session = Session.objects.filter(account=account).first()
        if session is not None:
            if session.session_key != session_key:
                session_store = import_module(settings.SESSION_ENGINE).SessionStore
                s = session_store(session_key=session.session_key)
                s.delete()
                session.session_key = session_key
                session.token = token
                session.save()
        else:
            Session.objects.create(account=account, session_key=session_key, token=token)

    @staticmethod
    def remove(account_id, session_key=None):
        from importlib import import_module
        from django.conf import settings

        session_store = import_module(settings.SESSION_ENGINE).SessionStore
        for session in Session.objects.filter(account_id=account_id):
            _session = session_store(session.session_key)
            _session.delete()
            session.delete()
        cache_account_delete(account_id)