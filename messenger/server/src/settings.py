import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_MODULES = (
    'auth',
    'echo',
    'security',
    'serverdate',
    'servererrors',
)

CONNECTION_STRING = 'sqlite:///default.db'
