from fabric.api import local


def server():
    local('python server -c config.yml')


def migrate():
    local('python server -m')


def client():
    local(f'python client -c config.yml')


def test():
    local('pytest --cov-report term-missing --cov server')


def notebook():
    local('jupyter notebook')


def kill():
    local('lsof -t -i tcp:8000 | xargs kill')
