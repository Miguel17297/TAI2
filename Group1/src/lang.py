from fcm import FCM
from utils import read_text
import argparse
import math


class Lang:

    def __init__(self, r, k, a, target, text_limit=None):

        self._r = r
        self._model = self.create_model(read_text(r, text_limit=text_limit), k, a)
        self._k = k
        self._cardinality = len(set(target))

    def create_model(self, r, k, a):
        fcm = FCM(r, a, k)
        fcm.calculate_probabilities()

        return fcm.prob_dic

    def compute_bits_list(self, target):

        k = self.k
        model = self.model

        compress_bits = []  # probabilities

        for i in range(len(target) - k):

            next_context = target[i:i + k]

            next_symbol = target[i + k]
            if next_context in model and next_symbol in model[next_context]:  # if context exits
                compress_bits.append(-math.log2(model[next_context][next_symbol]))

            else:
                compress_bits.append(math.log2(self._cardinality))

        return compress_bits

    def compute_compression(self, target):

        return round(sum(self.compute_bits_list(target)), 2)

    @property
    def model(self):
        return self._model

    @property
    def r(self):
        return self._r

    @property
    def k(self):
        return self._k


def main():
    parser = argparse.ArgumentParser(description="Lang",
                                     usage="python3 lang.py -a <smoothing_parameter> -k <order_of_the_model> -r <path_of_the_reference> --target <target-text> ")

    parser.add_argument("-a", help="Smoothing parameter", type=float, required=True)
    parser.add_argument("-k", help="Model context size", type=int, required=True)
    parser.add_argument("-r", help="Reference Text", required=True)
    parser.add_argument("--target", help="Text under analysis", required=True)

    args = parser.parse_args()

    r = read_text(args.r)

    lang = Lang(r, args.k, args.a)
    print(lang.compute_compression(args.target))


if __name__ == "__main__":
    main()
