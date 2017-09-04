from fabric.contrib.files import sed, append, exists
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/heron182/superlists_python_tdd'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'virtualenv', 'static', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % source_folder)
        current_commit = local('git log -n 1 --format=%H', capture=True)
        run('cd %s && git reset --hard %s' % (source_folder, current_commit))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))


def _update_virtualenv(site_folder):
    virtualenv_folder = '%s/virtualenv' % source_folder
    if not exists(virtualenv_folder + '/bin/pip'):
        run('cd %s && python3.6 -m venv virtualenv')
    run('cd %s/bin/pip install -r %s/source/requirements.txt' % (virtualenv_folder,
                                                                 site_folder))


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
