from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Submission

@login_required
def submit(request, course_id):
    questions = Question.objects.all()
    score = 0

    for question in questions:
        selected = request.POST.get(str(question.id))
        if selected:
            choice = get_object_or_404(Choice, id=selected)
            if choice.is_correct:
                score += question.grade

    submission = Submission.objects.create(
        exam=questions.first(),
        student=request.user,
        total_score=score
    )

    return render(request, "onlinecourse/exam_result_bootstrap.html",
                  {"submission": submission, "score": score})

@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission, id=submission_id, student=request.user
    )
    return render(request, "onlinecourse/exam_result_bootstrap.html",
                  {"submission": submission, "score": submission.total_score})
