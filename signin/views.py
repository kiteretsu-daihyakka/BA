import os
from django.shortcuts import render,redirect
from django.db.models import Max,Sum
from django.http import HttpResponse
from signin.models import *
from django.views.generic import CreateView
from django.contrib.auth import login,logout
from django.contrib.auth.models import User as SysUser,auth
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min
from django.http import FileResponse,JsonResponse
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
# Create your views here.
import datetime
from django.contrib.sessions.models import Session
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch, mm
# from django.conf import settings
# from ..BoardingAlleyWeb.settings import BASE_DIR

def cityselection(request):
   pass

def header(request):
    items = Cartdetail.objects.filter(auth_user=request.user.id).count()
    return render(request,'sigin/header.html',{"items":items})

def home(request):
    categories = Category.objects.all()
    cities = City.objects.all()
    if request.user.is_authenticated:
        items = Cartdetail.objects.filter(auth_user=request.user.id).count()
        return render(request,'signin/index.html',{"cities":cities,"categories":categories,"items":items})
    #return render(request,'signin/shop.html')
    else:
        return render(request,'signin/index.html',{"cities":cities,"categories":categories})

def signup_buyer(request):
    cities = City.objects.all()
    areas = Area.objects.all()
    docs=Sellerdoclist.objects.all()
    if request.method == 'POST':
        firstname_buyer = request.POST['f-name_reg_buyer']
        lastname_buyer = request.POST['l-name_reg_buyer']
        email_buyer = request.POST['email_reg_buyer']
        passwd_buyer = request.POST['passwd_reg_buyer']
        mo_no_buyer = request.POST['mo-no_buyer']
        sec_q = request.POST['sec_que_buyer']
        sec_ans = request.POST['sec_ans_buyer'] 
        area = Area.objects.get(id=int(request.POST['area_buyer']))
        roleid = Userrole.objects.get(roleid=3)
        user =  User(first_name=firstname_buyer,last_name=lastname_buyer,email=email_buyer,password=passwd_buyer,mobileno=mo_no_buyer,is_superuser=False,is_active=1,islocked=False,secque=sec_q,areaid=area,secqans=sec_ans,userroleid=roleid)
        user.is_staff=0
        user.date_joined=datetime.datetime.now()
        user.save()
        return redirect('/')
    else:
        return render(request,'signin/signup.html',{"cities":cities,"areas":areas,"docs":docs})

def signup_seller(request):
    cities = City.objects.all()
    areas = Area.objects.all()
    if request.method == 'POST':
        firstname_seller = request.POST['f-name_reg_seller']
        lastname_seller = request.POST['l-name_reg_seller']
        email_seller = request.POST['email_reg_seller']
        passwd_seller = request.POST['passwd_reg_seller']
        mo_no_seller = request.POST['mo-no_seller']
        sec_q = request.POST['sec_que_seller']
        sec_ans = request.POST['sec_ans_seller']
        area = Area.objects.get(id=int(request.POST['area_seller']))
        roleid = Userrole.objects.get(roleid=2)


        user =  User(first_name=firstname_seller,last_name=lastname_seller,email=email_seller,password=passwd_seller,mobileno=mo_no_seller,is_superuser=False,is_active=1,islocked=False,secque=sec_q,areaid=area,secqans=sec_ans,userroleid=roleid)
        user.is_staff = 0
        user.addressline1=request.POST['address']
        user.date_joined=datetime.datetime.now()
        user.save()
        # docName=Sellerdoclist.objects.values('docname')
        # print(docName)
        for filename,file in request.FILES.items():
            print(filename)
            print(file)
            uplddDocDtl=Sellerdocdetail(auth_user=user,docpath=file,sellerdoclist_docid=Sellerdoclist.objects.get(docname=filename))
            uplddDocDtl.save(force_insert=True)
        # for filename, file in request.FILES.items():
        #     # for i in range(adv_imgs_count):
        #     # print(filename)
        #
        #     docdetail = Sellerdocdetail(sellerdoclist_docid=Sellerdoclist.objects.get(docname='Aadhar card'),docpath=filename)
        #     # docdetail = Advimgs(id=advObj, adv_img=file)
        #     #
        #     # if objTmp['id__max'] == None:
        #     #     objTmp['id__max'] = 0
        #     # obj.id = objTmp['id__max'] + 1
        #     # print(new_advimg.adv_img2)
        #     docdetail.save(force_insert=True)
            # new_advimg.save(force_insert=True)

        # docdetail = Sellerdocdetail(id=User.objects.get(id=1), docpath=doc)
        # docdetail.save()

        return redirect('/')
    else:
        return render(request,'signin/signup.html',{"cities":cities,"areas":areas})

def loginview(request):
        if request.method == 'POST':
            email2=request.POST['email']
            password2=request.POST['psw']
            try:
                user=User.objects.get(email=email2,password=password2)
                auth.login(request,user)
                return redirect('/')
            except ObjectDoesNotExist:
                return render(request,'signin/index.html',{"invalid_log":"Invalid credentials"})
        else:
            return redirect('/')



def logoutview(request):
    auth.logout(request)
    return redirect('login:log_in')
#sub category wise product
def product_filter(request,subcat_id):
    subcat=Subcategory.objects.get(id=subcat_id)
    advs = subcat.advertisement_set.all()
    subcats=Subcategory.objects.filter(catid=subcat.catid)
    cat = subcat.catid
    for adi in advs:
        adi.startsfrm=adi.durationwisepricing_set.all().aggregate(Min('price'))['price__min']
        adi.days=adi.durationwisepricing_set.all().aggregate(Min('noofdays'))['noofdays__min']
    #d_prices = Durationwisepricing.objects.filter()
    # advs=Advertisement.objects.none()
    # advs=[]
    # for sub_cat in subcats:
        # advs.append(sub_cat.advertisement_set.all())
    # advs = Advertisement.objects.filter(subcategory_subcatid=)
    #subcategor = advs.subcategory_set.all()
    #result = Subcategory.objects.values('subcatname')
    #subcategories = Subcategory.objects.all()
    #result  = advs.union(subcategories)
    #ad_areas = Advertisement.objects.get(area_areaid=) 
    #products = Advertisement.objects.all()
    items = Cartdetail.objects.filter(auth_user=request.user.id).count()
    return render(request,'signin/shop.html',{"subcats":subcats,"advs":advs,"cat":cat,"items":items})

# category wise product bydefault
def product(request,cat_id):
    cat=Category.objects.get(id=cat_id)
    subcats = cat.subcategory_set.all()

    
    # advs=Advertisement.objects.none()
    advs=[]
    for sub_cat in subcats:
        for ad in sub_cat.advertisement_set.all():
            advs.append(ad)
    for adi in advs:
        adi.startsfrm=adi.durationwisepricing_set.all().aggregate(Min('price'))['price__min']
        adi.days=adi.durationwisepricing_set.all().aggregate(Min('noofdays'))['noofdays__min']
        # d_prices.append(Durationwisepricing.objects.filter(advertisement_advid=adi.advid))
        #for i in d_prices:
            #print(i)
        #for j in i:
        #print(j.price)
            #pr.append(j.price)
    
    #mpr = min(pr)
    #print(mpr)
    # advs = Advertisement.objects.filter(subcategory_subcatid=)
    #subcategor = advs.subcategory_set.all()
    #result = Subcategory.objects.values('subcatname')
    #subcategories = Subcategory.objects.all()
    #result  = advs.union(subcategories)
    #ad_areas = Advertisement.objects.get(area_areaid=) 
    #products = Advertisement.objects.all()
    items = Cartdetail.objects.filter(auth_user=request.user.id).count()
    return render(request,'signin/shop.html',{"subcats":subcats,"advs":advs,"cat":cat,"items":items})

def addcart(request,adv_id):
    if request.user.is_authenticated:
        adv=Advertisement.objects.get(advid=adv_id)
        usr=User.objects.get(id = request.user.id)
        if Cartdetail.objects.filter(id = adv,auth_user = usr).exists():
            return HttpResponse("already added")
        else:
            cartdetail = Cartdetail(id = Advertisement.objects.get(advid=adv_id),price =2000,auth_user = User.objects.get(id = request.user.id))
            cartdetail.save()
            return HttpResponse("Product added successful")
    else:
        return HttpResponse("please login")

def add_to_wishlist(request,adv_id):
    if request.user.is_authenticated:
        if Wishlistdetail.objects.filter(id = Advertisement.objects.get(advid=adv_id),auth_user = User.objects.get(id = request.user.id)).exists():
            return HttpResponse("already added")
        else:
            wishlistdetail = Wishlistdetail(id = Advertisement.objects.get(advid=adv_id),auth_user = User.objects.get(id = request.user.id))
            wishlistdetail.save()
            return HttpResponse("Product added successful")
    else:
        return HttpResponse(adv_id)

def product_detail(request,adv_id):
    ad = Advertisement.objects.get(advid=adv_id)
    price = ad.durationwisepricing_set.all()
    images = ad.advimgs_set.all()
    items = Cartdetail.objects.filter(auth_user=request.user.id).count()
    return render(request,'signin/product_detail.html',{"ad":ad,"price":price,"images":images,"items":items})

def profileview(request):
    if request.user.is_authenticated:
        print('coming here')
        pro = User.objects.get(id=request.user.id)
        items = Cartdetail.objects.filter(auth_user=request.user.id).count()
        return render(request,'signin/profile.html',{"pro":pro,"items":items})
    else:
        return render(request,'signin/index.html')

def profileedit(request):
    areas = Area.objects.all()
    if request.user.is_authenticated:
        pro = User.objects.get(id=request.user.id)
        items = Cartdetail.objects.filter(auth_user=request.user.id).count()
        return render(request,'signin/profile_edit.html',{"pro":pro,"areas":areas,"items":items})
    else:
        return render(request,'signin/profile.html')

def changePwd(request):
    # frmSignin=True
    return render(request,'login/changePwd.html',{'frmSignin':True})

#//Userr side here to..
@login_required
def validateCoupon(request):
    try:
        cpn=Coupondetail.objects.get(couponcode=request.GET.get('coupon'))
        if cpn.order_set.all().count()==1 or cpn.auth_user != get_object_or_404(User,email=request.user.email):
            msg=-1
        else:
            msg=cpn.coupondiscount
    except ObjectDoesNotExist:
        msg=-1
    data={
        'msg':msg
    }
    return JsonResponse(data)

@login_required
def cartAdvRemove(request,pk):
    cartAdv=Cartdetail.objects.get(id=int(pk))
    cartAdv.delete()
    return redirect('signin:cart')

@login_required
def fetch_booked_dates(request):
    lst=[]
    for odrDtl in Orderdetails.objects.filter(advertisement_advid__advid=request.GET.get('advid'),advenddate__gte = datetime.date.today()):
        if odrDtl.advstartdate < datetime.date.today():
            sdate=datetime.date.today()
        else:
            sdate=odrDtl.advstartdate
        sublst=[sdate,odrDtl.advenddate]
        lst.append(sublst)

    data={
        'lst_datesRange':lst,
    }
    return JsonResponse(data)

@login_required
def cart(request):
    print('coming in cart')
    if request.session.has_key('ordrPlaced'):
        if request.session['ordrPlaced'] == 1:
            request.session['ordrPlaced'] = 0
            return redirect('signin:cart')
    else:
        request.session['ordrPlaced'] = 0
    cartAdvs=Cartdetail.objects.filter(auth_user=get_object_or_404(User,email=request.user.email))
    # listOfAdv=[]
    # for adv in cartAdvs:
    #     listOfAdv.append(str(adv.id))
    # for adv in cartAdvs:
        # adv.offers=adv.id.durationwisepricing_set.all()
    # context=Cartdetail.advertisement_set.filter(auth_user=get_object_or_404(User,email=request.user.email))
    return render(request,'signin/cart.html',context={'cartAdvs':cartAdvs,'items':cartAdvs.count})

# @login_required
# def saveCart(request,cnt):
#     for i in range(1,cnt+1):
#         adv=get_object_or_404(Cartdetail,id=int(request.POST['adv'+str(i)]))
#         adv.startdate=request.POST['sdate'+str(i)]
#         adv.enddate=request.POST['edate'+str(i)]
#         adv.price=request.POST['price'+str(i)]
#         adv.save()
#     if request.POST['cpnCodeInput'] != '':
#         request.session['cpnId']=Coupondetail.objects.get(couponcode=request.POST['cpnCodeInput']).id
#     return redirect('signin:ordrSummery')

@login_required
def ordrSuccess(request):
    if request.session.has_key('ordrPlaced'):
        if request.session['ordrPlaced'] == 1:
            return render(request,'signin/ordrPlaced.html',context={'items':Cartdetail.objects.filter(auth_user=User.objects.get(id=request.user.id)).count(),'odrId':request.session['odrId']})
    return redirect('signin:cart')

@login_required
def ordrSummery(request):
    if request.method == 'POST':
        if 'odrPlaced' in request.POST:
            if request.POST['odrPlaced'] == 1:
                return redirect('signin:cart')
        print('coming in summery')
        if request.session.has_key('ordrPlaced'):
            if request.session['ordrPlaced'] == 1:
                request.session['ordrPlaced'] = 0
                return redirect('signin:cart')
        else:
            request.session['ordrPlaced'] = 0

        # cpnDiscount=None
        # if request.POST['cpnCodeInput'] != '':
        #     cpnDiscount=Coupondetail.objects.get(couponcode=request.POST['cpnCodeInput']).coupondiscount

        ttlDscnt=float(request.POST['ttlDscntPrice'])
        cartAdvs = Cartdetail.objects.filter(auth_user=get_object_or_404(User, email=request.user.email))

        i = 0
        for adv in cartAdvs:
            i += 1
            adv.startdate = datetime.datetime.strptime(request.POST['sdate' + str(i)],'%d-%m-%Y')
            adv.enddate = datetime.datetime.strptime(request.POST['edate' + str(i)],'%d-%m-%Y')
            adv.price = request.POST['price' + str(i)]
            adv.save()
        return render(request,'signin/ordrSummery.html',{'cartAdvs':cartAdvs,'cpn':'cpnDiscount','ttlDscnt':ttlDscnt,'items':cartAdvs.count})
    else: #if getting 'me' direct without following procedure cart->orderSummery.. go to cart!
        return redirect('signin:cart')

@login_required
def saveOrdr(request):
    if request.method=='POST':
        objTmp = Order.objects.aggregate(Max('id'))
        if objTmp['id__max'] == None:
            objTmp['id__max'] = 0
        newOrdr = Order(id=objTmp['id__max'] + 1,auth_user=User.objects.get(email=request.user.email),
                        orderdatetime=datetime.datetime.now(),discountamount=float(request.POST.get('dscntAmnt')),emipayment=0,gst_amount=0)
        if request.POST['cpnCodeInput'] != '':
            newOrdr.coupondetail_couponid=Coupondetail.objects.get(couponcode=request.POST['cpnCodeInput'])
        newOrdr.save()

        lst = (request.POST['advIdList']).split(' ')
        for advId in lst:
            if advId is not '':
                cartObj=Cartdetail.objects.get(id=int(advId))
                newOrdrDtl =Orderdetails(id=newOrdr, advertisement_advid=Advertisement.objects.get(advid=cartObj.id.advid),
                             advprice=cartObj.price, advstartdate=cartObj.startdate, advenddate=cartObj.enddate)
                newOrdrDtl.save(force_insert=True)
                cartObj.delete()
        request.session['ordrPlaced'] = 1
        request.session['odrId']= newOrdr.id
        return redirect('signin:ordrPlacedMsg')
    else: #if getting 'me' direct without following procedure cart->orderSummery.. go to cart!
        return redirect('signin:cart')
    # return render(request,'signin/ordrPlaced.html',context={'items':Cartdetail.objects.filter(auth_user=User.objects.get(id=request.user.id)).count()})
#..here//

@login_required
def odrReceipt(request,pk):

    order = Order.objects.get(id = pk)
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    logo=os.path.join(BASE_DIR, 'admm/static/admm/images/BoardingAlleyLogo.png')#'./static/signin/images/b1.jpg' 
    

    lst = [[Image(logo,width=200,height=50)],['Order Booking Receipt'],['CUSTOMER ID',request.user.id],['ORDER ID',order.id],['ORDER DATE TIME',datetime.datetime.strftime(order.orderdatetime, '%d %b,%Y %H:%M:%S')]
           ,['SR NO.','ADVERTISEMENT DETAIL','BOOKING DATES','PRICE']]

    styles = getSampleStyleSheet()
    ttlAmnt=0
    indx = 0
    for odr in order.orderdetails_set.all():
        if odr.quantity==0:
            random='Reg. No.: '+odr.advertisement_advid.advregno
        else:
            random='Quantity: '+str(odr.quantity)

        #get well soon.....................................................................adff..323e........
        state=''
        city=''
        area=''
        if odr.advertisement_advid.city_cityid is not None:
            city=odr.advertisement_advid.city_cityid.cityname
        if odr.advertisement_advid.city_cityid is not None:
            city = odr.advertisement_advid.city_cityid.cityname
        if odr.advertisement_advid.city_cityid is not None:
            city=odr.advertisement_advid.city_cityid.cityname

        indx = indx + 1
        sublst = [str(indx)+'\n',Paragraph('Size: '+str(odr.advertisement_advid.height)+' x '+str(odr.advertisement_advid.width)+'    '+random+'\n\nAddress: '+odr.advertisement_advid.addressline1+area+city+state, styles['Normal']),str(odr.advstartdate)+' To '+str(odr.advenddate)+'\n',str(odr.advprice)+'\n']
        # [,,odr.quantity,]
        lst.append(sublst)
        ttlAmnt+=odr.advprice
    addDscnt = 0
    print(order.coupondetail_couponid)
    if order.coupondetail_couponid is not None:
        addDscnt=(ttlAmnt*order.coupondetail_couponid.coupondiscount)/100
    lst.append(['TOTAL DISCOUNT',order.discountamount+addDscnt])
    lst.append(['GST AMOUNT',order.gst_amount])
    lst.append(['TOTAL AMOUNT PAID',ttlAmnt-addDscnt])
    lst.append(['Date-Time: '+str(datetime.datetime.today())])

    # print(lst)
    #datetime.datetime.strftime(odr.orderdatetime, '%d %b,%Y %H:%M:%S')
    filename = 'OrderBookingReceipt.pdf'
    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter,
        title='Order Booking Receipt'
    )
    style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('SPAN', (0, 1), (-1, 1)),
        ('SPAN', (1, 2), (-1, 2)),
        ('SPAN', (1, 3), (-1, 3)),
        ('SPAN', (1, 4), (-1, 4)),
        ('SPAN', (1, -4), (-1, -4)),
        ('SPAN', (1, -2), (-1, -2)),
        ('SPAN', (1, -3), (-1, -3)),
        ('SPAN', (0, -1), (-1, -1)),
        ('FONTSIZE', (0, 1), (0, 1), 20),

        ('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey),
        # ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),

        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 5), (1, -1), 'LEFT'),
        ('ALIGN', (1, -4), (1, -1), 'RIGHT'),
        ('ALIGN', (0, -1), (-1, -1),'RIGHT'),
        ('FONTSIZE', (0, 2), (-1, -1), 12),
        # ('RIGHTPADDING', (0, 1), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 35),
        ('BOTTOMPADDING', (0, 1), (0, 1), 35),
        ('GRID', (0, 2), (-1, -2), 0.25, colors.black)
    ])
    table = Table(lst)
    table.setStyle(style)
    elems = []
    # def get_python_image():
    #     if not os.path.exists(logo):
    #         response =
    
    
    elems.append(table)
    pdf.build(elems)

    return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)

def wishlist(request):
    print('coming in wishlist view')
    if request.user.is_authenticated:
        items = Cartdetail.objects.filter(auth_user=request.user.id).count()
        cartAdvs=Wishlistdetail.objects.filter(auth_user=get_object_or_404(User,email=request.user.email))
        # ads = []
        # adv = Advertisement.objects.filter(advid=9)
        #print(adv)
        #for ad in adv:
            #print(ad.area_areaid)
        #wili = Wishlistdetail.objects.filter(auth_user = User.objects.get(id = request.user.id))
        
        #for we in wili:
            #print(we.id)
            #ads.append(Advertisement.objects.filter(advid=(we.id)))

        return render(request,'signin/wishlist.html',{"cartAdvs":cartAdvs,"items":items})
    else:
    #   newitem = item.split(",")
        print('coming in else')
        if request.method == 'POST':
            print('coming in post if')
            itemval = request.POST['item']
            return HttpResponse(itemval)

        else:
            print('coming in post else notin')
            return HttpResponse('Notin')