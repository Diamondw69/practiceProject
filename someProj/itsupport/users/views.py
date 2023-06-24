from django.contrib.auth import login,authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm,ProblemForm,CommentForm,ReportForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Problem,Comment,Report
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request,'users/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            return redirect('home')
    else:
        form = ProblemForm()

    return render(request, 'users/problem.html', {'form': form})

def problem_list(request):
    problems = Problem.objects.all()
    problem_type = request.GET.get('problem_type')
    if problem_type:
        problems = problems.filter(problem_type=problem_type)
    return render(request, 'users/problem_list.html', {'problems': problems})


@staff_member_required
def solve_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    report = problem.report_set.first()  # Get the first Report instance for the Problem, if it exists
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            if report:  # If a report exists, update it
                report.solution = form.cleaned_data['solution']
                report.status = form.cleaned_data['status']
                report.notes = form.cleaned_data['notes']
                report.solver = request.user
            else:  # If a report does not exist, create a new one
                report = Report(
                    problem=problem,
                    solution=form.cleaned_data['solution'],
                    status=form.cleaned_data['status'],
                    notes=form.cleaned_data['notes'],
                    solver=request.user,
                )
            
            report.save()
            if report.status == "resolved":
                problem.problem_solved = True
                problem.save()
                
            return redirect('problem_detail', problem_id=problem.id)
    else:
        initial = {
            'solution': report.solution if report else '',
            'status': report.status if report else '',
            'notes': report.notes if report else '',
        }
        form = ReportForm(initial=initial)
        
    return render(request, 'users/solve_problem.html', {'form': form, 'problem': problem})




def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    report = Report.objects.filter(problem=problem).first()
    return render(request, 'users/problem_detail.html', {'problem': problem, 'report': report})

@login_required
def add_comment(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
         
            comment = Comment()
            comment.problem = problem
            comment.author = request.user
            comment.text = form.cleaned_data['text']
            comment.save()

            return HttpResponseRedirect(reverse('problem_detail', args=[problem.pk]))

    else:
        form = CommentForm()

    return render(request, 'users/add_comment.html', {'form': form})
