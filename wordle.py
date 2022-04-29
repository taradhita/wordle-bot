import numpy as np
from collections import Counter

class WordleSolver:
    def __init__(self) -> None:
        self.wrong_char = [] #wrong characters
        self.wrong_pos = {} #wrong position number as key, character as value (in list format)
        self.correct_char = {} #no. of correct position as key, character as value
        self.no_duplicates = [] #existing letters but not allowed to have frequency more than 1

    def load_wordlist(self):
        with open('wordlist-answer.txt') as fp:
            lines = [line.rstrip('\n') for line in fp]

        return lines

    def load_additional_wordlist(self):
        with open('wordlist-additional.txt') as fp:
            additional = [additional.rstrip('\n') for additional in fp]
        
        return additional
    
    def split_into_chars(self, lines):
        chars = np.array([list(char) for char in lines])
        return chars

    def count_word_score(self, chars):
        counter = {}
        for i in range(5):
            counter[i] = Counter(chars[:,i])
        score = [sum([counter[i].get(c[i], 0) for i in range(len(c)) if c[i] in counter[i].keys()]) for c in chars ]
        return score

    def sort_top_word_opening(self, lines, score):
        d = dict(zip(lines, score))
        return sorted(d.items(), key=lambda x: x[1], reverse=True)  

    def retrieve_answer(self, answer, evaluation):
        for i, (ans, eval) in enumerate(zip(list(answer), evaluation)):
            if eval == 2:
                self.correct_char[i] = ans
            elif eval == 1:
                self.wrong_pos[i] =[ans]
            elif eval == 0 and ans in self.correct_char.values() or ans in {x for v in self.wrong_pos.values() for x in v}:
                self.no_duplicates.append(ans)
            else:
                self.wrong_char.append(ans)
                self.wrong_char = list(set(self.wrong_char)) #eliminate duplicate list value
        return self

    def update_predict_list(self, chars):
        filter_wrong_chars = [c for c in chars if not any(i in self.wrong_char for i in c)] 
        filter_correct_chars = [c for c in filter_wrong_chars if not any((c[i] != self.correct_char[i] for i in range(len(c)) if i in self.correct_char.keys()))]
        filtered_words = [c for c in filter_correct_chars if not (any( i in self.wrong_pos.keys() and c[i] in self.wrong_pos[i] for i in range(len(c)) )) ]
        if (self.wrong_pos):
            filtered_words = [c for c in filtered_words if any(c[i] in {x for v in self.wrong_pos.values() for x in v} for i in range (len(c)))]
            filtered_words = [c for c in filtered_words if all(item in c for item in sum(self.wrong_pos.values(), []))]

        if (self.no_duplicates):
            filtered_words = [c for c in filtered_words if not any(Counter(c)[j] > 1 for j in self.no_duplicates)]

        return [''.join(c) for c in filtered_words]