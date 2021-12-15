import argparse
import math
import os
from utils import read_text
from lang import Lang


def read_folder(folder_path):
    return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]


def read_target(target_path):
    with open(target_path, 'r') as file:
        return file.read()




class LocateLang:

    def __init__(self, lang_refs, a, k):
        self.lang_refs = lang_refs
        self.a = a
        self.k = k

    def locate(self, target, chunk_size):

        threshold = math.log(len(set(target)))/2
        chunks = [(i, target[i:i + chunk_size + 1]) for i in range(0, len(target), chunk_size)]
        models = [Lang(filename, self.k, self.a) for filename in self.lang_refs]
        results = {}
        current_value = 0
        initial_pos = 0
        current_file = ""
        prev_file = ""

        for segment in chunks:
            values = []
            for model in models:
                bits_needed = model.compression_locate(target, segment[1])
                values.append((model.r, bits_needed))

            # Guardar Valor mais recent e file mais recent

            if not current_file:

                prev_file = min(values, key=lambda x: x[1])[0]
                current_file = prev_file

            else:
                prev_file = current_file
                current_file = min(values, key=lambda x: x[1])[0]

            current_value = min(values, key=lambda x: x[1])[1]

            # Obter valor de I
            # Se valor atual for menor que o threshold guardar e se o ficheiro é diferente do analisado anteriormente 
            if current_file != prev_file and current_value < threshold:
                # Guardar valor dos dados- Onde começou a ler e o qual a lingua que será a anterior
                results[f"{initial_pos}_{segment[0]}"] = (current_value, prev_file)
                # Reiniciar posição Inicial
                initial_pos = segment[0]

        return results


def main():
    parser = argparse.ArgumentParser(description="Recognize a text's language",
                                     usage="python3 locatelang -threshold <max_value> -chunk_size <divide_text> -a <smoothing_parameter> -k <order_of_the_model> --folder_path path_to_folder --target path_to_target")

    parser.add_argument("-a", help="Smoothing parameter for each model", type=float, required=True)
    parser.add_argument("-k", help="Models context size", type=int, required=True)
    #parser.add_argument("-threshold", help="max_value", type=float, required=True)
    parser.add_argument("--folder_path", help="Path to folder with language references", type=str, required=True)
    parser.add_argument("--target", help="Path to target text to analyze", type=str, required=True)

    args = parser.parse_args()
    lang_refs = read_folder(args.folder_path)
    target = read_target(args.target)

    fl = LocateLang(lang_refs, args.a, args.k)

    print(f"For target text:{args.target} we got {fl.locate(target, args.k)}")


if __name__ == "__main__":
    main()
