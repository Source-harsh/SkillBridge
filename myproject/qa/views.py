# qa/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Reply
from .forms import QuestionForm, ReplyForm

# View to display all questions
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')  # Show most recent first
    return render(request, 'qa/question_list.html', {'questions': questions})

# View to ask a new question
 # Ensure only logged-in users can ask questions
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Set the user who asked the question
            question.save()
            return redirect('question_list')  # Redirect to the list of questions
    else:
        form = QuestionForm()
    return render(request, 'qa/ask_question.html', {'form': form})

# View to reply to a question
# Ensure only logged-in users can reply
def reply_to_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user  # Set the user who is replying
            reply.question = question  # Associate the reply with the specific question
            reply.save()
            return redirect('question_detail', question_id=question.id)  # Redirect to the question detail page
    else:
        form = ReplyForm()
    return render(request, 'qa/reply_to_question.html', {'form': form, 'question': question})

# View to show question details and replies
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    replies = question.replies.all()  # Get all replies related to this question
    return render(request, 'qa/question_detail.html', {'question': question, 'replies': replies})
