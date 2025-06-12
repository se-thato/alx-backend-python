from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Message

@login_required
def delete_user(request):
    user = request.user
     #this will Log out user before deletion
    logout(request) 
    # This triggers post_delete signal       
    user.delete()         
    return redirect('') 


def build_thread(message):
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": [build_thread(reply) for reply in message.replies.all()]
    }

@login_required
def user_conversations(request):
    # Only get top-level messages (not replies), sent or received by user
    top_level_messages = Message.objects.filter(
        parent_message__isnull=True
    ).filter(
        sender=request.user
    ) | Message.objects.filter(
        parent_message__isnull=True,
        receiver=request.user
    )

    # Optimize with select_related and prefetch_related
    top_level_messages = top_level_messages.select_related('sender', 'receiver') \
    .prefetch_related('replies__sender', 'replies__receiver')

    # Build threads
    threads = [build_thread(msg) for msg in top_level_messages]

    return render(request, 'messaging/', {'threads': threads})



#unread messages views
@login_required
def unread_inbox(request):
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only('sender', 'content', 'timestamp')
    )
    return render(request, 'messaging/', {
        'unread_messages': unread_messages
    })
