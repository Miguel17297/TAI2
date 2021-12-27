from findlang import FindLang, read_folder
import os
import matplotlib.pyplot as plt

a = 1
k = 3
target = "../example/example.txt"
lang_refs = read_folder("../refs")
i = 10
right = 0
wrong = 0
max = 100
dataset = []

def test_3_3_2(i):
    while i <= max:
        right = 0
        wrong = 0
        for lang in ["Czech", "Danish", "German", "English", "Spanish", "French", "Hungarian", "Italian", "Portuguese",
                     "Romanian", "Lithuanian", "Estonian"]:
            target = "../example/example_" + lang.lower() + ".txt"
            fl = FindLang(lang_refs, a, k)
            result = fl.find(target, limit=i, limit_type='target')
            we_want = result.lower().split(".")[0].split("_")[1]
            if lang.lower() == we_want:
                right += 1
            else:
                wrong += 1
            print(result)
            print(
                f"% of text {i} wanted {lang} but got {we_want}: {right} well out of {right + wrong} Acc: {right / (right + wrong) * 100}")
        dataset.append((i, (right / (right + wrong) * 100)))
        i += 10

    x = [x for x, y in dataset]
    y = [y for p, y in dataset]
    plt.plot(x, y)
    plt.xlabel('Target Length (%)')
    plt.ylabel('Accuracy(%)')
    plt.show()

def test_3_3_1(i):
    while i <= max:
        right = 0
        wrong = 0
        for lang in ["Czech", "Danish", "German", "English", "Spanish", "French", "Hungarian", "Italian", "Portuguese",
                     "Romanian", "Lithuanian", "Estonian"]:
            target = "../example/example_" + lang.lower() + ".txt"
            fl = FindLang(lang_refs, a, k)
            result = fl.find(target, limit=i)
            we_want = result.lower().split(".")[0].split("_")[1]
            if lang.lower() == we_want:
                right += 1
            else:
                wrong += 1
            print(result)
            print(
                f"% of text {i} wanted {lang} but got {we_want}: {right} well out of {right + wrong} Acc: {right / (right + wrong) * 100}")
        dataset.append((i, (right / (right + wrong) * 100)))
        i += 10

    x = [x for x, y in dataset]
    y = [y for p, y in dataset]
    plt.plot(x, y)
    plt.xlabel('Reference Length (%)')
    plt.ylabel('Accuracy(%)')
    plt.show()


#test_3_3_1(i)

test_3_3_2(i)
