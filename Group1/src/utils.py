import sys
import lzma


def read_txt(filename):
    with open(filename, 'r') as file:
        text_unfiltered = file.read()
        text_letters = list(text_unfiltered)
        return text_letters


def read_xz(filename, limit=None):
    with lzma.open(filename, 'rt', encoding='utf-8') as file:
        text_unfiltered = file.read()
        if limit is not None:
            return list(text_unfiltered)[0:limit]
        text_letters = list(text_unfiltered)
        return text_letters


def read_text(address, text_limit=None):
    try:
        if address.endswith('xz'):
            return read_xz(filename=address, limit=text_limit)

        return read_txt(filename=address, limit=text_limit)
    except:
        print("Error: No such a file or directory. Could not open/read file:", address)
        sys.exit()
