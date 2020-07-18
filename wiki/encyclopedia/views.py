from django.shortcuts import render

from django import forms

from django.http import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse

from . import util

import random

import markdown2

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    textarea = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control'}))

class EditPageForm(forms.Form):
#    title = forms.CharField(label='Title')
    textarea = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        'entries': util.list_entries()
    })

def entry(request, title):
    output=util.get_entry(title)
    if output == None:
        return render(request, 'encyclopedia/error.html')
    else:
        content = markdown2.markdown(output)
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })
    

def search(request):
    #if request.method == "POST"
    query = request.POST["q"]
    entries = util.list_entries()
    matches = []

    #Check Equal Title
    for title in entries:
        if title.lower() == query:
            #redirect to entry page.
            return entry(request, title)
            # also posible: return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))

    #Check Similar/SubString Titles.

    for title in entries:
        if query in title.lower():
            matches.append(title)
        
    return render(request, 'encyclopedia/search.html', {
        'matches': matches,
        'query': query
    })



def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html",{
                'form': NewPageForm(),
                'error': False
            })

    if request.method == 'POST':
        form = NewPageForm(request.POST) #create new form
        if form.is_valid():
            title= form.cleaned_data['title']
            content = form.cleaned_data['textarea']
            if util.get_entry(title) == None: # if doesnt exist then save it
                util.save_entry(title, content)
                return entry(request, title) #redirect
                #return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            else:
                return render(request, "encyclopedia/create.html", {
                        'error': True
                    })
                    
            


def edit(request, title):
    
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            #title= form.cleaned_data['title']
            content = form.cleaned_data['textarea']
            util.save_entry(title, content)
            return entry(request, title) #redirect

            #if util.get_entry(title) == None: # if doesnt exist then save it
            #    util.save_entry(title, content)
            #    return entry(request, title) #redirect
                #return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            #else:
            #    return render(request, "encyclopedia/edit.html", {
            #            'error': True
            #        })
        else:
            return render(request, "encyclopedia/edit.html", {
            'title': title,
            'form': form
        })
    
    if request.method == "GET":
        content = util.get_entry(title)

        form = EditPageForm(initial={
            'textarea': content
            })

        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'form': form
        })

def random_page(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) -1)
        random_entry = entries[num]
        #title = util.get_entry(random_entry)
        return entry(request, random_entry)
