import settings


DEFAULT_MESSAGE_PATTERN = b'%(nonce)s%(key)s%(tag)s%(data)s'

MESSAGE_PATTERN = getattr(settings, 'MESSAGE_PATTERN', DEFAULT_MESSAGE_PATTERN)
