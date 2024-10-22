from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomUserCreationForm
from .models import Tip, Category
from .forms import TipForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')

    # Filter tips based on search query and category
    tips = Tip.objects.all().order_by('-created_at')
    
    if category_id:
        tips = tips.filter(category__id=category_id)
    
    if query:
        tips = tips.filter(title__icontains=query)

    categories = Category.objects.all()

    return render(request, 'tips/home.html', {
        'tips': tips,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'tips/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST['email']

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Create the user
        User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    
    return render(request, 'tips/register.html')


@login_required
def add_tip(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        Tip.objects.create(title=title, content=content, image=image, author=request.user, category=category)
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'tips/add_tip.html', {'categories': categories})

@login_required
def my_tips(request):
    tips = Tip.objects.filter(author=request.user)
    return render(request, 'tips/my_tips.html', {'tips': tips})

@login_required
def liked_tips(request):
    tips = request.user.liked_tips.all()
    return render(request, 'tips/liked_tips.html', {'tips': tips})


def user_logout(request):
    logout(request)
    return redirect('home')

def search_tips(request):
    if request.is_ajax():
        query = request.GET.get('query', '')
        tips = Tip.objects.filter(title__icontains=query)
        results = [{'title': tip.title, 'id': tip.id} for tip in tips]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def like_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user in tip.likes.all():
        tip.likes.remove(request.user)
    else:
        tip.likes.add(request.user)
    return redirect('home')    

def share_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    return render(request, 'tips/share_tip.html', {'tip': tip})    

def search_tips(request):
    query = request.GET.get('query', '')
    tips = Tip.objects.filter(title__icontains=query)  # Fetch tips matching the search query
    all_tips = Tip.objects.all()  # Fetch all tips for display below search results
    return render(request, 'tips/search_results.html', {'tips': tips, 'query': query})

class MyTipsView(View):
    def get(self, request):
        tips = Tip.objects.filter(author=request.user)
        return render(request, 'tips/my_tips.html', {'tips': tips})

class EditTipView(View):
    def get(self, request, tip_id):
        tip = get_object_or_404(Tip, id=tip_id, author=request.user)
        form = TipForm(instance=tip)
        return render(request, 'tips/edit_tip.html', {'form': form, 'tip': tip})

    def post(self, request, tip_id):
        tip = get_object_or_404(Tip, id=tip_id, author=request.user)
        form = TipForm(request.POST, request.FILES, instance=tip)
        if form.is_valid():
            form.save()
            return redirect('my_tips')
        return render(request, 'tips/edit_tip.html', {'form': form, 'tip': tip})

class DeleteTipView(View):
    def post(self, request, tip_id):
        tip = get_object_or_404(Tip, id=tip_id, author=request.user)
        tip.delete()
        return redirect('my_tips')

class TipDetailView(View):
    def get(self, request, tip_id):
        tip = get_object_or_404(Tip, id=tip_id)
        return render(request, 'tips/tip_detail.html', {'tip': tip})

class HomeView(View):
    def get(self, request):
        tips = Tip.objects.all().order_by('-created_at')[:10]  # Adjust the number of recent tips you want to show
        return render(request, 'tips/home.html', {'tips': tips})

class SearchTipsView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        tips = Tip.objects.filter(title__icontains=query)  # Adjust according to your search logic
        return render(request, 'tips/search_results.html', {'tips': tips, 'query': query})

def remove_like(request, tip_id):
    if request.method == 'POST' and request.user.is_authenticated:
        tip = get_object_or_404(Tip, id=tip_id)
        tip.likes.remove(request.user)  # Remove the like from the tip
        return redirect('liked_tips')  # Redirect to liked tips page
    return redirect('login')

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            subject = "Password Reset Requested"
            email_template_name = "registration/password_reset_email.html"
            context = {
                "email": user.email,
                "domain": request.META['HTTP_HOST'],
                "site_name": "Your Site Name",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "http",
            }
            email = render_to_string(email_template_name, context)
            send_mail(subject, email, "noreply@yourdomain.com", [user.email])
            messages.success(request, "Password reset email has been sent.")
            return redirect("password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "registration/password_reset.html", {"form": form})


