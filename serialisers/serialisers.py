def serialize_resp(data):
    if isinstance(data, int):
        return f":{data}\r\n"
    elif isinstance(data, str):
        # simple String or Error
        if data.startswith("+") or data.startswith("-"):
            return f"{data}\r\n"
        else:  # bulk String
            return f"${len(data)}\r\n{data}\r\n"
    elif data is None:
        return "$-1\r\n"
    elif isinstance(data, list):
        return f"*{len(data)}\r\n" + "".join([serialize_resp(item) for item in data])
    else:
        raise TypeError("Unsupported type for serialization")

def deserialize_resp(message):
    if message.startswith(":"):
        return int(message[1:-2])
    elif message.startswith("+") or message.startswith("-"):
        return message[1:-2]
    elif message.startswith("$"):
        length = int(message[1:message.index('\r')])
        if length == -1:
            return None
        return message[message.index('\n')+1:-2]
    elif message.startswith("*"):
        parts = message[2:].split("\r\n")
        array_length = int(parts[0])
        items = []
        i = 1
        while i < len(parts):
            if parts[i].startswith("$"):
                length = int(parts[i][1:])
                i += 1
                items.append(parts[i])
            i += 1
        return items
    else:
        raise ValueError("Invalid RESP message")
