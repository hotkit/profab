from profab import _Keys


class MockInstance(object):
    def __init__(self, state, next_state='running',
            instance_type='t1.micro', image_id='ami-12345', cnx=None,
            groups=None):
        self.dns_name = 'ec2-host'
        self.groups = groups or [_Keys(name='default')]
        self.id = 'i-test1'
        self.ip_address = '10.56.32.4'
        self.image_id = image_id
        self.instance_type = instance_type
        self.key_name = 'host'
        self.placement = 'ec2-zone'
        self.state = state
        self.tags = {}

        if cnx:
            self.region = cnx.region

        self.__next_state = next_state


    def update(self):
        self.state = self.__next_state

    def start(self):
        self.__next_state = 'running'
    def stop(self):
        self.__next_state = 'stopped'
    def terminate(self):
        self.__next_state = 'terminated'


class MockImage(object):
    def __init__(self, cnx, name):
        self._cnx = cnx
        self.id = name

    def run(self, _count=1, max_count=1, key_name=None, security_groups=[],
            user_data=None, addressing_type=None, instance_type='m1.small',
            placement=None, kernel_id=None, ramdisk_id=None,
            monitoring_enabled=False, subnet_id=None, block_device_map=None,
            disable_api_termination=False,
            instance_initiated_shutdown_behavior=None,
            private_ip_address=None, placement_group=None,
            security_group_ids=None):
        return _Keys(id='r-reservation',
            connection=self._cnx,
            instances=[MockInstance('pending',
                instance_type=instance_type, image_id=self.id,
                groups=[_Keys(id=g, name=g) for g in security_groups],
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
