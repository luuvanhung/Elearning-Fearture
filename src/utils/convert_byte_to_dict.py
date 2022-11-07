import ast


def convert_bytes_to_dict(data_bytes: bytes) -> dict:
    data = data_bytes.decode("utf-8")
    return ast.literal_eval(data)
