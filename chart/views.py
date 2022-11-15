from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.urls import reverse
User = get_user_model()
from django.utils import timezone


def home(request):
    charts_count = Chart.objects.count()
    user_count = User.objects.count()
    date_joined_count = User.objects.filter(date_joined__date=timezone.now()-timezone.timedelta(0)).count()
    users = User.objects.all().order_by('-id')[:date_joined_count]
    elem_count = Element.objects.count()
    following_actions = None
    # created_on_count = None
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user)
        # for user_f in user.followers.all():
        #     created_on_count = user_f.chart.filter(created_on__date=timezone.now()).count()
        following_actions = user.followers.all().order_by('-id')[:15]

    contact = ContactUsForm()
    if request.method == "POST":
        contact = ContactUsForm(request.POST)
        if contact.is_valid():
            contact.save()
            return redirect('app:home')
    context = {
        "charts_count":charts_count,
        "user_count":user_count,
        "elem_count":elem_count,
        "following_actions":following_actions,
        "users":users,
        "contact":contact
    }
    return render(request, 'pages/home.html', context)

def PublicProfileView(request, username):
        try:
            user_p = User.objects.get(username=username)
            author = get_object_or_404(User, username=username)
            # Tab
            tab = request.GET.get('tab')
            title = None
            tab_chart = None
            tab_following = None
            tab_followers = None
            if tab == "charts":
                tab_chart = author.chart.all()
                title = "Charts"
            elif tab == "following": # followingda foydalanuvchi uchun followerslar keladi. followersda esa teskarisi
                tab_followers = user_p.followers.all().order_by('-id')
                title = "Following"

            elif tab == "followers":
                title = "Followers"
                tab_following = user_p.following.all().order_by('-id')
            else:
                title = f"amCharts - @{user_p.username}"

            # Epdate Profile
            if request.user.is_authenticated:
                user_form = UpdateUserForm(instance=request.user)
                profile_form = UpdateProfileForm(instance=request.user.profile)
                if request.method == 'POST':
                    user_form = UpdateUserForm(request.POST, instance=request.user)
                    profile_form = UpdateProfileForm(request.POST,
                                                    request.FILES,
                                                    instance=request.user.profile)
                    if user_form.is_valid() and profile_form.is_valid():
                        user_name = user_form.cleaned_data.get('username')
                        user_form.save()
                        profile_form.save()
                        return redirect("app:profile", user_name)
                    
            else:
                user_form = None
                profile_form = None

            user_chart_count = author.chart.count()
            context = {
                "user_p": user_p,
                "user_following":tab_following,
                "user_followers":tab_followers,
                "user_form":user_form,
                "profile_form":profile_form,
                "tab_chart":tab_chart,
                "title":title,
                "user_chart_count":user_chart_count
            }
            return render(request, 'pages/profile.html', context)
        except:
            context={
                "username_z":request
            }
            return render(request, "pages/404.html", context)

def followToggle(request, author):
    if request.user.is_authenticated:
        authorObj = User.objects.get(username=author)
        currentUserObj = User.objects.get(username=request.user.username)
        following = authorObj.following.all()

        if author != currentUserObj.username:
            if currentUserObj in following:
                authorObj.following.remove(currentUserObj.id)
            else:
                authorObj.following.add(currentUserObj.id)

        return HttpResponseRedirect(reverse("app:profile", args=[authorObj.username]))
    else:
        return HttpResponseRedirect(reverse("login"))

def NewChartView(request):
    if request.user.is_authenticated:
        user_p = User.objects.get(username=request.user)
        user = User.objects.get(username=request.user)
        author = get_object_or_404(User, username=request.user)
        dash = author.chart.all()
        new_dash = None
        NewChart = ChartFrom()
        if request.method == 'POST':
            NewChart = ChartFrom(data=request.POST)
            if NewChart.is_valid():
                new_dash = NewChart.save(commit=False)
                slug = NewChart.cleaned_data.get('slug')
                new_dash.author = author
                new_dash.save()
                return redirect("app:chart", slug) 
    else:
        return redirect("app:signup")

    context={
        "NewChart":NewChart,
    }
    return render(request, "pages/new.html", context)

def signup(request):
    form = Registration()
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request, 'registration/signup.html', {"form":form})

def ChartView(request, slug):
    chart = Chart.objects.get(slug=slug)
    post = get_object_or_404(Chart, slug=slug)
    elements = post.element.all()
    elements_count = post.element.count()
    number_avg = post.element.aggregate(Avg("value"))
    new_element= None
    # chart_view = Chart.objects.get(slug=slug)
    if request.user.is_authenticated:
        chart.view_count = chart.view_count + 1
    else:
        chart.view_count = chart.view_count + 1
    chart.save()
    if request.method == 'POST':
        comment_form = ElementForm(data=request.POST)
        if comment_form.is_valid():
            new_element = comment_form.save(commit=False)
            new_element.post = post
            new_element.save()
            return redirect("app:chart", slug) # redirect to this url
    else:
        comment_form = ElementForm()
    update_chart_form = ChartFrom(instance=chart)
    if request.method == 'POST':
        update_chart_form = ChartFrom(request.POST, instance=chart)
        if update_chart_form.is_valid():
            update_chart_form.save()
            slug = update_chart_form.cleaned_data.get('slug')
            return redirect("app:chart", slug)
    context= {
        'elements': elements,
        'comment_form': comment_form,
        "chart":chart,
        "elements_count":elements_count,
        "number_avg":number_avg,
        "update_chart_form":update_chart_form
        }
    
    return render(request, "pages/chart.html", context)

# def UpdateChartView(request, slug)
