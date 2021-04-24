from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from .models import Post
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostCreationForm
from .loginpage import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginUser, logout as logoutUser
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/home.html'
    context_object_name = 'post'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog_app/user_posts.html'
    context_object_name = 'post'

    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}

    return render(request, 'blog_app/home.html', context=context)


def about(request):
    return render(request, 'blog_app/about.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # user = User.objects.filter(username=username, password=password)
        if user is not None:
            # print("User exists")
            # print(user)
            loginUser(request, user)
            return redirect('blog-home')
        else:
            # print("User doesn't exist")
            messages.info(request, f'Account doesn\'t exist')
            return redirect('/login/')

    else:
        form = LoginForm()
    return render(request, 'blog_app/login.html', {'form': form})


def logout(request):
    logoutUser(request)
    return render(request, 'blog_app/logout.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Account Successfully Created for {username}, Now you can Log In')
            print("form is valid")
            return redirect('blog-login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog_app/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile have been Updated')
            return redirect('blog-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog_app/profile.html', context)


@login_required
def postCreate(request):
    if request.method == 'POST':
        
        pass
    else:
        form = PostCreationForm()
        context = {
            'postform': form
        }
        return render(request, 'blog_app/postcreate.html', context)












