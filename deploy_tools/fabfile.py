from fabric.contrib.files import sed, append, exists
from fabric.api import env, local, run
import random
import string

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


def _update_settings(source_folder, site_name):
    settings_file = '%s/superlists/settings.py' % source_folder
    sed(settings_file, 'DEBUG = True', 'DEBUG = False')
    sed(settings_file, 'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % site_name)
    secret_key_file = '%s/superlists/secret_key.py' % source_folder
    if not exists(secret_key_file):
        secret = ''.join(random.SystemRandom().choice(string.ascii_letters)
                         for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "%s"' % secret)
    append(settings_file, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(site_folder):
    virtualenv_folder = '%s/virtualenv' % site_folder
    if not exists(virtualenv_folder + '/bin/pip'):
        run('cd %s && python3.6 -m venv virtualenv' % site_folder)
    run('%s/bin/pip install -r %s/source/requirements.txt' % (virtualenv_folder,
                                                                 site_folder))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3.6 '
        'manage.py collectstatic --noinput' % source_folder)


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3.6 '
        'manage.py migrate --noinput' % source_folder)


def deploy(sitename):
    site_folder = '/home/%s/sites/%s' % (env.user, sitename)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, sitename)
    _update_virtualenv(site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
