from profab import _Keys


class MockInstance(object):
    def __init__(self, state, next_state = 'running'):
        self.state = state
        self.dns_name='hostname'
        self.next_state = next_state
    
    def update(self):
        self.state = self.next_state

    def terminate(self):
        self.next_state = 'terminated'


class MockImage(object):
    def run(self, instance_type, key_name, security_groups):
        return _Keys(instances=[MockInstance('pending')])
