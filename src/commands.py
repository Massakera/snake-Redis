def handle_ping(message):
    return 'PONG'

def handle_set(message, data_store):
    if len(message) == 3:
        key, value = message[1], message[2]
        data_store[key] = value
        return "OK"
    return "ERROR: SET command requires exactly 2 arguments"

def handle_get(message, data_store):
    if len(message) == 2:
        key = message[1]
        return data_store.get(key, "(nil)")
    return "ERROR: GET command requires exactly 1 argument"

def handle_echo(message):
    if len(message) > 1:
        return message[1]
    return "ERROR: ECHO command requires at least 1 argument"

def handle_default(message):
    return "ERROR: Unrecognized or improperly formatted command"