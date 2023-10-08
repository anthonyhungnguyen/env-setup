def pre_spawn_hook(spawner):
    spawner.env["HADOOP_USER_NAME"] = spawner.user.name
    spawner.env["NB_USER"] = spawner.user.name
    spawner.env["GRANT_SUDO"] = "1"
    spawner.env["CHOWN_HOME"] = "1"
    spawner.env["CHOWN_HOME_OPTS"] = "-R"


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

c.JupyterHub.db_url = "mysql+pymysql://root:root@db:3306/jupyterhub"

# do not delete containers if hub restarts

c.JupyterHub.cleanup_servers = False

# volumes
NOTEBOOK_DIR = "/home/{username}"

c.DockerSpawner.notebook_dir = NOTEBOOK_DIR
c.CustomDockerSpawner.pre_spawn_hook = pre_spawn_hook

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"/home/{username}": NOTEBOOK_DIR}

# pick a docker image. This should have the same version of jupyterhub
# in it as our Hub.
c.DockerSpawner.image = "custom_image:latest"

c.DockerSpawner.use_internal_ip = True

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = "jupyterhub"

# delete containers when the stop
c.DockerSpawner.remove = True
