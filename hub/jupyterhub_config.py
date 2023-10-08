import os

# print(os.environ)

c = get_config()  # noqa

# dummy for testing. Don't use this in production!
c.JupyterHub.authenticator_class = "jupyterhub.auth.PAMAuthenticator"

# launch with docker
c.JupyterHub.spawner_class = "docker"

# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = "0.0.0.0"
# the hostname/ip that should be used to connect to the hub
# this is usually the hub container's name
c.JupyterHub.hub_connect_ip = "jupyterhub"

c.JupyterHub.db_url = "mysql+pymysql://root:root@db/jupyterhub"

# do not delete containers if hub restarts

c.JupyterHub.cleanup_servers = False

# volumes
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR") or "/home/jovyan/work"
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# pick a docker image. This should have the same version of jupyterhub
# in it as our Hub.
c.DockerSpawner.image = "custom_image:latest"

c.DockerSpawner.use_internal_ip = True

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = "jupyterhub"

# delete containers when the stop
c.DockerSpawner.remove = True
