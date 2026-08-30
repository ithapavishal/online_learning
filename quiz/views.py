from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from .models import *
from .forms import QuestionForm, OptionFormSet, AnswerForm, QuizForm
from online_learning_app.models import Course
# quiz


def create_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect('course_details', id=course_id)
    else:
        form = QuizForm()

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'quiz/create_quiz.html', context=context)


def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('course_details', id=quiz.course.id)

    else:
        form = QuizForm(instance=quiz)

    context = {
        'form': form,
    }
    return render(request, 'quiz/create_quiz.html', context=context)


def detele_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
# questions


def create_question(request, quiz_id):
    # Fetching data
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('options')

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        answer_form = AnswerForm(request.POST)

        if question_form.is_valid() and option_formset.is_valid() and answer_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            options = option_formset.save(commit=False)
            for option in options:
                option.question = question
                option.save()

            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            print(question_form.errors)
            print(option_formset.errors)
            print(answer_form.errors)

    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet(queryset=Option.objects.none())
        answer_form = AnswerForm()

    context = {
        'quiz': quiz,
        'question_form': question_form,
        'option_formset': option_formset,
        'answer_form': answer_form,
        'questions': questions,
    }

    return render(request, 'quiz/create_question.html', context)


# update


def update_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        # Process form data
        question_form = QuestionForm(request.POST, instance=question)
        option_formset = OptionFormSet(
            request.POST, queryset=Option.objects.filter(question=question))
        answer_form = AnswerForm(
            request.POST, instance=question.correct_answer if question.correct_answer else None)

        if question_form.is_valid() and option_formset.is_valid() and answer_form.is_valid():
            # Save the updated question
            question = question_form.save()

            # Save the updated options
            options = option_formset.save(commit=False)
            for option in options:
                option.question = question
                option.save()

            # Save the updated answer
            if answer_form.cleaned_data.get('answer_text'):
                answer = answer_form.save(commit=False)
                answer.question = question
                answer.save()

            # Redirect to a page that shows the updated quiz or question details
            # Adjust redirect as needed
            return redirect('create_question', quiz_id=quiz.id)

    else:
        # Initialize forms for GET request
        question_form = QuestionForm(instance=question)
        option_formset = OptionFormSet(
            queryset=Option.objects.filter(question=question))
        answer_form = AnswerForm(
            instance=question.correct_answer if question.correct_answer else None)

    context = {
        'quiz': quiz,
        'question_form': question_form,
        'option_formset': option_formset,
        'answer_form': answer_form,
    }

    return render(request, 'quiz/update_question.html', context)


# delete


def delete_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id, quiz_id=quiz_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question.delete()
    return redirect('create_question', quiz_id=quiz.id)


# quiz student

def show_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizes = Quiz.objects.filter(course=course)
    context = {
        'course': course,
        'quizes': quizes,
    }
    return render(request, 'quiz/quiz_stu/show_quiz.html', context=context)


def show_quiz_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('options')

    # Organize options by their related questions
    question_with_options = []
    for question in questions:
        options = question.options.all()
        question_with_options.append({
            'question': question,
            'options': options,
        })

    # quiz
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    is_correct = Answer.objects.filter(
                        question=question, answer_text=selected_option.option_text).exists()
                    if is_correct:
                        if not StudentProgress.objects.filter(
                            user=request.user, quiz=quiz, question=question
                        ).exists():
                            student_progress = StudentProgress(
                                user=request.user, quiz=quiz, question=question
                            )
                            student_progress.save()
                            score += 1
                            print('correct')
                            print(score)
                        else:
                            score += 1
                            print('correct')
                            print(score)

                except Option.DoesNotExist:
                    print(f'Option with ID {
                        selected_option_id} does not exist.')
        # Store the score and quiz ID in session
        request.session['score'] = score
        request.session['quiz_id'] = quiz_id
        return redirect('show_result')

    context = {
        'quiz': quiz,
        'question_with_options': question_with_options,
    }
    return render(request, 'quiz/quiz_stu/show_quiz_questions.html', context=context)


def show_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')

    # if not quiz_id:
    #     return redirect('')  # Handle missing quiz_id appropriately

    quiz = get_object_or_404(Quiz, id=quiz_id)
    total_questions = quiz.questions.count()
    incorrect_answers = total_questions - score
    questions = Question.objects.filter(quiz=quiz)

    # Create or update OverallProgress record
    OverallProgress.objects.update_or_create(
        user=request.user,
        quiz=quiz,
        defaults={
            'total_questions': total_questions,
            'score': score,
        }
    )

    # Clean up session
    request.session.pop('score', None)
    request.session.pop('quiz_id', None)

    context = {
        'score': score,
        'quiz': quiz,
        'total_questions': total_questions,
        'incorrect_answers': incorrect_answers,
        'questions': questions,
    }

    return render(request, 'quiz/quiz_stu/result_quiz.html', context=context)
