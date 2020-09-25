
from django.db import models
from django.urls import reverse
from django import template

# Create your models here.
class Advertisement(models.Model):
    advid = models.AutoField(db_column='AdvId', primary_key=True)  # Field name made lowercase.
    advregno = models.CharField(db_column='AdvRegNo', unique=True, max_length=45, blank=True, null=True,verbose_name='Registration No')  # Field name made lowercase.
    height = models.IntegerField(db_column='Height')  # Field name made lowercase.
    width = models.IntegerField(db_column='Width')  # Field name made lowercase.
    minquantity = models.IntegerField(db_column='MinQuantity', blank=True, null=True,verbose_name='Minimum quantity')  # Field name made lowercase.
    addressline1 = models.TextField(db_column='AddressLine1',verbose_name='Address')  # Field name made lowercase.
    area_areaid = models.ForeignKey('Area', models.DO_NOTHING, db_column='Area_AreaId', blank=True, null=True)  # Field name made lowercase.
    city_cityid = models.ForeignKey('City', models.DO_NOTHING, db_column='City_CityId', blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock', blank=True, null=True)  # Field name made lowercase.
    defaultimgpath = models.FileField(db_column='DefaultImgPath', blank=True, null=True)  # Field name made lowercase.
    subcategory_subcatid = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='SubCategory_SubCatId')  # Field name made lowercase.
    auth_user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'advertisement'

    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Advertisement'})
    def __str__(self):
        return str(self.advid)
    def get_add_url(self):
        return reverse('admm:adv-add')
    def get_del_url(self):
        return 'adv/'+str(self.advid)+'/delete/'
    def get_url(self):
        return 'adv'

# class Advertisement(models.Model):
#     advid = models.AutoField(models.DO_NOTHING,db_column='AdvId', primary_key=True)  # Field name made lowercase.
#     advregno = models.CharField(db_column='AdvRegNo', unique=True, max_length=45, null=True,verbose_name='Registration No')# Field name made lowercase.
#     height = models.IntegerField(db_column='Height')  # Field name made lowercase.
#     width = models.IntegerField(db_column='Width')  # Field name made lowercase.
#     maxdays = models.IntegerField(db_column='MaxDays',verbose_name='Maximum days',null=True)  # Field name made lowercase.
#     minquantity = models.IntegerField(db_column='MinQuantity',  null=True,verbose_name='Minimum quantity')  # Field name made lowercase.
#     addressline1 = models.TextField(db_column='AddressLine1',verbose_name='Address')  # Field name made lowercase.
#     area_areaid = models.ForeignKey('Area', models.DO_NOTHING, db_column='Area_AreaId', null=True,verbose_name='Area')  # Field name made lowercase.
#     city_cityid = models.ForeignKey('City', models.DO_NOTHING, db_column='City_CityId',null=True,verbose_name='City')  # Field name made lowercase.
#     stock = models.IntegerField(db_column='Stock', null=True)  # Field name made lowercase.
#     defaultimgpath = models.FileField(db_column='DefaultImgPath')  # Field name made lowercase.
#     subcategory_subcatid = models.ForeignKey('Subcategory', models.CASCADE,default=None, db_column='SubCategory_SubCatId',verbose_name='Subcategory')  # Field name made lowercase.
#     # userid = models.ForeignKey('User', models.DO_NOTHING, db_column='id')# Field name made lowercase.
#     auth_user = models.ForeignKey('User', models.CASCADE,default=None)
#     # isowned = models.IntegerField(db_column='IsOwned')  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'advertisement'
#
#     def get_absolute_url(self):
#         return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Advertisement'})
#
#     def __str__(self):
#         return str(self.advid)
#     def get_add_url(self):
#         return reverse('admm:adv-add')
#     def get_del_url(self):
#         return 'adv/'+str(self.advid)+'/delete/'
#     def get_url(self):
#         return 'adv'
#     # register=template.Library()
#     # @register.filter
#     # def get_values(self,fld):
#     #     if fld=='advid':
#     #         return self.advid
#     #     elif fld=='advregno':
#     #         return self.advregno
#     #     else:
#     #         return self.height

class Advimgs(models.Model):
    advertisement_advid = models.ForeignKey('Advertisement', models.CASCADE, db_column='Advertisement_AdvId', primary_key=True,name='id')  # Field name made lowercase.
    adv_img = models.FileField(db_column='ImagePath')
    # adv_img2 =models.FileField(null=True,upload_to='media/')
    class Meta:
        managed = False
        db_table = 'advimgs'
        unique_together = (('id', 'adv_img'),)
    def __str__(self):
        return 'advimgs'
    def get_del_url(self):
         return reverse('admm:advimgs-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:advimgs-upd',kwargs={'pk':self.pk})
    def get_add_url(self):
         return reverse('admm:advimgs-add')
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Advimgs'})

class Area(models.Model):
    areaid = models.IntegerField(name='id',db_column='AreaId', primary_key=True)  # Field name made lowercase.
    areaname = models.CharField(db_column='AreaName', max_length=45)  # Field name made lowercase.
    city_cityid = models.ForeignKey('City', models.DO_NOTHING, db_column='City_CityId')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'area'
    def __str__(self):
        return self.areaname
    def get_add_url(self):
        return reverse('admm:area-add')
    def get_del_url(self):
        return reverse('admm:area-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:area-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Area'})

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)



class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    # username = models.CharField(unique=True, max_length=150,null=True)
    first_name = models.CharField(max_length=30,verbose_name='First Name')
    last_name = models.CharField(max_length=150,verbose_name='Last Name')
    email = models.CharField(unique=True,max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    addressline1 = models.TextField(db_column='addressLine1',verbose_name='Address')  # Field name made lowercase.
    areaid = models.ForeignKey(Area, models.DO_NOTHING, db_column='areaid',verbose_name='Area')
    mobileno = models.DecimalField(db_column='MobileNo', max_digits=10, decimal_places=0,verbose_name='Mobile No ')  # Field name made lowercase.
    secque = models.TextField(db_column='secQue')  # Field name made lowercase.
    secqans = models.TextField(db_column='secQAns')  # Field name made lowercase.
    userroleid = models.ForeignKey('Userrole', models.DO_NOTHING, db_column='userRoleId')  # Field name made lowercase.
    branchid = models.ForeignKey('Branch', models.DO_NOTHING, db_column='branchId',blank=True)  # Field name made lowercase.
    islocked = models.IntegerField(db_column='isLocked')  # Field name made lowercase.


    # USERNAME_FIELD='username'
    # REQUIRED_FIELDS=[]
    # is_anonymous=False
    # is_authenticated=True

    class Meta:
        # verbose_name='User'
        managed = False
        db_table = 'auth_user'
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'User'})
    def __str__(self):
        return self.first_name+' '+self.last_name
        # return str(self.id)

class AuthUserGroups(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Branch(models.Model):
    branchid = models.IntegerField(name='id',db_column='BranchId', primary_key=True)  # Field name made lowercase.
    branchaddress = models.TextField(db_column='BranchAddress')  # Field name made lowercase.
    mobileno = models.DecimalField(db_column='MobileNo', max_digits=10, decimal_places=0)  # Field name made lowercase.
    company_companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='Company_CompanyId')  #Field name made lowercase.
    areaid=models.ForeignKey('Area',models.DO_NOTHING,db_column='areaId')
    class Meta:
        managed = False
        db_table = 'branch'
    def __str__(self):
        return str(self.id)
    def get_add_url(self):
         return reverse('admm:branch-add')
    def get_del_url(self):
         return reverse('admm:branch-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:branch-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Branch'})


# class Cancellationofordadv(models.Model):
#     order_id = models.ForeignKey('Orderdetails', models.DO_NOTHING, db_column='OrderId',primary_key=True,related_name='orderIdforCan',name='id')  # Field name made lowercase.
#     advrtid = models.ForeignKey('Orderdetails', models.DO_NOTHING, db_column='AdvId',related_name='advIdforCan')# Field name made lowercase.
#     cancellationdatetime = models.DateTimeField(db_column='CancellationDateTime')  # Field name made lowercase.
#     reasonofcancellation = models.TextField(db_column='ReasonOfCancellation', blank=True, null=True)  # Field name made lowercase.
#     paymentrefid = models.CharField(db_column='PaymentRefId', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
#     paymentdatetime = models.DateTimeField(db_column='PaymentDateTime', blank=True, null=True)  # Field name made lowercase.
#     refundedamount = models.IntegerField(db_column='RefundedAmount', blank=True, null=True)  # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'cancellationofordadv'
#         unique_together = (('id', 'advrtid'),)
#     def get_add_url(self):
#         return reverse('admm:cancellationofordadv-add')
#     def get_del_url(self):
#         return reverse('admm:cancellationofordadv-del',kwargs={'pk':self.pk})
#     def get_upd_url(self):
#          return reverse('admm:cancellationofordadv-upd',kwargs={'pk':self.pk})
#     def get_absolute_url(self):
#         return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Cancellationofordadv'})

class Cartdetail(models.Model):
    # userid = models.ForeignKey('User', models.DO_NOTHING)# Field name made lowercase.
    auth_user = models.ForeignKey('User', models.CASCADE)
    advertisement_advid = models.ForeignKey('Advertisement',models.CASCADE, db_column='Advertisement_AdvId',primary_key=True ,name='id')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'cartdetail'
        unique_together = (('auth_user', 'id'),)
    def __str__(self):
        return 'Cartdetail'
    def get_add_url(self):
        return reverse('admm:cartdetail-add')
    def get_del_url(self):
        return reverse('admm:cartdetail-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:cartdetail-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':''})

class Category(models.Model):
    categoryid = models.AutoField(db_column='CategoryId', primary_key=True,name='id')  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', unique=True, max_length=45,verbose_name='Category ')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'category'
    def __str__(self):
        return self.categoryname
        # return 'Category'
    def get_add_url(self):
         return reverse('admm:category-add',kwargs={'objname':'Category'})
    def get_del_url(self):
         return reverse('admm:category-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:category-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Category'})
    # def get_values(self,fld):
    #     if fld=='categoryid':
    #         return str(self.categoryid)
    #     else:
    #         return str(self.categoryname)HYIIIIIIIIIIIIUUUUUUUUUUUYYYYTTTTTTTTTTRRRRRRRRWWWWWWWWWSWSAADDDDDDDFFHHJJJJIIIIIIIIIIIIIIIIIIIIIIIIIUUYYYYYYYYYYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUJJJJJJKIIIIIIIIOOOOOOOOOOOOOOOOOOOOOOOOLLLLLLLLLLLL...///

class City(models.Model):
    cityid = models.IntegerField(db_column='CityId', primary_key=True,name='id')  # Field name made lowercase.
    cityname = models.CharField(db_column='CityName', max_length=45)  # Field name made lowercase.
    state_stateid = models.ForeignKey('State', models.DO_NOTHING, db_column='State_StateId')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'city'
    def __str__(self):
        return self.cityname
    def get_add_url(self):
        return reverse('admm:city-add',kwargs={'objname':'City'})
    def get_del_url(self):
        return reverse('admm:city-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:city-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'City'})

class Commissiondetail(models.Model):
    advertisement_advid = models.ForeignKey('Advertisement', models.CASCADE, db_column='Advertisement_AdvId', primary_key=True,name='id')  # Field name made lowercase.
    commission = models.FloatField(db_column='Commission')  # Field name made lowercase.
    createddatetime = models.DateTimeField(db_column='CreatedDateTime')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'commissiondetail'
        unique_together = (('id', 'commission', 'createddatetime'),)
    def __str__(self):
        return 'Commissiondetail'
    def get_add_url(self):
        return reverse('admm:commissiondetail-add',kwargs={'objname':'Commissiondetail'})
    def get_del_url(self):
        return reverse('admm:commissiondetail-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:commissiondetail-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Commissiondetail'})

class Company(models.Model):
    companyid = models.IntegerField(db_column='CompanyId', primary_key=True,name='id')  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=90)  # Field name made lowercase.
    logopath = models.TextField(db_column='logoPath') # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'company'
    def __str__(self):
        return 'Company'
    def get_add_url(self):
        return reverse('admm:company-add')
    def get_del_url(self):
        return reverse('admm:company-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:company-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Company'})


class Complaintdetail(models.Model):
    orderdetails_order_orderid = models.ForeignKey('Orderdetails', models.DO_NOTHING, db_column='orderdetails_Order_OrderId', primary_key=True,related_name='complaintOrder')  # Field name made lowercase.
    orderdetails_advertisement_advid = models.ForeignKey('Orderdetails', models.DO_NOTHING, db_column='orderdetails_Advertisement_AdvId',related_name='advIdComplaint')  # Field name made lowercase.
    complaintdatetime = models.DateTimeField(db_column='ComplaintDateTime',name='datetime')  # Field name made lowercase.
    complaintdescription = models.TextField(db_column='ComplaintDescription',name='description')  # Field name made lowercase.
    responsetext = models.TextField(db_column='ResponseText', blank=True, null=True)  # Field name made lowercase.
    responsedatetime = models.DateTimeField(db_column='ResponseDateTime', blank=True, null=True)  # Field name made lowercase.
    auth_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'complaintdetail'
        unique_together = (('orderdetails_order_orderid', 'orderdetails_advertisement_advid', 'datetime'),)


class Country(models.Model):
    countryid = models.IntegerField(db_column='CountryId', primary_key=True,name='id')  # Field name made lowercase.
    countryname = models.CharField(db_column='CountryName', unique=True, max_length=45)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'country'
    def get_add_url(self):
        return reverse('admm:country-add')
    def get_del_url(self):
        return reverse('admm:country-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:country-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Country'})
    def __str__(self):
        return 'Country'

class Coupondetail(models.Model):
    couponid = models.AutoField(db_column='CouponId', primary_key=True,name='id')  # Field name made lowercase.
    couponcode = models.CharField(db_column='CouponCode', unique=True, max_length=45)  # Field name made lowercase.
    coupondescription = models.TextField(db_column='CouponDescription', blank=True, null=True)  # Field name made lowercase.
    coupondiscount = models.FloatField(db_column='CouponDiscount')  # Field name made lowercase.
    couponstartdate = models.DateField(db_column='CouponStartDate')  # Field name made lowercase.
    couponenddate = models.DateField(db_column='CouponEndDate')  # Field name made lowercase.
    mincartvalue = models.IntegerField(db_column='MinCartValue', blank=True, null=True)  # Field name made lowercase.
    # userid = models.ForeignKey('User', models.DO_NOTHING, db_column='id')# Field name made lowercase.
    auth_user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'coupondetail'
    def get_add_url(self):
        return reverse('admm:coupondetail-add')
    def get_del_url(self):
        return reverse('admm:coupondetail-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:coupondetail-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Coupondetail'})
    def __str__(self):
        return str(self.id)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


# class Docdetail(models.Model):
#     userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId',primary_key=True)  # Field name made lowercase.
#     sellerdoclist_docid = models.IntegerField(db_column='SellerDocList_DocId')  # Field name made lowercase.
#     docpath = models.TextField(db_column='DocPath')  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'docdetail'
#         unique_together = (('userdetail_userid', 'sellerdoclist_docid'),)
#     def get_absolute_url(self):
#          return reverse('admm:sellerdoc-detail',kwargs={'pk':self.pk})

class Durationwisepricing(models.Model):
    advertisement_advid = models.ForeignKey('Advertisement', models.CASCADE, db_column='Advertisement_AdvId', primary_key=True)  # Field name made lowercase.
    noofdays = models.IntegerField(db_column='NoOfDays')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'durationwisepricing'
        unique_together = (('advertisement_advid', 'noofdays'),)
    def get_add_url(self):
        return reverse('admm:durationwisepricing-add')
    def get_del_url(self):
        return reverse('admm:durationwisepricing-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:durationwisepricing-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Durationwisepricing'})
    def __str__(self):
        return str(self.noofdays)+" "+str(self.price)


class Offercoveringadvs(models.Model):
    offerdetail_offerid = models.ForeignKey('Offerdetail', models.DO_NOTHING, db_column='OfferDetail_OfferId', primary_key=True,name='id')  # Field name made lowercase.
    advertisement_advid = models.ForeignKey('Advertisement', models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'offercoveringadvs'
        unique_together = (('id', 'advertisement_advid'),)
    def get_add_url(self):
        return reverse('admm:offercoveringadvs-add')
    def get_del_url(self):
        return reverse('admm:offercoveringadvs-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:offercoveringadvs-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Offercoveringadvs'})
    def __str__(self):
        return 'Offercoveringadvs'

class Offerdetail(models.Model):
    offerid = models.AutoField(db_column='OfferId', primary_key=True,name='id')  # Field name made lowercase.
    description = models.TextField(db_column='Description',default=None)  # Field name made lowercase.
    discount = models.FloatField(db_column='Discount')  # Field name made lowercase.
    offerstartdatetime = models.DateField(db_column='OfferStartDateTime',name='startdate')  # Field name made lowercase.
    offerenddatetime = models.DateField(db_column='OfferEndDateTime',name='enddate')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'offerdetail'
    def get_add_url(self):
        return reverse('admm:offerdetail-add')
    def get_del_url(self):
        return reverse('admm:offerdetail-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:offerdetail-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Offerdetail'})
    def __self__(self):
        return 'Offerdetail'

class Order( models.Model):
    orderid = models.AutoField(db_column='OrderId', primary_key=True,name='id')  # Field name made lowercase.
    auth_user = models.ForeignKey('User', models.DO_NOTHING)
    orderdatetime = models.DateTimeField(db_column='OrderDateTime')  # Field name made lowercase.
    emipayment = models.IntegerField(db_column='EmiPayment')  # Field name made lowercase.
    emimonths = models.IntegerField(db_column='EmiMonths', blank=True, null=True)  # Field name made lowercase.
    coupondetail_couponid = models.ForeignKey('Coupondetail', models.DO_NOTHING, db_column='CouponDetail_CouponId', blank=True, null=True)  # Field name made lowercase.
    discountamount = models.IntegerField(db_column='DiscountAmount', blank=True, null=True)  # Field name made lowercase.
    gst_amount = models.IntegerField(db_column='GST_Amount')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'order'
    def __str__(self):
        return str(self.id)
    def get_add_url(self):
        return reverse('admm:order-add')
    def get_del_url(self):
        return reverse('admm:order-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:order-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Order'})

# class Orderfeedback(models.Model):
#     orderdetail_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='OrderDetail_OrderId', primary_key=True)  # Field name made lowercase.
#     feedbackdatetime = models.DateTimeField(db_column='FeedbackDateTime')  # Field name made lowercase.
#     feedbacktext = models.TextField(db_column='FeedbackText', blank=True, null=True)  # Field name made lowercase.
#     rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
#     responsedatetime = models.CharField(db_column='ResponseDateTime', max_length=45, blank=True, null=True)  # Field name made lowercase.
#     responsetext = models.TextField(db_column='ResponseText', blank=True, null=True)  # Field name made lowercase.
#     userid = models.ForeignKey('User', models.DO_NOTHING, db_column='id',blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'orderfeedback'
#     def get_add_url(self):
#         return reverse('admm:orderfeedback-add')
#     def get_del_url(self):
#         return reverse('admm:orderfeedback-del',kwargs={'pk':self.pk})
#     def get_upd_url(self):
#          return reverse('admm:orderfeedback-upd',kwargs={'pk':self.pk})

class Orderfeedback(models.Model):
    # orderid=models.OneToOneField('Orderdetails',models.DO_NOTHING,db_column='orderdetails_Order_OrderId',primary_key=True,related_name='odrIdFdbkTable')
    orderdetails_order_orderid = models.ForeignKey('Orderdetails', models.DO_NOTHING, db_column='orderdetails_Order_OrderId', primary_key=True,related_name='orderfeedback',name='odrid')  # Field name made lowercase.
    orderdetails_advertisement_advid = models.ForeignKey('Orderdetails', models.DO_NOTHING, db_column='orderdetails_Advertisement_AdvId',related_name='advIdOrderFeedback',name='advid')  # Field name made lowercase.
    feedbackdatetime = models.DateTimeField(db_column='FeedbackDateTime',name='datetime')  # Field name made lowercase.
    feedbacktext = models.TextField(db_column='FeedbackText', blank=True, null=True,name='description')  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    responsedatetime = models.DateTimeField(db_column='ResponseDateTime', blank=True, null=True)  # Field name made lowercase.
    responsetext = models.TextField(db_column='ResponseText', blank=True, null=True)  # Field name made lowercase.
    auth_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orderfeedback'
        unique_together = (('odrid', 'advid'),)

    def get(self):
        return str(self.odrid)


class Orderpayment(models.Model):
    paymentrefid = models.CharField(db_column='PaymentRefId', primary_key=True, max_length=45,name='id')  # Field name made lowercase.
    orderdetail_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='OrderDetail_OrderId')  #Field name made lowercase.
    paymentdatetime = models.DateTimeField(db_column='PaymentDateTime')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderpayment'
    def get_add_url(self):
        return reverse('admm:orderpayment-add')
    def get_del_url(self):
        return reverse('admm:orderpayment-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:orderpayment-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Orderpayment'})
    def __self__(self):
        return 'Orderpayment'

# class Orderdetails(models.Model):
#     order_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='Order_OrderId', primary_key=True,name='id')  # Field name made lowercase.
#     advertisement_advid = models.ForeignKey('Advertisement', models.CASCADE, related_name='advertisements' ,db_column='Advertisement_AdvId')  # Field name made lowercase.
#     advprice = models.IntegerField(db_column='AdvPrice')  # Field name made lowercase.
#     advstartdate = models.DateField(db_column='AdvStartDate')  # Field name made lowercase.
#     advenddate = models.DateField(db_column='AdvEndDate')  # Field name made lowercase.
#     quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
#     class Meta:
#         managed = False
#         db_table = 'orderdetails'
#         unique_together = (('id', 'advertisement_advid'),)
#     def __str__(self):
#         return str(self.id)
#
#     def get_add_url(self):
#         return reverse('admm:orderdetails-add')
#     def get_del_url(self):
#         return reverse('admm:orderdetails-del',kwargs={'pk':self.pk})
#     def get_upd_url(self):
#          return reverse('admm:orderdetails-upd',kwargs={'pk':self.pk})
#     def get_absolute_url(self):
#         return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Orderdetails'})

class Orderdetails(models.Model):
    order_orderid = models.ForeignKey('Order', models.CASCADE, db_column='Order_OrderId', primary_key=True,name='id')  # Field name made lowercase.
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.
    advprice = models.IntegerField(db_column='AdvPrice')  # Field name made lowercase.
    advstartdate = models.DateField(db_column='AdvStartDate')  # Field name made lowercase.
    advenddate = models.DateField(db_column = 'AdvEndDate')  # Field name made lowercase.
    quantity = models.IntegerField(db_column = 'Quantity', blank=True, null=True)  # Field name made lowercase.
    cancellationdatetime = models.DateTimeField(db_column='CancellationDateTime', blank=True, null=True)  # Field name made lowercase.
    reasonofcancellation = models.TextField(db_column='ReasonOfCancellation', blank=True, null=True)  # Field name made lowercase.
    paymentrefid = models.CharField(db_column='PaymentRefId', unique=True, max_length=70, blank=True, null=True)  # Field name made lowercase.
    paymentdatetime = models.DateTimeField(db_column='PaymentDateTime', blank=True, null=True)  # Field name made lowercase.
    refundedamount = models.IntegerField(db_column='RefundedAmount', blank=True, null=True)  # Field name made lowercase.
    served = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orderdetails'
        unique_together = (('id', 'advertisement_advid'),)
    def __str__(self):
        return str(self.id)
    def get_add_url(self):
        return reverse('admm:orderdetails-add')

    def get_del_url(self):
        return reverse('admm:orderdetails-del', kwargs={'pk': self.pk})

    def get_upd_url(self):
        return reverse('admm:orderdetails-upd', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('admm:randomObjDetail', kwargs={'pk': self.pk, 'objname': 'Orderdetails'})

class Package(models.Model):
    packageid = models.IntegerField(name='id',db_column='PackageId', primary_key=True)  # Field name made lowercase.
    packagedescription = models.TextField(db_column='PackageDescription', max_length=200,default=None,name='description')  # Field name made lowercase.
    discount = models.FloatField(db_column='Discount', default=None)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'package'
    def get_add_url(self):
        return reverse('admm:package-add')
    def get_del_url(self):
        return reverse('admm:package-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:package-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Package'})
    def __self__(self):
        return 'Package'

class PackageHasAdv(models.Model):
    package_packageid = models.ForeignKey('Package', models.CASCADE, db_column='Package_PackageId', primary_key=True,name='id')  # Field name made lowercase.
    advertisement_advid = models.ForeignKey('Advertisement', models.CASCADE, db_column='Advertisement_AdvId')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'package_has_adv'
        unique_together = (('id', 'advertisement_advid'),)
    def __str__(self):
        return 'PackageHasAdv'
    def get_add_url(self):
        return reverse('admm:packageHasAdv-add')
    def get_del_url(self):
        return reverse('admm:packageHasAdv-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:packageHasAdv-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'PackageHasAdv'})

# class Sellerdocdetail(models.Model):
#     userdetail_userid = models.IntegerField('User',db_column='UserDetail_UserId', primary_key=True)  # Field name made lowercase.
#     sellerdoclist_docid = models.IntegerField(db_column='SellerDocList_DocId')  # Field name made lowercase.
#     docpath = models.TextField(db_column='DocPath')  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'sellerdocdetail'
#         unique_together = (('userdetail_userid', 'sellerdoclist_docid'),)


class Sellerdocdetail(models.Model):
    auth_user = models.ForeignKey('User', models.DO_NOTHING, primary_key=True,name='auth_user')
    sellerdoclist_docid = models.ForeignKey('Sellerdoclist', models.DO_NOTHING, db_column='sellerdoclist_DocId')  # Field name made lowercase.
    docpath = models.TextField(db_column='DocPath')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'sellerdocdetail'
        unique_together = (('auth_user', 'sellerdoclist_docid'),)
    def __str__(self):
        return 'Sellerdocdetail'
    def get_add_url(self):
        return reverse('admm:Sellerdocdetail-add')
    def get_del_url(self):
        return reverse('admm:Sellerdocdetail-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:Sellerdocdetail-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Sellerdocdetail'})

class Sellerdoclist(models.Model):
    docid = models.IntegerField(db_column='DocId', primary_key=True)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sellerdoclist'
    def __str__(self):
        return 'Sellerdoclist'
    def get_add_url(self):
        return reverse('admm:Sellerdoclist-add')
    def get_del_url(self):
        return reverse('admm:-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:Sellerdoclist-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Sellerdoclist'})

class State(models.Model):
    stateid = models.IntegerField(db_column='StateId', primary_key=True,name='id')  # Field name made lowercase.
    statename = models.CharField(db_column='StateName', max_length=45)  # Field name made lowercase.
    country_countryid = models.ForeignKey(Country, models.DO_NOTHING, db_column='Country_CountryId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'state'

    def __str__(self):
        return 'State'
    def get_add_url(self):
        return reverse('admm:State-add')
    def get_del_url(self):
        return reverse('admm:State-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:State-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'State'})

class Subcategory(models.Model):
    subcatid = models.IntegerField(db_column='SubCatId', primary_key=True,name='id')  # Field name made lowercase.
    subcatname = models.CharField(db_column='SubCatName', unique=True, max_length=45,verbose_name='SubCatName')  # Field name made lowercase.
    commission = models.FloatField(db_column='Commission')  # Field name made lowercase.
    category_categoryid = models.ForeignKey(Category,models.DO_NOTHING, db_column='Category_CategoryId',name='catid')
 # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subcategory'
        unique_together = (('id', 'catid'),)
    def get_add_url(self):
        return reverse('admm:Subcategory-add')
    def get_del_url(self):
        return reverse('admm:Subcategory-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:Subcategory-upd',kwargs={'pk':self.pk})
    def __str__(self):
        return self.subcatname
    def name(self):
        return self.subcatname
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Subcategory'})

class Updationinorder(models.Model):
    orderid = models.ForeignKey(Orderdetails, models.DO_NOTHING, db_column='OrderId', primary_key=True,related_name='ordIdForUpd',name='id')  # Field name made lowercase.
    advid = models.ForeignKey(Orderdetails, models.DO_NOTHING, db_column='AdvId')  # Field name made lowercase.
    updationdatetime = models.DateTimeField(db_column='UpdationDateTime')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    paymentrefid = models.CharField(db_column='PaymentRefId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    paymentdatetime = models.DateTimeField(db_column='PaymentDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updationinorder'
        unique_together = (('id', 'advid', 'updationdatetime'),)
    def get_add_url(self):
        return reverse('admm:Updationinorder-add')
    def get_del_url(self):
        return reverse('admm:Updationinorder-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:Updationinorder-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Updationinorder'})
    def __str__(self):
        return 'Updationinorder'

# class Userdetail(models.Model):
#     userid = models.IntegerField(db_column='UserId', primary_key=True)  # Field name made lowercase.
#     fname = models.CharField(db_column='Fname', max_length=45)  # Field name made lowercase.
#     lname = models.CharField(db_column='Lname', max_length=45)  # Field name made lowercase.
#     emailid = models.TextField(db_column='EmailId')  # Field name made lowercase.
#     username = models.CharField(db_column='UserName', unique=True, max_length=45, blank=True, null=True)# Field name made lowercase.
#     password = models.CharField(db_column='Password', max_length=45)  # Field name made lowercase.
#     secque = models.CharField(db_column='SecQue', max_length=90)  # Field name made lowercase.
#     secqueans = models.CharField(db_column='SecQueAns', max_length=45)  # Field name made lowercase.
#     mobileno = models.DecimalField(db_column='MobileNo', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     addressline1 = models.TextField(db_column='AddressLine1')  # Field name made lowercase.
#     islocked = models.IntegerField(db_column='IsLocked')  # Field name made lowercase.
#     area_areaid = models.ForeignKey(Area, models.DO_NOTHING, db_column='Area_AreaId')  # Field name made lowercase.
#     userrole_roleid = models.ForeignKey('Userrole', models.DO_NOTHING, db_column='UserRole_RoleId')  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'userdetail'
#     def __str__(self):
#         return 'Userdetail'
#     def get_add_url(self):
#          return reverse('admm:user-add')
#     def get_del_url(self):
#          return reverse('admm:user-del',kwargs={'pk':self.pk})
#     def get_upd_url(self):
#          return reverse('admm:user-upd',kwargs={'pk':self.pk})


class Userrole(models.Model):
    roleid = models.IntegerField(db_column='RoleId', primary_key=True)  # Field name made lowercase.
    rolename = models.CharField(db_column='RoleName', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userrole'
    def get_add_url(self):
        return reverse('admm:Userrole-add')
    def get_del_url(self):
        return reverse('admm:-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:Userrole-upd',kwargs={'pk':self.pk})
    def __str__(self):
        return str(self.rolename)
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Userrole'})

# class Wishlistdetail(models.Model):
#     userid = models.ForeignKey(User, models.DO_NOTHING, db_column='id', primary_key=True)  # Field name made lowercase.
#     advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'wishlistdetail'
#         unique_together = (('userid', 'advertisement_advid'),)
#     def __str__(self):
#         return 'Wishlistdetail'
#     def get_add_url(self):
#         return reverse('admm:Wishlistdetail-add')
#     def get_del_url(self):
#         return reverse('admm:Wishlistdetail-del',kwargs={'pk':self.pk})
#     def get_upd_url(self):
#          return reverse('admm:Wishlistdetail-upd',kwargs={'pk':self.pk})

class Wishlistdetail(models.Model):
    advertisement_advid = models.ForeignKey('Advertisement', models.CASCADE, db_column='Advertisement_AdvId', primary_key=True,name='id')  # Field name made lowercase.
    auth_user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wishlistdetail'
        unique_together = (('id', 'auth_user'),)
    def __str__(self):
        return 'Wishlistdetail'
    def get_add_url(self):
        return reverse('admm:Wishlistdetail-add')
    def get_del_url(self):
        return reverse('admm:Wishlistdetail-del',kwargs={'pk':self.pk})
    def get_upd_url(self):
         return reverse('admm:Wishlistdetail-upd',kwargs={'pk':self.pk})
    def get_absolute_url(self):
        return reverse('admm:randomObjDetail',kwargs={'pk':self.pk,'objname':'Wishlistdetail'})