from pycrossword import generate_crossword
import json
import os
from .models import Question, Answer
import random
import time

def is_correct_answer(id_answer, answer_text):
    
    is_correct = Answer.check_answer(id_answer, answer_text)
    return is_correct
    

def generate_crossword_data(count_words):
    words = Answer.get_all_answers()
    placed_words = []
    if count_words is None:
        dimensions, placed_words = gen_random_crossword(words)
    else:
        while len(placed_words) != int(count_words):
            dimensions, placed_words = gen_random_crossword(words)

    json_dict = { 
        'dimensions': {'cols':  dimensions[0], 'rows': dimensions[1]},
        'words': []
    }

    for word in placed_words:
        question = Question.get_question_by_answer(word[0])
        id_words = Answer.get_id_by_answer(word[0])
        start_x = word[2]
        start_y = word[1]
        orientation = 'horizontal' if word[3] else 'vertically'
        word_len = len(word[0])

        if orientation:
            end_x = start_x + word_len - 1
            end_y = start_y
        else:
            end_x = start_x
            end_y = start_y + word_len - 1

        word_info = {
            'id': id_words,
            'word': word[0],
            'orientation': orientation,
            'start_col': start_x,
            'start_row': start_y,
            'end_col': end_x,
            'end_row': end_y,
            'question': question
        }

        json_dict['words'].append(word_info)
    return json_dict

    # with open('data.json', 'w') as json_file:
    #     json.dump([json_dict], json_file)

def gen_random_crossword(words):
    random_number = int(random.random() * 1000) 
    dimensions, placed_words = generate_crossword(words.copy(), seed=random_number)

    return dimensions, placed_words