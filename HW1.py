from collections import defaultdict


def bigram_add_one():
    counts = defaultdict(int)
    context_counts = defaultdict(int)
    with open("venv\Iamsam2.txt") as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            words = line.split()

            for i in range(0,len(words)):
                two_word_join = words[i] + " " + words[i-1]
                counts[two_word_join] += 1
                context_counts[words[i]] +=1
                pass

    for ngram, count in counts.items():
        print(ngram + "\t" + "{}".format((counts[ngram]+1)/(context_counts[ngram.split()[0]] + len(context_counts))))




def trigram_train():
    counts = defaultdict(int)
    context_counts = defaultdict(int)
    with open("venv\Iamsam.txt") as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            words = line.split()

            for i in range(2, len(words)):
                two_word_join = words[i - 2] + " " + words[i - 1]
                three_word_join = words[i - 2] + " " + words[i - 1] + " " + words[i]

                counts[three_word_join] += 1
                context_counts[two_word_join] += 1
                pass

    print(counts)
    print(context_counts)
    for ngram, count in counts.items():
        context = ngram.split()[0:2]
        print(ngram + "\t" + "{}".format(counts[ngram] / context_counts[" ".join(context)]) + "\n")


bigram_add_one()
