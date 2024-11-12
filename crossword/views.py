from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils import generate_crossword_data, is_correct_answer, get_solution_data
from .models import Question, Answer, Solution
import json

@require_http_methods(["GET"])
def get_cross(request):
    count_words = request.GET.get('count')
    json_dict = generate_crossword_data(count_words)
    return JsonResponse([json_dict], safe=False)

@require_http_methods(["GET"])
def check_answer(request):
    id_value = request.GET.get('id')
    answer_value = request.GET.get('answer')
    json_correct = is_correct_answer(id_value, answer_value)
    return JsonResponse([json_correct], safe=False)

@require_http_methods(["GET"])
def get_data(request):
    return JsonResponse(get_solution_data(), safe=False)

@csrf_exempt
@require_http_methods(["PUT"])
def add_solution(request):
    try:
        data = json.loads(request.body)

        question_text = data.get("question")
        answer_text = data.get("answer")

        if not question_text or not answer_text:
            return JsonResponse({"error": "Both question and answer are required."}, status=400)

        question, created_question = Question.objects.get_or_create(question=question_text)
        answer, created_answer = Answer.objects.get_or_create(answer=answer_text)
        solution, created_solution = Solution.objects.get_or_create(id_question=question, id_answer=answer)

        return JsonResponse({
            "message": "Solution added successfully",
            "solution_id": solution.id_solution,
            "question_id": question.id_question,
            "answer_id": answer.id_answer
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
