import re, telnetlib, sys


class MemcachedStats:
    _client = None
    _key_regex = re.compile(r'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(r'STAT items:(.*):number ')
    _stat_regex = re.compile(r"STAT (.*) (.*)\r")

    def __init__(self, host=None, port=None):
        from django.conf import settings
        if host is None or port is None:
            if hasattr(settings, 'CACHES'):
                cached_setting = getattr(settings, 'CACHES', None)
                try:
                    host, port = cached_setting['default']['LOCATION'].split(':')
                except:
                    host, port = 'localhost', '11211'
            else:
                host, port = 'localhost', '11211'
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write(cmd.encode('ascii') + b"\n")
        return self.client.read_until(b'END').decode()

    def key_details(self, sort=True, limit=100):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s %s'
        keys = [key for id in self.slab_ids()
                for key in self._key_regex.findall(self.command(cmd % (id, limit)))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True, limit=100):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))


def main(argv=None):
    if not argv:
        argv = sys.argv
    host = argv[1] if len(argv) >= 2 else None
    port = argv[2] if len(argv) >= 3 else None
    import pprint
    m = MemcachedStats(host, port)
    pprint.pprint(m.keys())


if __name__ == '__main__':
    main()
