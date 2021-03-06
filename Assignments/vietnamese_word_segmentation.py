# -*- coding: utf-8 -*-
"""Vietnamese Word Segmentation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WPJoJeJyCZMBjetavpb4vt43rTJU-Zl5

#Trương Sĩ Thi Vũ
#USTHBI8-189
A part of this assignment is referenced from https://colab.research.google.com/drive/1FHn5GyqjO4nmE9Othcm1oJKOmIANecUY?fbclid=IwAR1BiC4zXJ7piEFVn2Tjza-k2vdOEEP08tnxza_SczISa2mR5PhSYj9nJ1k#scrollTo=QY4nkbfyjNMp

# Programming Assignment 4: Vietnamese Word Segmentation

In this assignment, you will need to build a model for Vietnamese Word Segmentation. 

**Rules**:

- You are freely to choose the approach, however, you are required to implement the model by yourself in the Google Colab. 
- **It is not allowed to use available Vietnamese Word Segmentation toolkits to do the assignment.**

**Due date: April 10, 2020 (Friday)**

## Vietnamese Word Segmentation

In Vietnamese, one word may contain multiple syllables (e.g., 'học sinh'). Since there is not delimiter between words, in some applications, we may need to do word segmentation in the preprocessing step.

The input of a Vietnamese Word Segmentation model is a sequence of syllables.
(Note that, you may need to separate punctuations from words in the real scenerio). The output is a word-segmented text.

Example:

- Input: Nam hồn nhiên : " Tụi tôi xài tiền ngân hàng không à " .
- Output: Nam hồn_nhiên : " Tụi tôi xài tiền ngân_hàng không à " .

Similar as named-entity recognition, we can formalize the word segmentation task as a sequence labeling task with BI encoding scheme. We will predict if the tag of a syllable is B-W (begin of a word) or I-W (inside of a word). Tags for the sequence in the above example will be.

```
Nam	B-W
hồn	B-W
nhiên	I-W
:	B-W
"	B-W
Tụi	B-W
tôi	B-W
xài	B-W
tiền	B-W
ngân	B-W
hàng	I-W
không	B-W
à	B-W
"	B-W
.	B-W
```

We can choose Hidden Markov Models, Maximum Entropy Markov Models, or Conditional Random Fields to solve the problem. Please refer to previous lectures and assignments for details about those models.

## Dataset

You will use the training data in the file [train.txt](https://www.dl.dropboxusercontent.com/s/reor8jnqedk7svt/train.txt) to train your Vietnamese Word Segmentation Model and evaluate the model on the test data in the file [test.txt](https://www.dl.dropboxusercontent.com/s/zp635cd1zhofm62/test.txt) derived from VLSP 2013 Word Segmentation dataset.

You can download the file using wget command.
"""

!rm -f train.txt
!wget https://www.dl.dropboxusercontent.com/s/reor8jnqedk7svt/train.txt

"""The training data contains 20000 sentences (sentences are separated by a blank line), and the test data contains 2000 sentences."""

!head -3 train.txt

tagset = set()
with open('train.txt') as f:
    for line in f:
        if line.strip():
            wordtags = line.split()
            tag = wordtags[-1]
            tagset.add(tag)
print(tagset)

def load_data(input_file):    
    data = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            wordtags = line.split()
            if len(wordtags) == 1:
                continue
            data.append((wordtags[0], wordtags[1]))
    return data

train_data = load_data('./train.txt')

train_data

#Copied from professor Minh's code
def feature_func(word, previous_tag):
    
    feat_vec = {}

    # Indicator (boolean) features
    # Nguyễn Văn A
    if word[0].isupper():
        feat_vec['is_first_capital'] = 1
    # IBM
    if int(word.upper() == word):
        feat_vec['is_all_caps'] = 1
    if word.lower() == word:
        feat_vec['is_all_lower'] = 1
    if '-' in word:
        feat_vec['has_hyphen'] = 1
    # 1, 2, 345
    if word.isdigit():
        feat_vec['is_numeric'] = 1
    # aBC
    if word[1:].lower() != word[1:]:
        feat_vec['capitals_inside'] = 1

    # Lexical features
    feat_vec['word'] = word
    feat_vec['word.lower()'] = word.lower()
    feat_vec['prefix_1'] = word[0]
    feat_vec['prefix_2'] = word[:2]
    feat_vec['prefix_3'] = word[:3]
    feat_vec['prefix_4'] = word[:4]
    feat_vec['suffix_1'] = word[-1]
    feat_vec['suffix_2'] = word[-2:]
    feat_vec['suffix_3'] = word[-3:]
    feat_vec['suffix_4'] = word[-4:]

    # Tag feature
    feat_vec['previous_tag'] = previous_tag

    return feat_vec

training_instances = []
training_labels = []
i = 0
for (word, tag) in train_data:
    if i == 0:
        previous_tag = '<bos>'
    else:
        previous_tag = train_data[i-1][1]
    training_instances.append((word, previous_tag))
    training_labels.append(tag)
    i += 1

list(zip(training_instances[:10], training_labels[:10]))

feature_func('cá', 'B-W')

train_feat_vecs = [feature_func(word, tag) for word, tag in training_instances]

from sklearn.feature_extraction import DictVectorizer

vectorizer = DictVectorizer()
X_train = vectorizer.fit_transform(train_feat_vecs)
X_train.shape

from sklearn.linear_model import LogisticRegression

maxent = LogisticRegression(max_iter=500)
maxent.fit(X_train, training_labels)

target_classes = maxent.classes_.tolist()
label2id = {k: v for v, k in enumerate(target_classes)}
print(label2id)

maxent.predict(vectorizer.transform([feature_func('sinh', 'B-W')]))

import numpy as np

np.argmax(maxent.predict_proba(vectorizer.transform([feature_func('học', 'B-W')])))

"""##Algorithm based on viterbi"""

def get_negative_log_proba(word, previous_tag):
    prob = maxent.predict_log_proba(vectorizer.transform([feature_func(word, previous_tag)]))
    return -prob[0]

def decode(words):
    """Get the tag sequence for a word sequence
    """
    l = len(words)
    best_score = {}
    best_edge = {}
    best_score[('0 <bos>')] = 0 
    best_edge[('0 <bos>')] = None

    # Forward Step
    w1 = words[0]
    neg_log_proba1 = get_negative_log_proba(w1, '<bos>')
    for tag in target_classes:
        idx = label2id[tag]
        best_score[str(1) + ' ' + tag] = neg_log_proba1[idx]
        best_edge[str(1) + ' ' + tag] = '0 <bos>'
    
    for i in range(1, l):
        w = words[i]
        for prev_tag in target_classes:
            neg_log_proba = get_negative_log_proba(w, prev_tag)
            for next_tag in target_classes: 
                idx = label2id[next_tag]
                if str(i) + ' ' + prev_tag in best_score:
                    score = best_score[str(i) + ' ' + prev_tag] + neg_log_proba[idx]

                    if str(i + 1) + " " + next_tag not in best_score or best_score[str(i + 1) + " " + next_tag] > score:
                        best_score[str(i + 1) + " " + next_tag] = score
                        best_edge[str(i + 1) + " " + next_tag] = str(i) + " " + prev_tag
    
    for prev in target_classes:
        if str(l) + ' ' + prev in best_score:
            score = best_score[str(l) + ' ' + prev]
            if str(l+1) + ' ' + '<eos>' not in best_score or best_score[str(l+1) + ' <eos>'] > score:
                best_score[str(l+1) + ' <eos>'] = score
                best_edge[str(l+1) + ' <eos>'] = str(l) + ' ' + prev
    
    # Backward Step
    tags = []
    next_edge = best_edge[str(l + 1) + " " + "<eos>"]
    while next_edge != "0 <bos>":
        position, tag= next_edge.split()
        tags.append(tag)
        next_edge = best_edge[next_edge]
    tags.reverse()
    return tags

print(viterbi('Tôi là giảng viên đại học'.split(' ')))
print(viterbi(['Học', 'sinh', 'học', '.']))

"""## Evaluation Measures

- P(recision): (number of words correctly segmented)/(number of words in the system output)
- R(ecall): (number of words correctly segmented)/(number of words in the reference corpus)
- F1 measure = 2*P*R/(P+R)

### Evaluation code

You will use the following code for your evaluation. The input of the function is two files:

- test_file is the file with gold word segmentation.
- output_file is the the output file which is generated by your system. output_file and test_file have the same format.

The function will return precision, recall, and f1 score.

We will use the package [seqeval](https://github.com/chakki-works/seqeval) for evaluation.
"""

!pip install seqeval[cpu]

"""Let's run the evaluate the model on two sample files:

- [answer.txt](https://www.dl.dropboxusercontent.com/s/uhzyv8ofrsoxepo/answer.txt)
- [output.txt](https://www.dl.dropboxusercontent.com/s/7g6w12i59srqqw4/output.txt)

The content of answer.txt and output.txt are as follows.

answer.txt

```
Tôi	B-W
là	B-W
sinh	B-W
viên	I-W
.	B-W

Tôi	B-W
là	B-W
giảng	B-W
viên	I-W
đại	B-W
học	I-W
.	B-W
```

output.txt
```
Tôi	B-W
là	B-W
sinh	B-W
viên	B-W
.	B-W

Tôi	B-W
là	B-W
giảng	B-W
viên	B-W
đại	B-W
học	I-W
.	B-W
```

#EVALUATION

##I created my own answer test because I don't know what to do with the extra line
"""

words = ('Tôi là sinh viên . Tôi là giảng viên đại học .'.split())
tags = ('B-W B-W B-W I-W B-W B-W B-W B-W I-W B-W I-W B-W'.split())

with open('answer.txt', 'w') as fo:
    for i in range(len(words)):
        fo.write("{} {}\n".format(words[i], tags[i]))

!cat answer.txt

test = ('Tôi là sinh viên . Tôi là giảng viên đại học .'.split())

with open('output.txt', 'w') as fo:
    tag = decode(test)
    for i in range(len(test)):
        fo.write("{} {}\n".format(test[i], tag[i]))

!cat output.txt

from seqeval.metrics import precision_score, recall_score, f1_score

def get_tags(filepath):
    res = []
    with open(filepath, 'r') as f:
        cur_sen = []
        for line in f:
            line = line.strip()
            if line == '':
                if len(cur_sen) != 0:
                    res.append(cur_sen)
                    cur_sen = []
            else:
                word, tag = line.split()
                cur_sen.append(tag)
    if len(cur_sen) != 0:
        res.append(cur_sen)
    return res

def evaluate(test_file, output_file):
    y_true = get_tags(test_file)
    y_pred = get_tags(output_file)

    p = precision_score(y_true, y_pred)
    r = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return p, r, f1

evaluate('./answer.txt', './output.txt')

"""## References

- Huyen, N. T. M., Roussanaly, A., & Vinh, H. T. (2008, March). A hybrid approach to word segmentation of Vietnamese texts. In International Conference on Language and Automata Theory and Applications (pp. 240-249). Springer, Berlin, Heidelberg.
- Nguyen, T. P., & Le, A. C. (2016, November). [A hybrid approach to Vietnamese word segmentation](https://www.researchgate.net/profile/Tuan_Phong_Nguyen/publication/311980397_A_hybrid_approach_to_Vietnamese_word_segmentation/links/5a9507e3a6fdccecff0771ff/A-hybrid-approach-to-Vietnamese-word-segmentation.pdf). In 2016 IEEE RIVF International Conference on Computing & Communication Technologies, Research, Innovation, and Vision for the Future (RIVF) (pp. 114-119). IEEE.
- Nguyen, D. Q., Nguyen, D. Q., Vu, T., Dras, M., & Johnson, M. (2017). [A fast and accurate vietnamese word segmenter](https://arxiv.org/abs/1709.06307). arXiv preprint arXiv:1709.06307.
- [seqeval](https://github.com/chakki-works/seqevalhttps://github.com/chakki-works/seqeval) for sequence labeling evaluation.
"""