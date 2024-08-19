from django.shortcuts import render,redirect,get_object_or_404,loader,HttpResponse
from .models import Task
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import  login_required


# Create your views here.


def login_views(request):
    if request.method == "GET":
        return render(request,'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are logged in as "+ username)
            return redirect('/myapp/task_list/')
        else:
            messages.error(request,"invalid username or password")
            return redirect('login')
        

def logout_views(request):
    logout(request)
    return redirect('/login/')


def task_list(request):
    tasks = Task.objects.all().order_by('-id')
    template = loader.get_template('task_list.html')
    context = {
        'tasks': tasks,
    }

    return HttpResponse(template.render(context,request))
@login_required(login_url='login')

def task_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        is_completed = request.POST.get('is_completed') == 'on'

        task = Task(title=title,description=description,due_date=due_date,is_completed=is_completed)
        task.save()

        messages.success(request,'task created successfully')
        return redirect('task_list')
    return render(request,'task_form.html')
@login_required(login_url='login')

def delete_task(request,task_id):
     task = get_object_or_404(Task,id = task_id)

     if request.method == 'POST':
        task.delete()
        messages.error(request,'task deleted successfully')
        return redirect('task_list')
      

     return render(request, 'delete_task.html',{'task':task}) 

#def delete_task(request,task_id)
 #     task = Task.objects.filter(id=task_id)
   #   task.delete()
   #   return redirect('/myapp/task_list/')

    
                
