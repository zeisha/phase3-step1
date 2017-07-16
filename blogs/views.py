from .forms import SendCommentForm, SendPostForm
from .models import Post, Blog, Comment
from django.http import HttpResponse
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def post(request, get_id):
    blog_id = get_id
    print(blog_id)
    blog = Blog.objects.get(blog_id=blog_id)
    if request.method == 'POST':
        print(request.META.__getitem__('HTTP_X_TOKEN'))
        print(blog.user.last_TOKEN)
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