from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Post
from .forms import PostForm, UserRegistrationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View


def registration_view(request):
    template_name = 'registration_form.html'
    success_url = reverse_lazy('verify_email_sent')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False



            verification_key = user.pk
            activation_link = f'http://127.0.0.1:8000/verify_email/{verification_key}/'
            send_mail(
                'Verify your email address',
                f'Click the following link to verify your email address: {activation_link}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Registration successful. Please check your email for verification.')
            return redirect(success_url)
    else:
        form = UserRegistrationForm()

    return render(request, template_name, {'form': form})

def verify_email_sent_view(request):
    template_name = 'verify_email_sent.html'
    return render(request, template_name)


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_post.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited successfully.')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})


def verify_email_sent(request):
    return render(request, 'verify_email_sent.html')

def verify_email_confirm(request, verification_key):
    user = get_object_or_404(get_user_model().objects.select_related('profile'), verification_key=verification_key)
    user.verification_key = ''
    user.save()
    user.is_active = True
    user.save()
    messages.success(request, 'Your email has been verified successfully. You can now log in.')
    return redirect('home')