# python functions to declare helper functions.


def convert_json_serialisable(data):
    """
    takes sql executed query as output and returns json data.
    """
    def check_for_bytearr(data):
        for k,v in data.items():
            if isinstance(v,bytearray) or v == b'':
                data[k] = v.decode()
        return data
    if isinstance(data, list):
        return [check_for_bytearr(each) for each in data]
    elif isinstance(data, dict):
        return check_for_bytearr(data)
    else:
        return data
