import sys
import lzma


def read_txt(filename):
    with open(filename, 'r') as file:
        text_unfiltered = file.read()
        text_letters = list(text_unfiltered)
        return text_letters

def read_xz(filename):
    with lzma.open(filename, 'rt', encoding='utf-8') as file:
        text_unfiltered = file.read()
        text_letters = list(text_unfiltered)
        return text_letters

def read_text(address):
    try:
        if address.endswith('xz'):
            return read_xz(filename=address)

        return read_txt(filename=address)
    except:
        print("Error: No such a file or directory. Could not open/read file:", address)
        sys.exit()