from .forms import SendCommentForm, SendPostForm
from .models import Post, Blog, Comment
from django.http import HttpResponse
import json
from django.utils import timezone


def post(request, get_id=1):
    print("1")
    blog_id = get_id
    blog = Blog.objects.get(blog_id=blog_id)
    if request.method == 'POST':
        print("2")
        if blog.user.last_TOKEN == request.META.get('X_Token'):
            print("3")
            form = SendPostForm(request.POST)
            # if request.POST.get('text') != None:
            if form.is_valid():
                post_id = (Post.objects.filter(blog_id=blog_id).count() + 1)
                #form.save()
                ppost = Post(
                    title=request.POST.get('title'),
                    summary=request.POST.get('summary'),
                    text=request.POST.get('text'),
                    dateTime=timezone.now(),
                    blog_id=blog_id,
                    post_id=post_id
                )
                ppost.save()
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
            'title': wanted_post.title,
            'summary': wanted_post.summary,
            'text': wanted_post.text
        }
    else:
        response = {
            "status": -1,
            "message": "just for check"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")


def posts(request, get_id):
    if request.method == 'GET':
        blog_id = get_id
        count = request.GET.get('count')
        offset = request.GET.get('offset')
        wanted_post = Post.objects.filter(blog_id = blog_id).orderd_by('creation_date').values()
        response = [{
            'title': wanted_post[offset].title,
            'summary': wanted_post[offset].summary,
            'text': wanted_post[offset].text,
            'dateTime': wanted_post[offset].creation_date
        }]
        for i in range(offset+1, offset+count):
            response.append({
                'title': wanted_post[i].title,
                'summary': wanted_post[i].summary,
                'text': wanted_post[i].text,
                'dateTime': wanted_post[i].creation_date
            })
    else:
        response = {
            'status': -1,
            'message': "some error occurred"
        }

    return HttpResponse(json.dumps(response), content_type="application/json")


def comments(request, get_id):
    if request.method == 'GET':
        blog_id = get_id
        post_id = request.GET.get('post_id')
        count = request.GET.get('count')
        offset = request.GET.get('offset')
        wanted_comments = Comment.objects.filter(blog_id=blog_id, post_id=post_id).orderd_by('creation_date').values()
        response = [{
            'text': wanted_comments[offset].text,
            'dateTime': wanted_comments[offset].creation_date
        }]
        for i in range(offset+1, offset+count):
            response.append({
                'text': wanted_comments[i].text,
                'dateTime': wanted_comments[i].creation_date
            })
    else:
        response = {
            'status': -1,
            'message': "some error occurred"
        }

    return HttpResponse(json.dumps(response), content_type="application/json")


def comment(request, get_id):
    if request.method == 'POST':
        blog_id = get_id
        form = SendCommentForm(data=request.POST)
        # if request.POST.get('text') != None:
        if form.is_valid():
            post_id = request.POST.get('post_id')
            ccomment = Post(
                text=request.POST.get('text'),
                dateTime=timezone.now(),
                blog_id=blog_id,
                post_id=post_id,
                comment_id=(Comment.objects.filter(blog_id=blog_id, post_id=post_id).count() + 1)
            )
            ccomment.save()
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