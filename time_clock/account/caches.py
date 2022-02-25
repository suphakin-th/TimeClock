from django.contrib.auth import get_user_model
from django.core.cache import cache

from utils.caches.time_out import get_time_out
from django.contrib.auth.models import Group, Permission
# from utils.redis import delete_value


def cache_account(account_id):
    from .models import Account
    key = 'account_%s' % account_id
    result = cache.get(key)
    if result is None:
        try:
            result = Account.objects.get(id=account_id)
        except:
            result = -1
        cache.set(key, result, get_time_out())
    return None if result == -1 else result


def cache_account_delete(account_id):
    key = 'account_%s' % account_id
    cache.delete(key)
    cache.delete('account_profile_%s' % account_id)
    cache.delete('auth_group_list_%s' % account_id)
    cache.delete('auth_permission_%s' % account_id)


def cached_auth_permission(user_id, group):
    if group is None:
        key = 'auth_permission_%s' % user_id
    else:
        key = 'auth_permission_%s_%s' % (user_id, group.id)
    result = cache.get(key)
    if result is None:
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        perms = Permission.objects.filter(**{user_groups_query: user_id})
        if group is not None:
            perms = perms.filter(group=group)
        result = perms.values_list('content_type__app_label', 'codename').order_by()
        cache.set(key, result, get_time_out())
    return result


def cached_auth_group(group_id):
    key = 'auth_group_%s' % group_id
    result = cache.get(key)
    if result is None:
        try:
            result = Group.objects.get(id=group_id)
            cache.set(key, result, get_time_out())
        except:
            result = -1
    return None if result == -1 else result


def cached_auth_group_delete(group_id):
    key = 'auth_group_%s' % group_id
    cache.delete(key)


def cache_account_delete_all():
    from .models import Account
    account_id_list = Account.objects.all().values_list('id', flat=True)
    cache.delete_many(['account_%d' % i for i in account_id_list])
    cache.delete_many(['account_profile_%d' % i for i in account_id_list])


def cached_auth_group_list(account):
    key = 'auth_group_list_%s' % account.id
    result = cache.get(key)
    if result is None:
        result = account.groups.all()
        if (len(result) < 1):
            result = None
            cache.set(key, result, get_time_out())
        else:
            cache.set(key, result, get_time_out())
    return result


def cached_account_profile(account_id):
    from account.serializers import AccountSerializer
    from .models import Account
    key = 'account_profile_%s' % account_id
    result = cache.get(key)
    if result is None:
        try:
            account = Account.objects.get(id=account_id)
            result = AccountSerializer(account).data
            result.update({"clockIn": "-"})
            cache.set(key, result, get_time_out())
            return result
        except:
            result = {}
    return result
