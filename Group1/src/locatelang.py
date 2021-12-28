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
        text_target=read_target(target)
        results = {(i,i+k): {} for i in range(len(text_target)-k)}
        models = [Lang(filename, self.k, self.a, target) for filename in self.lang_refs]
        for model in models:
            bits = model.compute_bits_list(text_target)
            s_bits = self.suavization(bits, window_size)
            for i, b in enumerate(s_bits):
                results[(i,i+k)][model._r]=b
        for pos in results:
            if len([val for val  in results[pos].values() if val < threshold])==0:
                for lan in list(results[pos]):
                    if results[pos][lan] > min(results[pos].values()):
                            results[pos].pop(lan)
            else:
                for lan in list(results[pos]):
                    if results[pos][lan] > threshold:
                            results[pos].pop(lan)
    
        short_results={}
        positions={position[0] : position for position in list(results.keys())}
        initial_pos=positions[0]
        end_position=None
        for pos in list(positions):
            if pos!=list(positions)[-1]:
                if results[initial_pos].keys()==results[positions[pos+1]].keys():
                    end_position=positions[pos+1]
                elif results[initial_pos].keys()!=results[positions[pos+1]].keys() and end_position is not None:
                    short_results[(initial_pos[0],end_position[1])]=sorted(results[initial_pos], key=results[initial_pos].get)
                    initial_pos=positions[pos+1]
                    end_position=None
                elif end_position is None:
                    short_results[initial_pos]=sorted(results[initial_pos], key=results[initial_pos].get)
                    initial_pos=positions[pos+1]
            else:
                if results[initial_pos].keys()==results[positions[pos]].keys():
                    end_position=positions[pos]
                    short_results[(initial_pos[0],end_position[1])]=sorted(results[initial_pos], key=results[initial_pos].get)
                elif results[initial_pos].keys()!=results[positions[pos]].keys() and end_position is not None:
                    short_results[(initial_pos[0],end_position[1])]=sorted(results[initial_pos], key=results[initial_pos].get)
                    initial_pos=positions[pos]
                    end_position=None
        
        return short_results, results

    def suavization(self, bits_list, window_size):

        for i in range(len(bits_list) - window_size):
            bits_list[i] = sum(bits_list[i:i + window_size]) / window_size

        return bits_list


def main():
    parser = argparse.ArgumentParser(description="Recognize a text's language",
                                     usage="python3 locatelang -threshold <max_value> --window <window_size> -a <smoothing_parameter> -k <order_of_the_model> --folder_path path_to_folder --target path_to_target")

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
    print(f"Threshold: {threshold}")
    if not window_size:
        window_size = args.k
    print(f"Window Size: {window_size}")
    
    short_results, results =fl.locate(args.target, args.k, threshold, window_size)
    
    print(f"For target text:{args.target} we got:")
    print("Long Results:")
    for key in results:
        print(f"{key} - {results[key]}")
    print("-------------------------------------------")
    print("Short Results:")
    for key in short_results:
        print(f"{key} - {short_results[key]}")

if __name__ == "__main__":
    main()
