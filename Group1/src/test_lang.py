import random
from utils import read_text
from lang import Lang
import os

ROOT = '/'.join(os.getcwd().split("/")[:-1])
PATH = os.path.join(ROOT, 'results')

a = [0, 0.01, 0.1, 1]
context = [i for i in range(1, 6)]
refs = [os.path.join(ROOT, "refs", f) for f in os.listdir(os.path.join(ROOT, "refs"))]
ref_density = [0.25, 0.50, 0.75, 1]
targets = ["in the beginning god created the heaven and the earth.", "in the beginning god created",
           "Ao contrário da crença popular, o texto não é simplesmente texto aleatório."]


def k_variation(a, r, target, r_path):
    print(f"Reference Text (r): {r_path}")
    print(f"Smothing parameter(a): {a}")
    print(f"Target Text (target): {target}")

    print("\n{:<6s} | {:<6s}".format("K", "bits"))
    for k in context:
        lang = Lang(read_text(r), k, a)
        res = lang.compute_compression(target)
        print("{:<6d} | {:<6.2f}".format(k, res))


def smoth_variation(k, r, target, r_path):
    print(f"Reference Text (r): {r_path}")
    print(f"Context Size(k) : {k}")
    print(f"Target Text (target): {target}")

    print("\n {:<6s} | {:<6s}".format("a", "bits"))
    for v in a:
        lang = Lang(r, k, a)
        res = lang.compute_compression(target)
        print("{:<6d} | {:<6.2f}".format(a, res))


def ref_variation(a, k, target, r):
    print(f"Reference Text (r): {r}")
    print(f"Context Size(k) : {k}")
    print(f"Target Text (target): {target}")
    print("\n {:<6s} | {:<6s}".format("density", "bits"))
    for d in ref_density:
        lang = Lang(read_text(r[:round(len(r) * d)]), k, a)
        res = lang.compute_compression(target)
        print("{:<6d} | {:<6.2f}".format(d, res))


def test_lang():

    prev = 1

    print(f"===========================  Lang =========================== ")
    for ref in refs:
        print(f"Reference Text (r): {ref}")
        r = read_text(ref)
        for t in targets:
            print(f"Target Text (target): {t}")

            print("{:<6s} | {:<6s} | {:<8s} | {:<8s} | {:<8s}".format("K", "a", "ref_size(%)", "res", "ratio"))
            for k in context:
                for v in a:
                    for d in ref_density:
                        lang = Lang(r, k, v)
                        res = lang.compute_compression(t)
                        print("{:<6d} | {:<6s} | {:<11d} | {:<8.2f} | {:<8.2f}".format(k, str(v), int(d * 100), res, res / prev))
                        prev = res


if __name__ == '__main__':
    test_lang()
