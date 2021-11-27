from fcm import FCM
from utils import read_text
import argparse
import math

class Lang:

    def __init__(self, r, target, k, a):
        """
        """
        self._model = self.create_model(r, k, a)
        self.k = k
        self._target = target
        self._cardinality = len(set(target))

    def create_model(self, r, k, a):
        fcm = FCM(r, a, k)
        fcm.calculate_probabilities()

        return fcm.prob_dic

    def compute_compression(self):
        k = self.k
        t = self.target
        model = self.model

        prob = []  # probabilities

        for i in range(len(t) - k):

            next_context = t[i:i + k]

            next_symbol = t[i + k]
            if next_context in model and next_symbol in model[next_context]:  # if context exits
                prob.append(-math.log(model[next_context][next_symbol]))

            else:
                prob.append(-math.log((1 / self.cardinality)))

        return round(sum(prob), 2)

    @property
    def model(self):
        return self._model

    @property
    def target(self):
        return self._target

    @property
    def cardinality(self):
        return self._cardinality


def main():
    parser = argparse.ArgumentParser(description="Lang",
                                     usage="python3 lang.py -a <smoothing_parameter> -k <order_of_the_model> -r <path_of_the_reference> --target <target-text> ")

    parser.add_argument("-a", help="Smoothing parameter", type=float, required=True)
    parser.add_argument("-k", help="Model context size", type=int, required=True)
    parser.add_argument("-r", help="Reference Text", required=True)
    parser.add_argument("--target", help="Text under analysis", required=True)

    args = parser.parse_args()

    # t = "I went to our house in the country with my Family. It’s a small house in a village in the mountains."
    # t = "Estava uma noite muito escura e fria. Os candeeiros da rua projectavam grandes triângulos de luz mortiça. Tinha-se levantado uma neblina que dava a tudo um ar de mistério."

    # text = read_text("../example/por_PT.latn.Portugese.EP7.utf8.xz")
    l = Lang(read_text(args.r), args.target, args.k, args.a)
    print(l.compute_compression())


if __name__ == "__main__":
    main()
