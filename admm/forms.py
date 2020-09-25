from django import forms
from .models import *

class CouponForm(forms.ModelForm):
    couponstartdate=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    couponenddate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model=Coupondetail
        exclude=('id','auth_user','couponcode')
        # fields=['couponcode','coupondescription','coupondiscount','couponstartdate','couponenddate','mincartvalue']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        exclude=('id',)

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model=Subcategory
        exclude=('id','catid')

class AdvForm(forms.ModelForm):
    advregno=forms.CharField(widget=forms.TextInput(attrs={'class':'hoardingFild'}))
    addressline1=forms.CharField(widget=forms.TextInput(attrs={'class':'hoardingFild'}))
    # area_areaid=forms.ChoiceField(widget=forms.NumberInput(attrs={'class':'hoardingFild'}))

    # city_cityid=forms.CharField(widget=forms.TextInput(attrs={'class':'rickFilds'}))
    stock=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'rickFilds'}))
    minquantity=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'rickFilds'}))
    class Meta:
        model = Advertisement
        fields = ['subcategory_subcatid','height','width','advregno','minquantity','addressline1','city_cityid','area_areaid','stock']

class PricingForm(forms.ModelForm):
    noofdays=forms.IntegerField(label='No. of Days')
    class Meta:
        model = Durationwisepricing
        # fields = ['noofdays', 'price']#,'width','maxdays','defaultimgpath']
        exclude=('advertisement_advid',)

class CartForm(forms.ModelForm):
    class Meta:
        model=Cartdetail
        exclude=('startdate','enddate','quantity','id')

class BranchForm(forms.ModelForm):
    class Meta:
        model=Branch
        exclude=('id','company_companyid',)

# class UserForm(forms.ModelForm):
#     first_name=forms.CharField(widget=forms.TextInput())
#     last_name=forms.CharField(widget=forms.TextInput())
#     addressline1=forms.Textarea()
#     email=forms.CharField(widget=forms.TextInput())
#     mobileno=forms.IntegerField(widget=forms.NumberInput())
#
#     class Meta:
#         model=User
#         fields =['first_name','last_name','addressline1','email','mobileno']

class SellerDocForm(forms.ModelForm):
    docname=forms.CharField(label='Add New')
    class Meta:
        model=Sellerdoclist
        exclude=('docid',)
class UserroleForm(forms.ModelForm):
    rolename=forms.CharField(label='Add New')
    class Meta:
        model=Userrole
        exclude=('roleid',)
class CompanyForm(forms.ModelForm):
    # companyname=forms.CharField(label='Add New')
    class Meta:
        model=Company
        exclude=('companyid',)