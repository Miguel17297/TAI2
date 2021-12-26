import argparse
import math
import os
from utils import read_text
from lang import Lang


def read_folder(folder_path):
    return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]


def read_target(target_path):
    with open(target_path, 'r',encoding='utf-8') as file:
        return file.read()


class LocateLang:

    def __init__(self, lang_refs, a, k):
        self.lang_refs = lang_refs
        self.a = a
        self.k = k

    def locate(self, target, k, threshold, window_size):

        models = [Lang(filename, self.k, self.a, target) for filename in self.lang_refs]
        results = {}
        text_target=read_target(target)
        for model in models:
            bits = model.compute_bits_list(text_target)
            s_bits = self.suavization(bits, window_size)

            initial_pos = None
            for i, b in enumerate(s_bits):

                if b < threshold and not initial_pos:
                    initial_pos = i

                if initial_pos and b > threshold:
                    results.setdefault(model.r, []).append((initial_pos, i + k))
                    initial_pos = None

        return results

    def suavization(self, bits_list, window_size):

        for i in range(len(bits_list) - window_size):
            bits_list[i] = sum(bits_list[i:i + window_size]) / window_size

        return bits_list


def main():
    parser = argparse.ArgumentParser(description="Recognize a text's language",
                                     usage="python3 locatelang -threshold <max_value> -chunk_size <divide_text> -a <smoothing_parameter> -k <order_of_the_model> --folder_path path_to_folder --target path_to_target")

    parser.add_argument("-a", help="Smoothing parameter for each model", type=float, required=True)
    parser.add_argument("-k", help="Models context size", type=int, required=True)
    parser.add_argument("-threshold", help="max_value", type=float)
    parser.add_argument("--folder_path", help="Path to folder with language references", type=str, required=True)
    parser.add_argument("--target", help="Path to target text to analyze", type=str, required=True)
    parser.add_argument("--window", help="Slinding Window Size", type=int)
    args = parser.parse_args()
    lang_refs = read_folder(args.folder_path)
    target = read_target(args.target)

    fl = LocateLang(lang_refs, args.a, args.k)

    threshold = args.threshold
    window_size = args.window

    if not threshold:
        threshold = math.log2(len(set(target))) / 2

    if not window_size:
        window_size = args.k

    print(f"For target text:{args.target} we got {fl.locate(args.target, args.k, threshold, window_size)}")


if __name__ == "__main__":
    main()
