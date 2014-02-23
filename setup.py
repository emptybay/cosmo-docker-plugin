__author__ = 'kobyn'

import setuptools

COSMO_CELERY_VERSION = '0.3'
COSMO_CELERY_BRANCH = 'develop'
COSMO_CELERY = "https://github.com/CloudifySource/cosmo-celery-common/tarball/{0}".format(COSMO_CELERY_BRANCH)

setuptools.setup(
    zip_safe=True,
    name='cosmo-plugin-docker-provisioner',
    version='0.1',
    author='kobyn',
    author_email='kobyn@gigaspaces.com',
    packages=['docker_host_provisioner'],
    license='LICENSE',
    description='Plugin for provisioning docker containers',
    install_requires=[
        "bernhard",
        "docker-py>=0.2.3",
        "cosmo"
    ],
    dependency_links=["{0}#egg=cosmo-celery-common-{1}".format(COSMO_CELERY, COSMO_CELERY_VERSION)]
)
