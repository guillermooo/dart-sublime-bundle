"""Helpers related to text encoding.
"""


def utf8_to_text(data):
    """Decodes UTF-8-encoded @data bytes.
    """
    return data.decode('utf-8')


def text_to_utf8(text):
    """Encodes @text as UTF-8.
    """
    return text.encode('utf-8')
