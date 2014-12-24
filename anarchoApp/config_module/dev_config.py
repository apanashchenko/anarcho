import os

AUTO_RELOAD = True
DEBUG = True
PORT = 5000
PUBLIC_HOST = 'http://localhost:{0}'.format(PORT)
TMP_DIR = os.path.abspath('tmp')
LOGS_DIR = os.path.abspath('log')
SQLALCHEMY_DATABASE_URI = 'sqlite:///anarcho.db'

STORAGE_WORKER = {'type': 'local_storage',
                  'storage_dir': os.path.abspath('builds'),
                  'storage_host_name': 'http://localhost:5000'
}