from .controllers import (
    echo_controller, get_messages_controller,
    update_message_controller, delete_message_controller
)

actionnames = [
    {
        'action': 'echo',
        'controller': echo_controller,
    },
    {
        'action': 'messages',
        'controller': get_messages_controller,
    },
    {
        'action': 'upd_message',
        'controller': update_message_controller,
    },
    {
        'action': 'del_message',
        'controller': delete_message_controller,
    },
]
