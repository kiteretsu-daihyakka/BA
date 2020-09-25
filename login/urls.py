from django.urls import path
from . import views

app_name='login'

urlpatterns=[
    path('',views.loginview,name='log_in'),
    path('logout/',views.logoutview,name='logout'),
    # path('register/',views.UserFormView.as_view(),name='register'),
    # path('register/',views.UserFormView.as_view(),name='register'),
    path('forgotPassword/',views.frgtPwd,name='frgtPwd'),
    path('sendOTP/',views.sendOTP,name='send_otp'),
    path('checkOTP/',views.checkOTP,name='check_otp'),
    path('enterOTP/',views.enterOTP,name='enterOTP'),
    path('oldpwdcheck/',views.checkOldPwd,name='check_old_pwd'),
    path('newpassword/',views.newPassword,name='new_pwd'),
    path('changePassword/',views.changePwd,name='chng_pwd'),#Password change from user profile
    path('savenewpassword/',views.savenewpwd,name='savenewpwd'),
]