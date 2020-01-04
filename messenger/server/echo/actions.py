from .controllers import echo_controller, get_messages_controller

actionnames = [
    {
        'action': 'echo',
        'controller': echo_controller,
    },
    {
        'action': 'all_messages',
        'controller': get_messages_controller,
    },
]
