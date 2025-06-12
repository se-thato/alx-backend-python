from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def delete_user(request):
    user = request.user
     #this will Log out user before deletion
    logout(request) 
    # This triggers post_delete signal       
    user.delete()         
    return redirect('') 
