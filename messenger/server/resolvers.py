from functools import reduce
from settings import INSTALLED_MODULES


def get_server_actions():
    modules = [__import__(f'{module}.actions') for module in INSTALLED_MODULES]
    submodules = [getattr(module, 'actions', []) for module in modules]
    actionnames = reduce(
        lambda result, submodule: result + getattr(submodule, 'actionnames', []),
        submodules, []
    )
    return {
        actionname.get('action'): actionname.get('controller') for actionname in actionnames
    }


def resolve(action_name, actions=None):
    actionnames = actions or get_server_actions()
    return actionnames.get(action_name)
