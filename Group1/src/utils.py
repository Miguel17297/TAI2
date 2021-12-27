import sys
import lzma


def read_txt(filename, limit=None):
    with open(filename, 'r', encoding='utf-8') as file:
        text_unfiltered = file.read()
 
        if limit is not None:
            char_limit = int(len(text_unfiltered) * limit/100)
            return list(text_unfiltered)[0:char_limit]
        text_letters = list(text_unfiltered)
        return text_letters


def read_xz(filename, limit=None):
    with lzma.open(filename, 'rt', encoding='utf-8') as file:
        text_unfiltered = file.read()
        if limit is not None:
            upper = round(len(text_unfiltered) * limit)
            return list(text_unfiltered)[0:upper]
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
