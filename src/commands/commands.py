import time

def current_millis():
    return int(round(time.time() * 1000))

def set_with_expiry(data_store, key, value, expiry=None):
    if expiry:
        expiry_millis = current_millis() + expiry
        data_store[key] = (value, expiry_millis)
    else:
        data_store[key] = (value, None)

def handle_ping(message):
    return 'PONG'

def handle_set(message, data_store):
    # parsing the command for expiry options
    args = message[1:]  # exclude the command itself
    if len(args) < 2:
        return "ERROR: SET command requires at least 2 arguments"
    
    key, value = args[0], args[1]
    expiry = None
    if 'EX' in args:
        expiry_index = args.index('EX') + 1
        if expiry_index < len(args):
            expiry = int(args[expiry_index]) * 1000  # convert seconds to milliseconds
    elif 'PX' in args:
        expiry_index = args.index('PX') + 1
        if expiry_index < len(args):
            expiry = int(args[expiry_index])  
    elif 'EXAT' in args:
        expiry_index = args.index('EXAT') + 1
        if expiry_index < len(args):
            expiry = (int(args[expiry_index]) - int(time.time())) * 1000
    elif 'PXAT' in args:
        expiry_index = args.index('PXAT') + 1
        if expiry_index < len(args):
            expiry = int(args[expiry_index]) - current_millis()

    set_with_expiry(data_store, key, value, expiry)
    return "OK"

def handle_get(message, data_store):
    if len(message) == 2:
        key = message[1]
        value, expiry = data_store.get(key, (None, None))
        if value is not None and (expiry is None or expiry > current_millis()):
            return value
        else:
            return "(nil)"
    return "ERROR: GET command requires exactly 1 argument"

def handle_echo(message):
    if len(message) > 1:
        return message[1]
    return "ERROR: ECHO command requires at least 1 argument"

def handle_default(message):
    return "ERROR: Unrecognized or improperly formatted command"