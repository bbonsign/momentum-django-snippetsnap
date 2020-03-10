from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Snippet, Tag
from .forms import SnippetForm


@login_required
def user_home(request):
    user = request.user
    snippets = user.snippets.all()
    context = {'snippets': snippets}
    return render(request, 'snippets/user_home.html', context=context)


@login_required
def snippet_detail(request, snip_id):
    snippet = Snippet.objects.get(id=snip_id)
    context = {'snippet': snippet}
    return render(request, 'snippets/snippet_detail.html', context=context)


@login_required
def fork(request, snip_id):
    user = request.user
    snippet = Snippet.objects.get(id=snip_id)
    if user == snippet.owner:
        return redirect('user_home')
    new_snippet = snippet
    new_snippet.pk = None
    new_snippet.owner = user
    new_snippet.parent = Snippet.objects.get(id=snip_id)
    new_snippet.save()
    snippet.copies += 1
    snippet.save()
    context = {'snippet': new_snippet, 'message': "You're cloned snippet:"}
    return render(request, 'snippets/snippet_detail.html', context=context)
    # return redirect('snippet_detail', new_snippet.id)


@login_required
def add_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.owner = request.user
            snippet.save()
            return redirect('user_home')
    else:
        form = SnippetForm()
        context = {'form': form}
        return render(request, 'snippets/form.html', context=context)
