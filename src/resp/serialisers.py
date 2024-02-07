def serialize_resp(value):
    if isinstance(value, str):
        if value == "":  # empty string
            return b"$0\r\n\r\n"
        else:
            return b'+' + value.encode('utf-8') + b'\r\n'
    elif isinstance(value, int):  # integer
        return b':' + str(value).encode('utf-8') + b'\r\n'
    elif value is None:  # null
        return b'$-1\r\n'
    elif isinstance(value, list):  # array
        array_content = b''.join(serialize_resp(item) for item in value)
        return b'*' + str(len(value)).encode('utf-8') + b'\r\n' + array_content
    else:
        raise TypeError('Value type not supported for serialization')

def deserialize_resp(data, offset=0):
    full_data = data[offset:]
    first_byte = full_data[0:1]
    
    if first_byte == b'+':  # simple String
        end = full_data.index(b'\r\n') + 2
        return full_data[1:end-2].decode('utf-8'), end
    elif first_byte == b'-':  # error
        end = full_data.index(b'\r\n') + 2
        return full_data[1:end-2].decode('utf-8'), end
    elif first_byte == b':':  # integer
        end = full_data.index(b'\r\n') + 2
        return int(full_data[1:end-2]), end
    elif first_byte == b'$':  # bulk String
        header_end = full_data.index(b'\r\n') + 2
        length = int(full_data[1:header_end-2])
        if length == -1:
            return None, header_end
        string_end = header_end + length + 2
        return full_data[header_end:string_end - 2].decode('utf-8'), string_end
    elif first_byte == b'*':  # array
        header_end = full_data.index(b'\r\n') + 2
        num_elements = int(full_data[1:header_end-2])
        elements = []
        total_length = header_end
        for _ in range(num_elements):
            element, element_length = deserialize_resp(full_data, total_length)
            elements.append(element)
            total_length += element_length
        return elements, total_length
    else:  # unsupported type
        raise ValueError('Unsupported RESP data type')
