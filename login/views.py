from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.views.generic import View
from .forms import AuthForm,UserForm
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User as UserModel
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sessions.models import Session
import random
# Create your views here.

# def login(request):
#     return render(request,'login/loginPage.html')
def frgtPwd(request):
    # send_mail(
    #     'Subject blah blah ',
    #     "that's fckin working!!",
    #     'seeyouatthetop42@gmail.com',
    #     ['seeyouatthetop42@yahoo.com','viraj0118@gmail.com','parmarapurva1999@gmail.com'],
    #     fail_silently=False
    # )
    return render(request,'login/forgotPwd.html')

# this newPwd is used right now not the admm one
def sendOTP(request):
    if request.method=='POST':
        try:
            usr = User.objects.get(email=request.POST['email'])
            # if request.user.password==request.POST['passwrd'] & usr.secque== & usr.secqans==:
            otp = random.randint(a=0, b=9991999)
            try:
                send_mail(
                    'BoardingAlley Password Reset',
                    "OTP to change your BoardingAlley account password is : " + str(otp),
                    usr.email,
                    [request.POST['email']],
                    fail_silently=False
                )
            except:
                messages.info(request,'Error sending OTP')
                return redirect('login:frgtPwd')
            request.session['otp'] = otp
            request.session['email'] = request.POST['email']
            return redirect('login:enterOTP')

        except ObjectDoesNotExist:
            messages.info(request,'No account registered with this email')
            return redirect('login:frgtPwd')
    return redirect('login:log_in')
    # return redirect('login:chngPwd')
def enterOTP(request):
    if request.session.has_key('email'):
        return render(request, 'login/emailOTP.html', {'email': request.session['email']})
    return redirect('login:log_in')
def checkOTP(request):
    if request.method=='POST':
        print('coming here!')
        print(request.session['otp'])
        print(request.POST['otp'])
        if int(request.POST['otp'])==int(request.session['otp']):
            print('both are same')
            request.session['approved']=True
            return redirect('login:new_pwd')
        else:
            messages.info(request,'Invalid OTP')
            return render(request,'login/emailOTP.html',{'email': request.session['email']})
    # request.session['email'] =request.session['email'] = None
    return redirect('login:log_in')

# @login_required
def checkOldPwd(request):
    if request.user.is_authenticated:
        usr=User.objects.get(email=request.user.email)
        if usr.password == request.POST['passwrd']:
            request.session['approved'] = True
            request.session['email'] = request.user.email
            return redirect('login:new_pwd')
        else:
            messages.info(request,'Invalid password')
            return redirect('login:chng_pwd')
    return redirect('login:log_in')

def newPassword(request):
    if request.session.has_key('approved'):
        return render(request, 'login/newPwd.html')
    return redirect('login:log_in')

def logoutview(request):
    logout(request)
    # request.user=''
    return redirect('login:log_in')

def changePwd(request):
    if request.user.is_authenticated:
        return render(request,'login/changePwd.html')
    return redirect('login:log_in')

def savenewpwd(request):
    print('save new password')
    if request.method=='POST':
        if request.session.has_key('email'):
            # try:
            print('if part')
            usr=User.objects.get(email=request.session['email'])
            usr.password=request.POST['passwd']
            usr.save()
            messages.info(request, 'Password changed successfully.')
            print('before login')
            usrDjango=UserModel.objects.get(id=usr.id)
            login(request,usrDjango)
            print('after login')
            if usr.userroleid==Userrole.objects.get(roleid=3):
                print('buyer userrole')
                return redirect('signin:home')
            else:
                print('admin userrole')
                return redirect('admm:index')
            # except:
            #     messages.info(request,'Error changing password.')
    return redirect('login:log_in')

def loginview(request):
    if request.user.is_authenticated:
        return render(request,'login/logoutfirst.html',{'items':Cartdetail.objects.filter(auth_user=User.objects.get(email=request.user.email)).count})

    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        # nwpassword=
        # user=authenticate(username=username,password=password)
        try:
            userObj=UserModel.objects.get(email=email,password=password)
            # ourModelusr=User.objects.get(email=email,password=password)
            # print(ourModelusr.userroleid)
            # if user is not None:
            # messages.info(request,'coming here..')
            if userObj.is_active:
                login(request, userObj)
                ourModelusr = User.objects.get(id=userObj.id)
                if ourModelusr.userroleid.roleid == 3:
                    return redirect('signin:home')
                return redirect('admm:index')
            messages.info(request,'User is locked.')
        except ObjectDoesNotExist:
            messages.info(request,'Invalid username or password.')
        # return redirect('login:login')

    return render(request,'login/loginPage.html')

class AuthFormView(View):
    form_class=AuthForm
    template_name='login/loginPage.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        try:
            if form.is_valid():
            # user=form.save(commit=False)
            #cleaned (normalized) data
            # username = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user.set_password(password)
            # username=form.cleaned_data['username']
            # password=form.cleaned_data['password']
            # user = authenticate(username=username,password=password)
            # user = UserModel.objects.get(username=username)
            # if user.username == 'virajchetan':
                #if user.is_active:
                # login(request, user)
            # messages.info(request,str(user.email))
                # messages.info(request,str(password))
                # return redirect('admm:index')
                messages.info(request,'ehy')
        except Exception as e:
            messages.info(request,e)
        return redirect('login:login')
    # return render()

class UserFormView(View):
    form_class=UserForm
    template_name='login/loginPage.html'

    #display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():

            user=form.save(commit=False)

            #cleaned (normalized) data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            #returns user objects if credentials are correct
            user=authenticate(email=email,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('admm:index')
        return redirect('login:login')

























