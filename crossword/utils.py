from pycrossword import generate_crossword
from .models import Question, Answer
import random

def is_correct_answer(id_answer, answer_text):
    
    is_correct = Answer.check_answer(id_answer, answer_text)
    return is_correct
    

def generate_crossword_data(count_words):
    words = Answer.get_all_answers()
    placed_words = []

    if count_words is None:
        dimensions, placed_words = gen_random_crossword(words, 13)
    else:
        count_words = int(count_words)
        x = 13 if count_words == 10 else 10
        while len(placed_words) != count_words:
            dimensions, placed_words = gen_random_crossword(words, x)

    json_dict = { 
        'dimensions': {'cols':  dimensions[0], 'rows': dimensions[1]},
        'words': []
    }

    counter = 1
    for word in placed_words:
        question = Question.get_question_by_answer(word[0])
        start_x = word[2]
        start_y = word[1]
        orientation = 'Горизонтально' if word[3] else 'Вертикально'
        word_len = len(word[0])

        if orientation:
            end_x = start_x + word_len - 1
            end_y = start_y
        else:
            end_x = start_x
            end_y = start_y + word_len - 1

        word_info = {
            'id': counter,
            'word': word[0],
            'orientation': orientation,
            'start_col': start_x,
            'start_row': start_y,
            'end_col': end_x,
            'end_row': end_y,
            'question': question
        }
        
        counter += 1
        json_dict['words'].append(word_info)
    return json_dict


def gen_random_crossword(words, x):
    random_number = int(random.random() * 1000)
    dimensions, placed_words = generate_crossword(words.copy(), seed=random_number, x=x, y=x)

    return dimensions, placed_words
