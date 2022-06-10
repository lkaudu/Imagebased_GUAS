from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from graphical_pwd_auth.settings import N, TBA, EMAIL_HOST_USER, ALLOWED_HOSTS
from .models import LoginInfo
import random, uuid
from django.db.models import Q

# username = ''
def get_pwd_imgs():
    # These images are just to confuse the attacker
    # images = random.sample(range(1, 13), N * 4)
    images= range(1, 13)
    print(images)
    p_images = []
    for i in range(0, N * 4, N):
        p_images.append(images[i:i+N])
    print(p_images)
    return p_images

def get_pwd_imgs2():
    # These images are just to confuse the attacker
    images = random.sample(range(1, 13), N * 4)
    print(images)
    p_images = []
    for i in range(0, N * 4, N):
        p_images.append(images[i:i+N])
    print(p_images)
    return p_images



def get_clpwd():
    
    images = random.sample(range(1, 10), N * 3)
    print(images)
    p_colours = []
    for i in range(0, N * 3, N):
        p_colours.append(images[i:i+N])
    print(p_colours)
    return p_colours
    


def update_login_info(user, didSuccess):
    if didSuccess:
        user.logininfo.fails = 0
    else:
        user.logininfo.fails += 1
    
    user.logininfo.save()
    print('{} Failed attempts: {}'.format(user.username, user.logininfo.fails))



def isBlocked(username):
    try:
        user = User.objects.get(username=username)
    except Exception:
        return None
    print('isBlocked: {} - {}'.format(user.logininfo, TBA))
    if user.logininfo.fails >= TBA:
        return True
    else:
        return False


def sendLoginLinkMailToUser(username):
    user = User.objects.get(username=username)
    # send email only id user.logininfo.login_link is not None
    if user.logininfo.login_link is None:
        link = str(uuid.uuid4())
        user.logininfo.login_link = link
        user.logininfo.save()
        email = EmailMessage(
            subject='Link to Log in to your account',
            body='''
            Someone tried to bruteforce on your account.
            Click the Link to Login to your account directly.
            The link is one-time clickable
            link: http://{}:8000/login/{}
            '''.format(ALLOWED_HOSTS[-1], link), # might wanna change the allowd_host
            from_email=EMAIL_HOST_USER,
            to=[user.email],
        )
        email.send()
        print('LOGIN LINK EMAIL SENT')


def sendPasswordResetLinkToUser(username):
    # send reset link everytime user requests
    try:
        user = User.objects.get(username=username)
        return True

    except Exception:
        return False
    
    # link = str(uuid.uuid4())
    # user.logininfo.reset_link = link
    # user.logininfo.save()
    # email = EmailMessage(
    #     subject='Link to Rest your Password',
    #     body='''
    #     You have requested to reset your password.
    #     Click the Link to reset your password directly.
    #     The link is one-time clickable
    #     link: http://{}:8000/reset/{}
    #     '''.format(ALLOWED_HOSTS[-1], link), # might wanna change the allowd_host
    #     from_email=EMAIL_HOST_USER,
    #     to=[user.email],
    
    # print('PWD RESET LINK EMAIL SENT')
    


def index(request):
    # user = User.objects.all()
    # user.delete()
    return render(request, 'index.html')
    # return HttpResponse(html)


def successful_page(request):
    return render(request, 'successful.html')


def register_page(request):
    logout(request)
    messages.warning(request, '')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        print(username, password)
        try:
            # create user and loginInfo for him
            user = User.objects.create_user(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            login_info = LoginInfo(user=user, fails=0)
            login_info.save()
            messages.success(request, 'Sign up successful')
        except Exception:
            messages.warning(request, 'Sign up failed. Kindly pick another username')
            return redirect('register')
        # return redirect('index')
    else:
        data = {
            'p_images': get_pwd_imgs(),
        }
        return render(request, 'register.html', context=data)
    return redirect('index')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        print(username, password)
        selected_project_id = username
        request.session['selected_project_id'] = selected_project_id

        block_status = isBlocked(username)
        if block_status is None:
            # No user exists
            messages.warning(request, 'Account doesn\'t Exist')
            return redirect('login')

        elif block_status == True:
            # Blocked - send login link to email
            # check if previously sent, if not send
            sendLoginLinkMailToUser(username)
            messages.warning(request, 'Your account is Blocked, please check your Email!')
            return redirect('login')
        else:
            # Not Blocked
            usr = authenticate(username=username, password=password, request=request)
            if usr is not None:
                # login(request, usr)
                # update_login_info(usr, True)
                messages.success(request, 'Good, kindly proceed to the 2nd Login Phase')
                return redirect ('login2')
                
            
            else:
                user = User.objects.get(username=username)
                update_login_info(user, False)
                messages.warning(request, 'Sorry, You entered a wrong Password! Try again')
                return redirect('login')

    else:
        data = {
            'p_images': get_pwd_imgs(),
        }
        return render(request, 'login.html', context=data)
    return redirect('login2')

# def login2_page(request):
#     if request.method == 'POST':
                
#         first_name = request.POST['first_name']
#         # user = User.objects.get(username=username)
#         user = User.objects.filter(first_name=first_name).first()
#         if not user:
#             messages.warning(request, 'Sorry, You entered a wrong Password! Try again')
#             return redirect ('login2')
                    
#         else:
#             messages.warning(request, 'Good! Kindly proceed to the Final Login Phase')
#             return redirect ('login3')
            
#     else:
#         data = {
#         'p_images': get_pwd_imgs(),
#     }
#         return render(request, 'login2.html', context=data)
#     return redirect('login3')

def login2_page(request):
    if request.method == 'POST':
                
        first_name = request.POST['first_name']
        # user = User.objects.get(username=username)
        # username = login_page(request).username
        username= request.session.get('selected_project_id')
        user = User.objects.filter(first_name=first_name, username =username ).exists()
        # qs = User.objects.all()
        # for term in query_name.split():
        # qs = qs.filter( Q(first_name__icontains = first_name) | Q(username__icontains = selected_project_id))
       
        if not user:
            messages.warning(request, 'Sorry, You entered a wrong Password! Try again')
            return redirect ('login2')
                    
        else:
            messages.warning(request, 'Good! Kindly proceed to the Final Login Phase')
            return redirect ('login3')
            
    else:
        data = {
        'p_images': get_pwd_imgs(),
    }
        return render(request, 'login2.html', context=data)
    return redirect('login3')

def login3_page(request):
    if request.method == 'POST':
                
        last_name = request.POST['last_name']
        # user = User.objects.get(username=username)
        # user = User.objects.filter(last_name=last_name).first()
        username= request.session.get('selected_project_id')
        user = User.objects.filter(last_name=last_name, username =username ).first()

        if not user:
            messages.warning(request, 'Sorry, You entered a wrong Password! Try again')
            return redirect ('login3')
                    
        else:
            messages.warning(request, 'Login Successful!')
            login(request, user)
            update_login_info(user, True)
            
            return redirect ('index')
            
    else:
        data = {
        'p_images': get_pwd_imgs(),
    }
        return render(request, 'login3.html', context=data)
    return redirect('login3')
    

def login_from_uid(request, uid):
    try:
        # get user from the uid and reset the Link to 'NO_LINK' again
        login_info = LoginInfo.objects.get(login_link=uid)
        user = login_info.user
        login(request, user)
        update_login_info(user, True)
        login_info.login_link = None
        login_info.save()
        messages.success(request, 'Login successfull!')
    except Exception:
        messages.warning(request, 'Invalid Link. Please check again!')

    return redirect('index')


def reset_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        selected_project_id2 = username
        request.session['selected_project_id2'] = selected_project_id2

        if not user:
            messages.warning(request, 'Username Name Not found!')
            return render(request, 'reset_request.html')
                    
        else:
            messages.warning(request, 'Reset Your Password here!')
            usr = User.objects.filter(id=user.id)
            usr.delete()
            return redirect ('passreset')
            

    else:
        return render(request, 'reset_request.html')

def passreset(request):
    if request.method == 'POST':
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        print(password)
        
        # login_info = LoginInfo.objects.get(reset_link=uid)
        username= request.session.get('selected_project_id2')
        # user = User.objects.get(username=username)
        # user = login_info.user
        # if not user:
        #     # reset user and loginInfo for him
        #     messages.warning(request, 'Please check again!')
        #     return redirect('passreset')
            

        # else:
        try:
            user = User.objects.create_user(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            login_info = LoginInfo(user=user, fails=0)
            login_info.save()
            # # reset pwd
            # user.set_password = User.cleaned_data['password']
            # user.first_name = User.cleaned_data['first_name']
            # user.last_name = User.cleaned_data['last_name']
            # user.set_last_name = User.cleaned_data['last_name']
            # user.set_password(password)
            # user.first_name(first_name)
            # user.last_name(last_name)

            # user.password = User.cleaned_data['password']
            # user.first_name = User.cleaned_data['first_name']
            # user.last_name = User.cleaned_data['last_name']
            
           
            # login_info.save()
            user.save()
            messages.success(request, 'Password Reset Successfully!')
            return redirect('index')

        except Exception:
            messages.warning(request, 'Password Setup failed')
            return redirect('passreset')
           
    else:
        data = {
            'p_images': get_pwd_imgs(),
        }
        return render(request, 'reset.html', context=data)
    return redirect('index')




def logout_page(request):
    logout(request)
    messages.warning(request, 'You\'ve been logged out!')
    return redirect('index')