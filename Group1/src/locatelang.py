import argparse
import os
from utils import read_text
from lang import Lang
from findlang import FindLang


def read_folder(folder_path):
    texts_read = {}
    for filename in os.listdir(folder_path):
        texts_read[filename] = read_text(os.path.join(folder_path,filename))
    return texts_read


def read_target(target_path):
    with open(target_path, 'r') as file:
        return file.read()


class LocateLang:
    def __init__(self, lang_refs, a, k,):
            self.fl=FindLang(lang_refs,a,k)

    def locate(self,target,chunk_size):
        #Depois alterar para adicionar (pos, testo)
        chunks=[target[i:i+chunk_size] for i in range(0, len(target), chunk_size)]
        results={}
        for segment in chunks:
            values = []
            for filename,ref in self.lang_refs.items():
                lang = Lang(ref, segment, self.k, self.a)
                bits_needed = lang.compute_compression()
                values.append((filename, bits_needed))
            results[segment]=min(values, key=lambda x: x[1])[0]
        return results

    



def main():
    parser = argparse.ArgumentParser(description="Recognize a text's language",
                                    usage="python3 locatelang -chunk_size <divide_text> -a <smoothing_parameter> -k <order_of_the_model> --folder_path path_to_folder --target path_to_target")

    parser.add_argument("-a", help="Smoothing parameter for each model", type=float, required=True)
    parser.add_argument("-k", help="Models context size", type=int, required=True)
    parser.add_argument("-chunk_size",help="Divide text", type=int, required=True)
    parser.add_argument("--folder_path", help="Path to folder with language references", type=str, required=True)
    parser.add_argument("--target", help="Path to target text to analyze", type=str, required=True)

    args = parser.parse_args()
    lang_refs = read_folder(args.folder_path)
    target = read_target(args.target)
    chunk_size=args.chunk_size
    fl = LocateLang(lang_refs,args.a,args.k)
    print(f"For target text:{args.target} we got {fl.locate(target,chunk_size)}")
if __name__ == "__main__":
    main()

