
def decode_and_clean(data_bytes, encoding='utf-8'):
    return clean(decode(data_bytes, encoding))


def decode(data_bytes, encoding='utf-8'):
    return data_bytes.decode(encoding)


def clean(text):
    return text.replace('\r', '')
