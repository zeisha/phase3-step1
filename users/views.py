from django.views.decorators.csrf import csrf_exempt
from .models import User
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse
import json, random, string
from django.contrib.auth import authenticate
from blogs.models import Blog


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user == None:
            response = {
                "status": -1,
                "message": "some error occurred"
            }
        else:
            n=20
            token = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
            user = User.objects.get(username=username)
            user.last_TOKEN = token(20)
            user.save()
            response = {
                "status": 0,
                "token": user.last_TOKEN
            }

    else:
        response = {
            "status": -1,
            "message": "some error occurred"
        }

    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            blog_id = Blog.objects.count() + 1
            user = User.objects.get(username=request.POST.get('username'))
            blog = Blog(blog_id=blog_id, user=user)
            user.default_blog_id = blog_id
            user.save()
            blog.save()

            response = {
                "status": 0,
            }
        else:
            response = {
                'status': -1,
                'message': "some other error occurred"
            }
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {
            "status": -1,
            "message": "some error occurred"
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
        #return JsonResponse(response)


def blog_id(request):
    user = User.objects.get(last_TOKEN=request.GET.get('TOKEN'))
    response = {
        "blog_id": user.default_blog_id
    }
    return HttpResponse(json.dumps(response), content_type="application/json")