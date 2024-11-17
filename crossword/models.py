from django.db import models

class Question(models.Model):
    id_question = models.AutoField(primary_key=True)
    question = models.TextField()

    @staticmethod
    def get_question_by_answer(answer_text):
        questions = Question.objects.filter(
            solution__id_answer__answer=answer_text
        ).values('question')

        if questions.exists():
            return questions.first()['question']
        return None

    def __str__(self):
        return self.question

class Answer(models.Model):
    id_answer = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=255)

    @staticmethod
    def get_all_answers():
        try:
            answers = Answer.objects.all()
            words = [answer.answer for answer in answers]
            return words
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    @staticmethod
    def get_id_by_answer(answer_text):
        answer_id = Answer.objects.filter(answer=answer_text).values('id_answer')
        if answer_id.exists():
            return answer_id.first()['id_answer']
        return None
    
    @staticmethod
    def check_answer(answer_id, checked_answer):
        answer = Answer.objects.filter(id_answer=answer_id).values('answer')
        return answer.first()['answer'].lower() == checked_answer.lower()

    def __str__(self):
        return self.answer

class Solution(models.Model):
    id_solution = models.AutoField(primary_key=True)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    @staticmethod
    def get_all_solutions():
        solutions = Solution.objects.select_related('id_question', 'id_answer').values(
            'id_solution',
            'id_question__question',
            'id_answer__answer'
        )
        return list(solutions)

    def __str__(self):
        return f"Solution {self.id_solution}"
