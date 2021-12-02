import argparse
import os
from utils import read_text
from lang import Lang


def read_folder(folder_path):
    texts_read = {}
    for filename in os.listdir(folder_path):
        texts_read[filename] = read_text(os.path.join(folder_path,filename))
    return texts_read


def read_target(target_path):
    with open(target_path, 'r') as file:
        return file.read()


class LocateLang:

    def locate(self,target,chunk_size,threshold):
        chunks=[(i,target[i:i+chunk_size]) for i in range(0, len(target), chunk_size)]
        results={}
        current_value=0
        initial_pos=0
        current_file=""
        for segment in chunks:
            values = []
            for filename,ref in self.lang_refs.items():
                lang = Lang(ref, segment[1], self.k, self.a)
                bits_needed = lang.compute_compression()
                values.append((filename, bits_needed)) 
            #Obter valor de I     
            #Se valor de I menor que o threshold guardar e se o ficheiro é diferent do anterior e passar a considerar outra lingua 
            if min(values, key=lambda x: x[1]) < threshold and current_file!=min(values, key=lambda x: x[1])[0]:
                #Guardar valor 
                results[f"{initial_pos}_{segment[0]}"]=current_value
                #Reiniciar posição Inicial 
                initial_pos=segment[0]
            
            #Guardar Valor mais recent e file mais recent
            current_value=min(values, key=lambda x: x[1])
            current_file=min(values, key=lambda x: x[1])[0]
        
        return results

    



def main():
    parser = argparse.ArgumentParser(description="Recognize a text's language",
                                    usage="python3 locatelang -threshold <max_value> -chunk_size <divide_text> -a <smoothing_parameter> -k <order_of_the_model> --folder_path path_to_folder --target path_to_target")

    parser.add_argument("-a", help="Smoothing parameter for each model", type=float, required=True)
    parser.add_argument("-k", help="Models context size", type=int, required=True)
    parser.add_argument("-chunk_size",help="Divide text", type=int, required=True)
    parser.add_argument("-threshold",help="max_value",type=float, required=True)
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

