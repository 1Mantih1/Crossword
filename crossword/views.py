from django.shortcuts import render
from django.http import JsonResponse
from .utils import generate_crossword_data, is_correct_answer

def get_data(request):
    if request.method == 'GET': #hey
        count_words = request.GET.get('count')
        json_dict = generate_crossword_data(count_words)
        return JsonResponse([json_dict], safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
def check_answer(request):
    if request.method == 'GET':
        id_value = request.GET.get('id')
        answer_value = request.GET.get('answer')
        json_correct = is_correct_answer(id_value, answer_value)
        return JsonResponse([json_correct], safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
