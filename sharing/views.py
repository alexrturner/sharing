from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from sharing.models import Message

# from .forms import MessageForm


def index(request):
    # if not request.user.is_authenticated:
    #     return redirect('login_view')

    all_messages = Message.objects.all().order_by('timestamp')
    
    chat_pairs = set()
    for message in all_messages:
        # Create a tuple of the sender and receiver usernames in a sorted order
        pair = tuple(sorted([message.sender.username, message.receiver.username]))
        chat_pairs.add(pair)

    return render(request, "index.html", {"chat_pairs": chat_pairs})



def login_view(request):
    if request.method == 'POST':
        username = request.POST["user"]
        password = request.POST["pwd"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list_view')
        else:
            return render(request, 'login.html', {"error_info": "Invalid username or password"})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    #return render(request, 'login.html')
    return redirect('index')




def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'sign_up.html', {'error': 'Username already exists'})

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('login_view')
        except IntegrityError:
            # Handle any other database integrity issues
            return render(request, 'sign_up.html', {'error': 'An error occurred during registration'})

    return render(request, 'sign_up.html')

@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    
    # Fetch messages sent by both users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # Handle new message posting
    if request.method == 'POST':
        text = request.POST.get('message', '')
        audio = request.FILES.get('audio', None)
        recorded_together = 'together' in request.POST
        Message.objects.create(
            sender=request.user,
            receiver=other_user,
            text=text,
            audio=audio,
            recorded_together=recorded_together
        )
        return redirect('chat_view', user_id=user_id)

    # Render chat
    return render(request, 'chat.html', {'other_user': other_user, 'messages': messages})


def jump_view(request):
    return render(request, "jump.html")


@csrf_exempt
@login_required
def main(request):
    if request.method == 'POST':
        items_to_delete = request.POST.get('id')
        Userplan.objects.filter(id=items_to_delete).delete()
    user_plan = Userplan.objects.filter(name=request.user.username).values()
    return render(request, "main.html", {"user_plan": user_plan})


def user_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    users = User.objects.exclude(id=request.user.id)  # Exclude current user
    return render(request, 'user_list.html', {'users': users})

def chat_history_view(request, user1, user2):
    # Fetch the users
    user1 = User.objects.get(username=user1)
    user2 = User.objects.get(username=user2)

    # Fetch the chat history
    messages = Message.objects.filter(
        Q(sender=user1, receiver=user2) | 
        Q(sender=user2, receiver=user1)
    ).order_by('timestamp')

    return render(request, 'chat_history.html', {'messages': messages, 'user1': user1, 'user2': user2})

# def message_submit_view(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the form and handle as required
#             form.save()
#             # Redirect or render as needed
#     else:
#         form = MessageForm()
#     return render(request, 'template_name.html', {'form': form})
