import argparse
import os
from utils import read_text
from lang import Lang


def read_folder(folder_path):
    texts_read = {}
    for filename in os.listdir(folder_path):
        texts_read[filename] = folder_path + "/" + filename
    return texts_read


class FindLang:
    def __init__(self, lang_refs, a, k):
        self.lang_refs = lang_refs
        self.a = a
        self.k = k

    def find(self, target, limit=None, limit_type=None):
        results = []
        for filename, ref in self.lang_refs.items():
            lang = Lang(ref, self.k, self.a, target=target, text_limit=limit, limit_type=limit_type)
            bits_needed = lang.compute_compression()
            results.append((filename, bits_needed))
            # print(f'Model processed {filename} - {bits_needed}')
        return min(results, key=lambda x: x[1])[0]


def main():
    parser = argparse.ArgumentParser(description="Recognize a text's language",
                                     usage="python3 findlang --folder_path path_to_folder --target path_to_target")

    parser.add_argument("-a", help="Smoothing parameter for each model", type=float, required=True)
    parser.add_argument("-k", help="Models context size", type=int, required=True)
    parser.add_argument("--folder_path", help="Path to folder with language references", type=str, required=True)
    parser.add_argument("--target", help="Path to target text to analyze", type=str, required=True)

    args = parser.parse_args()
    lang_refs = read_folder(args.folder_path)
    target = args.target
    fl = FindLang(lang_refs, args.a, args.k)
    print(f"For target text:{args.target} we got {fl.find(target)}")


if __name__ == "__main__":
    main()
