# Generated by Django 2.2.3 on 2019-12-08 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adv', '0007_auto_20191208_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('advid', models.AutoField(db_column='AdvId', primary_key=True, serialize=False)),
                ('advregno', models.CharField(blank=True, db_column='AdvRegNo', max_length=45, null=True, unique=True)),
                ('height', models.IntegerField(db_column='Height')),
                ('width', models.IntegerField(db_column='Width')),
                ('maxdays', models.IntegerField(db_column='MaxDays')),
                ('minquantity', models.IntegerField(blank=True, db_column='MinQuantity', null=True)),
                ('addressline1', models.TextField(db_column='AddressLine1')),
                ('stock', models.IntegerField(blank=True, db_column='Stock', null=True)),
                ('defaultimgpath', models.TextField(db_column='DefaultImgPath')),
                ('isowned', models.IntegerField(db_column='IsOwned')),
            ],
            options={
                'db_table': 'advertisement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('areaid', models.IntegerField(db_column='AreaId', primary_key=True, serialize=False)),
                ('areaname', models.CharField(db_column='AreaName', max_length=45)),
            ],
            options={
                'db_table': 'area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branchid', models.IntegerField(db_column='BranchId', primary_key=True, serialize=False)),
                ('branchaddress', models.TextField(db_column='BranchAddress')),
                ('mobileno', models.DecimalField(db_column='MobileNo', decimal_places=0, max_digits=10)),
            ],
            options={
                'db_table': 'branch',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cancellationofordadv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancellationdatetime', models.DateTimeField(db_column='CancellationDateTime')),
                ('reasonofcancellation', models.TextField(blank=True, db_column='ReasonOfCancellation', null=True)),
                ('paymentrefid', models.CharField(blank=True, db_column='PaymentRefId', max_length=45, null=True, unique=True)),
                ('paymentdatetime', models.DateTimeField(blank=True, db_column='PaymentDateTime', null=True)),
                ('refundedamount', models.IntegerField(blank=True, db_column='RefundedAmount', null=True)),
            ],
            options={
                'db_table': 'cancellationofordadv',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cartdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(db_column='Price')),
                ('startdate', models.DateField(blank=True, db_column='StartDate', null=True)),
                ('enddate', models.DateField(blank=True, db_column='EndDate', null=True)),
                ('quantity', models.IntegerField(blank=True, db_column='Quantity', null=True)),
            ],
            options={
                'db_table': 'cartdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categoryid', models.AutoField(db_column='CategoryId', primary_key=True, serialize=False)),
                ('categoryname', models.CharField(db_column='CategoryName', max_length=45, unique=True)),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('cityid', models.IntegerField(db_column='CityId', primary_key=True, serialize=False)),
                ('cityname', models.CharField(db_column='CityName', max_length=45)),
            ],
            options={
                'db_table': 'city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('companyid', models.IntegerField(db_column='CompanyId', primary_key=True, serialize=False)),
                ('companyname', models.CharField(db_column='CompanyName', max_length=90)),
                ('logopath', models.TextField(db_column='logoPath')),
            ],
            options={
                'db_table': 'company',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('countryid', models.IntegerField(db_column='CountryId', primary_key=True, serialize=False)),
                ('countryname', models.CharField(db_column='CountryName', max_length=45, unique=True)),
            ],
            options={
                'db_table': 'country',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Coupondetail',
            fields=[
                ('couponid', models.AutoField(db_column='CouponId', primary_key=True, serialize=False)),
                ('couponcode', models.CharField(db_column='CouponCode', max_length=45, unique=True)),
                ('coupondescription', models.TextField(blank=True, db_column='CouponDescription', null=True)),
                ('coupondiscount', models.FloatField(db_column='CouponDiscount', unique=True)),
                ('couponstartdate', models.DateField(db_column='CouponStartDate')),
                ('couponenddate', models.DateField(db_column='CouponEndDate')),
                ('mincartvalue', models.IntegerField(blank=True, db_column='MinCartValue', null=True)),
            ],
            options={
                'db_table': 'coupondetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offerdetail',
            fields=[
                ('offerid', models.AutoField(db_column='OfferId', primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, db_column='Description', null=True)),
                ('discount', models.FloatField(db_column='Discount')),
                ('offerstartdatetime', models.DateField(db_column='OfferStartDateTime')),
                ('offerenddatetime', models.DateField(db_column='OfferEndDateTime')),
            ],
            options={
                'db_table': 'offerdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.AutoField(db_column='OrderId', primary_key=True, serialize=False)),
                ('orderdatetime', models.DateTimeField(db_column='OrderDateTime')),
                ('emipayment', models.IntegerField(db_column='EmiPayment')),
                ('emimonths', models.IntegerField(blank=True, db_column='EmiMonths', null=True)),
                ('discountamount', models.IntegerField(blank=True, db_column='DiscountAmount', null=True)),
                ('gst_amount', models.IntegerField(db_column='GST_Amount')),
            ],
            options={
                'db_table': 'order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orderpayment',
            fields=[
                ('paymentrefid', models.CharField(db_column='PaymentRefId', max_length=45, primary_key=True, serialize=False)),
                ('paymentdatetime', models.DateTimeField(db_column='PaymentDateTime')),
                ('amount', models.IntegerField(db_column='Amount')),
            ],
            options={
                'db_table': 'orderpayment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('packageid', models.IntegerField(db_column='PackageId', primary_key=True, serialize=False)),
                ('packagedescription', models.CharField(blank=True, db_column='PackageDescription', max_length=70, null=True)),
                ('discount', models.FloatField(blank=True, db_column='Discount', null=True)),
                ('startdate', models.DateField(db_column='StartDate')),
                ('enddate', models.DateField(db_column='EndDate')),
            ],
            options={
                'db_table': 'package',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sellerdocdetail',
            fields=[
                ('userdetail_userid', models.IntegerField(db_column='UserDetail_UserId', primary_key=True, serialize=False)),
                ('sellerdoclist_docid', models.IntegerField(db_column='SellerDocList_DocId')),
                ('docpath', models.TextField(db_column='DocPath')),
            ],
            options={
                'db_table': 'sellerdocdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sellerdoclist',
            fields=[
                ('docid', models.IntegerField(db_column='DocId', primary_key=True, serialize=False)),
                ('docname', models.CharField(db_column='DocName', max_length=45, unique=True)),
            ],
            options={
                'db_table': 'sellerdoclist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('stateid', models.IntegerField(db_column='StateId', primary_key=True, serialize=False)),
                ('statename', models.CharField(db_column='StateName', max_length=45)),
            ],
            options={
                'db_table': 'state',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('subcatid', models.IntegerField(db_column='SubCatId', primary_key=True, serialize=False)),
                ('subcatname', models.CharField(db_column='SubCatName', max_length=45, unique=True)),
            ],
            options={
                'db_table': 'subcategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userdetail',
            fields=[
                ('userid', models.IntegerField(db_column='UserId', primary_key=True, serialize=False)),
                ('fname', models.CharField(db_column='Fname', max_length=45)),
                ('lname', models.CharField(db_column='Lname', max_length=45)),
                ('emailid', models.TextField(db_column='EmailId')),
                ('username', models.CharField(blank=True, db_column='UserName', max_length=45, null=True, unique=True)),
                ('password', models.CharField(db_column='Password', max_length=45)),
                ('secque', models.CharField(db_column='SecQue', max_length=90)),
                ('secqueans', models.CharField(db_column='SecQueAns', max_length=45)),
                ('mobileno', models.DecimalField(db_column='MobileNo', decimal_places=0, max_digits=10)),
                ('addressline1', models.TextField(db_column='AddressLine1')),
                ('islocked', models.IntegerField(db_column='IsLocked')),
            ],
            options={
                'db_table': 'userdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userrole',
            fields=[
                ('roleid', models.IntegerField(db_column='RoleId', primary_key=True, serialize=False)),
                ('rolename', models.CharField(db_column='RoleName', max_length=45, unique=True)),
            ],
            options={
                'db_table': 'userrole',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Advimgs',
            fields=[
                ('advertisement_advid', models.ForeignKey(db_column='Advertisement_AdvId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Advertisement')),
                ('imagepath', models.CharField(db_column='ImagePath', max_length=150)),
            ],
            options={
                'db_table': 'advimgs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Commissiondetail',
            fields=[
                ('advertisement_advid', models.ForeignKey(db_column='Advertisement_AdvId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Advertisement')),
                ('commission', models.FloatField(db_column='Commission')),
                ('createddatetime', models.DateTimeField(db_column='CreatedDateTime')),
            ],
            options={
                'db_table': 'commissiondetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Complaintdetail',
            fields=[
                ('orderdetail_orderid', models.ForeignKey(db_column='OrderDetail_OrderId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Order')),
                ('complaintdatetime', models.DateTimeField(db_column='ComplaintDateTime')),
                ('complaintdescription', models.TextField(db_column='ComplaintDescription')),
                ('responsetext', models.TextField(blank=True, db_column='ResponseText', null=True)),
                ('responsedatetime', models.DateTimeField(blank=True, db_column='ResponseDateTime', null=True)),
            ],
            options={
                'db_table': 'complaintdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Docdetail',
            fields=[
                ('userdetail_userid', models.ForeignKey(db_column='UserDetail_UserId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Userdetail')),
                ('sellerdoclist_docid', models.IntegerField(db_column='SellerDocList_DocId')),
                ('docpath', models.TextField(db_column='DocPath')),
            ],
            options={
                'db_table': 'docdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Durationwisepricing',
            fields=[
                ('advertisement_advid', models.ForeignKey(db_column='Advertisement_AdvId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Advertisement')),
                ('noofdays', models.IntegerField(db_column='NoOfDays')),
                ('price', models.IntegerField(db_column='Price')),
            ],
            options={
                'db_table': 'durationwisepricing',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Offercoveringadvs',
            fields=[
                ('offerdetail_offerid', models.ForeignKey(db_column='OfferDetail_OfferId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Offerdetail')),
            ],
            options={
                'db_table': 'offercoveringadvs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orderdetails',
            fields=[
                ('order_orderid', models.ForeignKey(db_column='Order_OrderId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Order')),
                ('advprice', models.IntegerField(db_column='AdvPrice')),
                ('advstartdate', models.DateField(db_column='AdvStartDate')),
                ('advenddate', models.DateField(db_column='AdvEndDate')),
                ('quantity', models.IntegerField(blank=True, db_column='Quantity', null=True)),
            ],
            options={
                'db_table': 'orderdetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orderfeedback',
            fields=[
                ('orderdetail_orderid', models.ForeignKey(db_column='OrderDetail_OrderId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Order')),
                ('feedbackdatetime', models.DateTimeField(db_column='FeedbackDateTime')),
                ('feedbacktext', models.TextField(blank=True, db_column='FeedbackText', null=True)),
                ('rating', models.IntegerField(db_column='Rating')),
                ('responsedatetime', models.CharField(blank=True, db_column='ResponseDateTime', max_length=45, null=True)),
                ('responsetext', models.TextField(blank=True, db_column='ResponseText', null=True)),
            ],
            options={
                'db_table': 'orderfeedback',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PackageHasAdv',
            fields=[
                ('package_packageid', models.ForeignKey(db_column='Package_PackageId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Package')),
                ('quantity', models.IntegerField(blank=True, db_column='Quantity', null=True)),
            ],
            options={
                'db_table': 'package_has_adv',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlistdetail',
            fields=[
                ('userdetail_userid', models.ForeignKey(db_column='UserDetail_UserId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='adv.Userdetail')),
            ],
            options={
                'db_table': 'wishlistdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Updationinorder',
            fields=[
                ('orderid', models.ForeignKey(db_column='OrderId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='ordIdForUpd', serialize=False, to='adv.Orderdetails')),
                ('updationdatetime', models.DateTimeField(db_column='UpdationDateTime')),
                ('amount', models.IntegerField(blank=True, db_column='Amount', null=True)),
                ('paymentrefid', models.CharField(blank=True, db_column='PaymentRefId', max_length=45, null=True)),
                ('paymentdatetime', models.DateTimeField(blank=True, db_column='PaymentDateTime', null=True)),
            ],
            options={
                'db_table': 'updationinorder',
                'managed': False,
            },
        ),
    ]
