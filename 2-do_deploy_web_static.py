from fabric.api import env, run, put, sudo
from os.path import exists, isdir

env.hosts = ['18.204.20.1', '3.86.7.120']

def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_name = archive_path.split('/')[-1]
        archive_name_without_ext = archive_name.split('.')[0]
        release_path = f'/data/web_static/releases/{archive_name_without_ext}/'

        # Create the release path if it doesn't exist
        sudo('mkdir -p {}'.format(release_path))

        # Uncompress the archive to the release path
        sudo('tar -xzf /tmp/{} -C {}'.format(archive_name, release_path))

        # Delete the archive from the web server
        sudo('rm /tmp/{}'.format(archive_name))

        # Delete the symbolic link /data/web_static/current
        if isdir('/data/web_static/current'):
            sudo('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        sudo('ln -sf {} /data/web_static/current'.format(release_path))

        return True
    except:
        return False
