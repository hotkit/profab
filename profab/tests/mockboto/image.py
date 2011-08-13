from profab import _Keys


class MockInstance(object):
    def __init__(self, state, next_state='running',
            image_id='ami-12345', cnx=None):
        self.dns_name = 'ec2-host'
        self.groups = [_Keys(name='default')]
        self.id = 'i-test1'
        self.ip_address = '10.56.32.4'
        self.image_id = image_id
        self.key_name = 'host'
        self.placement = 'ec2-zone'
        self.state = state
        self.tags = {}

        if cnx:
            self.region = cnx.region

        self.__next_state = next_state


    def update(self):
        self.state = self.__next_state

    def terminate(self):
        self.__next_state = 'terminated'


class MockImage(object):
    def __init__(self, cnx, name):
        self._cnx = cnx
        self.id = name
    def run(self, instance_type, key_name, security_groups):
        return _Keys(instances=[MockInstance('pending', image_id=self.id,
            cnx=self._cnx)])


class MockVolume(object):
    def __init__(self):
        self.id = 'v-test1'
        self.attach_data = _Keys(instance_id='i-test1',
            device='/dev/sda1', status='attached')


    def attach(self, instance_id, device):
        print "Attaching", instance_id, device
        self.intance_id = instance_id
        return True
