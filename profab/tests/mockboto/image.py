from profab import _Keys


class MockImage(object):
    def run(self, instance_type, key_name, security_groups):
        return _Keys(instances=[_Keys(state='running', dns_name='hostname')])
