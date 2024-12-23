from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from asgiref.sync import sync_to_async
from .utils import generate_crossword_data, is_correct_answer, get_solution_data
from .models import Question, Answer, Solution
import json

passwd = "Terminator090123"

@require_http_methods(["GET"])
async def get_cross(request):
    count_words = request.GET.get('count')
    json_dict = await sync_to_async(generate_crossword_data)(count_words)
    return JsonResponse([json_dict], safe=False)

@require_http_methods(["GET"])
async def check_answer(request):
    id_value = request.GET.get('id')
    answer_value = request.GET.get('answer')
    json_correct = await sync_to_async(is_correct_answer)(id_value, answer_value)
    return JsonResponse(json_correct, safe=False)

@require_http_methods(["GET"])
async def check_login(request):
    password = request.GET.get('password')
    flag = password == passwd
    return JsonResponse(flag, safe=False)

@require_http_methods(["GET"])
async def get_data(request):
    password = request.GET.get('password')

    if password == 'null':
        return JsonResponse('', safe=False)

    if password == passwd:
        data = await sync_to_async(get_solution_data)()
        return JsonResponse(data, safe=False)

@csrf_exempt
async def add_solution(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_text = data.get('question')
            answer_text = data.get('answer')

            question, _ = await sync_to_async(Question.objects.get_or_create)(question=question_text)
            answer, _ = await sync_to_async(Answer.objects.get_or_create)(answer=answer_text)

            solution = Solution(id_question=question, id_answer=answer)
            await sync_to_async(solution.save)()

            return JsonResponse({'message': 'Solution added successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_solution(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            id_solution = data.get('id_solution')
            new_question_text = data.get('question')
            new_answer_text = data.get('answer')

            solution = Solution.objects.get(id_solution=id_solution)
            question = solution.id_question
            answer = solution.id_answer

            if new_question_text and question.question != new_question_text:
                question.question = new_question_text
                question.save()

            if new_answer_text and answer.answer != new_answer_text:
                answer.answer = new_answer_text
                answer.save()

            solution.save()

            return JsonResponse({'message': 'Solution updated successfully'}, status=200)

        except Solution.DoesNotExist:
            return JsonResponse({'error': 'Solution not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_solution(request):
    if request.method == 'DELETE':
        try:
            id_solution = request.GET.get('id_solution')

            solution = Solution.objects.get(id_solution=id_solution)

            question = solution.id_question
            answer = solution.id_answer

            question.delete()
            answer.delete()

            return JsonResponse({'message': 'Solution and related Question and Answer deleted successfully'}, status=200)

        except Solution.DoesNotExist:
            return JsonResponse({'error': 'Solution not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)