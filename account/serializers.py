import re

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from utils.datetime import convert_to_local
from .models import Account, Clocking


# TODO: Move to utils
def check_password(value):
    if re.compile('(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+|~=`{}:;<>?,.])').match(value):
        return True
    else:
        return False


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
        )


class AccountSerializer(serializers.ModelSerializer):
    clock_in = serializers.SerializerMethodField()
    clock_out = serializers.SerializerMethodField()
    currentClock = serializers.SerializerMethodField()
    clockedHours = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            'id',
            'email',
            'username',
            'clock_in',
            'clock_out',
            'currentClock',
            'clockedHours',
        )

    def get_clock_in(self, account):
        clocking = Clocking.checking_today(account.id)
        return convert_to_local(clocking.clock_in) if clocking and clocking.clock_in else '-'

    def get_clock_out(self, account):
        clocking = Clocking.checking_today(account.id)
        return convert_to_local(clocking.clock_out) if clocking and clocking.clock_out else '-'

    def get_currentClock(self, account):
        return account.today

    def get_clockedHours(self, account):
        return AccountWorkingTimeSerializer(account).data


class AccountWorkingTimeSerializer(serializers.ModelSerializer):
    today = serializers.SerializerMethodField()
    currentWeek = serializers.SerializerMethodField()
    currentMonth = serializers.SerializerMethodField()

    class Meta:
        model = Account

        fields = (
            'today',
            'currentWeek',
            'currentMonth',
        )

    def get_today(self, account):
        return account.today

    def get_currentWeek(self, account):
        return account.currentWeek

    def get_currentMonth(self, account):
        return account.currentMonth


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=settings.PASSWORD_MIN)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=False)
    email = serializers.CharField(max_length=255, required=False)
