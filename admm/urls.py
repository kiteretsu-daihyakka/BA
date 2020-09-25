from django.urls import path,re_path
from django.http import HttpRequest
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='admm'

urlpatterns = [
    # path('tmp/<int:pk>/',views.tmp,name='tmp'),
    path('subInit/<int:pk>/',views.subCatInit,name='subCatInit'),

    path('report/orders/',views.reportOrders,name='rprt_ordrs'),
    # path('report/orders/pdf/',views.reportBasicViewLatestCopy,name='rprt_copy'),
    path('report/users/<int:pk>/',views.reportUsers,name='rprt_usrs'),

    path('advregnocheck/',views.checkAdvRegNo,name='checkAdvRegNo'),

    path('commissions/',views.commission,name='cmisnLst'),

    path('cart/',views.cart,name='cart'),
    path('cart/rem/<int:pk>/',views.cartAdvRemove,name='cartAdvRemove'),
    path('cart/save/<int:cnt>/',views.saveCart,name='cart_save'),
    path('ordr/place/',views.saveOrdr,name='ordr_save'),
    path('ordrsummry/',views.ordrSummery,name='ordrSummery'),
    path('cpnvalidate/',views.validateCoupon,name='cpn_validate'),

    path('location/',views.location,name='locationcreatorview'),
    path('location/upd/',views.locationUpdt,name='location_upd'),
    path('location/del/',views.locationDel,name='location_del'),
    path('location/stobjects/',views.stateObjs,name='location_stObjs'),
    path('location/citiobjects/',views.cityObjs,name='location_citiObjs'),
    path('location/areaobjects/',views.areaObjs,name='location_areaObjs'),

    # path('location/<int:cn>/',views.LocationViewCreateForm.as_view(),name='locationcreatorview'),
    # path('location/<int:cn>/<int:st>/',views.LocationViewCreateForm.as_view(),name='locationcreatorview'),
    # path('location/<int:cn>/<int:st>/<int:ct>/',views.LocationViewCreateForm.as_view(),name='locationcreatorview'),

    path('subcats/',views.subCatInit,name='subCatsDD'),
    path('advs/',views.listAdv,name='listadv'),
    path('adv/add/',views.AdvCreateLatest.as_view(),name='advcreatenew'),
    path('adv/add/check/',views.tmpForCheck,name='advcreatenewTmp'),
    path('adv/<int:pk>/del/', views.delAdv, name='adv_del'),
    path('adv/<int:pk>/dtl', views.adv_detail, name='adv_detail'),
    path('adv/<int:pk>/edit/', views.adv_edit, name='adv_edit'),
    path('adv/<int:pk>/save/', views.adv_save, name='adv_save'),

    path('listorders/',views.listOrders,name='list_orders'),
    path('listorders/served/',views.markOdrDtlServed,name='markOdrDtlServed'),
    path('orderdetail/<int:pk>/',views.ordr_detail,name='ordr_detail'),
    path('listcncldordrs/',views.listCncldOrdrs,name='list_cncld_odrs'),
    path('listcncldordrs/saveRfnd/',views.saveRefnd,name='save_rfnd'),

    # path('cnclordrdetail/<int:pk>/',views.cnclordr_detail,name='cnclordr_detail'),

    # path('pack/create/', views.packOrOffer_create, name='pack_create'),
    path('<str:packOrOffr>/listing/', views.packOfferList, name='packOrOffr_list'),
    path('packoffr/<str:packOrOffr>/<int:pk>', views.packOfferDetail, name='packoffr_detail'),
    path('packoffr/<str:packOrOffr>/<int:pk>/del/', views.packOffrDel, name='packoffr_del'),
    path('packoffr/<str:packOrOffr>/<int:pk>/edit/', views.packOffrEdit, name='packoffr_edit'),
    # path('packoffr/<str:packOrOffr>/<int:pk>/save/', views.packOffrSave, name='packoffr_save'),
    path('<str:packOrOffr>/create/',views.packOrOffer_create,name='addNewPackOffr'),
    path('buyers/<str:objname>/',views.fdbckOrCmplntList,name='fdbckCmplntList'),
    path('fdbkresponse/save/<int:isFdbk>/',views.fdbkRcmplnt_save,name='fdbk_save'),
    # path('offers/', views.offrList, name='offr_list'),

    path('advs/packoffr/', views.fetch_advs, name='fetch_advs'),

    # re_path(r'^advertisement/(?P<pk>[0-9]+)/$',views.advUpdate.as_view(),name='adv_edit'),

    path('coupon/<int:pk>/',views.coupon_detail,name='coupon_detail'),
    path('coupons/',views.CouponLstOrAdd.as_view(),name='couponsListOrAdd'),
    path('coupons/<int:pk>/edit/', views.CoupondetailUpdate.as_view(), name='cpn_edit'),
    path('coupons/del/', views.delCoupon, name='cpn_del'),

    path('addcart/',views.CartAddLatest.as_view(),name='cartcreatenew'),

    path('seller-documents/',views.sellerDocs,name='selr_docs'),
    # path('sellerdoclist/',views.SellerDocCreate.as_view(),name='sellerdoclist'),
    path('seller-documents/del/',views.sellerDocDel,name='selr_doc_del'),
    # re_path(r'^sellerdoclist/edit/(?P<sdlpk>[0-9]+)/$',views.sellerDocEdit,name='sellerdocedit'),
    path('seller-documents/edit/',views.sellerDocEdit,name='selr_doc_edit'),

    path('userroles/',views.UserRoleCreate.as_view(),name='userrolecreateorview'),
    path('userroles/del/<int:rlpk>/',views.UserRoleDel,name='userroledel'),
    path('userroles/edit/<int:rlpk>/<str:role>',views.UserRoleEdit,name='userroleedit'),
    path('userrole/save/',views.userRoleInUserList,name='save_role'),#for user list page

    path('category/save/',views.categorySave,name='saveCat'),
    path('categories/',views.CategoryCreateForm.as_view(),name='categorycreateorview'),
    path('categories/<int:pk>/',views.CategoryCreateForm.as_view(),name='categorycreateorviewforsubcat'),
    path('categories/del/',views.categoryDel,name='categoryDel'),
    path('categories/edit/',views.categoryEdit,name='categoryEdit'),

    path('subcat/save/',views.subCatSave,name='subCatSave'),
    path('subcategories/<int:pk>/',views.SubcategoryCreateForm.as_view(),name='subcategorycreateorview'),
    path('subcat/del/',views.subcategoryDel,name='subcatdel'),
    path('subcategories/edit/',views.subcategoryEdit,name='subcategoryedit'),

    path('company/',views.CmpnyCreate.as_view(),name='cmpnycreateorview'),
    path('company/del/<int:cmpnypk>/',views.CmpnyDel,name='cmpnydel'),
    path('company/edit/<int:cmpnypk>/<str:cmpnyname>',views.CmpnyEdit,name='cmpnyedit'),


    path('users/',views.userList,name='usersList'),
    # path('addadv/',views.advCreateLatest.as_view(),name='advcreatenew'),
    path('users/<int:pk>/delete/', views.UserDel.as_view(), name='usr_del'),
    path('users/<int:pk>/edit/', views.adv_edit, name='adv_edit'),
    # path('adv/<int:pk>/save/', views.adv_save, name='adv_save'),
    path('users/<int:pk>/',views.userDetail,name='usr_detail'),
    path('users/lockunlock/<int:pk>/<int:frmBranchPage>/',views.lockUnlockUser,name='lockUnlockUser'),
    path('users/userrole/create/',views.addRole,name='addRole'),
    path('users/makeadmin/',views.makeAdmin,name='makeAdmin'),


    path('upload/',views.upldImg,name='advImgUpld'),
    path('',views.index,name='index'),
    path('profile/',views.adminSellerProfile,name='profile'),
    path('profile/chckPwd/',views.checkPassword,name='checkPassword'),
    path('profile/doc-upload/',views.sellerDocsUpld,name='seller_docs'),
    # path('profile2/<int:pk>/',views.UserDetailAndUpdate.as_view(),name='profile2'),
    path('chngpwd/',views.chngPwd,name='chngpwd'),
    # path('newpwd/',views.newPwd,name='newpwd'),
    path('list/<str:objname>/',views.List.as_view(),name='list'),

    #....................................old school..............................
    # path('tables/',views.tables,name='tables'),
    #path('<str:advname>/<int:pk>/delete',views.randomadvDelView.as_view(),name='randomadv-del'),
    #path('<str:advname>/<int:pk>/upd',views.randomadvUpdView.as_view(),name='randomadv-upd'),
    #path('<str:advname>/add/',views.randomadvAddView.as_view(),name='randomadv-add'),
    path('detail/<str:advname>/<int:pk>/',views.randomObjDetailView.as_view(),name='randomadvDetail'),
    #path(r'^(?P<advname>[a-z][A-Z])/(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    #     path('adv/detail/<int:pk>/',views.advDetailView.as_view(),name='adv-detail'),
    #     path('advertisement/add/',views.advCreate.as_view(),name='adv-add'),
    # re_path(r'^advertisement/(?P<pk>[0-9]+)/$',views.advUpdate.as_view(),name='adv-upd'),
    # path('advertisement/<int:pk>/delete/',views.advDelete.as_view(),name='adv-del'),
    # path('advimgs/detail/<int:pk>/',views.advImgsDetailView.as_view(),name='advimgs-detail'),
    # path('advimgs/add',views.advImgsCreate.as_view(),name='advimgs-add'),
    # re_path(r'^advimgs/(?P<pk>[0-9]+)/$',views.advImgsUpdate.as_view(),name='advimgs-upd'),
    # re_path(r'^advimgs/(?P<pk>[0-9]+)/delete/$',views.advImgsDelete.as_view(),name='advimgs-del'),
    #     path('<str:advname>/detail/<int:pk>/',views.AreaDetailView.as_view(),name='Area-detail'),
    path('Area/add/',views.AreaCreate.as_view(),name='area-add'),
    path('Area/<int:pk>/',views.AreaUpdate.as_view(),name='area-upd'),
    path('Area/<int:pk>/delete/',views.AreaDelete.as_view(),name='area-del'),
    # path('branch/detail/<int:pk>/',views.BranchDetailView.as_view(),name='advimgs-detail'),
    path('branch/',views.BranchCreateViewForm.as_view(),name='branch_viewadd'),
    re_path(r'^branch/edit/(?P<pk>[0-9]+)/$',views.branchEdit,name='branch-upd'),
    re_path(r'^branch/(?P<pk>[0-9]+)/delete/$',views.BranchDeleteForm,name='branch-del'),
    path('branch/admins/<int:pk>',views.branchAdmins,name='branch_admin'),
    # re_path(r'^branch/(?P<pk>[0-9]+)/delete/$',views.BranchDelete.as_view(),name='branch-del'),
    #     path('order/detail/<int:pk>/',views.OrderDetailView.as_view(),name='advimgs-detail'),
    path('Order/add',views.OrderCreate.as_view(),name='order-add'),
    re_path(r'^Order/(?P<pk>[0-9]+)/$',views.OrderUpdate.as_view(),name='order-upd'),
    re_path(r'^Order/(?P<pk>[0-9]+)/delete/$',views.OrderDelete.as_view(),name='order-del'),
    #     path('orderdetails/detail/<int:pk>/',views.OrderdetailDetailView.as_view(),name='advimgs-detail'),
    path('Orderdetails/add',views.OrderdetailsCreate.as_view(),name='orderdetails-add'),
    re_path(r'^Orderdetails/(?P<pk>[0-9]+)/$',views.OrderdetailsUpdate.as_view(),name='orderdetails-upd'),
    re_path(r'^Orderdetails/(?P<pk>[0-9]+)/delete/$',views.OrderdetailsDelete.as_view(),name='orderdetails-del'),
    #     path('cancellationofordadv/detail/<int:pk>/',views.CancellationsDetailView.as_view(),name='advimgs-detail'),
    # path('Cancellationofordadv/add',views.CancellationofordadvCreate.as_view(),name='cancellationofordadv-add'),
    # re_path(r'^Cancellationofordadv/(?P<pk>[0-9]+)/$',views.CancellationofordadvUpdate.as_view(),name='cancellationofordadv-upd'),
    # re_path(r'^Cancellationofordadv/(?P<pk>[0-9]+)/delete/$',views.CancellationofordadvDelete.as_view(),name='cancellationofordadv-del'),
    #     path('cartdetail/detail/<int:pk>/',views.CartDetailView.as_view(),name='advimgs-detail'),
    path('Cartdetail/add/',views.CartdetailCreate.as_view(),name='cartdetail-add'),
    re_path(r'^Cartdetail/(?P<pk>[0-9]+)/$',views.CartdetailUpdate.as_view(),name='cartdetail-upd'),
    re_path(r'^Cartdetail/(?P<pk>[0-9]+)/delete/$',views.CartdetailDelete.as_view(),name='cartdetail-del'),
    #     path('category/detail/<int:pk>',views.CategoryDetailView.as_view(),name='category-detail'),
    path('Category/add/',views.CategoryCreate.as_view(),name='category-add'),
    re_path(r'^Category/(?P<pk>[0-9]+)/$',views.CategoryUpdate.as_view(),name='category-upd'),
    re_path(r'^Category/(?P<pk>[0-9]+)/delete/$',views.CategoryDelete.as_view(),name='category-del'),
    #     path('city/detail/<int:pk>/',views.CityDetailView.as_view(),name='advimgs-detail'),
    path('City/add',views.CityCreate.as_view(),name='city-add'),
    re_path(r'^City/(?P<pk>[0-9]+)/$',views.CityUpdate.as_view(),name='city-upd'),
    re_path(r'^City/(?P<pk>[0-9]+)/delete/$',views.CityDelete.as_view(),name='city-del'),
    #     path('commissiondetail/detail/<int:pk>/',views.CommissionDetailView.as_view(),name='advimgs-detail'),
    path('Commissiondetail/add',views.CommissiondetailCreate.as_view(),name='commissiondetail-add'),
    re_path(r'^Commissiondetail/(?P<pk>[0-9]+)/$',views.CommissiondetailUpdate.as_view(),name='commissiondetail-upd'),
    re_path(r'^Commissiondetail/(?P<pk>[0-9]+)/delete/$',views.CommissiondetailDelete.as_view(),name='commissiondetail-del'),
    #     path('company/detail/<int:pk>/',views.CompanyDetailView.as_view(),name='advimgs-detail'),
    path('Company/add',views.CompanyCreate.as_view(),name='company-add'),
    re_path(r'^Company/(?P<pk>[0-9]+)/$',views.CompanyUpdate.as_view(),name='company-upd'),
    re_path(r'^Company/(?P<pk>[0-9]+)/delete/$',views.CompanyDelete.as_view(),name='company-del'),
    #     path('complaintdetail/detail/<int:pk>/',views.ComplaintDetailView.as_view(),name='advimgs-detail'),
    #path('complaintdetail/add', views.ComplaintdetailCreate.as_view(), name='complaintdetail-add'),
    re_path(r'^Complaintdetail/(?P<pk>[0-9]+)/$', views.ComplaintdetailUpdate.as_view(), name='complaintdetail-upd'),
    re_path(r'^Complaintdetail/(?P<pk>[0-9]+)/delete/$', views.ComplaintdetailDelete.as_view(), name='complaintdetail-del'),
    #     path('country/detail/<int:pk>/',views.CountryDetailView.as_view(),name='advimgs-detail'),
    path('Country/add', views.CountryCreate.as_view(), name='country-add'),
    re_path(r'^Country/(?P<pk>[0-9]+)/$', views.CountryUpdate.as_view(), name='country-upd'),
    re_path(r'^Country/(?P<pk>[0-9]+)/delete/$', views.CountryDelete.as_view(), name='country-del'),
    #     path('coupondetail/detail/<int:pk>/',views.CouponDetailView.as_view(),name='advimgs-detail'),
    path('Coupondetail/add', views.CoupondetailCreate.as_view(), name='coupondetail-add'),
    re_path(r'^Coupondetail/(?P<pk>[0-9]+)/$', views.CoupondetailUpdate.as_view(), name='coupondetail-upd'),
    # re_path(r'^Coupondetail/(?P<pk>[0-9]+)/delete/$', views.CoupondetailDelete.as_view(), name='coupondetail-del'),
    #     path('durationwisepricing/detail/<int:pk>/',views.PricingDetailView.as_view(),name='advimgs-detail'),
    path('Durationwisepricing/add', views.DurationwisepricingCreate.as_view(), name='durationwisepricing-add'),
    re_path(r'^Durationwisepricing/(?P<pk>[0-9]+)/$', views.DurationwisepricingUpdate.as_view(), name='durationwisepricing-upd'),
    re_path(r'^Durationwisepricing/(?P<pk>[0-9]+)/delete/$', views.DurationwisepricingDelete.as_view(), name='durationwisepricing-del'),
    #     path('offercoveringadvs/detail/<int:pk>/',views.OfferadvDetailView.as_view(),name='advimgs-detail'),
    path('Offercoveringadvs/add', views.OffercoveringadvsCreate.as_view(), name='offercoveringadvs-add'),
    re_path(r'^Offercoveringadvs/(?P<pk>[0-9]+)/$', views.OffercoveringadvsUpdate.as_view(), name='offercoveringadvs-upd'),
    re_path(r'^Offercoveringadvs/(?P<pk>[0-9]+)/delete/$', views.OffercoveringadvsDelete.as_view(), name='offercoveringadvs-del'),
    # path('offerdetail/detail/<int:pk>/',views.OfferDetailView.as_view(),name='advimgs-detail'),
    path('Offerdetail/add', views.OfferdetailCreate.as_view(), name='offerdetail-add'),
    re_path(r'^Offerdetail/(?P<pk>[0-9]+)/$', views.OfferdetailUpdate.as_view(), name='offerdetail-upd'),
    re_path(r'^Offerdetail/(?P<pk>[0-9]+)/delete/$', views.OfferdetailDelete.as_view(), name='offerdetail-del'),
    # path('orderfeedback/detail/<int:pk>/',views.OrdfdbackDetailView.as_view(),name='advimgs-detail'),
    path('Orderfeedback/add', views.OrderfeedbackCreate.as_view(), name='orderfeedback-add'),
    re_path(r'^Orderfeedback/(?P<pk>[0-9]+)/$', views.OrderfeedbackUpdate.as_view(), name='orderfeedback-upd'),
    re_path(r'^Orderfeedback/(?P<pk>[0-9]+)/delete/$', views.OrderfeedbackDelete.as_view(), name='orderfeedback-del'),
    # path('orderpayment/detail/<int:pk>/',views.OrdpaymntDetailView.as_view(),name='advimgs-detail'),
    path('Orderpayment/add', views.OrderpaymentCreate.as_view(), name='orderpayment-add'),
    re_path(r'^Orderpayment/(?P<pk>[0-9]+)/$', views.OrderpaymentUpdate.as_view(), name='orderpayment-upd'),
    re_path(r'^Orderpayment/(?P<pk>[0-9]+)/delete/$', views.OrderpaymentDelete.as_view(), name='orderpayment-del'),
    # path('package/detail/<int:pk>/',views.PackageDetailView.as_view(),name='advimgs-detail'),
    path('Package/add', views.PackageCreate.as_view(), name='package-add'),

    #-----------------in-use---------------------------------#
    re_path(r'^Package/(?P<pk>[0-9]+)/$', views.PackageUpdate.as_view(), name='package-upd'),
    #------------------end------------------------------------#

    re_path(r'^Package/(?P<pk>[0-9]+)/delete/$', views.PackageDelete.as_view(), name='package-del'),
    # path('packageHasadv/detail/<int:pk>/',views.PackadvDetailView.as_view(),name='advimgs-detail'),
    path('PackageHasadv/add', views.PackageHasAdvCreate.as_view(), name='packageHasadv-add'),
    re_path(r'^PackageHasadv/(?P<pk>[0-9]+)/$', views.PackageHasAdvUpdate.as_view(), name='packageHasadv-upd'),
    re_path(r'^PackageHasadv/(?P<pk>[0-9]+)/delete/$', views.PackageHasAdvDelete.as_view(), name='packageHasadv-del'),
    # path('Sellerdocdetail/detail/<int:pk>/',views.SellerdocDetailView.as_view(),name='advimgs-detail'),
    path('Sellerdocdetail/add', views.SellerdocdetailCreate.as_view(), name='Sellerdocdetail-add'),
    re_path(r'^Sellerdocdetail/(?P<pk>[0-9]+)/$', views.SellerdocdetailUpdate.as_view(), name='Sellerdocdetail-upd'),
    re_path(r'^Sellerdocdetail/(?P<pk>[0-9]+)/delete/$', views.SellerdocdetailDelete.as_view(), name='Sellerdocdetail-del'),
    # path('Sellerdoclist/detail/<int:pk>/',views.SellerdoclistDetailView.as_view(),name='advimgs-detail'),
    path('Sellerdoclist/add', views.SellerdoclistCreate.as_view(), name='Sellerdoclist-add'),
    re_path(r'^Sellerdoclist/(?P<pk>[0-9]+)/$', views.SellerdoclistUpdate.as_view(), name='Sellerdoclist-upd'),
    re_path(r'^Sellerdoclist/(?P<pk>[0-9]+)/delete/$', views.SellerdoclistDelete.as_view(), name='Sellerdoclist-del'),
    # path('State/detail/<int:pk>/',views.StateDetailView.as_view(),name='advimgs-detail'),
    path('State/add', views.StateCreate.as_view(), name='State-add'),
    re_path(r'^State/(?P<pk>[0-9]+)/$', views.StateUpdate.as_view(), name='State-upd'),
    re_path(r'^State/(?P<pk>[0-9]+)/delete/$', views.StateDelete.as_view(), name='State-del'),
    #     path('Subcategory/detail/<int:pk>/',views.SubcatDetailView.as_view(),name='advimgs-detail'),
    path('Subcategory/add/', views.SubcategoryCreate.as_view(), name='Subcategory-add'),
    re_path(r'^Subcategory/(?P<pk>[0-9]+)/$', views.SubcategoryUpdate.as_view(), name='Subcategory-upd'),
    re_path(r'^Subcategory/(?P<pk>[0-9]+)/delete/$', views.SubcategoryDelete.as_view(), name='Subcategory-del'),
    # path('Updationinorder/detail/<int:pk>/',views.UpdationsDetailView.as_view(),name='advimgs-detail'),
    path('Updationinorder/add', views.UpdationinorderCreate.as_view(), name='Updationinorder-add'),
    re_path(r'^Updationinorder/(?P<pk>[0-9]+)/$', views.UpdationinorderUpdate.as_view(), name='Updationinorder-upd'),
    re_path(r'^Updationinorder/(?P<pk>[0-9]+)/delete/$', views.UpdationinorderDelete.as_view(), name='Updationinorder-del'),
    #     path('user/detail/<int:pk>/',views.UserDetailView.as_view(),name='user-detail'),
    path('User/add/', views.UserdetailCreate.as_view(), name='user-add'),
    re_path(r'^User/(?P<pk>[0-9]+)/$', views.UserdetailUpdate.as_view(), name='user-upd'),
    re_path(r'^User/(?P<pk>[0-9]+)/delete/$', views.UserdetailDelete.as_view(), name='user-del'),
    #     path('Userrole/detail/<int:pk>/',views.UserroleDetailView.as_view(),name='advimgs-detail'),
    path('Userrole/add', views.UserroleCreate.as_view(), name='Userrole-add'),
    re_path(r'^Userrole/(?P<pk>[0-9]+)/$', views.UserroleUpdate.as_view(), name='Userrole-upd'),
    re_path(r'^Userrole/(?P<pk>[0-9]+)/delete/$', views.UserroleDelete.as_view(), name='Userrole-del'),
    #     path('Wishlistdetail/detail/<int:pk>/',views.WishlistDetailView.as_view(),name='advimgs-detail'),
    path('Wishlistdetail/add', views.WishlistdetailCreate.as_view(), name='Wishlistdetail-add'),
    re_path(r'^Wishlistdetail/(?P<pk>[0-9]+)/$', views.WishlistdetailUpdate.as_view(), name='Wishlistdetail-upd'),
    re_path(r'^Wishlistdetail/(?P<pk>[0-9]+)/delete/$', views.WishlistdetailDelete.as_view(), name='Wishlistdetail-del'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




























