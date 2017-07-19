from .forms import SendCommentForm, SendPostForm, SearchForm
from .models import Post, Blog, Comment
from django.http import HttpResponse
import json, string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def post(request, get_id):
    blog_id = get_id
    blog = Blog.objects.get(blog_id=blog_id)
    if request.method == 'POST':
        if blog.user.last_TOKEN == request.META.__getitem__('HTTP_X_TOKEN'):
            form = SendPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post_id = (Post.objects.filter(blog_id=blog_id).count() + 1)
                post.post_id = post_id
                post.save()
                post.blog_id = blog_id
                post.save()
                post.dateTime = timezone.now()
                post.save()

                response = {
                    'status': 0,
                    'post_id': post_id
                }
            else:
                response = {
                    "status": -1,
                    'message': "some error occurred"
                }

        else:
            response = {
                "status": -1,
                "message": "You can't post in this blog"
            }

    elif request.method == 'GET':
        blog_id = get_id
        post_id = request.GET.get('id')
        wanted_post = Post.objects.get(post_id=post_id, blog_id=blog_id)
        response = {
            'status': 0,
            'post': {
                'title': wanted_post.title,
                'summary': wanted_post.summary,
                'text': wanted_post.text,
                'dateTime': wanted_post.dateTime
            }
        }
    else:
        response = {
            "status": -1,
            "message": "just for check"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def posts(request, get_id):
    if request.method == 'GET':
        blog_id = get_id
        if 'offset' in request.GET:
            offset = int(request.GET['offset'])
        else:
            offset = 0
        if 'count' in request.GET:
            count = int(request.GET['count'])
        else:
            count = Post.objects.filter(blog_id=blog_id).count()
        wanted_comments = Comment.objects.filter(blog_id=blog_id).values()
        response = [{
            'title': wanted_comments[offset].get('title'),
            'summary': wanted_comments[offset].get('summary'),
            'text':wanted_comments[offset].get('text'),
            'dateTime': wanted_comments[offset].get('dateTime')
        }]
        for i in range(offset+1, offset+count):
            response.append({
                'title': wanted_comments[offset].get('title'),
                'summary': wanted_comments[offset].get('summary'),
                'text':wanted_comments[offset].get('text'),
                'dateTime': wanted_comments[offset].get('dateTime')
            })
    else:
        response = {
            'status': -1,
            'message': "some error occurred"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def comments(request, get_id):
    if request.method == 'GET':
        blog_id = get_id
        post_id = request.GET.get('post_id')
        if 'offset' in request.GET:
            offset = int(request.GET['offset'])
        else:
            offset = 0
        if 'count' in request.GET:
            count = int(request.GET['count'])
        else:
            count = Comment.objects.filter(blog_id=blog_id, post_id=post_id).count()
        wanted_comments = Comment.objects.filter(blog_id=blog_id, post_id=post_id).values()
        response = [{
            'text': wanted_comments[offset].get('text'),
            #'dateTime': wanted_comments[offset].get('dateTime')
        }]
        for i in range(offset+1, offset+count):
            response.append({
                'text': wanted_comments[i].get('text'),
                #'dateTime': wanted_comments[i].get('dateTime')
            })
        print("befor else")
    else:
        response = {
            'status': -1,
            'message': "some error occurred"
        }
    print("after else")
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def comment(request, get_id):
    if request.method == 'POST':
        blog_id = get_id
        form = SendCommentForm(request.POST)
        if form.is_valid():
            commentobj = form.save(commit=False)
            post_id = request.POST.get('post_id')

            commentobj.blog_id = blog_id
            commentobj.comment_id = Comment.objects.filter(post_id=post_id, blog_id = blog_id).count()+1
            commentobj.dateTime = timezone.now()
            commentobj.save()
            response = {
                'status': 0,
                'post_id': post_id
            }
        else:
            response = {
                "status": -1,
                "message": "your comment not been sent"
            }
    else:
        response = {
            "status": -1,
            "message": "your comment not been sent"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")


def search(request):
    if request.method == 'GET':
        form = SearchForm
        return render(request, 'search/search.html', {'form': form})
    else:
        search_text = "for test, for test, for test, for test,"
        words = search_text.split()
        words_number = len(words)
        if words_number in range(2, 11):
            for blog in Blog.objects:
                blog.score = 0
                for word in words:
                    blog.score += blog.wordcount[word]
            blogs = Blog.objects.order_by('score')[:10]
            return render(request, 'search/result.html', {'blogs': blogs})
        else:
            print("g")
