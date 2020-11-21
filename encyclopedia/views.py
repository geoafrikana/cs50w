from django.shortcuts import render, redirect
import markdown2, random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    title = title.lower()
    post = util.get_entry(title)
    if post:
        post = markdown2.markdown(post)
        return render(request, "encyclopedia/article.html", {
        'title':title, "post":post})
    else:
        return render(request, "encyclopedia/article.html", {
        'title': 'Not found', "post":'<h1>Article not found</h1>'})

def searcher(request):
    matches = []
    if request.method == 'POST':
        query = request.POST.get('q').lower()
        lowered = [item.lower() for item in util.list_entries()]
        if query in lowered:
            return redirect("article", title=query)
        elif query not in lowered:
            for entry in lowered:
                if query in entry:
                    matches.append(entry)
        return render(request, 'encyclopedia/search_results.html', {'matches':matches, 'message': 'Similar results', 'query':query})

def newpage(request):
    if request.method == 'POST':
        post_title = request.POST.get('post_title').lower()
        post_content = request.POST.get('post_content').lower()
        lowered = [item.lower() for item in util.list_entries()]
        if post_title in lowered:
            return render(request, 'encyclopedia/newpage.html', {'message': 'The entry already exists'})
        else:
            util.save_entry(post_title, post_content)
            return redirect("article", title=post_title)
    return render(request, 'encyclopedia/newpage.html')

def editcontent(request):
    if request.method == 'POST':
        post_title = request.POST.get('post_title').lower()
        upper_title = post_title.upper()
        post_content = util.get_entry(post_title)
        return render(request, 'encyclopedia/editcontent.html', {'post_content': post_content, 'upper_title': upper_title, 'post_title': post_title})
    return render(request, 'encyclopedia/editcontent.html')

def save_edit(request):
    if request.method == 'POST':
        revised_content = request.POST.get('post_content')
        post_title = request.POST.get('post_title')
        util.save_entry(post_title, revised_content)
        return redirect("article", title=post_title)

def random_post(request):
    lowered = [item.lower() for item in util.list_entries()]
    selected = random.choice(lowered)
    return redirect("article", title=selected)