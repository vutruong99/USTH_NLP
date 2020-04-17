from collections import defaultdict


def trainNaiveBayesClassifier():
    c = ()
    countclass = defaultdict(int)
    classdocs = defaultdict(int)
    words = []
    distinctwords = []
    with open("./genre.txt") as f:
        for line in f:
            n=0
            strline = line.replace(',','')
            countclass[strline.split()[-1]] += 1


            n = len(strline.split())-1

            classdocs[strline.split()[-1]] += n
            words = strline.split()
            for word in words:

                if word not in distinctwords:
                    distinctwords.append(word)
    print(distinctwords)

    pofaction = countclass.get("action")/len(countclass)
    pofcomedy = countclass.get("comedy")/len(countclass)

    # count = defaultdict(int)
    # for word in distinctwords:
    #     count[]
    # prob = defaultdict(float)
    # print(words)
    # for key in countclass.items():
    #     Ndoc = len(distinctwords)
    #     Nc = len(classdocs)
    #
    #     logsprior[key] = Math.log(Nc/Ndoc)
    #     v = distinctwords
    #
    #     for d in distinctwords
    #
    #     for doc in D.split(", "):
    #         if doc
    #     for word in D.split(", "):
    #         prob[word + key] =



trainNaiveBayesClassifier()