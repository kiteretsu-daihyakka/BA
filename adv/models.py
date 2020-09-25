from django.db import models

# Create your models here.

class Advertisement(models.Model):
    advid = models.AutoField(db_column='AdvId', primary_key=True)  # Field name made lowercase.
    advregno = models.CharField(db_column='AdvRegNo', unique=True, max_length=45, blank=True, null=True)
# Field name made lowercase.
    height = models.IntegerField(db_column='Height')  # Field name made lowercase.
    width = models.IntegerField(db_column='Width')  # Field name made lowercase.
    maxdays = models.IntegerField(db_column='MaxDays')  # Field name made lowercase.
    minquantity = models.IntegerField(db_column='MinQuantity', blank=True, null=True)  # Field name made lowercase.
    addressline1 = models.TextField(db_column='AddressLine1')  # Field name made lowercase.
    area_areaid = models.ForeignKey('Area', models.DO_NOTHING, db_column='Area_AreaId', blank=True, null=True)  # Field name made lowercase.
    city_cityid = models.ForeignKey('City', models.DO_NOTHING, db_column='City_CityId', blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock', blank=True, null=True)  # Field name made lowercase.
    defaultimgpath = models.TextField(db_column='DefaultImgPath')  # Field name made lowercase.
    subcategory_subcatid = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='SubCategory_SubCatId')  # Field name made lowercase.
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId')
 # Field name made lowercase.
    isowned = models.IntegerField(db_column='IsOwned')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'advertisement'


class Advimgs(models.Model):
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId', primary_key=True)  # Field name made lowercase.
    imagepath = models.CharField(db_column='ImagePath', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'advimgs'
        unique_together = (('advertisement_advid', 'imagepath'),)


class Area(models.Model):
    areaid = models.IntegerField(db_column='AreaId', primary_key=True)  # Field name made lowercase.
    areaname = models.CharField(db_column='AreaName', max_length=45)  # Field name made lowercase.
    city_cityid = models.ForeignKey('City', models.DO_NOTHING, db_column='City_CityId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'area'


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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Branch(models.Model):
    branchid = models.IntegerField(db_column='BranchId', primary_key=True)  # Field name made lowercase.
    branchaddress = models.TextField(db_column='BranchAddress')  # Field name made lowercase.
    mobileno = models.DecimalField(db_column='MobileNo', max_digits=10, decimal_places=0)  # Field name made lowercase.
    company_companyid = models.ForeignKey('Company', models.DO_NOTHING, db_column='Company_CompanyId')  #Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'branch'

class Order(models.Model):
    orderid = models.AutoField(db_column='OrderId', primary_key=True)  # Field name made lowercase.
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId')# Field name made lowercase.
    orderdatetime = models.DateTimeField(db_column='OrderDateTime')  # Field name made lowercase.
    emipayment = models.IntegerField(db_column='EmiPayment')  # Field name made lowercase.
    emimonths = models.IntegerField(db_column='EmiMonths', blank=True, null=True)  # Field name made lowercase.
    coupondetail_couponid = models.ForeignKey('Coupondetail', models.DO_NOTHING, db_column='CouponDetail_CouponId', blank=True, null=True)  # Field name made lowercase.
    discountamount = models.IntegerField(db_column='DiscountAmount', blank=True, null=True)  # Field name made lowercase.
    gst_amount = models.IntegerField(db_column='GST_Amount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order'

class Orderdetails(models.Model):
    order_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='Order_OrderId', primary_key=True)  # Field name made lowercase.
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.
    advprice = models.IntegerField(db_column='AdvPrice')  # Field name made lowercase.
    advstartdate = models.DateField(db_column='AdvStartDate')  # Field name made lowercase.
    advenddate = models.DateField(db_column='AdvEndDate')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderdetails'
        unique_together = (('order_orderid', 'advertisement_advid'),)

class Cancellationofordadv(models.Model):
    order_id = models.ForeignKey(Orderdetails, models.DO_NOTHING, db_column='OrderId',related_name='orderIdforCan')  # Field name made lowercase.  
    advrtid = models.ForeignKey(Orderdetails, models.DO_NOTHING, db_column='AdvId',related_name='advIdforCan')# Field name made lowercase.
    cancellationdatetime = models.DateTimeField(db_column='CancellationDateTime')  # Field name made lowercase.
    reasonofcancellation = models.TextField(db_column='ReasonOfCancellation', blank=True, null=True)  # Field name made lowercase.
    paymentrefid = models.CharField(db_column='PaymentRefId', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    paymentdatetime = models.DateTimeField(db_column='PaymentDateTime', blank=True, null=True)  # Field name made lowercase.
    refundedamount = models.IntegerField(db_column='RefundedAmount', blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'cancellationofordadv'
        unique_together = (('order_id', 'advrtid'),)


class Cartdetail(models.Model):
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId')  # Field name made lowercase.
    advertisement_advid = models.ForeignKey('Advertisement', models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cartdetail'
        unique_together = (('userdetail_userid', 'advertisement_advid'),)


class Category(models.Model):
    categoryid = models.AutoField(db_column='CategoryId', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'


class City(models.Model):
    cityid = models.IntegerField(db_column='CityId', primary_key=True)  # Field name made lowercase.
    cityname = models.CharField(db_column='CityName', max_length=45)  # Field name made lowercase.
    state_stateid = models.ForeignKey('State', models.DO_NOTHING, db_column='State_StateId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city'


class Commissiondetail(models.Model):
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId', primary_key=True)  # Field name made lowercase.
    commission = models.FloatField(db_column='Commission')  # Field name made lowercase.
    createddatetime = models.DateTimeField(db_column='CreatedDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'commissiondetail'
        unique_together = (('advertisement_advid', 'commission', 'createddatetime'),)


class Company(models.Model):
    companyid = models.IntegerField(db_column='CompanyId', primary_key=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=90)  # Field name made lowercase.
    logopath = models.TextField(db_column='logoPath')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'


class Complaintdetail(models.Model):
    orderdetail_orderid = models.ForeignKey('Order', models.DO_NOTHING, db_column='OrderDetail_OrderId', primary_key=True)  # Field name made lowercase.
    complaintdatetime = models.DateTimeField(db_column='ComplaintDateTime')  # Field name made lowercase.
    complaintdescription = models.TextField(db_column='ComplaintDescription')  # Field name made lowercase.
    responsetext = models.TextField(db_column='ResponseText', blank=True, null=True)  # Field name made lowercase.
    responsedatetime = models.DateTimeField(db_column='ResponseDateTime', blank=True, null=True)  # Field name made lowercase.
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId',
blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complaintdetail'
        unique_together = (('orderdetail_orderid', 'complaintdatetime'),)


class Country(models.Model):
    countryid = models.IntegerField(db_column='CountryId', primary_key=True)  # Field name made lowercase.
    countryname = models.CharField(db_column='CountryName', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'country'


class Coupondetail(models.Model):
    couponid = models.AutoField(db_column='CouponId', primary_key=True)  # Field name made lowercase.
    couponcode = models.CharField(db_column='CouponCode', unique=True, max_length=45)  # Field name made lowercase.
    coupondescription = models.TextField(db_column='CouponDescription', blank=True, null=True)  # Field name made lowercase.
    coupondiscount = models.FloatField(db_column='CouponDiscount', unique=True)  # Field name made lowercase.
    couponstartdate = models.DateField(db_column='CouponStartDate')  # Field name made lowercase.
    couponenddate = models.DateField(db_column='CouponEndDate')  # Field name made lowercase.
    mincartvalue = models.IntegerField(db_column='MinCartValue', blank=True, null=True)  # Field name made lowercase.
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId')
 # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'coupondetail'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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


class Docdetail(models.Model):
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId',primary_key=True)  # Field name made lowercase.
    sellerdoclist_docid = models.IntegerField(db_column='SellerDocList_DocId')  # Field name made lowercase.
    docpath = models.TextField(db_column='DocPath')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'docdetail'
        unique_together = (('userdetail_userid', 'sellerdoclist_docid'),)


class Durationwisepricing(models.Model):
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId', primary_key=True)  # Field name made lowercase.
    noofdays = models.IntegerField(db_column='NoOfDays')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'durationwisepricing'
        unique_together = (('advertisement_advid', 'noofdays'),)


class Offercoveringadvs(models.Model):
    offerdetail_offerid = models.ForeignKey('Offerdetail', models.DO_NOTHING, db_column='OfferDetail_OfferId', primary_key=True)  # Field name made lowercase.
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'offercoveringadvs'
        unique_together = (('offerdetail_offerid', 'advertisement_advid'),)


class Offerdetail(models.Model):
    offerid = models.AutoField(db_column='OfferId', primary_key=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    discount = models.FloatField(db_column='Discount')  # Field name made lowercase.
    offerstartdatetime = models.DateField(db_column='OfferStartDateTime')  # Field name made lowercase.
    offerenddatetime = models.DateField(db_column='OfferEndDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'offerdetail'







class Orderfeedback(models.Model):
    orderdetail_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='OrderDetail_OrderId', primary_key=True)  # Field name made lowercase.
    feedbackdatetime = models.DateTimeField(db_column='FeedbackDateTime')  # Field name made lowercase.
    feedbacktext = models.TextField(db_column='FeedbackText', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    responsedatetime = models.CharField(db_column='ResponseDateTime', max_length=45, blank=True, null=True)  # Field name made lowercase.
    responsetext = models.TextField(db_column='ResponseText', blank=True, null=True)  # Field name made lowercase.
    userdetail_userid = models.ForeignKey('Userdetail', models.DO_NOTHING, db_column='UserDetail_UserId',
blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderfeedback'


class Orderpayment(models.Model):
    paymentrefid = models.CharField(db_column='PaymentRefId', primary_key=True, max_length=45)  # Field name made lowercase.
    orderdetail_orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='OrderDetail_OrderId')  #Field name made lowercase.
    paymentdatetime = models.DateTimeField(db_column='PaymentDateTime')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderpayment'


class Package(models.Model):
    packageid = models.IntegerField(db_column='PackageId', primary_key=True)  # Field name made lowercase.
    packagedescription = models.CharField(db_column='PackageDescription', max_length=70, blank=True, null=True)  # Field name made lowercase.
    discount = models.FloatField(db_column='Discount', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'package'


class PackageHasAdv(models.Model):
    package_packageid = models.ForeignKey(Package, models.DO_NOTHING, db_column='Package_PackageId', primary_key=True)  # Field name made lowercase.
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'package_has_adv'
        unique_together = (('package_packageid', 'advertisement_advid'),)


class Sellerdocdetail(models.Model):
    userdetail_userid = models.IntegerField(db_column='UserDetail_UserId', primary_key=True)  # Field name made lowercase.
    sellerdoclist_docid = models.IntegerField(db_column='SellerDocList_DocId')  # Field name made lowercase.
    docpath = models.TextField(db_column='DocPath')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sellerdocdetail'
        unique_together = (('userdetail_userid', 'sellerdoclist_docid'),)


class Sellerdoclist(models.Model):
    docid = models.IntegerField(db_column='DocId', primary_key=True)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sellerdoclist'


class State(models.Model):
    stateid = models.IntegerField(db_column='StateId', primary_key=True)  # Field name made lowercase.
    statename = models.CharField(db_column='StateName', max_length=45)  # Field name made lowercase.
    country_countryid = models.ForeignKey(Country, models.DO_NOTHING, db_column='Country_CountryId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'state'


class Subcategory(models.Model):
    subcatid = models.IntegerField(db_column='SubCatId', primary_key=True)  # Field name made lowercase.
    subcatname = models.CharField(db_column='SubCatName', unique=True, max_length=45)  # Field name made lowercase.
    category_categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='Category_CategoryId')
 # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subcategory'
        unique_together = (('subcatid', 'category_categoryid'),)


class Updationinorder(models.Model):
    orderid = models.ForeignKey(Orderdetails, models.DO_NOTHING, db_column='OrderId', primary_key=True,related_name='ordIdForUpd')  # Field name made lowercase.
    advid = models.ForeignKey(Orderdetails, models.DO_NOTHING, db_column='AdvId')  # Field name made lowercase.
    updationdatetime = models.DateTimeField(db_column='UpdationDateTime')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    paymentrefid = models.CharField(db_column='PaymentRefId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    paymentdatetime = models.DateTimeField(db_column='PaymentDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updationinorder'
        unique_together = (('orderid', 'advid', 'updationdatetime'),)


class Userdetail(models.Model):
    userid = models.IntegerField(db_column='UserId', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=45)  # Field name made lowercase.
    lname = models.CharField(db_column='Lname', max_length=45)  # Field name made lowercase.
    emailid = models.TextField(db_column='EmailId')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', unique=True, max_length=45, blank=True, null=True)# Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=45)  # Field name made lowercase.
    secque = models.CharField(db_column='SecQue', max_length=90)  # Field name made lowercase.
    secqueans = models.CharField(db_column='SecQueAns', max_length=45)  # Field name made lowercase.
    mobileno = models.DecimalField(db_column='MobileNo', max_digits=10, decimal_places=0)  # Field name made lowercase.
    addressline1 = models.TextField(db_column='AddressLine1')  # Field name made lowercase.
    islocked = models.IntegerField(db_column='IsLocked')  # Field name made lowercase.
    area_areaid = models.ForeignKey(Area, models.DO_NOTHING, db_column='Area_AreaId')  # Field name made lowercase.
    userrole_roleid = models.ForeignKey('Userrole', models.DO_NOTHING, db_column='UserRole_RoleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userdetail'


class Userrole(models.Model):
    roleid = models.IntegerField(db_column='RoleId', primary_key=True)  # Field name made lowercase.
    rolename = models.CharField(db_column='RoleName', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userrole'


class Wishlistdetail(models.Model):
    userdetail_userid = models.ForeignKey(Userdetail, models.DO_NOTHING, db_column='UserDetail_UserId', primary_key=True)  # Field name made lowercase.
    advertisement_advid = models.ForeignKey(Advertisement, models.DO_NOTHING, db_column='Advertisement_AdvId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wishlistdetail'
        unique_together = (('userdetail_userid', 'advertisement_advid'),)