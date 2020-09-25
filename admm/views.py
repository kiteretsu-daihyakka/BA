from django.utils.dateparse import parse_datetime
import random
from django.views import generic
from .models import *
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.forms.models import model_to_dict

from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.apps import apps
from django.http import request, HttpRequest,HttpResponse
from .forms import *
from django.db.models import Max, Sum
from django.core.mail import send_mail
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse, JsonResponse
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required#,register.filter()
from django.db.models import Q

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen.canvas import Canvas
from BoardingAlleyWeb.settings import STATIC_URL as static
from BoardingAlleyWeb.settings import BASE_DIR


# Create your views here.


# def index(request):
#     return render(request,'admm/index.html')
# def detail(request):
#     all_adv=Advertisement._check_fields
#     adObj=Advertisement()
#     return render(request,'admm/detailPage.html')

# def getQueryString(request):
#    super.tmp= request.GET.get('objname', 'Area')

# def show(request,object_id):
#     object=FooForm(data=model_to_dict(Foo.objects.get(pk=object_id)))
#     return render_toresponse()
# def login(request):
#     return render(request,'admm/loginPage.html')

def reportCommon(request):
    pass

@login_required
def reportBasicViewLatestCopy(request,*ordrs):
    # try for orders report
    # buffer=io.BytesIO()
    # p=canvas.Canvas(buffer)
    # p.drawString(274,770,'Title')
    # p.setTitle('Order Report')
    # p.line(30,410,550,910)
    odrList = ordrs
    # if request.user.is_staff == 0:
    #     users = User.objects.filter(id=request.user.id)
    # else:
    #     users = User.objects.filter(is_staff=1)

    # odrs = Order.objects.all()
    # for odr in odrs:
    #     odrDtl = odr.orderdetails_set.first()
    #     if odrDtl.advertisement_advid.auth_user in users:
    #         odr.totalAmnt = (Orderdetails.objects.filter(id=odr, cancellationdatetime=None).aggregate(Sum('advprice')))[
    #             'advprice__sum']
    #         odr.noOfAdvs = Orderdetails.objects.filter(id=odr, cancellationdatetime=None).count()
    #         if odr.noOfAdvs is 0:
    #             continue
    #         odrList.append(odr)

    # else:
    #     odrs = Order.objects.all()
    #     for odr in odrs:
    #         odrDtl = odr.orderdetails_set.first()
    #         if odrDtl.advertisement_advid.auth_user in :
    #             odrList.append(odr)
    #
    #
    #     for admin in admsn:
    #         for adv in admin.advertisement_set.all():
    #             odrDtl=adv.orderdetails_set.all().first()
    #             odrList.append(odrDtl.id)
    # print(odrList)
    lst = [['Orders'],
           ['SR\nNO.', 'ORDER\nID','NO. OF\nADVERTISEMENT', 'ORDER\nDATE TIME', 'DISCOUNT\nAMOUNT', 'GST\nAMOUNT', 'TOTAL\nAMOUNT',
            'BUYER\n']]
    indx = 0
    for odr in odrList:
        indx = indx + 1
        sublst = [indx,odr.id, odr.noOfAdvs, datetime.datetime.strftime(odr.orderdatetime, '%d %b,%Y %H:%M:%S'),
                  odr.discountamount, odr.gst_amount, odr.totalAmnt,
                  odr.auth_user.first_name + '\n' + odr.auth_user.last_name]
        lst.append(sublst)
    print(lst)
    # p.

    # data=[
    #     ['1','sahil'],
    #     ['2','viraj'],
    #     ['3','apu']
    # ]
    filename = 'report.pdf'
    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter,
        title='Orders'
    )
    style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('FONTSIZE', (0, 0), (0, 0), 20),

        ('BACKGROUND', (0, 1), (-1, 1), colors.green),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        # ('RIGHTPADDING', (0, 1), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 7),
        # ('TOPPADDING', (0, 2), (-1, 2), 5),
        ('BOTTOMPADDING', (0, 0), (0, 0), 35),
        ('GRID',(0,1),(-1,-1),0.25,colors.black)
    ])

    table = Table(lst)
    table.setStyle(style)
    elems = []
    elems.append(table)

    pdf.build(elems)

    return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)

@login_required
def reportOrders(request):
    # try for orders report
    # buffer=io.BytesIO()
    # p=canvas.Canvas(buffer)
    # p.drawString(274,770,'Title')
    # p.setTitle('Order Report')
    # p.line(30,410,550,910)
    flag = int(request.POST.get('isServed', default=0))
            # objects = Order.objects.all()
            # if flag == 1:
            #
            #     ordrObjects=Order.objects.all()
            # elif flag == 0:
    ordrObjects = Order.objects.all()
    if request.user.is_staff:
        users = User.objects.filter(is_staff=1)
    else:
        users = User.objects.filter(id=request.user.id)
    lst_ordrObjects = []
    title=None
    if flag == 0:
        title='Orders\n\n(Not Served)'
        for ordr in ordrObjects:
            if ordr.orderdetails_set.filter(served=0,
                                            cancellationdatetime=None).count() == 0 or ordr.orderdetails_set.all().first().advertisement_advid.auth_user not in users:
                continue
            ordr.totalAmnt = \
                (Orderdetails.objects.filter(id=ordr, cancellationdatetime=None).aggregate(Sum('advprice')))[
                    'advprice__sum']
            ordr.noOfAdvs = Orderdetails.objects.filter(id=ordr, cancellationdatetime=None).count()
            lst_ordrObjects.append(ordr)
    elif flag == 1:
        title = 'Orders\n\n(Served)'
        for ordr in ordrObjects:
            if ordr.orderdetails_set.filter(served=1,
                                            cancellationdatetime=None).count() == ordr.orderdetails_set.all().count() and ordr.orderdetails_set.all().first().advertisement_advid.auth_user in users:
                ordr.totalAmnt = \
                    (Orderdetails.objects.filter(id=ordr, cancellationdatetime=None).aggregate(Sum('advprice')))[
                        'advprice__sum']
                ordr.noOfAdvs = Orderdetails.objects.filter(id=ordr, cancellationdatetime=None).count()
                lst_ordrObjects.append(ordr)
                        # else:
                        #     odrs = Order.objects.all()
                        #     for odr in odrs:
                        #         odrDtl = odr.orderdetails_set.first()
                        #         if odrDtl.advertisement_advid.auth_user in :
                        #             odrList.append(odr)
                        #
                        #
                        #     for admin in admsn:
                        #         for adv in admin.advertisement_set.all():
                        #             odrDtl=adv.orderdetails_set.all().first()
                        #             odrList.append(odrDtl.id)
                        # print(lst_ordrObjects)
    lst = [[title],
           ['SR\nNO.', 'ORDER\nID','NO. OF\nADVERTISEMENT', 'ORDER\nDATE TIME', 'DISCOUNT\nAMOUNT', 'GST\nAMOUNT', 'TOTAL\nAMOUNT',
            'BUYER\n']]
    indx = 0
    for odr in lst_ordrObjects:
        indx = indx + 1
        sublst = [indx,odr.id, odr.noOfAdvs, datetime.datetime.strftime(odr.orderdatetime, '%d %b,%Y %H:%M:%S'),
                  odr.discountamount, odr.gst_amount, odr.totalAmnt,
                  odr.auth_user.first_name + '\n' + odr.auth_user.last_name]
        lst.append(sublst)
    print(lst)
                # p.

                # data=[
                #     ['1','sahil'],
                #     ['2','viraj'],
                #     ['3','apu']
                # ]
    filename = 'report.pdf'
    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter,
        title='Orders'
    )
    style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('FONTSIZE', (0, 0), (0, 0), 20),

        ('BACKGROUND', (0, 1), (-1, 1), colors.green),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        # ('RIGHTPADDING', (0, 1), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 7),
        # ('TOPPADDING', (0, 2), (-1, 2), 5),
        ('BOTTOMPADDING', (0, 0), (0, 0), 35),
        ('GRID',(0,1),(-1,-1),0.25,colors.black)
    ])
    table = Table(lst)
    table.setStyle(style)
    elems = []
    elems.append(table)

    pdf.build(elems)
        # p.drawCentredString(274,800,'Orders')
        # p.showPage()
        # p.save()
        # buffer.seek(0)

        # return FileResponse(buffer,as_attachment=False,filename=filename)
    return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)


@login_required
def reportUsers(request, pk):
    users = User.objects.filter(userroleid=pk)

    role = None
    try:
        role = Userrole.objects.get(roleid=pk).rolename + 's List'
    except:
        pass

            # lst = [[role],['SR\nNO.', 'NAME', 'EMAIL', 'MOBILE\nNO.', 'IS\nLOCKED', 'ADDRESS', 'AREA', 'CITY']]#, 'LAST\nLOGIN']]
    lst = [[role],
           ['SR\nNO.', 'NAME\n', 'EMAIL\n', 'MOBILE\nNO.', 'ADDRESS\n', 'AREA\n', 'CITY\n']]  # , 'LAST\nLOGIN']]

    if pk == 1:
        lst[1].append('BRANCH ID\n')

    styles = getSampleStyleSheet()

    indx = 0
    for usr in users:
        indx = indx + 1
            # [str(indx),
        sublst = [indx, usr.first_name + '\n' + usr.last_name, usr.email, usr.mobileno,
                  Paragraph(usr.addressline1, styles['Normal']), usr.areaid.areaname,
                  usr.areaid.city_cityid.cityname]  # ,(datetime.datetime.strftime(usr.last_login,'%d %b,%Y %H:%M:%S'))]
        if pk == 1:
            sublst.append(usr.branchid)
        lst.append(sublst)
    print(lst)

    filename = 'report.pdf'
    pdf = SimpleDocTemplate(
        filename,
        # buffer=buffer,
        pagesize=letter,
        title=role
    )

        # buffer = io.BytesIO()
        # p=canvas.Canvas()
        # p.drawString(274,770,'Title')
        # p.setTitle('Order Report')
        # canv = canvas.Canvas(buffer)
        # canv.setTitle('Users')
        # canv.drawString(274, 770, 'Title')
        # canv.showPage()
        # canv.save()
        # buffer.seek(0)

        # pdf..setTitle('Fallin')
        # pdf.canv.save()

    style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('FONTSIZE', (0, 0), (0, 0), 20),

        ('BACKGROUND', (0, 1), (-1, 1), colors.green),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        # ('FONTSIZE', (5, 1), (5, -1), 10),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 7),

        # sr no. left right padding reducing
        # ('LEFTPADDING', (0,0),(-1,-1), 0),
        # ('PADDING',(5,1),(5,-1), 0),

        ('TOPPADDING', (0, 1), (-1, 1), 7),
        ('BOTTOMPADDING', (0, 0), (0, 0), 35),
        ('GRID',(0,1),(-1,-1),0.25,colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),

        # ('WIDTH', (5, 1), (5, -1), [1.9*inch]*5),
    ])

    # table=Table(lst)
    if pk==1:
        table = Table(lst, colWidths=(10 * mm, None, None, None, 40*mm, None, None,None))
    else:
        table = Table(lst, colWidths=(10 * mm, None, None, None, 40 * mm, None, None))
    table.setStyle(style)
    elems = []

    # elems.append(['Users']) #doesn't work

    elems.append(table)

    pdf.build(elems)
    # return FileResponse(buffer, as_attachment=False, filename=filename)
    return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)


@login_required
def checkAdvRegNo(request):
    count = Advertisement.objects.filter(advregno=request.GET.get('regNoPreCheck')).count()
    # print(obj)
    # result=1
    return JsonResponse(data={'count': count})


@login_required
def subCatInit(request):
    cat = Category.objects.get(id=int(request.GET.get('id')))
    subCats = list(cat.subcategory_set.values('id', 'subcatname', 'commission'))

    # print(subCats)
    # data=serializers.serialize('json',subCats)
    # print('heythere')

    data = {
        'subCats': subCats,
        'catid': cat.id,
    }
    # print(data)
    return JsonResponse(data)


# @login_required
# @register.filter(name='getkey')
# def getkey(value,arg):
    # if key:
    # return dict_data.get(key)
    # return value[arg]

@login_required
def commission(request):
    # @register.filter(name='getkey')
    # @register.filter(name='getkey')
    # def getkey(value, arg):
        # if key:
        # return dict_data.get(key)
        # return value[arg]

    # Order.objects.filter(orderdatetime=datetime.datetime.now())
    # print(request.POST.get('demandedSubCat',default=0))
    isSubCatDmanded=0
    if request.method == 'POST':
        isSubCatDmanded=int(request.POST.get('demandedSubCat','0'))
    if isSubCatDmanded == 1:
        # print(1)
        objects=Subcategory.objects.all()
    else:
        objects=Category.objects.all()
    # for date in datetime.date.month:
    # cmishanLst=[]
    # cmishanLst[0]=datetime.date.today()

    dtTmp=None
    rows=[]

    #subcategory or category wise cmishan, each ele(!date) will have total of commission for particular date
    scatWiseCmisnForDate={'date':None}
    for obj in objects:
        scatWiseCmisnForDate[obj.__str__()]=0
        # print(obj.__str__())


    i=1
    for odr in Order.objects.all().order_by('orderdatetime'):
        # print(str(i)+'\n')
        if i==1:    #for first time save datetime of order in dtTmp
            dtTmp = datetime.datetime.strftime(odr.orderdatetime, '%d %b,%Y')
            # print('first time!')
                
        if datetime.datetime.strftime(odr.orderdatetime, '%d %b,%Y') != dtTmp or i==Order.objects.all().count():  #going only if current date is different from previous one in dtTmp,then saving the row in row[]
            scatWiseCmisnForDate['date']=dtTmp
            scatWiseCmisnForDate['total'] = 0
            for obj in objects:
                scatWiseCmisnForDate[obj.__str__()] = round(scatWiseCmisnForDate[obj.__str__()],2)
                scatWiseCmisnForDate['total'] += scatWiseCmisnForDate[obj.__str__()]
            scatWiseCmisnForDate['total'] = round(scatWiseCmisnForDate['total'],2)
            rows.append(scatWiseCmisnForDate)
            # print(scatWiseCmisnForDate)

            scatWiseCmisnForDate = {'date': None}
            for obj in objects:
                scatWiseCmisnForDate[obj.__str__()] = 0
            dtTmp = datetime.datetime.strftime(odr.orderdatetime, '%d %b,%Y')
            #scatWiseCmisnForDate=0,None & dtTmp(second group date) from now onwards!
            # print('saved to row!')

        for odrDtl in odr.orderdetails_set.all():
            print(str(odrDtl.id.id)+' '+str(odrDtl.advertisement_advid.advid))
            if odrDtl.advertisement_advid.auth_user.userroleid.roleid == 2 :
                sub_cat = odrDtl.advertisement_advid.subcategory_subcatid
                if isSubCatDmanded==1:
                    scatWiseCmisnForDate[sub_cat.__str__()]+=(odrDtl.advprice*100/118)*sub_cat.commission/100
                else:
                    scatWiseCmisnForDate[sub_cat.catid.__str__()] += (odrDtl.advprice * 100 / 118) * sub_cat.commission / 100
                # print(sub_cat.subcatname)
                # print('coming in cmishan count')

        i+=1
        # print(rows)

        # if odrDtl.advertisement_advid.auth_user.userroleid.roleid == 2:
        #     sub_cat=odrDtl.advertisement_advid.subcategory_subcatid
        #     odrDtl.cmishan=(odrDtl.advprice*100/118)*sub_cat.commission
        #     odrDtl.subCatName=sub_cat.subcatname
        #     selrOdrDtl.append(odrDtl)

    # i=1
    # cmishanLstSub = []
    # for cat in subCats:
    pdfFlag = int(request.POST.get('pdfDemanded',0))
    if pdfFlag == 1:
        head=['SR NO.','DATE']
        for obj in objects: #categories or subcategories
            head.append(str.upper(obj.__str__()))
        head.append('TOTAL')
        if isSubCatDmanded == 1:
            wise='(Subcategory Wise)'
        else:
            wise = '(Category Wise)'
        lst = [['Date:- '+str(datetime.datetime.now())],['Commission'+wise],head]

        # styles = getSampleStyleSheet()

        indx = 0
        for ro in rows:
            indx = indx + 1
            # [str(indx),
            sublst = [indx,ro['date']]  # ,(datetime.datetime.strftime(usr.last_login,'%d %b,%Y %H:%M:%S'))]
            for obj in objects:  # categories or subcategories
                if ro[obj.__str__()]==0:
                    ro[obj.__str__()]='-'
                sublst.append(ro[obj.__str__()])
            sublst.append(ro['total'])
            lst.append(sublst)

        filename = 'commissionReport.pdf'
        # canvas = Canvas(filename)
        # logo_path=BASE_DIR+'/admm/static/images/'+Company.objects.filter(id=1)[0].logopath
        # lst.append([canvas.drawImage(logo_path,500,800)])
        print(lst)

        pdf = SimpleDocTemplate(
            filename,
            # buffer=buffer,
            pagesize=letter,
            title='Commission Report',
        )
        style = TableStyle([
            ('SPAN', (0, 0), (-1, 1)),
            ('FONTSIZE', (0, 1), (-1, 1), 20),

            ('BACKGROUND', (0, 2), (-1, 2), colors.green),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 2), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            # ('FONTSIZE', (5, 1), (5, -1), 10),
            # ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 7),

            # sr no. left right padding reducing
            # ('LEFTPADDING', (0,0),(-1,-1), 0),
            # ('PADDING',(5,1),(5,-1), 0),

            #recent ('TOPPADDING', (0, 1), (-1, 1), 7),
            #recent ('BOTTOMPADDING', (0, 0), (0, 0), 35),
            ('GRID', (0, 2), (-1, -1), 0.25, colors.black),
            # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),

            # ('WIDTH', (5, 1), (5, -1), [1.9*inch]*5),
        ])

        table=Table(lst)
        # if pk == 1:
        #     table = Table(lst, colWidths=(10 * mm, None, None, None, 40 * mm, None, None, None))
        # else:
        #     table = Table(lst, colWidths=(10 * mm, None, None, None, 40 * mm, None, None))
        table.setStyle(style)
        elems = []

        # elems.append(['Users']) #doesn't work

        elems.append(table)

        pdf.build(elems)
        # return FileResponse(buffer, as_attachment=False, filename=filename)
        return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)

        # cmishanLstSub.append()
    # cmishanLst[1]= cmishanLstSub
    return render(request, 'admm/cmishanList.html',context={'objects':objects,'rows':rows,'isSubCatDmanded':isSubCatDmanded})
    # return render(request, 'admm/cmishanList.html',context={'objects':subCats})


# //Userr side here to..
@login_required
def validateCoupon(request):
    cpn = request.GET.get('coupon')
    print(cpn)
    print('hey')
    try:
        Coupondetail.objects.get(couponcode=str(cpn))
        msg = 'succeed'
        messages.info(request, msg)
    except ObjectDoesNotExist:
        msg = 'not succeed'
        messages.info(request, msg)
    data = {
        'msg': msg
    }
    return JsonResponse(data)


@login_required
def cartAdvRemove(request, pk):
    cartAdv = Cartdetail.objects.get(id=int(pk))
    cartAdv.delete()
    return redirect('admm:cart')


@login_required
def cart(request):
    cartAdvs = Cartdetail.objects.filter(auth_user=get_object_or_404(User, email=request.user.email))
    # listOfAdv=[]
    # for adv in cartAdvs:
    #     listOfAdv.append(str(adv.id))
    # for adv in cartAdvs:
    #     cartAdvs['dwps']=(adv.id.durationwisepricing_set.all())
    # context=Cartdetail.advertisement_set.filter(auth_user=get_object_or_404(User,email=request.user.email))
    return render(request, 'admm/cart.html', context={'cartAdvs': cartAdvs})


@login_required
def saveCart(request, cnt):
    for i in range(1, cnt + 1):
        adv = get_object_or_404(Cartdetail, id=int(request.POST['adv' + str(i)]))
        adv.startdate = request.POST['sdate' + str(i)]
        adv.enddate = request.POST['edate' + str(i)]
        adv.price = request.POST['price' + str(i)]
        adv.save()
    return redirect('admm:ordrSummery')


@login_required
def ordrSummery(request):
    cartAdvs = Cartdetail.objects.filter(auth_user=get_object_or_404(User, email=request.user.email))
    return render(request, 'admm/ordrSummery.html', {'cartAdvs': cartAdvs})


@login_required
def saveOrdr(request):
    objTmp = Order.objects.aggregate(Max('id'))
    if objTmp['id__max'] == None:
        objTmp['id__max'] = 0
    newOrdr = Order(id=objTmp['id__max'] + 1, auth_user=User.objects.get(email=request.user.email),
                    orderdatetime=datetime.datetime.now(), emipayment=0, gst_amount=0)
    newOrdr.save()
    ordrdAdvList = []
    lst = (request.POST['advIdList']).split(' ')
    for advId in lst:
        if advId is not '':
            ordrdAdvList.append(Cartdetail.objects.get(id=int(advId)))
    for adv in ordrdAdvList:
        newOrdrDtl = Orderdetails(id=newOrdr, advertisement_advid=adv.id,
                                  advprice=adv.price, advstartdate=adv.startdate, advenddate=adv.enddate)
        newOrdrDtl.save(force_insert=True)
    return redirect('admm:list_orders')


# ..here//


@login_required
def reportBasicView(request):
    # try for orders report
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    # p.drawString(274,770,'Title')
    p.setTitle('Order Report')
    # p.line(30,410,550,910)
    # odrList=Order.objects.values('id')
    # print(odrList)

    filename = 'order_report.pdf'
    data = [
        ['1', 'sahil'],
        ['2', 'viraj'],
        ['3', 'apu']
    ]
    p.drawCentredString(274, 800, 'Orders')
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=False, filename=filename)


#@login_required
    #def adminSellerProfile(request):
    # user=User.objects.get(id=request.user.id)
    # request.user.get_deferred_fields()
    #return render(request, 'admm/profile.html',context={'userForm':})

@login_required
def adminSellerProfile(request):
    return UserDetailAndUpdate.as_view()(request, pk=request.user.id)

class UserDetailAndUpdate(generic.UpdateView):
    #NOTE: Have template name as modelname_form.html 
    model = User
    def get_context_data(self, **kwargs):
        usr = User.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
            # extra_context = {'packHasAdvs': packDtlLst}
            # context['sar']=ar=usr.areaid
            # context['sct']=ct=usr.areaid.city_cityid
            # context['sst']=st=usr.areaid.city_cityid.state_stateid

        #documents for seller
        if usr.userroleid.roleid == 2 and Sellerdocdetail.objects.filter(auth_user=usr).count() < 3:
            context['sellerDocList']=Sellerdoclist.objects.values('docname')
        print(Sellerdoclist.objects.values_list('docname',flat=True))
        print('hi')
        context['usr'] = usr
        context['Areas'] = (Area.objects.values('id','areaname').filter(city_cityid=usr.areaid.city_cityid))
        context['Cities'] = (City.objects.values('id','cityname').filter(state_stateid=usr.areaid.city_cityid.state_stateid))
        context['States'] = (State.objects.values('id','statename'))
            # ct =
            # arObjs = list(ct.area_set.values('id', 'areaname'))

            # print('hi'+str(usrProfile.profile_pic)+'sahil')
        return context

    fields = ['first_name', 'last_name', 'email', 'mobileno', 'addressline1','areaid']
    success_url = reverse_lazy('admm:profile')
        # #new adminprofile2.0
        # class UserDetailAndUpdate(generic.UpdateView):
        #     model = User
        #
        #     def get_context_data(self, **kwargs):
        #
        #         usrProfile = User.objects.get(id=self.kwargs['pk'])
        #         context = super().get_context_data(**kwargs)
        #
        #         # extra_context = {'packHasAdvs': packDtlLst}
        #         # context = {}
        #
        #         context['profile_url'] = usrProfile.profile_pic
        #
        #         # print('hi'+str(usrProfile.profile_pic)+'sahil')
        #         return context
        #
        #     fields = [ 'first_name', 'last_name', 'email', 'date_joined']
        #     success_url = reverse_lazy('admm:profile2')

@login_required
def checkPassword(request):
    try:
        usr=User.objects.get(password=request.GET.get('pwd'),email=request.user.email)
        # print(usr.email+' '+usr.password)
        rslt=1
    except:
        rslt=0
    data={
        'result':rslt,
    }
    return JsonResponse(data) 

@login_required
def sellerDocsUpld(request):
    usr = User.objects.get(id=request.user.id)

    for filename, file in request.FILES.items():
        print(filename)
        obj = Sellerdocdetail(auth_user=usr,sellerdoclist_docid=Sellerdoclist.objects.get(docname=filename),docpath=file)
        obj.save(force_insert=True)
    
    return redirect('admm:profile')

@login_required
def chngPwd(request):
    return render(request,'login/changePwd.html')


def newPwd(request):
    isFrgt = int(request.POST.get('isFromFrgtPage', default=0))
    try:
        usr = User.objects.get(email=request.POST['email'], secque=request.POST['secque'],
                               secqans=request.POST['secans'])
        # if request.user.password==request.POST['passwrd'] & usr.secque== & usr.secqans==:
        if usr is not None:
            if isFrgt == 0:
                return render(request, 'login/newPwd.html')
            else:
                otp = random.randint(a=0, b=9999999999)
                send_mail(
                    'OTP to change your BoardingAlley Password',
                    "OTP is : " + str(otp),
                    usr.email,
                    [request.POST['email']],
                    fail_silently=False
                )
                return render(request, 'login/emailOTP.html', {'otp': otp})
    except ObjectDoesNotExist:
        messages.info(request, 'Invalid credentials.')
    if isFrgt == 1:
        return redirect('login:frgtPwd')
    return redirect('login:chngPwd')

@login_required
def markOdrDtlServed(request):
    try:
        Orderdetails.objects.filter(id=Order.objects.get(id=request.GET.get('odrId')),advertisement_advid=request.GET.get('advId')).update(served=1)
        rslt=1
    except:
        rslt=0
    data={
        'result':rslt,
    }
    return JsonResponse(data)

@login_required
def listOrders(request):#order details baby!
    flag = int(request.POST.get('srvdOnes', default=0))

    if request.user.is_staff:
        users=User.objects.filter(is_staff=1)
    else:
        users=User.objects.filter(id=request.user.id)

    servedNotTitl=None
    ordrDtlObjects = []
    if flag == 0:
        servedNotTitl = '(Not Served)'
        for odr in Orderdetails.objects.filter(served=0, cancellationdatetime=None):
            if odr.advertisement_advid.auth_user in users:
                ordrDtlObjects.append(odr)

    elif flag == 1:
        servedNotTitl = '(Served)'
        for odr in Orderdetails.objects.filter(served=1,cancellationdatetime=None):
            if odr.advertisement_advid.auth_user in users:
                ordrDtlObjects.append(odr)

    if int(request.POST.get('pdfDemanded',default=0))==1:

        lst = [['Orders\n\n'+servedNotTitl],
               ['SR\nNO.', 'ADV.\nID', 'ADDRESS\n', 'AREA\n', 'CITY\n','PRICE\n','START\nDATE','END\nDATE','QUANTITY\n']]

        indx = 0
        styles=getSampleStyleSheet()

        for odr in ordrDtlObjects:
            indx = indx + 1

            # if odr.reasonofcancellation is None:
            #     odr.reasonofcancellation=''
            # addressline1=odr.advertisement_advid.addressline1
            # if addressline1 is None:
            #     addressline1='-'
            # area=odr.advertisement_advid.area_areaid
            # if area is None:
            #     area = '-'
            # if odr.advertisement_advid.city_cityid is None:
            #     odr.advertisement_advid.city_cityid = '-'
            # if odr.quantity is None:
            #     odr.quantity='-'

            sublst = [indx, odr.advertisement_advid.advid, Paragraph(odr.advertisement_advid.addressline1,styles['Normal']),odr.advertisement_advid.area_areaid,odr.advertisement_advid.city_cityid,odr.advprice,odr.advstartdate,odr.advenddate,odr.quantity]
            lst.append(sublst)
        endRowTxt = '---------End---------'
        if len(ordrDtlObjects) is 0:
            endRowTxt='No Orders'
        lst.append([endRowTxt])
        print(lst)

        filename = 'orders.pdf'
        pdf = SimpleDocTemplate(
            filename,
            pagesize=letter,
            title='Orders'
        )
        style = TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTSIZE', (0, 0), (0, 0), 20),

            ('BACKGROUND', (0, 1), (-1, 1), colors.green),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),

            ('BOTTOMPADDING', (0, 1), (-1, 1), 7),

            ('TOPPADDING', (0, 1), (-1, 1), 7),

            #LAST ROW
            ('TOPPADDING', (0, -1), (-1, -1), 15),
            ('SPAN', (0, -1), (-1, -1)),
            ('FONTSIZE', (0, 1), (-1, -1), 12),


            ('BOTTOMPADDING', (0, 0), (0, 0), 35),
            ('GRID', (0, 1), (-1, len(lst)-2), 0.25, colors.black),
        ])
        # table=Table(lst)
        # if flag == 1:
        table = Table(lst, colWidths=(13 * mm, None, 50*mm, None, None, None, None,None,None))
        # else:
        #     table = Table(lst, colWidths=(13 * mm, None, None, None, None))

        table.setStyle(style)
        elems = []
        elems.append(table)

        pdf.build(elems)

        return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)

    return render(request, 'admm/orderList.html', {'ordrObjects': ordrDtlObjects, 'flagIsSrvd': flag})


@login_required
def listCncldOrdrs(request):
    flag = int(request.POST.get('flagRforN', default=0))
    if request.user.is_staff:
        users=User.objects.filter(is_staff=1) #admins
    else:
        users=User.objects.filter(id=request.user.id) #one seller

    tmpOdrObj=None
    lst_objects=[]
    servedNotTitl=None
    if flag == 1:
        servedNotTitl = '(Refunded)'
        for obj in Orderdetails.objects.filter(~Q(cancellationdatetime=None), ~Q(refundedamount=None)):
            if tmpOdrObj==obj.id or obj.advertisement_advid.auth_user in users:
                lst_objects.append(obj)
                tmpOdrObj=obj.id
    elif flag == 0:
        servedNotTitl = '(Not Refunded)'
        for obj in Orderdetails.objects.filter(~Q(cancellationdatetime=None), refundedamount=None):
            if tmpOdrObj==obj.id or obj.advertisement_advid.auth_user in users:
                lst_objects.append(obj)
                tmpOdrObj = obj.id
    # lst_ordrObjects = []
    # for ordr in objects:
    #     if ordr.orderdetails_set.filter(cancellationdatetime=None).count() == 0:
    #         # lst_ordrObjects.remove(ordr)
    #         continue
    #     ordr.totalAmnt = (Orderdetails.objects.filter(id=ordr, cancellationdatetime=None).aggregate(Sum('advprice')))[
    #         'advprice__sum']
    #     ordr.noOfAdvs = Orderdetails.objects.filter(id=ordr, cancellationdatetime=None).count
    #     lst_ordrObjects.append(ordr)
    # for ordr in objects:
    # odrDtls=Orderdetails.objects.all()
    # for odr_dtl in odrDtls:
    #     odr_dtl.cancellationofordadv_set.all()
    # ordr.oId=oIds.id

    # print(Objects)
    # for ordr in Objects:
    #     for odtl in ordr.orderdetails_set.all():
    #         ordr.ordrId = (Order.objects.get(id=odtl.id[0],advertisement_advid=ordr.advrtid[0]))

    if int(request.POST.get('demandedPDF',default=0))==1:
        lst = [['Cancelled Orders\n\n'+servedNotTitl],
               ['SR\nNO.', 'ORDER\nID', 'CANCEL.\nADV. ID', 'CANCEL.\nDATE TIME', 'REASON OF\nCANCEL.']]
        if flag==1:
            lst[1].append('REFUND\nDATE TIME')
            lst[1].append('REFUND\nAMOUNT')

        indx = 0
        styles=getSampleStyleSheet()

        # myStyle=ParagraphStyle(
        #     'small',
        #     parent=styles['Heading4'],
        #     fontsize=11,
        #     leading=8,
        # )
        for odr in lst_objects:
            indx = indx + 1
            if odr.reasonofcancellation is None:
                odr.reasonofcancellation=''
            sublst = [indx, odr.id, odr.advertisement_advid, datetime.datetime.strftime(odr.cancellationdatetime, '%d %b,%Y %H:%M:%S'),
                      Paragraph(odr.reasonofcancellation,styles['Normal'])]
            if flag == 1:
                sublst.append(datetime.datetime.strftime(odr.paymentdatetime, '%d %b,%Y %H:%M:%S'))
                sublst.append(odr.refundedamount)
            lst.append(sublst)

        print(lst)
        # p.

        # data=[
        #     ['1','sahil'],
        #     ['2','viraj'],
        #     ['3','apu']
        # ]
        filename = 'cencelled_orders.pdf'
        pdf = SimpleDocTemplate(
            filename,
            pagesize=letter,
            title='Cancelled Orders'
        )
        style = TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('FONTSIZE', (0, 0), (0, 0), 20),

            ('BACKGROUND', (0, 1), (-1, 1), colors.green),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            # ('FONTSIZE', (5, 1), (5, -1), 10),
            # ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 7),

            # sr no. left right padding reducing
            # ('LEFTPADDING', (0,0),(-1,-1), 0),
            # ('PADDING',(5,1),(5,-1), 0),

            ('TOPPADDING', (0, 1), (-1, 1), 7),
            ('BOTTOMPADDING', (0, 0), (0, 0), 35),
            ('GRID', (0, 1), (-1, len(lst_objects)), 0.25, colors.black),
        ])
        # table=Table(lst)
        if flag == 1:
            table = Table(lst, colWidths=(13 * mm, None, None, None, 60*mm, None, None))
        else:
            table = Table(lst, colWidths=(13 * mm, None, None, None, None))
        table.setStyle(style)
        elems = []
        elems.append(table)

        pdf.build(elems)
        # p.drawCentredString(274,800,'Orders')
        # p.showPage()
        # p.save()
        # buffer.seek(0)

        # return FileResponse(buffer,as_attachment=False,filename=filename)
        return FileResponse(open(filename, 'rb'), as_attachment=False, filename=filename)

    return render(request, 'admm/cncldOdrList.html', {'Objects': lst_objects, 'flagRforNot': flag})


@login_required
def saveRefnd(request):
    Orderdetails.objects.filter(id=int(request.POST['odrId']), advertisement_advid=int(request.POST['advId'])).update(refundedamount = request.POST['refndAmnt'],paymentdatetime = datetime.datetime.now(),paymentrefid = random.randint(a=0, b=9999999999))
    return redirect('admm:list_cncld_odrs')


@login_required
def ordr_detail(request, pk):
    ordrObj = get_object_or_404(Order, id=int(pk))
    ordrAdvs = Orderdetails.objects.filter(id=ordrObj)
    return render(request, 'admm/orderDetail.html', {'ordrObj': ordrObj, 'ordrAdvs': ordrAdvs})


# def cnclordr_detail(request,pk):
#     ordrObj=get_object_or_404(Order,id=int(pk))
#     ordrAdvs=Cancellationofordadv.objects.filter(id=ordrObj)
#     return render(request, 'admm/orderDetail.html', {'ordrObj': ordrObj,'ordrAdvs':ordrAdvs})

@login_required
def coupon_detail(request, pk):
    return render(request, 'admm/couponDetail.html', {'cpnObj': Coupondetail.objects.get(id=pk)})


# @login_required
class CouponLstOrAdd(View):
    def get(self, request):
        if request.user.is_authenticated:
            cpnObjects = None
            lst = []
            flag = int(request.GET.get('actvOnes', default=1))
            if flag == 1:  # active
                cpnObjects = Coupondetail.objects.filter(couponenddate__gte=datetime.date.today())
                for cpnObj in cpnObjects:
                    if cpnObj.order_set.all().count() == 0:
                        lst.append(cpnObj)
            elif flag == 0:  # used
                cpnObjects = Coupondetail.objects.all()
                for cpnObj in cpnObjects:
                    if cpnObj.order_set.all().count() == 1 or cpnObj.couponenddate < datetime.date.today():
                        lst.append(cpnObj)
            # elif flag == 2:#expired
            #     cpnObjects = Coupondetail.objects.filter(couponenddate__lt=datetime.datetime.now())
            #     for cpnObj in cpnObjects:
            #         if cpnObj.order_set.all().count() == 1:
            #             lst.append(cpnObj)
            buyers = User.objects.filter(userroleid=3)
            cpn_form = CouponForm(instance=Coupondetail())
            template = 'admm/couponListOrCreate.html'
            context = {'cpn_form': cpn_form, 'lst': lst, 'buyers': buyers,
                       'flag': flag}  # ,'usrObjects':usrObjects}#, 'cart_forms': cart_forms}
            return render(request, template, context)
        else:
            return redirect('login:log_in')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login:log_in')
        cpn_form = CouponForm(request.POST, instance=Coupondetail())
        if cpn_form.is_valid():  # and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_cpn = cpn_form.save(commit=False)
            # objTmp = Coupondetail.objects.aggregate(Max('id'))
            # if objTmp['id__max'] == None:
            #     objTmp['id__max'] = 0
            # new_cpn.id = objTmp['id__max'] + 1
            # new_cpn.couponcode=request.POST['code']
            # new_cpn.coupondescription = request.POST['desc']
            # new_cpn.coupondiscount = int(request.POST['discount'])
            # new_cpn.couponstartdate = request.POST['sdate']
            # new_cpn.couponenddate = request.POST['edate']
            # new_cpn.mincartvalue = int(request.POST['minval'])
            # new_cpn.auth_user = User.objects.get(id=int(request.POST['usr']))
            new_cpn.auth_user = User.objects.get(id=int(request.POST['byrId']))
            new_cpn.couponcode = request.POST['cpnCode']
            new_cpn.save()
            return redirect("admm:couponsListOr"
                            ""
                            "Add")
        cpnObjects = Coupondetail.objects.all()
        messages.info(request, 'Something bad happened..')
        context = {'cpn_form': cpn_form, 'cpnObjects': cpnObjects}
        return render(request, 'admm/couponListOrCreate.html', context)


@login_required
def listAdv(request):
    advObjs = []
    if request.user.is_staff == 1:
        if request.method == 'POST' and request.POST.get('isowned', default='1') == '0':
            # print('post here')
            OwnedOnes = False
            for usr in User.objects.filter(userroleid=2):
                for adv in Advertisement.objects.filter(auth_user=usr):
                    advObjs.append(adv)
        else:
            # print('coming')
            OwnedOnes = True
            for usr in User.objects.filter(is_staff=1):
                for adv in Advertisement.objects.filter(auth_user=usr):
                    advObjs.append(adv)
    else:
        OwnedOnes = True
        advObjs = Advertisement.objects.filter(auth_user=User.objects.get(email=request.user.email))
        # if advObjs.length:
        # print(len(advObjs))
    return render(request, 'admm/advList.html',
                  {'advObjs': advObjs, 'pipeAdv': 'Advertisement', 'OwnedOnes': OwnedOnes})


@login_required
def adv_detail(request, pk):
    advObj = get_object_or_404(Advertisement, advid=pk)
    advImgObjects = Advimgs.objects.filter(id=advObj)
    priceObjects = Durationwisepricing.objects.filter(advertisement_advid=advObj)
    return render(request, 'admm/advDetail.html',
                  {'advObj': advObj, 'advImgObjects': advImgObjects, 'priceObjects': priceObjects,
                   'catid': advObj.subcategory_subcatid.catid.id})


@login_required
def delAdv(request, pk):
    adv = Advertisement.objects.get(advid=pk)
    try:
        adv.delete()
        messages.info(request, "Advertisement deleted.")
        return redirect('admm:listadv')
    except:
        messages.info(request,
                      "Couldn't delete it. It's used at other places in data entries, try to delete those entries first..")
        return redirect('admm:listadv')


def canIdeleteIt(adv):
    adv.delete()
    pass


@login_required
def adv_edit(request, pk):
    advObj = get_object_or_404(Advertisement, advid=pk)
    # canIdeleteIt(advObj)
    advImgObjects = Advimgs.objects.filter(id=advObj)
    priceObjects = Durationwisepricing.objects.filter(advertisement_advid=advObj)
    areaObjects = Area.objects.all()
    cityObjects = City.objects.all()
    subCatObjects = advObj.subcategory_subcatid.catid.subcategory_set.all()
    # indx=0
    return render(request, 'admm/advEdit.html', {'advObj': advObj,
                                                 'advImgObjects': advImgObjects,
                                                 'priceObjects': priceObjects,
                                                 'catid': advObj.subcategory_subcatid.catid.id,
                                                 'areaObjects': areaObjects,
                                                 'cityObjects': cityObjects,
                                                 'subCatObjects': subCatObjects,
                                                 'categories': Category.objects.all()})


@login_required
def adv_save(request, pk):
    print(request.method)
    if request.method == 'POST':
        advObj = get_object_or_404(Advertisement, advid=pk)
        if request.POST.get('height', default=None) is not None:
            advObj.height = request.POST['height']
        if request.POST.get('width', default=None) is not None:
            advObj.width = request.POST['width']
        if request.POST.get('subcategory', default=None) is not None:
            advObj.subcategory_subcatid = Subcategory.objects.get(id=request.POST.get('subcategory'))

        if advObj.subcategory_subcatid.catid.id == 1:
            if request.POST.get('regno', default=None) is not None:
                advObj.advregno = request.POST.get('regno')
            if request.POST.get('address', default=None) is not None:
                advObj.addressline1 = request.POST.get('address')
            if request.POST.get('area', default=None) is not None:
                advObj.area_areaid = Area.objects.get(id=request.POST.get('area'))

        elif advObj.subcategory_subcatid.catid.id == 2:
            if request.POST.get('city', default=None) is not None:
                advObj.city_cityid = City.objects.get(id=request.POST.get('city'))
            if request.POST.get('min_qn', default=None) is not None:
                advObj.minquantity = int(request.POST.get('min_qn'))
            if request.POST.get('stock', default=None) is not None:
                advObj.stock = int(request.POST.get('stock'))

        Durationwisepricing.objects.filter(advertisement_advid=advObj).delete()
        # priceObjects = Durationwisepricing.objects.filter(advertisement_advid=advObj)
        # for priceObj in priceObjects:
        #     priceObj.delete()
        for i in range(1, int(request.POST.get('DWPcount')) + 1):
            new_price = Durationwisepricing(advertisement_advid=advObj, noofdays=request.POST.get('day' + str(i)),
                                            price=request.POST.get('price' + str(i)))
            # new_price.noofdays=request.POST['day'+str(i)]
            new_price.save(force_insert=True)
        # advObj.maxdays = int(request.POST['maxdays'])
        # i=1
        # for adimg in Advimgs.objects.filter(id=advObj):
        #     if adimg.adv_img == imgsListForDel[i]:
        #         adimg.delete()
        #     i+=1
        # for img in imgsListForDel:
        #     print(img)
        #     if img=='bingo':
        #         continue

        # old way deleting imgs
        # imgsListForDel=request.GET['imgsList'].split('?')
        # for adimg in Advimgs.objects.filter(id=advObj):
        #     if str(adimg.adv_img) in imgsListForDel and str(adimg.adv_img) is not 'bingo':
        #         print('deleted'+str(adimg.adv_img))
        #         adimg.delete()

        # new way deleting imgs
        delAdvLst = request.POST.get('deletedAdvLst').split()
        print(type(delAdvLst))
        adv_images = Advimgs.objects.filter(id=advObj)
        for del_adv in delAdvLst:
            if del_adv is '':
                continue
            for img in adv_images:
                if str(img.adv_img) == del_adv:
                    img.delete()
                    break

        for filename, file in request.FILES.items():
            # for i in range(adv_imgs_count):
            # print(filename)
            new_advimg = Advimgs(id=advObj, adv_img=file)
            # print(new_advimg.adv_img2)
            new_advimg.save(force_insert=True)

        advObj.auth_user = User.objects.get(email=request.user.email)
        advObj.save()
        # return redirect('/adminsite/adv/'+str(advObj.advid))
        return redirect('admm:adv_detail', pk=advObj.advid)
    return redirect('admm:adv_edit', pk=pk)


@login_required
def fdbckOrCmplntList(request, objname):
    if objname == 'feedbacks':
        mdl = Orderfeedback
    elif objname == 'complaints':
        mdl = Complaintdetail
    else:
        return redirect('/adminsite/buyers/responses/' + objname + '/')
    # objects = (mdl.objects.all()).order_by('-datetime')
    lst=[]
    # for fdbk in Orderfeedback.objects.all():
    for odr in Orderdetails.objects.all():
        for fdbk in odr.orderfeedback_.all():
            print(fdbk.description)
            # if odr.id in fdbk.odrid:
        # print(fdbk.get())

    # for obj in Orderdetails.objects.all():
    #     for fdbk in obj.id.orderfeedback_set.all():
    #         fdbk.auth_user=obj.id.auth_user
    #         lst.append(fdbk)
    #     obj.auth_user=obj.orderdetails_set.first().id.auth_user
    # for obj in objects:
    #     ordrDtl=obj.orderdetails_order_orderid_set.all().first()
    #     obj.auth_user=obj.orderdetails_order_orderid.first()
    # fdbckObj = Orderfeedback.objects.get(description='nice work')
    # print (fdbckObj.datetime)
    return render(request, 'admm/fdbckOrCmplnt.html',
                  {'object_list': lst, 'objname': objname})


@login_required
def fdbkRcmplnt_save(request, isFdbk):
    if request.method == 'POST':
        dtime = datetime.datetime.now()
        if isFdbk == 1:
            objname = 'feedbacks'
            Obj = Orderfeedback.objects.filter(id=request.POST['ODR_id'], datetime=request.POST['dtime']).update(
                resDatetime=dtime.strftime('%Y-%m-%d %H:%M:%S'), responsetext=request.POST['rspns'],
                auth_user=User.objects.get(email=request.user.email))
        else:
            objname = 'complaints'
            Obj = Complaintdetail.objects.filter(id=request.POST['ODR_id'], datetime=request.POST['dtime']).update(
                resDatetime=dtime.strftime('%Y-%m-%d %H:%M:%S'), responsetext=request.POST['rspns'],
                auth_user=User.objects.get(email=request.user.email))
    return redirect('admm:fdbckCmplntList', objname=objname)
    # dtime=datetime.datetime()
    # print(dtime)
    # Complaintdetail.objects.all()
    # dtime=datetime.datetime.strptime(request.GET.get('dtime'),'%B %d,%Y,%I:%M %p]')
    # print(dtime)
    # ordr=Order.objects.get(id=19)
    # dtime=datetime.datetime.now()
    # Obj.resDatetime=dtime.strftime('%Y-%m-%d %H:%M:%S')
    # Obj.responsetext=request.GET.get('rspns')
    # Obj.auth_user=User.objects.get(email=request.user.email)
    # Obj.save()
    # data={
    #     'msg':'done dana',
    #     'datetime':Obj.resDatetime,
    #     'rspns':Obj.responsetext,
    # }
    # return JsonResponse(data)


@login_required
def fetch_advs(request):
    usr = User.objects.get(email=request.user.email)
    advs = []
    alrdyAdv = request.GET.get('alreadyAdvs').split(' ')
    print(alrdyAdv)
    for adv_details in usr.advertisement_set.values():
        adv = Advertisement.objects.get(advid=adv_details['advid'])
        
        if str(adv.advid) in alrdyAdv:
            continue
        # ar = '-'
        if adv.subcategory_subcatid.catid.id == 2: #rickshaw
            adv_details['area_areaid']='-'
            adv_details['addressline1']='-'
            adv_details['advregno']='-'
        elif adv.subcategory_subcatid.catid.id == 1: #hoarding
            adv_details['stock']='-'
            adv_details['minquantity']='-'
            adv_details['area_areaid']=adv.area_areaid.areaname
            
            
        # if ad.area_areaid is not None:
        #     adv_details['area']=ad.area_areaid.areaname
        # else:
        #     adv_details['area']='-'
        # # ct = '-'
        # if ad.city_cityid is not None:
        #     adv['city']=ad.city_cityid.cityname
        # else:
        #     adv['city']='-'
        
        adv_details['city_cityid_id']=adv.city_cityid.cityname
        adv_details['subcategory_subcatid_id']=adv.subcategory_subcatid.subcatname
        adv_details['catid']=adv.subcategory_subcatid.catid.id
        # adv_details['minQntt']=adv.minquantity
        adv_details['auth_user_id']=adv.auth_user.first_name + ' ' + adv.auth_user.last_name
        # adv['dict'] = {'area': ar, 'city': ct, 'subcat': ad.subcategory_subcatid.subcatname,
        #                'ownr': ad.auth_user.first_name + ' ' + ad.auth_user.last_name}
        advs.append(adv_details)
    return JsonResponse(data={'advs': advs})
    # advs=Advertisement.objects.filter(auth_user=)


@login_required
def packOfferList(request, packOrOffr):
    if request.method == 'GET':
        print('get')
        if packOrOffr == 'package':
            if request.user.is_staff:
                print('is staff')
                object_list = []
                packs = Package.objects.all()
                for pack in packs:
                    print('pack for loop')
                    fstPackDtl = pack.packagehasadv_set.all().first()
                    if fstPackDtl is not None and fstPackDtl.advertisement_advid.auth_user.is_staff:
                        pack.advCnt = pack.packagehasadv_set.all().count()
                        object_list.append(pack)
                        print('coming here')
            else:
                object_list = []
                packs = Package.objects.all()
                for pack in packs:
                    fstPackDtl = pack.packagehasadv_set.all().first()
                    if fstPackDtl is not None and fstPackDtl.advertisement_advid.auth_user.is_staff:
                        continue
                    pack.advCnt = pack.packagehasadv_set.all().count()
                    object_list.append(pack)

                # usr=User.objects.get(email=request.user.email)
            # advCnt = 0
            # for obj in object_list:
            #     pass
            isPack = 1
        elif packOrOffr == 'offer':
            if request.user.is_staff:
                print('is staff')
                object_list = []
                for offr in Offerdetail.objects.all():
                    print('offr for loop')
                    fstPackDtl = offr.offercoveringadvs_set.all().first()
                    if fstPackDtl is not None and fstPackDtl.advertisement_advid.auth_user.is_staff:
                        offr.advCnt = offr.offercoveringadvs_set.all().count()
                        object_list.append(offr)
                        print('coming here')
            else:
                object_list = []
                for offr in Offerdetail.objects.all():
                    fstOffrDtl = offr.offercoveringadvs_set.all().first()
                    if fstOffrDtl is not None and fstOffrDtl.advertisement_advid.auth_user.is_staff:
                        continue
                    offr.advCnt = offr.offercoveringadvs_set.all().count()
                    object_list.append(offr)
            isPack = 0
        else:
            return redirect('/adminsite/' + packOrOffr + '/listing/')
        return render(request, 'admm/packOfferList.html',
                      {'object_list': object_list, 'isPack': isPack, 'packOffr': packOrOffr})


@login_required
def packOfferDetail(request, packOrOffr, pk):
    if packOrOffr == 'package':
        mdl = Package
        subMdl = PackageHasAdv
    else:
        mdl = Offerdetail
        subMdl = Offercoveringadvs
    obj = get_object_or_404(mdl, id=int(pk))
    subObjs = subMdl.objects.filter(id=obj)
    return render(request, 'admm/packOrOfferDetail.html',
                  {'obj': obj, 'subObjs': subObjs, 'packOffr': packOrOffr, 'pk': pk})


# def tmp(request,pk):
#     pack=Package.objects.get(id=pk)
#     print(pack.packagehasadv_set.all())
#     return HttpResponse('hello')

@login_required
def packOffrEdit(request, packOrOffr, pk):
    if request.method == 'POST':
        if packOrOffr == 'offer':
            pack = Offerdetail.objects.get(id=int(pk))
        else:
            pack = Package.objects.get(id=int(pk))
        if 'startdate' in request.POST:
            pack.startdate = request.POST['startdate']
            print(pack.startdate)
        if 'enddate' in request.POST:
            pack.enddate = request.POST['enddate']
            print(pack.enddate)
        if 'discount' in request.POST:
            pack.discount = request.POST['discount']
            print(pack.discount)
        if 'description' in request.POST:
            pack.description = request.POST['description']
            print(pack.description)
        pack.save()

        pack.packagehasadv_set.all().delete()
        
        for adId in request.POST['adv_list'].split(','):
            if adId == '':
                break
            if packOrOffr == 'offer':
                dtlObj = Offercoveringadvs()
            else:
                dtlObj = PackageHasAdv()
            dtlObj.id = pack
            dtlObj.advertisement_advid = Advertisement.objects.get(advid=adId)
            if dtlObj.advertisement_advid.subcategory_subcatid.catid.id == 2:
                dtlObj.quantity = request.POST['quant' + str(adId)]
            dtlObj.save(force_insert=True)
            
        # chngdAdvQnt = request.POST['changedAdvQnts'].split(' ')
        # for adId in chngdAdvQnt:
        #     if adId == '':
        #         break
        #     PackageHasAdv.objects.filter(id=pack, advertisement_advid=Advertisement.objects.get(advid=adId)).update(
        #         quantity=int(request.POST['quant' + str(adId)]))

        # dltdAdv = request.POST['deletedAdvs'].split(' ')
        # for adId in dltdAdv:
        #     if adId == '':
        #         break
        #     PackageHasAdv.objects.filter(id=pack, advertisement_advid=Advertisement.objects.get(advid=adId)).delete()
        #     # print('qaunt '+str(obj.quantity))
        #     # obj.delete()
        if pack.packagehasadv_set.all().count() == 0:
            pack.delete()
            return redirect('admm:packOrOffr_list',packOrOffr=packOrOffr)
        return redirect('admm:packoffr_detail',packOrOffr=packOrOffr,pk=pk)
    if packOrOffr == 'package':
        return PackageUpdate.as_view()(request, packOrOffr=packOrOffr, pk=pk)
    if packOrOffr == 'offer':
        return OfferdetailUpdate.as_view()(request, packOrOffr=packOrOffr, pk=pk)
    else:
        return redirect('adminsite/packoffr/' + packOrOffr + '/' + str(pk) + '/edit/')
    # return render(request,'packOfferEdit.html')


@login_required
def packOffrDel(request, packOrOffr, pk):
    if packOrOffr == 'package':
        mdl = Package
    else:
        mdl = Offerdetail
    obj = mdl.objects.get(id=int(pk))
    obj.delete()
    return redirect('/adminsite/' + packOrOffr + '/listing/')


# @login_required
# def packOffrSave(request,packOrOffr,pk):
#     # return redirect('/adminsite/packoffr/'+packOrOffr+'/'+pk+'/edit/')
#     return redirect('admm:packoffr_edit',packOrOffr=packOrOffr,pk=pk)
# @login_required
# def packOrOffer_create_link(request):
#     messages.info(request, 'Select the Advertisements first.. ')
#     return redirect('admm:listadv')


@login_required
def packOrOffer_create(request,packOrOffr):
    if request.method=='GET':
        if packOrOffr == 'package':
            isPack=1
        else:
            isPack=0
        return render(request,'admm/packOffer_create.html',context={'isPack':isPack,'packOrOffr':packOrOffr,'advObjs':Advertisement.objects.filter(auth_user=User.objects.get(email=request.user.email))})
    if int(request.POST['isPack']) == 1:
        mdl = Package
        mdl2 = PackageHasAdv
        messages.info(request, 'Package created successfully!')
    else:
        mdl = Offerdetail
        mdl2 = Offercoveringadvs
        messages.info(request, 'Offer created successfully!')
    obj = mdl(description=request.POST['description'], startdate=request.POST['startdate'],
              enddate=request.POST['enddate'], discount=request.POST['discount'])
    objTmp = mdl.objects.aggregate(Max('id'))
    if objTmp['id__max'] == None:
        objTmp['id__max'] = 0
    obj.id = objTmp['id__max'] + 1
    obj.save()
    
    for id in (request.POST['selectedAdvs']).split(','):
        if id is '':
            continue
        detailObj = mdl2(id=obj, advertisement_advid=Advertisement.objects.get(advid=int(id)))
        if int(request.POST['isPack']) == 1 and detailObj.advertisement_advid.subcategory_subcatid.catid.id == 2:
            detailObj.quantity = request.POST['selectedAdvQntt'+str(id)]
        detailObj.save(force_insert=True)
    return redirect('admm:packOrOffr_list',packOrOffr=packOrOffr)


# @login_required
class randomObjAddView(CreateView):
    fields = []
    sai = 'dd'
    if 'df':
        model = Advertisement

    def get_queryset(self):
        if self.kwargs.get('objname') == 'Advertisement':
            model = Advertisement
        elif self.kwargs.get('objname') == 'Category':
            model = Category
        elif self.kwargs.get('objname') == 'Subcategory':
            model = Subcategory
        # elif self.kwargs.get('objname') == 'Userdetail':
        #     return Userdetail.objects.all()
        else:
            return Area.objects.all()

    # fields = ['advid', 'advregno', 'height', 'width', 'maxdays', 'minquantity', 'addressline1', 'area_areaid','city_cityid', 'stock', 'defaultimgpath', 'subcategory_subcatid', 'userdetail_userid', 'isowned']


# @login_required
class randomObjUpdView(UpdateView):
    fields = []

    def get_queryset(self):
        if self.kwargs.get('objname') == 'Advertisement':
            return Advertisement.objects.all()
        elif self.kwargs.get('objname') == 'Category':
            return Category.objects.all()
        elif self.kwargs.get('objname') == 'Subcategory':
            return Subcategory.objects.all()
        # elif self.kwargs.get('objname') == 'Userdetail':
        #     return Userdetail.objects.all()
        else:
            return Area.objects.all()
    # fields = ['advid', 'advregno', 'height', 'width', 'maxdays', 'minquantity', 'addressline1', 'area_areaid','city_cityid', 'stock', 'defaultimgpath', 'subcategory_subcatid', 'userdetail_userid', 'isowned']


# @login_required
class randomObjDelView(DeleteView):
    success_url = reverse_lazy('admm:randomObj-detail')

    def get_queryset(self):
        if self.kwargs.get('objname') == 'Advertisement':
            return Advertisement.objects.all()
        elif self.kwargs.get('objname') == 'Category':
            return Category.objects.all()
        elif self.kwargs.get('objname') == 'Subcategory':
            return Subcategory.objects.all()
        elif self.kwargs.get('objname') == 'User':
            return User.objects.all()
        else:
            return Area.objects.all()


# from django.forms.models import
# data = serializers.serialize('xml', Advertisement.objects.all())
# @login_required
class randomObjDetailView(generic.DetailView):
    # model=Advertisement
    template_name = 'admm/detail.html'

    # data = serializers.serialize('python', Advertisement.objects.all(),fields=('advid','defaultimgpath'))
    def get_queryset(self):
        if self.kwargs.get('objname') == 'Advertisement':
            return Advertisement.objects.all()
            # return Advertisement.objects.all()
            # return Advertisement.objects.filter(id=self.kwargs.get('pk')).values()
        # elif self.kwargs.get('objname') == 'Advimgs':
        #     return Advimgs.objects.all()
        elif self.kwargs.get('objname') == 'Area':
            return Area.objects.all()
        elif self.kwargs.get('objname') == 'User':
            return User.objects.all()
        elif self.kwargs.get('objname') == 'Branch':
            return Branch.objects.all()
        # elif self.kwargs.get('objname') == 'Cancellationofordadv':
        #     return Cancellationofordadv.objects.all()
        elif self.kwargs.get('objname') == 'Cartdetail':
            return Cartdetail.objects.all()
        elif self.kwargs.get('objname') == 'Category':
            return Category.objects.all()
        elif self.kwargs.get('objname') == 'City':
            return City.objects.all()
        elif self.kwargs.get('objname') == 'Commissiondetail':
            return Commissiondetail.objects.all()
        elif self.kwargs.get('objname') == 'Company':
            return Company.objects.all()
        elif self.kwargs.get('objname') == 'Complaintdetail':
            return Complaintdetail.objects.all()
        elif self.kwargs.get('objname') == 'Country':
            return Country.objects.all()
        elif self.kwargs.get('objname') == 'Coupondetail':
            return Coupondetail.objects.all()
        elif self.kwargs.get('objname') == 'Durationwisepricing':
            return Durationwisepricing.objects.all()
        elif self.kwargs.get('objname') == 'Offercoveringadvs':
            return Offercoveringadvs.objects.all()
        elif self.kwargs.get('objname') == 'Offerdetail':
            return Offerdetail.objects.all()
        elif self.kwargs.get('objname') == 'Order':
            return Order.objects.all()
        elif self.kwargs.get('objname') == 'Orderfeedback':
            return Orderfeedback.objects.all()
        elif self.kwargs.get('objname') == 'Orderpayment':
            return Orderpayment.objects.all()
        elif self.kwargs.get('objname') == 'Orderdetails':
            return Orderdetails.objects.all()
        elif self.kwargs.get('objname') == 'Package':
            return Package.objects.all()
        elif self.kwargs.get('objname') == 'PackageHasAdv':
            return PackageHasAdv.objects.all()
        elif self.kwargs.get('objname') == 'Sellerdocdetail':
            return Sellerdocdetail.objects.all()
        elif self.kwargs.get('objname') == 'Sellerdoclist':
            return Sellerdoclist.objects.all()
        elif self.kwargs.get('objname') == 'State':
            return State.objects.all()
        elif self.kwargs.get('objname') == 'Subcategory':
            return Subcategory.objects.all()
        elif self.kwargs.get('objname') == 'Updationinorder':
            return Updationinorder.objects.all()
        elif self.kwargs.get('objname') == 'Userrole':
            return Userrole.objects.all()
        elif self.kwargs.get('objname') == 'Wishlistdetail':
            return Wishlistdetail.objects.all()
        else:
            return Area.objects.all()

    def get_context_data(self, **kwargs):
        if self.kwargs.get('objname') == 'Advertisement':
            advobject = model_to_dict(Advertisement.objects.get(advid=self.kwargs.get('pk')))
            modelName = Advertisement
            priceobjects = Durationwisepricing.objects.filter(advertisement_advid=self.kwargs.get('pk'))
            # super.queryset(randomObjDetailView, self).get_context_data()=Advertisement.objects.all()
            return {'object': advobject, 'priceobj': priceobjects, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
            # return Advertisement.objects.all()
            # return Advertisement.objects.filter(id=self.kwargs.get('pk')).values()
        # elif self.kwargs.get('objname') == 'Advimgs':
        #     objects = Advimgs.objects.filter(id=self.kwargs.get('pk'))
        #     modelName = Advimgs
        #     return {'advimg_objects': objects, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        # return Category.objects.all()
        elif self.kwargs.get('objname') == 'Area':
            object = model_to_dict(Area.objects.get(id=self.kwargs.get('pk')))
            modelName = Area
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'User':
            object = model_to_dict(User.objects.get(id=self.kwargs.get('pk')))
            modelName = User
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Branch':
            object = model_to_dict(Branch.objects.get(id=self.kwargs.get('pk')))
            modelName = Branch
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        # elif self.kwargs.get('objname') == 'Cancellationofordadv':
        #     object = model_to_dict(Cancellationofordadv.objects.get(id=self.kwargs.get('pk')))
        #     modelName = Cancellationofordadv
        #     return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Cartdetail':
            object = model_to_dict(Cartdetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Cartdetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Category':
            object = model_to_dict(Category.objects.get(id=self.kwargs.get('pk')))
            modelName = Category
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'City':
            object = model_to_dict(City.objects.get(id=self.kwargs.get('pk')))
            modelName = City
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Commissiondetail':
            object = model_to_dict(Commissiondetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Commissiondetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Company':
            object = model_to_dict(Company.objects.get(id=self.kwargs.get('pk')))
            modelName = Company
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Complaintdetail':
            object = model_to_dict(Complaintdetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Complaintdetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Country':
            object = model_to_dict(Country.objects.get(id=self.kwargs.get('pk')))
            modelName = Country
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Coupondetail':
            object = model_to_dict(Coupondetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Coupondetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Durationwisepricing':
            object = model_to_dict(Durationwisepricing.objects.get(id=self.kwargs.get('pk')))
            modelName = Durationwisepricing
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Offercoveringadvs':
            object = model_to_dict(Offercoveringadvs.objects.get(id=self.kwargs.get('pk')))
            modelName = Offercoveringadvs
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Offerdetail':
            object = model_to_dict(Offerdetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Offerdetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Order':
            object = model_to_dict(Order.objects.get(id=self.kwargs.get('pk')))
            modelName = Order
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Orderfeedback':
            object = model_to_dict(Orderfeedback.objects.get(id=self.kwargs.get('pk')))
            modelName = Orderfeedback
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Orderpayment':
            object = model_to_dict(Orderpayment.objects.get(id=self.kwargs.get('pk')))
            modelName = Orderpayment
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Orderdetails':
            object = model_to_dict(Orderdetails.objects.get(id=self.kwargs.get('pk')))
            modelName = Orderdetails
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Package':
            object = model_to_dict(Package.objects.get(id=self.kwargs.get('pk')))
            modelName = Package
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'PackageHasAdv':
            object = model_to_dict(PackageHasAdv.objects.get(id=self.kwargs.get('pk')))
            modelName = PackageHasAdv
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Sellerdocdetail':
            object = model_to_dict(Sellerdocdetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Sellerdocdetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Sellerdoclist':
            object = model_to_dict(Sellerdoclist.objects.get(id=self.kwargs.get('pk')))
            modelName = Sellerdoclist
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'State':
            object = model_to_dict(State.objects.get(id=self.kwargs.get('pk')))
            modelName = State
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Subcategory':
            object = model_to_dict(Subcategory.objects.get(id=self.kwargs.get('pk')))
            modelName = Subcategory
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Updationinorder':
            object = model_to_dict(Updationinorder.objects.get(id=self.kwargs.get('pk')))
            modelName = Updationinorder
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Userrole':
            object = model_to_dict(Userrole.objects.get(id=self.kwargs.get('pk')))
            modelName = Userrole
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        elif self.kwargs.get('objname') == 'Wishlistdetail':
            object = model_to_dict(Wishlistdetail.objects.get(id=self.kwargs.get('pk')))
            modelName = Wishlistdetail
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
        else:
            object = model_to_dict(Area.objects.get(id=self.kwargs.get('pk')))
            modelName = Area
            return {'object': object, 'modelName': modelName, 'spk': self.kwargs.get('pk')}
    # tmp = ""
    # HttpRequest.GET.get
    # def get_object(self, queryset=None):
    #     pk=self.kwargs.get('pk')
    #     if self.kwargs.get('objname')=='Advertisement':
    #         return self.get_object(Advertisement)
    #     elif self.kwargs.get('objname')=='Category':
    #         return self.get_object(Category)
    #     elif self.kwargs.get('objname')=='Userdetail':
    #         return self.get_object(Userdetail)
    #     return self.get_object(Area)
    # tmp='Advertisement'
    # q = "<class 'admm.models." +  + "'>"
    # mdls = apps.get_app_config('admm').get_models()
    # for mdl in mdls:
    #     if q == str(mdl):
    #         model = mdl


@login_required
def index(request):
    # mdlLst = ['Advertisement', 'Advimgs', 'Area', 'User', 'Branch', 'Cancellationofordadv', 'Cartdetail',
    #           'Category', 'City', 'Commissiondetail', 'Company', 'Complaintdetail', 'Country', 'Coupondetail',
    #           'Durationwisepricing', 'Offercoveringadvs', 'Offerdetail', 'Order', 'Orderfeedback', 'Orderpayment',
    #           'Orderdetails', 'Package', 'PackageHasAdv', 'Sellerdocdetail', 'Sellerdoclist', 'State', 'Subcategory',
    #           'Updationinorder', 'Userrole', 'Wishlistdetail']
    catCnt = Category.objects.count()
    admins = User.objects.filter(userroleid=Userrole.objects.get(roleid=1))
    advOwnd = 0
    for admin in admins:
        advOwnd += admin.advertisement_set.count()
    advTtl = Advertisement.objects.count()
    areas = Area.objects.all().count
    cities = City.objects.all().count
    states = State.objects.all().count
    countries = Country.objects.all().count
    buyers = User.objects.filter(userroleid=Userrole.objects.get(roleid=3)).count
    sellers = User.objects.filter(userroleid=Userrole.objects.get(roleid=2)).count
    packsTtl = Package.objects.all().count
    packsAdm = Package.objects.filter().count
    cpnListAdtv = []
    cpnObjects = Coupondetail.objects.filter(couponenddate__gte=datetime.date.today())
    cpnsTtl = Coupondetail.objects.all().count()
    for cpnObj in cpnObjects:
        if cpnObj.order_set.all().count() == 0:
            cpnListAdtv.append(cpnObj)
    cpnListAdtv = len(cpnListAdtv)

    odrsTtl = Order.objects.all().count()
    todayDateTime = datetime.datetime.today().replace(hour=0, minute=0, second=0)
    odrsTdy = Order.objects.filter(orderdatetime__gte=todayDateTime,
                                   orderdatetime__lte=todayDateTime.replace(hour=23, minute=59, second=59)).count()
    todayDate = datetime.date.today().replace(day=1)
    # print(todayDate)
    # print(todayDate.replace(month=int(todayDate.month)+1))
    odrsThisMnth = Order.objects.filter(orderdatetime__gte=todayDate,
                                        orderdatetime__lt=todayDate.replace(month=int(todayDate.month) + 1)).count()

    if request.user.is_staff:
        users=User.objects.filter(is_staff=1)#all admins
    else:
        users=User.objects.filter(id=request.user.id)#current logged in seller
    packCnt=0
    for pack in Package.objects.all():
        fstPackDtl = pack.packagehasadv_set.all().first()
        if fstPackDtl is not None and fstPackDtl.advertisement_advid.auth_user in users:
            packCnt = packCnt +1

    offrCnt = 0
    for offr in Offerdetail.objects.all():
        print('offr for loop')
        fstPackDtl = offr.offercoveringadvs_set.all().first()
        if fstPackDtl is not None and fstPackDtl.advertisement_advid.auth_user in users:
            offrCnt=offrCnt+1

    return render(request, 'admm/index.html', {
        'pipeHome': 'Home',
        'advSlrs': advTtl - advOwnd, 'advOwnd': advOwnd, 'advTtl': advTtl,
        'catCnt': catCnt, 'scatCnt': Subcategory.objects.count(),
        'areas': areas, 'cities': cities, 'states': states, 'countries': countries,
        'buyers': buyers, 'sellers': sellers, 'admins': admins.count(),
        'cpnsActv': cpnListAdtv, 'cpnsTtl': cpnsTtl, 'usedORexpired': cpnsTtl - cpnListAdtv,
        'odrsTtl': odrsTtl, 'odrsThisMnth': odrsThisMnth, 'odrsTdy': odrsTdy,
        'packCnt':packCnt,'offrCnt':offrCnt
    })


# class Tables(generic.DetailView):

# def tables(request):
#     mdlLst=['Advertisement','Advimgs','Area','User','Branch','Cancellationofordadv','Cartdetail','Category','City','Commissiondetail','Company','Complaintdetail','Country','Coupondetail','Durationwisepricing','Offercoveringadvs','Offerdetail','Order','Orderfeedback','Orderpayment','Orderdetails','Package','PackageHasAdv','Sellerdocdetail','Sellerdoclist','State','Subcategory','Updationinorder','Userrole','Wishlistdetail']
#     return render(request,'admm/index.html',{'mdlLst':mdlLst})

# class Tables(generic.Vi):
#     template_name = 'admm/tables.html'
#     # model = Advertisement
#     def get_context_data(self, **kwargs):
#         mdls = apps.get_app_config('admm').get_models()
#         mdlList=[]
#         for mdl in mdls:
#             mdlList.append(mdl.__name__)
#         return {'mdlList':mdlList,'Gm':'Good Morning'}
# @login_required
class List(generic.ListView):
    template_name = 'admm/list-view.html'

    def get_queryset(self):
        if self.kwargs['objname'] == 'Advertisement':
            # object_list_here2 = model_to_dict(Advertisement.objects.get(advid=self.kwargs.get('pk')))
            # return {'objects':objects,'object_list_here2':object_list_here2}
            return Advertisement.objects.all()
        elif self.kwargs['objname'] == 'advimgs':
            # object_list_here2 = model_to_dict(Advertisement.objects.get(advid=self.kwargs.get('pk')))
            # return {'objects':objects,'object_list_here2':object_list_here2}
            return Advimgs.objects.all()
        elif (self.kwargs['objname'] == 'Category'):
            # objectsHere = Category.objects.all()
            # object_list_here2 = model_to_dict(Category.objects.get(categoryid=self.kwargs.get('pk')))
            # return {'objects': objects, 'object_list_here2': object_list_here2}
            return Category.objects.all()
        elif (self.kwargs['objname'] == 'Offerdetail'):
            objects = Offerdetail.objects.all()
            return objects
        elif self.kwargs['objname'] == 'Package':
            objects = Package.objects.all()
            return objects
        elif (self.kwargs['objname'] == 'Coupondetail'):
            objects = Coupondetail.objects.all()
            return objects
        elif (self.kwargs['objname'] == 'Order'):
            objectsHere = Order.objects.all()
            return objectsHere
        elif (self.kwargs['objname'] == 'Orderfeedback'):
            objects = Orderfeedback.objects.all()
            return objects
        elif (self.kwargs['objname'] == 'Complaintdetail'):
            return Complaintdetail.objects.all()
        elif (self.kwargs['objname'] == 'User'):
            return User.objects.all()
        elif (self.kwargs['objname'] == 'User'):
            return User.objects.all()
        elif (self.kwargs['objname'] == 'Area'):
            return Area.objects.all()
        else:
            return Area.objects.all()

    def get_context_data(self, **kwargs):
        if self.kwargs['objname'] == 'Advertisement':
            # object = model_to_dict(Advertisement.objects.get(advid=self.kwargs.get('pk')))
            modelName = Advertisement
            objectList = []
            for obj in Advertisement.objects.all():
                objectList.append(model_to_dict(obj))
            # objects=model_to_dict(Advertisement.objects.all(),excludde='_meta') #,fields=['advid','advregno','height','width','maxdays','minquantity','addressline1','area_areaid','city_cityid','stock','defaultimgpath','subcatid','auth_user'])
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}
            # return Advertisement.objects.all()
            # return Advertisement.objects.filter(id=self.kwargs.get('pk')).values()
        elif (self.kwargs['objname'] == 'advimgs'):
            # object = model_to_dict(Advimgs.objects.get(d=self.kwargs.get('pk')))
            modelName = Advimgs
            objectList = []
            for obj in Advimgs.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Advimgs.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Area'):
            # object = model_to_dict(Area.objects.get(d=self.kwargs.get('pk')))
            modelName = Area
            objectList = []
            for obj in Area.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Area.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Branch'):
            # object = model_to_dict(Branch.objects.get(d=self.kwargs.get('pk')))
            modelName = Branch
            objectList = []
            for obj in Branch.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Branch.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Order'):
            # object = model_to_dict(Order.objects.get(d=self.kwargs.get('pk')))
            modelName = Order
            objectList = []
            for obj in Order.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Order.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Orderdetails'):
            # object = model_to_dict(Orderdetails.objects.get(d=self.kwargs.get('pk')))
            modelName = Orderdetails
            objectList = []
            for obj in Orderdetails.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Orderdetails.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        # elif (self.kwargs['objname'] == 'Cancellationofordadv'):
        #     # object = model_to_dict(Cancellationofordadv.objects.get(d=self.kwargs.get('pk')))
        #     modelName = Cancellationofordadv
        #     objectList = []
        #     for obj in Cancellationofordadv.objects.all():
        #         objectList.append(model_to_dict(obj))
        #     # objects = Cancellationofordadv.objects.all()
        #     return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Cartdetail'):
            # object = model_to_dict(Cartdetail.objects.get(d=self.kwargs.get('pk')))
            modelName = Cartdetail
            objectList = []
            for obj in Cartdetail.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Cartdetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Category'):
            # object = model_to_dict(Category.objects.get(d=self.kwargs.get('pk')))
            modelName = Category
            objectList = []
            for obj in Category.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Category.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'City'):
            # object = model_to_dict(City.objects.get(d=self.kwargs.get('pk')))
            modelName = City
            objectList = []
            for obj in City.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = City.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Commissiondetail'):
            # object = model_to_dict(Commissiondetail.objects.get(d=self.kwargs.get('pk')))
            modelName = Commissiondetail
            objectList = []
            for obj in Commissiondetail.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Commissiondetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Company'):
            # object = model_to_dict(Company.objects.get(d=self.kwargs.get('pk')))
            modelName = Company
            objectList = []
            for obj in Company.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Company.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Country'):
            # object = model_to_dict(Country.objects.get(d=self.kwargs.get('pk')))
            modelName = Country
            objectList = []
            for obj in Country.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Country.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Complaintdetail'):
            # object = model_to_dict(Complaintdetail.objects.get(d=self.kwargs.get('pk')))
            modelName = Complaintdetail
            objectList = []
            for obj in Complaintdetail.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Complaintdetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Durationwisepricing'):
            # object = model_to_dict(Durationwisepricing.objects.get(d=self.kwargs.get('pk')))
            modelName = Durationwisepricing
            objectList = []
            for obj in Durationwisepricing.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Durationwisepricing.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Offercoveringadvs'):
            # object = model_to_dict(Offercoveringadvs.objects.get(d=self.kwargs.get('pk')))
            modelName = Offercoveringadvs
            objectList = []
            for obj in Offercoveringadvs.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Offercoveringadvs.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Offerdetail'):
            # object = model_to_dict(Offerdetail.objects.get(d=self.kwargs.get('pk')))
            modelName = Offerdetail
            objectList = []
            for obj in Offerdetail.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Offerdetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Orderfeedback'):
            # object = model_to_dict(Orderfeedback.objects.get(d=self.kwargs.get('pk')))
            modelName = Orderfeedback
            objectList = []
            for obj in Orderfeedback.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Orderfeedback.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Orderpayment'):
            # object = model_to_dict(Orderpayment.objects.get(d=self.kwargs.get('pk')))
            modelName = Orderpayment
            objectList = []
            for obj in Orderpayment.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Orderpayment.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Package'):
            # object = model_to_dict(Package.objects.get(d=self.kwargs.get('pk')))
            modelName = Package
            objectList = []
            for obj in Package.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Package.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'PackageHasAdv'):
            # object = model_to_dict(Packagehasadv.objects.get(d=self.kwargs.get('pk')))
            modelName = PackageHasAdv
            objectList = []
            for obj in PackageHasAdv.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Packagehasadv.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Sellerdocdetail'):
            # object = model_to_dict(Sellerdocdetail.objects.get(d=self.kwargs.get('pk')))
            modelName = Sellerdocdetail
            objectList = []
            for obj in Sellerdocdetail.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Sellerdocdetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Sellerdoclist'):
            # object = model_to_dict(Sellerdoclist.objects.get(d=self.kwargs.get('pk')))
            modelName = Sellerdoclist
            objectList = []
            for obj in Sellerdoclist.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Sellerdoclist.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'State'):
            # object = model_to_dict(State.objects.get(d=self.kwargs.get('pk')))
            modelName = State
            objectList = []
            for obj in State.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = State.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Subcategory'):
            # object = model_to_dict(Subcategory.objects.get(d=self.kwargs.get('pk')))
            modelName = Subcategory
            objectList = []
            for obj in Subcategory.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Subcategory.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Updationinorder'):
            # object = model_to_dict(Updationinorder.objects.get(d=self.kwargs.get('pk')))
            modelName = Updationinorder
            objectList = []
            for obj in Updationinorder.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Updationinorder.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'User'):
            # object = model_to_dict(User.objects.get(d=self.kwargs.get('pk')))
            modelName = User
            objectList = []
            for obj in User.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = User.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Userrole'):
            # object = model_to_dict(Userrole.objects.get(d=self.kwargs.get('pk')))
            modelName = Userrole
            objectList = []
            for obj in Userrole.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Userrole.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        elif (self.kwargs['objname'] == 'Wishlistdetail'):
            # object = model_to_dict(Wishlistdetail.objects.get(d=self.kwargs.get('pk')))
            modelName = Wishlistdetail
            objectList = []
            for obj in Wishlistdetail.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Wishlistdetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}

        else:
            modelName = Area
            objectList = []
            for obj in Area.objects.all():
                objectList.append(model_to_dict(obj))
            # objects = Wishlistdetail.objects.all()
            return {'objectList': objectList, 'modelName': modelName}  # , 'spk': self.kwargs.get('pk')}


# class AdvDetailView(generic.DetailView):
#     model=Advertisement
#     template_name = 'admm/detail.html'
# class CategoryDetailView(generic.DetailView):
#     model=Category
#     template_name = 'admm/detail.html'
# class AdvImgsDetailView(generic.DetailView):
#     model = Advimgs
#     template_name = 'admm/detail.html'
# class AreaDetailView(generic.DetailView):
#     model = Area
#     template_name = 'admm/detail.html'
# class BranchDetailView(generic.DetailView):
#     model = Branch
#     template_name = 'admm/detail.html'
# class CancellationsDetailView(generic.DetailView):
#     model = Cancellationofordadv
#     template_name = 'admm/detail.html'
# class CartDetailView(generic.DetailView):
#     model = Cartdetail
#     template_name = 'admm/detail.html'
# class CityDetailView(generic.DetailView):
#     model = City
#     template_name = 'admm/detail.html'
# class CommissionDetailView(generic.DetailView):
#     model = Commissiondetail
#     template_name = 'admm/detail.html'
# class CompanyDetailView(generic.DetailView):
#     model = Company
#     template_name = 'admm/detail.html'
# class CouponDetailView(generic.DetailView):
#     model = Coupondetail
#     template_name = 'admm/detail.html'
# class ComplaintDetailView(generic.DetailView):
#     model = Complaintdetail
#     template_name = 'admm/detail.html'
# class CountryDetailView(generic.DetailView):
#     model = Country
#     template_name = 'admm/detail.html'
# class PricingDetailView(generic.DetailView):
#     model = Durationwisepricing
#     template_name = 'admm/detail.html'
# class OfferadvDetailView(generic.DetailView):
#     model = Offercoveringadvs
#     template_name = 'admm/detail.html'
# class OfferDetailView(generic.DetailView):
#     model = Offerdetail
#     template_name = 'admm/detail.html'
# class OrderDetailView(generic.DetailView):
#     model = Order
#     template_name = 'admm/detail.html'
# class OrderdetailDetailView(generic.DetailView):
#     model = Orderdetails
#     template_name = 'admm/detail.html'
# class OrdfdbackDetailView(generic.DetailView):
#     model = Orderfeedback
#     template_name = 'admm/detail.html'
# class OrdpaymntDetailView(generic.DetailView):
#     model = Orderpayment
#     template_name = 'admm/detail.html'
# class PackageDetailView(generic.DetailView):
#     model = Package
#     template_name = 'admm/detail.html'
# class PackadvDetailView(generic.DetailView):
#     model = PackageHasAdv
#     template_name = 'admm/detail.html'
# class SellerdocDetailView(generic.DetailView):
#     model = Sellerdocdetail
#     template_name = 'admm/detail.html'
# class SellerdoclistDetailView(generic.DetailView):
#     model = Sellerdoclist
#     template_name = 'admm/detail.html'
# class StateDetailView(generic.DetailView):
#     model = State
#     template_name = 'admm/detail.html'
# class SubcatDetailView(generic.DetailView):
#     model = Subcategory
#     template_name = 'admm/detail.html'
# class UpdationsDetailView(generic.DetailView):
#     model = Updationinorder
#     template_name = 'admm/detail.html'
# class UserDetailView(generic.DetailView):
#     model = Userdetail
#     template_name = 'admm/detail.html'
# class UserroleDetailView(generic.DetailView):
#     model = Userrole
#     template_name = 'admm/detail.html'
# class WishlistDetailView(generic.DetailView):
#     model = Wishlistdetail
#     template_name = 'admm/detail.html'

@login_required
def userRoleInUserList(request):
    obj = Userrole.objects.aggregate(Max('roleid'))
    if obj['roleid__max'] == None:
        obj['roleid__max'] = 0
    (Userrole(roleid=obj['roleid__max'] + 1, rolename=request.POST['role'])).save()
    return redirect('admm:usersList')


@login_required
def userList(request):
    object_list = None
    if request.method == 'GET':
        object_list = User.objects.filter(userroleid=1)
    elif request.method == 'POST':
        object_list = User.objects.filter(userroleid=int(request.POST['usrRoleFilter']))
    return render(request, 'admm/user_list.html', {'object_list': object_list, 'roles': Userrole.objects.all(),
                                                   'roleId': int(request.POST.get('usrRoleFilter', default=1))})


# @login_required
class UserDel(generic.DeleteView):
    model = User
    success_url = ''


@login_required
def userDetail(request, pk):
    template_name = 'admm/user_detail.html'
    usr=get_object_or_404(User, id=pk)
    if usr.userroleid.roleid==2:
        sellerDocs=usr.sellerdocdetail_set.all()
    else:
        sellerDocs=None
    return render(request, template_name, {'object': usr,'sellerDocs':sellerDocs})


@login_required
def lockUnlockUser(request, pk, frmBranchPage):
    usr = get_object_or_404(User, id=pk)
    if usr.is_active == 1:
        usr.is_active = 0
    else:
        usr.is_active = 1
    usr.save()
    if frmBranchPage == 0:
        return redirect('/adminsite/users/' + str(usr.id) + '/')
    else:
        return redirect('/adminsite/branch/admins/' + str(frmBranchPage))

@login_required
def addRole(request):
    obj = Userrole.objects.aggregate(Max('roleid'))
    if obj['roleid__max'] == None:
        obj['roleid__max'] = 0
    usrrole=Userrole(roleid=obj['roleid__max']+1,rolename=request.GET.get('role'))
    usrrole.save()
    result=1
    data={
        'result':result,
    }
    return JsonResponse(data)

@login_required
def makeAdmin(request):
    if User.objects.filter(id=request.GET.get('id')).update(userroleid=Userrole.objects.get(roleid=1)):
        result=1
    else:
        result=0
    data={
        'result':result,
    }
    return JsonResponse(data)
# class UserEdit(UpdateView):
#     model = User
#     fields = ['first_name', 'last_name', 'mobileno', 'company_companyid']
# fields = '__all__'

# class UserList(View):
#     pass

# Advertisement

@login_required
def upldImg(request):
    adv = Advertisement.objects.get(id=1)
    advImgObj = Advimgs(id=adv, adv_img=request.POST.get('advImgUpld'))
    advImgObj.save()
    return render(request, 'admm/advertisement_form.html', {'advImgObj': advImgObj})


# @login_required
class CartAddLatest(View):
    def get(self, request):
        adv_form = AdvForm(instance=Advertisement())
        cart_forms = [CartForm(prefix=str(x), instance=Cartdetail()) for x in range(2)]
        template = 'admm/new_cart.html'
        context = {'adv_form': adv_form, 'cart_forms': cart_forms}
        return render(request, template, context)

    def post(self, request):
        # context = {}
        adv_form = AdvForm(request.POST, instance=Advertisement())
        cart_forms = [CartForm(request.POST, prefix=str(x),
                               instance=Cartdetail()) for x in range(2)]
        if adv_form.is_valid() and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_adv = adv_form.save(commit=False)
            new_adv.auth_user = User.objects.get(email=request.user.email)
            print(new_adv.auth_user.email)
            print(cart_forms)
            new_adv.save()
            for cart_form in cart_forms:
                new_cart = cart_form.save(commit=False)
                new_cart.id = new_adv
                # new_cart.auth_user=User.objects.get(id=1)
                new_cart.save()
                # print(new_cart.noofdays)
            return redirect("/adminsite/list/Cartdetail")
        context = {'adv_form': adv_form, 'cart_forms': cart_forms}
        return render(request, 'admm/new_cart.html', context)


# @login_required
class AdvCreateLatest(View):
    def get(self, request):
        # adv_form=AdvForm(instance=Advertisement())
        # price_form=PricingForm(instance=Durationwisepricing())
        template = 'admm/new_adv.html'
        context = {'categories': Category.objects.all(), 'sts': State.objects.all()}
        return render(request, template, context)

    def post(self, request):
        # context = {}
        # new_adv=None
        # adv_form=AdvForm(request.POST,instance=Advertisement())
        # price_form=PricingForm(request.POST,instance=Durationwisepricing())

        # if price_form.is_valid() and new_adv is not None:
        #     new_price=price_form.save(commit=False)
        #     new_price.advertisement_advid=new_adv
        #     new_price.save(force_insert=True)
        #     return redirect("/adminsite/list/Advertisement")
        # adv_imgs_count = int(request.POST['for_advImg_loop'])
        # addd=request.FILES['advimg1']
        # print(addd)
        # for filename,file
        # request.FILES
        # for i in range(adv_imgs_count):
        # request.POST['advimg' + str(i + 1)
        # print(request.FILES)
        # for filename,file in request.FILES.items():
        # # for i in range(adv_imgs_count):
        #     # print(filename)
        #     new_advimg = Advimgs(id=Advertisement.objects.get(advid=14), adv_img=file)
        #     # print(new_advimg.adv_img2)
        #     new_advimg.save(force_insert=True)
        # if adv_imgs_count is not None:
        #     return redirect('/adminsite/list/advimgs/')
        # if adv_form.is_valid() : #and price_form.is_valid():
        new_adv = Advertisement()

        new_adv.auth_user = User.objects.get(email=request.user.email)

        obj = Advertisement.objects.aggregate(Max('advid'))
        if obj['advid__max'] == None:
            obj['advid__max'] = 0
        new_adv.advid = obj['advid__max'] + 1
        new_adv.height = request.POST['height']
        new_adv.width = request.POST['width']
        new_adv.subcategory_subcatid = Subcategory.objects.get(id=request.POST['subCat'])
        # new_adv.maxdays = 0

        if request.POST['advregno'] is not '':
            new_adv.advregno = request.POST['advregno']
            new_adv.addressline1 = request.POST['addrs']
            new_adv.area_areaid = Area.objects.get(id=request.POST['aria'])

        # rickshaw
        # stock =
        # if stock is not '':
        else:
            new_adv.stock = request.POST['stok']

            # if request.POST['aria'] is not '0':

            # if request.POST['citi'] is not '':
            new_adv.city_cityid = City.objects.get(id=request.POST['citi'])

            # if request.POST['minQntt'] is not '':
            new_adv.minquantity = request.POST['minQntt']
        # end--rickshaw
        # new_adv.defaultimgpath = 't'
        # new_adv.save()

        # for i in range(adv_imgs_count):
        #     new_advimg = Advimgs(id=new_adv,adv_img=request.POST['advimg' + str(i)])
        #     new_advimg.save(force_insert=True)
        # setDflt=True
        # print('coming here babr')
        for filename, file in request.FILES.items():
            # print('for loop')
            # if setDflt is True:
            # print('bad guy')
            new_adv.defaultimgpath = file
            new_adv.save()
            # setDflt=False
            # for i in range(adv_imgs_count):
            print(filename)
            new_advimg = Advimgs(id=new_adv, adv_img=file)
            # print(new_advimg.adv_img2)
            # new_adv.defaultimgpath=file
            new_advimg.save(force_insert=True)

        # priceRowCnt =
        #old process
        # for i in range(1, int(request.POST['for_dwp_loop']) + 1):
        #     new_price = Durationwisepricing(advertisement_advid=new_adv, noofdays=request.POST['days' + str(i)],
        #                                     price=request.POST['price' + str(i)])
        #     new_price.save(force_insert=True)

        #new process
        priceList = request.POST['priceList'].split(',')
        daysList = request.POST['daysList'].split(',')
        print(priceList)
        print(daysList)

        for i in range(len(priceList)):
            new_price = Durationwisepricing(advertisement_advid=new_adv, noofdays=int(daysList[i]),
                                            price=int(priceList[i]))
            new_price.save(force_insert=True)
        new_adv.save()

        return redirect('admm:listadv')

        # context={'adv_form':adv_form}#,'price_form':price_form}

        # messages.info(request,'something went wrong')
        # return render(request,'admm/new_adv.html',)

def tmpForCheck(request):
    priceList = request.POST['priceList'].split(',')
    daysList = request.POST['daysList'].split(',')
    print(priceList)
    print(daysList)

    for i in range(priceList.len):

        new_price = Durationwisepricing(advertisement_advid=new_adv, noofdays=int(daysList[i]),price=int(priceList[i]))
        new_price.save(force_insert=True)

    return HttpResponse('go fast in cmd')

# @login_required
class PriceCreate(View):
    def post(self, request):
        price_form = PricingForm(request.POST, instance=Durationwisepricing())
        pass


# @login_required
class CmpnyCreate(View):
    def get(self, request):
        objects = Company.objects.all()
        cmpny_form = CompanyForm(instance=Company())
        template = 'admm/company.html'
        context = {'cmpny_form': cmpny_form, 'objects': objects}
        return render(request, template, context)

    def post(self, request):
        objects = Company.objects.all()
        cmpny_form = CompanyForm(request.POST, instance=Company())
        if cmpny_form.is_valid():  # and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_cmpny = cmpny_form.save(commit=False)
            obj = Company.objects.aggregate(Max('companyid'))
            # print(obj)
            if obj['companyid__max'] == None:
                obj['companyid__max'] = 0
            new_cmpny.companyid = obj['companyid__max'] + 1
            new_cmpny.save()
            return redirect("/adminsite/company")
        context = {'cmpny_form': cmpny_form, 'objects': objects}
        return render(request, 'admm/company.html', context)


# @login_required
def CmpnyEdit(request, cmpnypk, cmpnyname):
    obj = get_object_or_404(Company, companyid=cmpnypk)
    # tmp='doc_Name'+str(sdlpk)
    obj.companyname = cmpnyname
    obj.save()
    return redirect('/adminsite/company')


# @login_required
def CmpnyDel(request, cmpnypk):
    # obj=Sellerdoclist.objects.get()
    obj = get_object_or_404(Company, companyid=cmpnypk)
    obj.delete()
    return redirect('/adminsite/company')


# @login_required
class UserRoleCreate(View):
    def get(self, request):
        objects = Userrole.objects.all()
        userrole_form = UserroleForm(instance=Userrole())
        template = 'admm/userrole.html'
        context = {'userrole_form': userrole_form, 'objects': objects}
        return render(request, template, context)

    def post(self, request):
        objects = Userrole.objects.all()
        userrole_form = UserroleForm(request.POST, instance=Userrole())
        if userrole_form.is_valid():  # and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_userrole = userrole_form.save(commit=False)
            obj = Userrole.objects.aggregate(Max('roleid'))
            # print(obj)
            if obj['roleid__max'] == None:
                obj['roleid__max'] = 0
            new_userrole.roleid = obj['roleid__max'] + 1
            new_userrole.save()
            return redirect("/adminsite/userroles")
        context = {'userrole_form': userrole_form, 'objects': objects}
        return render(request, 'admm/userrole.html', context)


# @login_required
def UserRoleEdit(request, rlpk, role):
    obj = get_object_or_404(Userrole, roleid=rlpk)
    # tmp='doc_Name'+str(sdlpk)
    obj.rolename = role
    obj.save()
    return redirect('/adminsite/userroles')


@login_required
def UserRoleDel(request, rlpk):
    # obj=Sellerdoclist.objects.get()
    obj = get_object_or_404(Userrole, roleid=rlpk)
    obj.delete()
    return redirect('/adminsite/userroles')


def location(request):
    template = 'admm/ar_ct_st_cn.html'
    context = {'cnobjects': Country.objects.all()}
    return render(request, template, context)


def locationUpdt(request):
    cnId = int(request.GET.get('id'))
    print(cnId)
    print('hey')
    try:
        obj = Country.objects.get(id=str(cnId))
        obj.countryname = request.GET.get('name')
        obj.save()
        msg = 'succeed'
        messages.info(request, msg)
    except ObjectDoesNotExist:
        msg = 'not succeed'
        messages.info(request, msg)
    data = {
        'msg': msg,
        'name': obj.countryname
    }
    return JsonResponse(data)


def locationDel(request):
    cnId = int(request.GET.get('id'))
    print(cnId)
    print('hey')
    try:
        obj = Country.objects.get(id=str(cnId))
        obj.delete()
        msg = 1
    except:
        msg = 0
    data = {
        'msg': msg,
    }
    return JsonResponse(data)


def cityObjs(request):
    stateId = int(request.GET.get('id'))
    # print(stateId)
    # print('hey')
    # stObjs = None
    # try:
    state = State.objects.get(id=int(stateId))
    ctObjs = list(state.city_set.values('id', 'cityname'))
    print(ctObjs)
    # lst_stObjs=serializers.serialize('json',stObjs,fields=)
    # msg = 1
    # except:
    #     msg = 0
    # strOflist=''
    # for st in stObjs:

    data = {
        'ctObjs': ctObjs,
    }
    return JsonResponse(data)


def areaObjs(request):
    ctId = int(request.GET.get('id'))
    # print(stateId)
    # print('hey')
    # stObjs = None
    # try:
    ct = City.objects.get(id=int(ctId))
    arObjs = list(ct.area_set.values('id', 'areaname'))
    print(arObjs)
    # lst_stObjs=serializers.serialize('json',stObjs,fields=)
    # msg = 1
    # except:
    #     msg = 0
    # strOflist=''
    # for st in stObjs:

    data = {
        'arObjs': arObjs,
    }
    return JsonResponse(data)


def stateObjs(request):
    stObjs = None
    # try:
    cnObj = Country.objects.all().first()
    stObjs = list(cnObj.state_set.values('id', 'statename'))
    print(stObjs)
    # lst_stObjs=serializers.serialize('json',stObjs,fields=)
    # msg = 1
    # except:
    #     msg = 0
    # strOflist=''
    # for st in stObjs:

    data = {
        'stObjs': stObjs,
    }
    return JsonResponse(data)


# class LocationViewCreateForm(View):
#     def get(self,request,cn=None,st=None,ct=None):
#         stobjects = ctobjects = arobjects = None
#         if cn is not None:
#             stobjects = State.objects.filter(country_countryid=cn)
#             if st is not None:
#                 ctobjects=City.objects.filter(state_stateid=st)
#                 if ct is not None:
#                     arobjects=Area.objects.filter(city_cityid=ct)
#         # subcat_form = SubcategoryForm(instance=Subcategory())
#         # cat_form=CategoryForm(instance=Category())
#         subcat_form = None
#         cat_form=None
#         template='admm/ar_ct_st_cn.html'
#         context={'cat_form':cat_form,'cnobjects':Country.objects.all(),'stobjects':stobjects,'ctobjects':ctobjects,'arobjects':arobjects,'subcat_form':subcat_form}
#         return render(request,template,context)

def categorySave(request):
    try:
        obj = Category.objects.aggregate(Max('id'))
        # print(obj)
        if obj['id__max'] == None:
            obj['id__max'] = 0
        newCat = Category(id=obj['id__max'] + 1, categoryname=request.GET.get('catName'))
        newCat.save()
        catId = obj['id__max'] + 1
    except:
        catId = -1
    data = {
        'catId': catId,
    }
    return JsonResponse(data)


class CategoryCreateForm(View):
    def get(self, request):
        if request.user.is_authenticated:
            subcat_form = SubcategoryForm(instance=Subcategory())
            objects = Category.objects.all()
            cat_form = CategoryForm(instance=Category())
            template = 'admm/categoryLatest.html'
            context = {'cat_form': cat_form, 'objects': objects, 'subcat_form': subcat_form}
            return render(request, template, context)
        return redirect('login:log_in')

    def post(self, request, pk=None):
        objects = Category.objects.all()
        cat_form = CategoryForm(request.POST, instance=Category())
        # subcat_form = SubcategoryForm(instance=Subcategory())
        if cat_form.is_valid():  # and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_cat = cat_form.save(commit=False)
            obj = Category.objects.aggregate(Max('id'))
            # print(obj)
            if obj['id__max'] == None:
                obj['id__max'] = 0
            new_cat.id = obj['id__max'] + 1
            new_cat.save()
            return redirect("/adminsite/categories")
        context = {'cat_form': cat_form, 'objects': objects}  # ,'subcat_form':subcat_form}
        return render(request, 'admm/category.html', context)


@login_required
def catWiseSubcats(request):
    pass


@login_required
def categoryEdit(request):
    try:
        obj = get_object_or_404(Category, id=request.GET.get('id'))
        obj.categoryname = request.GET.get('catName')
        obj.save()
        result = 1
    except:
        result = 0
    data = {
        'result': result
    }
    return JsonResponse(data)


@login_required
def categoryDel(request):
    # obj=Sellerdoclist.objects.get()
    try:
        obj = get_object_or_404(Category, id=request.GET.get('id'))
        obj.delete()
        result = 1
    except:
        result = 0
    data = {
        'result': result,
    }
    return JsonResponse(data)


@login_required
def subCatSave(request):
    # catid=
    # scatname=
    # dscnt=
    obj = Subcategory.objects.aggregate(Max('id'))
    # print(obj)
    try:
        if obj['id__max'] == None:
            obj['id__max'] = 0
        newScat = Subcategory(id=obj['id__max'] + 1, subcatname=request.GET.get('scat_name'),
                              commission=request.GET.get('cmsn'),
                              catid=Category.objects.get(id=request.GET.get('category_id')))
        newScat.save()
        result = newScat.id
    except:
        result = -1
    data = {
        'result': result,
    }
    return JsonResponse(data)


# @login_required
class SubcategoryCreateForm(View):
    # def get(self,request,pk):
    #     subobjects=Subcategory.objects.filter(catid=pk)
    #     subcat_form=SubcategoryForm(instance=Subcategory())
    #     template='admm/subcategory.html'
    #     context={'subcat_form':subcat_form,'objects':objects}
    #     return render(request,template,context)

    def post(self, request, pk):
        # objects = Subcategory.objects.filter(catid=pk)
        subcat_form = SubcategoryForm(request.POST, instance=Subcategory())
        if subcat_form.is_valid():  # and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_subcat = subcat_form.save(commit=False)
            obj = Subcategory.objects.aggregate(Max('id'))
            # print(obj)
            if obj['id__max'] == None:
                obj['id__max'] = 0
            new_subcat.id = obj['id__max'] + 1
            new_subcat.catid = Category.objects.get(id=pk)
            new_subcat.save()
        return redirect("/adminsite/categories/" + str(pk))
        # context = {'subcat_form': subcat_form, 'objects': objects}
        # return render(request,'admm/subcategory.html',context)

@login_required
def sellerDocs(request):
    return render(request,'admm/sellerDocs.html',context={'objects':Sellerdoclist.objects.all()})

@login_required
def subcategoryEdit(request):
    hasNameUpdtd = hasCmsnUpdtd = 0
    try:
        obj = get_object_or_404(Subcategory, id=request.GET.get('sid'))
        # tmp='doc_Name'+str(sdlpk)
        if request.GET.get('new_name') is not '':
            obj.subcatname = request.GET.get('new_name')
            hasNameUpdtd = 1
        if request.GET.get('new_cmishan') is not '':
            obj.commission = request.GET.get('new_cmishan')
            hasCmsnUpdtd = 1
        obj.save()
        result = 1
    except:
        result = 0
    data = {
        'result': result,
        'hasNameUpdtd': hasNameUpdtd,
        'hasCmsnUpdtd': hasCmsnUpdtd,
    }
    return JsonResponse(data)


@login_required
def subcategoryDel(request):
    # obj=Sellerdoclist.objects.get()
    try:
        obj = Subcategory.objects.get(subcatname=request.GET.get('scat_name'))
        obj.delete()
        result = 1
    except:
        result = 0
    data = {
        'result': result,
    }
    return JsonResponse(data)


# @login_required
class SellerDocCreate(View):
    def get(self, request):
        objects = Sellerdoclist.objects.all()
        sellerDocList_form = SellerDocForm(instance=Sellerdoclist())
        template = 'admm/seller_doc_list.html'
        context = {'sellerDocList_form': sellerDocList_form, 'objects': objects}
        return render(request, template, context)

    def post(self, request):
        objects = Sellerdoclist.objects.all()
        sellerDocList_form = SellerDocForm(request.POST, instance=Sellerdoclist())
        if sellerDocList_form.is_valid():  # and all([cart_form.is_valid() for cart_form in cart_forms]):
            new_sellerDoc = sellerDocList_form.save(commit=False)
            obj = Sellerdoclist.objects.aggregate(Max('docid'))
            # print(obj)
            if obj['docid__max'] == None:
                obj['docid__max'] = 0
            new_sellerDoc.docid = obj['docid__max'] + 1
            new_sellerDoc.save()
            return redirect("/adminsite/sellerdoclist")
        context = {'sellerDocList_form': sellerDocList_form, 'objects': objects}
        return render(request, 'admm/seller_doc_list.html', context)


@login_required
def sellerDocEdit(request):
    try:
        Sellerdoclist.objects.filter(docid=request.GET.get('id')).update(docname = request.GET.get('docName'))
        result=1
    except:
        result = 0
    data={
        'result':result,
    }
    return JsonResponse(data)


@login_required
def sellerDocDel(request):
    try:
        Sellerdoclist.objects.get(docid=request.GET.get('id')).delete()
        result = 1
    except:
        result = 0
    data = {
        'result': result,
    }
    return JsonResponse(data)


# @login_required
class BranchCreateViewForm(View):
    def get(self, request):
        objects = Branch.objects.all()
        for obj in objects:
            obj.admnCnt = obj.user_set.all().count()
        ctObs = City.objects.all()
        branch_form = BranchForm(instance=Branch())
        template = 'admm/branch.html'
        context = {'branch_form': branch_form, 'objects': objects, 'cmpny': Company.objects.get(companyid=1),
                   'cities': ctObs}
        return render(request, template, context)

    def post(self, request):
        # objects = Branch.objects.filter(int(request.POST['context']))
        # branch_form=BranchForm(request.POST,instance=Branch())
        # if branch_form.is_valid():# and all([cart_form.is_valid() for cart_form in cart_forms]):
        #     new_branch = branch_form.save(commit=False)
        if request.method == "POST":
            new_branch = Branch()
            obj = Branch.objects.aggregate(Max('id'))
            # print(obj)
            if obj['id__max'] == None:
                obj['id__max'] = 0
            new_branch.id = obj['id__max'] + 1
            new_branch.mobileno = request.POST['mobile']
            new_branch.branchaddress = request.POST['addrs']
            new_branch.areaid = Area.objects.get(id=request.POST['area'])
            new_branch.company_companyid = Company.objects.get(companyid=1)
            new_branch.save()
            return redirect("admm:branch_viewadd")

        messages.info(request, 'Error saving branch.')
        return render(request, 'admm/branch.html')


@login_required
def branchEdit(request, pk):
    obj = get_object_or_404(Branch, id=pk)
    obj.branchaddress = request.POST.get('branch_address' + str(pk))
    obj.mobileno = request.POST.get('mobileno' + str(pk))
    obj.save()
    return redirect('/adminsite/branch')


@login_required
def BranchDeleteForm(request, pk):
    # obj=Sellerdoclist.objects.get()
    obj = get_object_or_404(Branch, id=pk)
    obj.delete()
    return redirect('/adminsite/branch')


@login_required
def branchAdmins(request, pk):
    try:
        objects = User.objects.filter(branchid=int(pk))
    except ObjectDoesNotExist:
        messages.info(request, 'No admins')
    return render(request, 'admm/branchAdmins.html', context={'objects': objects})


# @login_required
class AdvCreate(CreateView):
    model = Advertisement
    # fields = ['id', 'advregno', 'height', 'width', 'maxdays', 'minquantity', 'addressline1', 'area_areaid',
    #           'city_cityid', 'stock', 'defaultimgpath', 'subcategory_subcatid', 'auth_user']
    fields = '__all__'
    # def get_context_data(self, **kwargs):
    #
    #     return {}


# class AdvUpdate(UpdateView):
#     model = Advertisement
#     # fields = ['id', 'advregno', 'height', 'width', 'maxdays', 'minquantity', 'addressline1', 'area_areaid',
#     #           'city_cityid', 'stock', 'defaultimgpath', 'subcategory_subcatid', 'auth_user']
#     # success_url = reverse_lazy('admm:randomObjDetail',kw)
#     fields = '__all__'
#
# class AdvDelete(DeleteView):
#     model = Advertisement
#     success_url = reverse_lazy('admm:index')


# AdvImgs
# @login_required
class AdvImgsCreate(CreateView):
    model = Advimgs
    # fields = ['advertisement_advid', 'imagepath']
    fields = '__all__'


# @login_required
class AdvImgsUpdate(UpdateView):
    model = Advimgs
    # fields = ['advertisement_advid', 'imagepath']
    fields = '__all__'


# @login_required
class AdvImgsDelete(DeleteView):
    model = Advimgs
    success_url = reverse_lazy('admm:index')


# @login_required
# Area
class AreaCreate(CreateView):
    model = Area
    # fields = ['areaid','areaname','city_cityid']
    fields = '__all__'


# @login_required
class AreaUpdate(UpdateView):
    model = Area
    # fields = ['areaid', 'areaname', 'city_cityid']
    fields = '__all__'


# @login_required
class AreaDelete(DeleteView):
    model = Area
    # success_url = 'list/12'
    success_url = reverse_lazy('admm:index')
    # success_url = model.get_absolut_url(12)


# @login_required
# Branch
class BranchCreate(CreateView):
    model = Branch
    # fields = ['branchaddress','mobileno','company_companyid']
    fields = '__all__'


# @login_required
class BranchUpdate(UpdateView):
    model = Branch
    # fields = ['branchid', 'branchaddress', 'mobileno', 'company_companyid']
    fields = '__all__'


# @login_required
class BranchDelete(DeleteView):
    model = Branch
    success_url = reverse_lazy('admm:index')


# @login_required
# Order
class OrderCreate(CreateView):
    model = Order
    # fields = ['orderid','userdetail_userid','orderdatetime','emipayment','emimonths','coupondetail','discountamount','gst_amount']
    fields = '__all__'


# @login_required
class OrderUpdate(UpdateView):
    model = Order
    # fields = ['orderid','userdetail_userid','orderdatetime','emipayment','emimonths','coupondetail','discountamount','gst_amount']
    fields = '__all__'


# @login_required
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('admm:index')


# @login_required
# Orderdetails
class OrderdetailsCreate(CreateView):
    model = Orderdetails
    # fields = ['order_orderid', 'advertisement_advid', 'advprice', 'advstartdate', 'quantity']
    fields = '__all__'


# @login_required
class OrderdetailsUpdate(UpdateView):
    model = Orderdetails
    # fields = ['order_orderid', 'advertisement_advid', 'advprice', 'advstartdate', 'quantity']
    fields = '__all__'


# @login_required
class OrderdetailsDelete(DeleteView):
    model = Orderdetails
    success_url = reverse_lazy('admm:index')


# Cancellationofordadv
# class CancellationofordadvCreate(CreateView):
#     model = Cancellationofordadv
#     # fields = ['order_id', 'advrtid', 'cancellationdatetime', 'reasonofcancellation', 'paymentrefid', 'paymentdatetime',
#     #           'refundedamount']
#     fields = '__all__'

# class CancellationofordadvUpdate(UpdateView):
#     model = Cancellationofordadv
#     # fields = ['order_id', 'advrtid', 'cancellationdatetime', 'reasonofcancellation', 'paymentrefid', 'paymentdatetime',
#     #           'refundedamount']
#     fields = '__all__'
#
# class CancellationofordadvDelete(DeleteView):
#     model = Cancellationofordadv
#     success_url = reverse_lazy('admm:index')


# Cartdetail


class CartdetailCreate(CreateView):
    model = Cartdetail
    # fields = ['userdetail_userid', 'advertisement_advid', 'price', 'startdate', 'enddate', 'quantity']
    fields = '__all__'


class CartdetailUpdate(UpdateView):
    model = Cartdetail
    # fields = ['userdetail_userid', 'advertisement_advid', 'price', 'startdate', 'enddate', 'quantity']
    fields = '__all__'


class CartdetailDelete(DeleteView):
    model = Cartdetail
    success_url = reverse_lazy('admm:index')


# Category
class CategoryCreate(CreateView):
    model = Category
    # fields = ['categoryid','categoryname']
    fields = '__all__'


class CategoryUpdate(UpdateView):
    model = Category
    # fields = ['categoryid','categoryname']
    fields = '__all__'


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('admm:index')


# City
class CityCreate(CreateView):
    model = City
    # fields = ['cityid', 'cityname', 'state_stateid']
    fields = '__all__'


class CityUpdate(UpdateView):
    model = City
    # fields = ['cityid', 'cityname', 'state_stateid']
    fields = '__all__'


class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('admm:index')


# Commissiondetail
class CommissiondetailCreate(CreateView):
    model = Commissiondetail
    # fields = ['advertisement_advid', 'commission', 'createddatetime']
    fields = '__all__'


class CommissiondetailUpdate(UpdateView):
    model = Commissiondetail
    # fields = ['advertisement_advid', 'commission', 'createddatetime']
    fields = '__all__'


class CommissiondetailDelete(DeleteView):
    model = Commissiondetail
    success_url = reverse_lazy('admm:index')


# Company
class CompanyCreate(CreateView):
    model = Company
    # fields = ['companyid', 'companyname', 'logopath']
    fields = '__all__'


class CompanyUpdate(UpdateView):
    model = Company
    # fields = ['companyid', 'companyname', 'logopath']
    fields = '__all__'


class CompanyDelete(DeleteView):
    model = Company
    # success_url = reverse_lazy('admm:index')


# Complaintdetail
class ComplaintdetailCreate(CreateView):
    model = Company
    # fields = ['companyid', 'companyname', 'logopath']
    fields = '__all__'


class ComplaintdetailUpdate(UpdateView):
    model = Company
    # fields = ['companyid', 'companyname', 'logopath']
    fields = '__all__'


class ComplaintdetailDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('admm:index')


# Country
class CountryCreate(CreateView):
    model = Country
    # fields = ['countryid', 'countryname']
    fields = '__all__'


class CountryUpdate(UpdateView):
    model = Country
    # fields = ['countryid', 'countryname']
    fields = '__all__'


class CountryDelete(DeleteView):
    model = Country
    success_url = reverse_lazy('admm:index')


# Coupondetail
class CoupondetailCreate(CreateView):
    model = Coupondetail
    # fields = ['couponid', 'couponcode', 'coupondescription', 'coupondiscount', 'couponstartdate', 'couponenddate',
    #           'mincartvalue', 'userdetail_userid']
    fields = '__all__'


class CoupondetailUpdate(UpdateView):
    model = Coupondetail
    fields = ['couponcode', 'coupondescription', 'coupondiscount', 'couponstartdate', 'couponenddate',
              'mincartvalue', 'auth_user']
    # fields = '__all__'
    template_name = 'admm/couponEdit.html'
    success_url = reverse_lazy('admm:couponsListOrAdd')


def delCoupon(request):
    try:
        obj = Coupondetail.objects.get(id=request.GET.get('cpnId'))
        obj.delete()
        rslt = 1
    except:
        rslt = 0
    data = {
        'result': rslt
    }
    return JsonResponse(data)


# Docdetail
# class DocdetailCreate(CreateView):
#     model = Docdetail
#     fields = ['userdetail_userid','sellerdoclist_docid','docpath']
# class DocdetailUpdate(UpdateView):
#     model = Docdetail
#     fields = ['userdetail_userid','sellerdoclist_docid','docpath']
# class DocdetailDelete(DeleteView):
#     model = Docdetail
#     success_url = reverse_lazy('admm:index')

# Durationwisepricing
class DurationwisepricingCreate(CreateView):
    model = Durationwisepricing
    fields = ['noofdays', 'price']
    # fields = ['advertisement_advid', 'noofdays', 'price']
    # fields = '__all__'


class DurationwisepricingUpdate(UpdateView):
    model = Durationwisepricing
    # fields = ['advertisement_advid', 'noofdays', 'price']
    fields = '__all__'


class DurationwisepricingDelete(DeleteView):
    model = Durationwisepricing
    success_url = reverse_lazy('admm:index')


# Offercoveringadvs
class OffercoveringadvsCreate(CreateView):
    model = Offercoveringadvs
    # fields = ['offerdetail_offerid', 'advertisement_advid']
    fields = '__all__'


class OffercoveringadvsUpdate(UpdateView):
    model = Offercoveringadvs
    # fields = ['offerdetail_offerid', 'advertisement_advid']
    fields = '__all__'


class OffercoveringadvsDelete(DeleteView):
    model = Offercoveringadvs
    success_url = reverse_lazy('admm:index')


# Offerdetail
class OfferdetailCreate(CreateView):
    model = Offerdetail
    # fields = ['offerid', 'description', 'discount', 'offerstartdatetime', 'offerenddatetime']
    fields = '__all__'


class OfferdetailUpdate(UpdateView):
    model = Offerdetail
    # fields = ['offerid', 'description', 'discount', 'offerstartdatetime', 'offerenddatetime']
    fields = '__all__'
    success_url = '/adminsite/offer/listing/'


class OfferdetailDelete(DeleteView):
    model = Offerdetail
    success_url = reverse_lazy('admm:index')


# Orderfeedback
class OrderfeedbackCreate(CreateView):
    model = Orderfeedback
    # fields = ['orderdetail_orderid', 'feedbackdatetime', 'feedbacktext', 'rating', 'responsedatetime', 'responsetext',
    #           'userdetail_userid']
    fields = '__all__'


class OrderfeedbackUpdate(UpdateView):
    model = Orderfeedback
    # fields = ['orderdetail_orderid', 'feedbackdatetime', 'feedbacktext', 'rating', 'responsedatetime', 'responsetext',
    #           'userdetail_userid']
    fields = '__all__'


class OrderfeedbackDelete(DeleteView):
    model = Orderfeedback
    success_url = reverse_lazy('admm:index')


# Orderpayment
class OrderpaymentCreate(CreateView):
    model = Orderpayment
    fields = '__all__'
    # fields = ['paymentrefid', 'orderdetail_orderid', 'paymentdatetime', 'amount']


class OrderpaymentUpdate(UpdateView):
    model = Orderpayment
    fields = '__all__'
    # fields = ['paymentrefid', 'orderdetail_orderid', 'paymentdatetime', 'amount']


class OrderpaymentDelete(DeleteView):
    model = Orderpayment
    success_url = reverse_lazy('admm:index')


# Package
class PackageCreate(CreateView):
    model = Package
    fields = '__all__'
    # fields = ['packageid', 'packagedescription', 'discount', 'startdate', 'enddate']


# ------------------in use-----------------#
class PackageUpdate(UpdateView):
    model = Package

    # fields = '__all__'
    # packDtlLst=None
    def get_context_data(self, **kwargs):
        pack = Package.objects.get(id=self.kwargs['pk'])
        packDtlLst = pack.packagehasadv_set.all()
        context = super().get_context_data(**kwargs)
        # extra_context = {'packHasAdvs': packDtlLst}
        # context={}
        context['packDtls'] = packDtlLst
        return context

    fields = ['description', 'discount', 'startdate', 'enddate']
    success_url = '/adminsite/package/listing/'


# -------------------end-------------------#

class PackageDelete(DeleteView):
    model = Package
    success_url = reverse_lazy('admm:index')


# PackageHasAdv
class PackageHasAdvCreate(CreateView):
    model = PackageHasAdv
    fields = '__all__'
    # fields = ['package_packageid', 'advertisement_advid', 'quantity']


class PackageHasAdvUpdate(UpdateView):
    model = PackageHasAdv
    fields = '__all__'
    # fields = ['package_packageid', 'advertisement_advid', 'quantity']


class PackageHasAdvDelete(DeleteView):
    model = PackageHasAdv
    success_url = reverse_lazy('admm:index')


# Sellerdocdetail
class SellerdocdetailCreate(CreateView):
    model = Sellerdocdetail
    fields = '__all__'
    # fields = ['userdetail_userid', 'sellerdoclist_docid', 'docpath']


class SellerdocdetailUpdate(UpdateView):
    model = Sellerdocdetail
    fields = '__all__'
    # fields = ['userdetail_userid', 'sellerdoclist_docid', 'docpath']


class SellerdocdetailDelete(DeleteView):
    model = Sellerdocdetail
    success_url = reverse_lazy('admm:index')


# Sellerdoclist


class SellerdoclistCreate(CreateView):
    model = Sellerdoclist
    fields = '__all__'
    # fields = ['docid', 'docname']


class SellerdoclistUpdate(UpdateView):
    model = Sellerdoclist
    fields = '__all__'
    # fields = ['docid', 'docname']


class SellerdoclistDelete(DeleteView):
    model = Sellerdoclist
    success_url = reverse_lazy('admm:index')


# State
class StateCreate(CreateView):
    model = State
    fields = '__all__'
    # fields = ['stateid', 'statename', 'country_countryid']


class StateUpdate(UpdateView):
    model = State
    fields = '__all__'
    # fields = ['stateid', 'statename', 'country_countryid']


class StateDelete(DeleteView):
    model = State
    success_url = reverse_lazy('admm:index')


# Subcategory
class SubcategoryCreate(CreateView):
    model = Subcategory
    fields = '__all__'
    # fields = ['subcatid', 'subcatname','catid']


class SubcategoryUpdate(UpdateView):
    model = Subcategory
    fields = '__all__'
    # fields = ['subcatid', 'subcatname', 'catid']


class SubcategoryDelete(DeleteView):
    model = Subcategory
    success_url = reverse_lazy('admm:index')


# Updationinorder
class UpdationinorderCreate(CreateView):
    model = Updationinorder
    # fields = ['orderid', 'advid', 'updationdatetime', 'amount', 'paymentrefid', 'paymentdatetime']
    fields = '__all__'


class UpdationinorderUpdate(UpdateView):
    model = Updationinorder
    # fields = ['orderid', 'advid', 'updationdatetime', 'amount', 'paymentrefid', 'paymentdatetime']
    fields = '__all__'


class UpdationinorderDelete(DeleteView):
    model = Updationinorder
    success_url = reverse_lazy('admm:index')


# Userdetail
class UserdetailCreate(CreateView):
    model = User
    fields = '__all__'


class UserdetailUpdate(UpdateView):
    model = User
    fields = '__all__'


class UserdetailDelete(DeleteView):
    model = User
    success_url = reverse_lazy('admm:index')


# Userrole
class UserroleCreate(CreateView):
    model = Userrole
    fields = '__all__'


class UserroleUpdate(UpdateView):
    model = Userrole
    fields = '__all__'


class UserroleDelete(DeleteView):
    model = Userrole
    success_url = reverse_lazy('admm:index')


# Wishlistdetail
class WishlistdetailCreate(CreateView):
    model = Wishlistdetail
    fields = '__all__'


class WishlistdetailUpdate(UpdateView):
    model = Wishlistdetail
    fields = '__all__'


class WishlistdetailDelete(DeleteView):
    model = Wishlistdetail
    success_url = reverse_lazy('admm:index')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
