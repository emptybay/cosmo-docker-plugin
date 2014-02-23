

import random
from cloudify.mocks import MockCloudifyContext
import docker_host_provisioner
import time


rand_id = 'docker_demo_' + str(random.randint(1, 10000))
ctx = MockCloudifyContext(
    node_id='cfy_id555_' + str(rand_id),
    properties={'docker_config': {'image': 'sullof/sshd', 'container_name': rand_id, 'master_host_ip': '15.185.89.106', 'hostname': rand_id}}

)
plugin_instance = docker_host_provisioner
plugin_instance.create(ctx)
plugin_instance.start(ctx)
time.sleep(10000)
plugin_instance.stop(ctx)
plugin_instance.delete(ctx)


 # properties={'docker_config': {'image': 'ubuntu', 'container_name': 'docker_demo1', 'master_host_ip': '15.185.127.88'}}

