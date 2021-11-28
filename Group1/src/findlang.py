import argparse
import os


def read_folder(folder_path):
    texts_read = {}
    for filename in os.listdir(folder_path):
        with open(filename, 'r') as file:
            texts_read[filename] = file.readlines()
    return texts_read


def read_target(target_path):
    with open(target_path, 'r') as file:
        return file.readlines()


# This is just a placeholder
class LangInterface():

    def estimate(self, ref, target):
        pass


class FindLang:
    def __init__(self, lang_refs):
        self.lang_refs = lang_refs

    def find(self, target):
        results = []
        for ref in self.lang_refs:
            lang = LangInterface()
            bits_needed = lang.estimate(ref, target)
            results.append((ref, bits_needed))
        return max(results, key=lambda x: x[1])[0]


parser = argparse.ArgumentParser(description="Recognize a text's language",
                                 usage="python3 findlang -folder_path path_to_folder -target path_to_target")

parser.add_argument("-folder_path", help="Path to folder with language references", type=str, required=True)
parser.add_argument("-path_to_folder", help="Path to target text to analyze", type=str, required=True)

args = parser.parse_args()
lang_refs = read_folder(args.folder_path)
target = read_target(args.path_to_folder)
fl = FindLang(lang_refs.values())
print(f"For target text:{args.path_to_folder} we got {lang_refs[fl.find(target)]}")
