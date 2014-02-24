__author__ = 'kobyn'


"""
Docker provisioner tasks.
"""

import time
from cloudify.decorators import operation
from cloudify.utils import get_local_ip
import docker
import socket

get_ip = get_local_ip

container_cmds = ['/bin/sh -c "while true; do echo hello world; sleep 1; done"', '/usr/bin/python -m SimpleHTTPServer',
                  '/usr/sbin/sshd -D']

RUNNING = 'running'



def validate_ip(ipadd):
    try:
        socket.inet_aton(ipadd)
    except socket.error:
        raise RuntimeError('Failed creating docker API connection. Bad docker address: {'
                           '}'.format(ipadd))



@operation
def create(ctx, **kwargs):
    print ctx.properties
    docker_url = "http://{}:5555".format(ctx['master_host_ip'])
    print docker_url
    # validate_ip(master_host_ip)
    c = docker.Client(base_url=docker_url, version='1.8')
    ctx.logger.info('Creating container with params: container_name={0},container_ip{1}'.format(ctx.node_name, ctx.node_id))
    inst_id = c.create_container(ctx['docker_config']['image'], command=container_cmds[2],
                   hostname=ctx['master_host_ip'], user='root',
                   detach=True, stdin_open=True, tty=True, mem_limit=0,
                   ports=None, environment=None, dns=None, volumes=None,
                   volumes_from=None, name=ctx['docker_config']['container_name'])
    ctx['container_id'] = inst_id
    ctx.update()


@operation
def start(ctx, **kwargs):
    docker_url = "http://{}:5555".format(ctx['master_host_ip'])
    # validate_ip(master_host_ip)
    c = docker.Client(base_url=docker_url, version='1.8')
    inst_id = ctx['container_id']
    ctx.logger.info('Starting container id:{0}'.format(inst_id))
    res = c.start(inst_id, publish_all_ports=True, port_bindings={})
    for atmpt in range(10):
        try:
            inst_inspect = c.inspect_container(inst_id)
            if inst_inspect:
                ctx.set_started()
                ctx.update()
                break
            else:
                time.sleep(1)
        except BaseException:
            raise RuntimeError("failed to start container")


@operation
def stop(ctx, **kwargs):
    docker_url = "http://{}:5555".format(ctx['master_host_ip'])
    # validate_ip(master_host_ip)
    c = docker.Client(base_url=docker_url, version='1.8')
    inst_id = ctx['container_id']
    ctx.logger.info('Stopping container id:{0}'.format(inst_id))
    res = c.stop(inst_id, timeout=10)



@operation
def delete(ctx, **kwargs):
    docker_url = "http://{}:5555".format(ctx['master_host_ip'])
    # validate_ip(master_host_ip)
    c = docker.Client(base_url=docker_url, version='1.8')
    inst_id = ctx['container_id']
    ctx.logger.info('Removing container id:{0}'.format(inst_id))
    res = c.remove_container(inst_id, v=False, link=False)
    ctx.set_stopped()
    ctx.update()

