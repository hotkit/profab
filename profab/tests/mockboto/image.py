from profab import _Keys


class MockInstance(object):
    def __init__(self, state):
        self.state = state
        self.dns_name='hostname'
    
    def update(self):
        self.state = 'running'


class MockImage(object):
    def run(self, instance_type, key_name, security_groups):
        return _Keys(instances=[MockInstance('pending')])
