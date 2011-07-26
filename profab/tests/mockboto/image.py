from profab import _Keys


class MockInstance(object):
    def __init__(self, state, next_state = 'running'):
        self.dns_name = 'ec2-host'
        self.groups = [_Keys(name='default')]
        self.id = 'i-test1'
        self.ip_address = '10.56.32.4'
        self.key_name = 'host'
        self.placement = 'ec2-zone'
        self.state = state
        self.tags = {}

        self.__next_state = next_state


    def update(self):
        self.state = self.__next_state

    def terminate(self):
        self.__next_state = 'terminated'


class MockImage(object):
    def run(self, instance_type, key_name, security_groups):
        return _Keys(instances=[MockInstance('pending')])


class MockVolume(object):
    def __init__(self):
        self.id = 'v-test1'
        self.attach_data = _Keys(instance_id='i-test1',
            device='/dev/sda1', status='attached')


    def attach(self, instance_id, device):
        print "Attaching", instance_id, device
        self.intance_id = instance_id
        return True
