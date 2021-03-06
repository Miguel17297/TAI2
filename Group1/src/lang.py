from fcm import FCM
from utils import read_text, read_target
import argparse
import math


class Lang:

    def __init__(self, r, k, a, target, text_limit=None, limit_type=None):

        self._r = r
        if limit_type is None:
            self._model = self.create_model(read_text(r, text_limit=text_limit), k, a)
        else:
            self._model = self.create_model(read_text(r), k, a)
        self._k = k
        if limit_type is None:
            self._target = read_target(target)
        else:
            self._target = read_target(target, text_limit=text_limit)
        self._cardinality = len(set(self._target))

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

    def compute_compression(self):
        s = self.compute_bits_list(self._target)
        return round(sum(s), 2)

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

    lang = Lang(args.r, args.k, args.a, target=args.target)
    bits = lang.compute_compression()
    print(f"Estimated number of bits required to compress {args.target}: {bits} bits")
    print(f"Average bits per character: {round(bits / len(read_target(args.target)), 2)} bits")


if __name__ == "__main__":
    main()