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

# ___________________________________________________________________________________________ #
def write_zeroes():
    with open("train_0.txt",'w') as fo:
        for i in range(91):
            fo.write("0 ")
        for i in range(9):
            fo.write(str(i+1) + " ")


def train_unigram():
    counts = defaultdict(int)
    context_counts = defaultdict(int)
    with open("train_0.txt") as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            words = line.split()


            for i in range(0, len(words)):
                counts[words[i]] += 1
    with open("model_file_0.txt",'w') as fo:
        for ngram, count in counts.items():
            fo.write(ngram + "\t" + "{}\n".format(counts[ngram]/100))

train_unigram()

def load_bigram_model():
    probs = {}
    with open("model_file_0.txt", 'r') as f:
        for line in f:
            line = line.strip()
            probs[line.split("\t")[0]] = float(line.split("\t")[1])
            pass
    return probs

load_bigram_model()

def test_zeroes(lambda1=0.95, N=1000000):
    P = 1
    W = 0

    probs = load_bigram_model()

    with open("test_0.txt",'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            words = line.split()

            for i in range(1, len(words)):
                P = P * 1/probs.get(words[i])
                W += 1
            P = pow(P, 1/float(W))
    print(P)

test_zeroes()

