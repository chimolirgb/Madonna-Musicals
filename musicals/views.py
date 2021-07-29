from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import ProfileForm,MusicForm,UpdateUserProfileForm,UpdateUserForm,CategoryForm,CommentForm
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer

# Create your views here.

def welcome(request):
    categories = Category.objects.all()
  
    return render(request, 'index.html', {"categories": categories})

def post(request):
    if request.method == 'POST':
        form =MusicForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
        return redirect('/')
    else:
        form =MusicForm()

    return render(request,'post.html',{'form':form})

def category(request):
    if request.method == 'POST':
        form =CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user.profile
            category.save()
        return redirect('/')
    else:
        form =CategoryForm()

    return render(request,'categories.html',{'form':form})

def musics_list(request,id):
    category = Category.objects.get(id=id)
    musics = Music.objects.filter(category=category)
    comments = Comment.objects.filter(id =id)
    print(musics)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = category
            comment.user = request.user.profile
            # comment.save(comments)
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'musics': musics,
        'form': form,
        'comments':comments,
        'category':category
    }
    
    return render(request,'category_musics.html',params)

def music_update(request,id):
    music=Music.objects.get(id=id)
    category = Category.objects.filter(name=music.category)
    print(music)
    
    form = MusicForm(instance=music)
    if request.method == 'POST':
        form = MusicForm(request.POST,request.FILES,instance=music)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
        return redirect('musics_list',id=music.category_id)
  
    return render(request,'update_music.html',{'form':form})
    
def music_delete(request,id):
    Music = Music.objects.get(id=id)
    category = Category.objects.filter(name=music.category)
  
    music.delete()
    
    return redirect('musics_list',id=music.category_id)
  
@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user = request.user
    if request.method=='POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = current_user

            profile.save()
        return redirect('Index')
    else:
        form=ProfileForm()

    return render(request,'create_profile.html',{"form":form})

@login_required(login_url='/accounts/login/')
def profile(request,username):
 
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        # 'projects': projects,
    }
    return render(request, 'profile.html',params)

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category(category_name=form.cleaned_data.get('category_name'),
                        user=request.user)
            category.save()
            return redirect('welcome')
        else:
            return render(request, 'addcategory.html', {'form': form})
    else:
        form = CategoryForm()
        return render(request, 'addcategory.html', {'form': form})

def add_music(request, category):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            music = Music(title=form.cleaned_data.get('title'),
                        content=form.cleaned_data.get('content'),
                        category=Category.objects.get(id=category))
            music.save()
            return redirect('category', category=int(category))
        else:
            return render(request, 'post.html', {'form': form})
    else:
        form = MusicForm()
        return render(request, 'post.html', {'form': form})

def delete_music(request, music):
    current_music=Music.objects.get(id=music)
    category=current_music.category
    current_music.delete()
    return redirect('category', category=category.id)

def edit_music(request, music):
    page_title = "Edit Music"
    editting_music = Music.objects.get(id=music)

    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            music = Music.objects.get(id=music)
            music.title=form.cleaned_data.get('title')
            music.notes=form.cleaned_data.get('notes')
            music.date_updated = timezone.now()
            music.save()
            return redirect('category', category=music.category.id)
        else:
            return render(request, 'add-card.html', {'form': form, "page_title": page_title})
    else:
        form = MusicForm(initial={'title': editting_music.title, 'notes': editting_music.notes})
        return render(request, 'add-music.html', {'form': form, "page_title": page_title})

@login_required(login_url='/accounts/login/')
def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_two_profile = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_two_profile)
        unfollow_d.delete()
        return redirect('user_profile', user_two_profile.user.username)

@login_required(login_url='/accounts/login/')
def follow(request, to_follow):
    if request.method == 'GET':
        user_three_profile = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=user_three_profile)
        follow_s.save()
        return redirect('user_profile', user_three_profile.user.username)

def logout(request):
    logout(request)
    return redirect('login')

def video(request):
    object = Item.objects.all()
    listtobe = []
    for i in object:
        x = i.video.split('/')
        z = x[-1]
        y = i.author
        listtobe.append({'author':y, 'yt_id':z})
        


    return render(request,'video.html',{'listtobe':listtobe})

    