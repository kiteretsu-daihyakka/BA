$(document).ready(function(){
    $('#id_startdate').parent().css('float','left');
    $('#id_startdate').parent().css('width','150px');
    $('#id_enddate').parent().css('width','150px');
    $('#id_enddate,#id_startdate').attr('type','date');
    $('#packUpdtform').submit(function () {
        alert($("input[type='checkbox']:checked").length);
        if($("input[type='checkbox']:checked").length<0){
            alert('Please select at least one advertisement.');
            return false;
        }
        $.each($("input[type='checkbox']:checked"), function () { 
            $('#id_adv_list').val($('#id_adv_list').val()+$(this).val()+',');  
        });
    });
    $('#addAdvLnk').click(function(){
        $('.adv_id_input').each(function(){
            $('#alreadyAdvsIds').val($('#alreadyAdvsIds').val()+$(this).val()+' ');
        });
        $('#alreadyAdvsIds').val().trim();
        $.ajax({
            url:fetch_advs,
            data:{
                'alreadyAdvs':$('#alreadyAdvsIds').val(),
            },
            dataType:'json',
            success: function (data){
                $('#advListHeading').show();
                $('#advListTbl').empty();
                $('#advListTbl').append("<tr style=''><th></th><th>Image</th><th>Height</th><th>Width</th><th>Registration No.</th><th style='width:120px;'>Address</th><th>Subcategory</th><th>Area</th><th>City</th><th>Minimum Quantity</th><th>Owner</th><th>Stock</th><th>Package quantity</th></tr>");
                //<!-- $('#advListTbl').append("<tr><th>Select</th><th>Image</th><th>HEIGHT</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr>");--> -->
                for(var i=0;i<data['advs'].length;i++){
                    if ((i+1)%2==0){
                        var styleStr='lightgray';
                    }
                    else{
                        var styleStr='default';
                    }
                    console.log(data['advs']);
                    // alert(data['advs'][i]['catid']);
                    if(data['advs'][i]['catid'] == 2){
                        $('#advListTbl').append("<tr style='background-color:"+styleStr+
                        ";' style='height:50px;'><td><input type='checkbox' value='"+
                        data['advs'][i]['advid']+"'></td><td><img src='/media/"+data['advs']['defaultimgpath']+"' height='70px' width='80px'/></td><td>"+
                        data['advs'][i]['height']+"</td><td>"+
                        data['advs'][i]['width']+"</td><td>"+
                        data['advs'][i]['advregno']+"</td><td style='text-align:left;width:160px;'>"+
                        data['advs'][i]['addressline1']+"</td><td style='font-weight:bold'>"+
                        data['advs'][i]['subcategory_subcatid_id']+"</td><td>"+
                        data['advs'][i]['area_areaid']+"</td><td>"+
                        data['advs'][i]['city_cityid_id']+"</td><td>"+
                        data['advs'][i]['minquantity']+"</td><td>"+
                        data['advs'][i]['auth_user_id']+"</td><td>"+
                        data['advs'][i]['stock']+"</td><td><input type=number min=0 max="+
                        data['advs'][i]['stock']+" id=advQntt"+
                        data['advs'][i]['advid']+" name=quant"+
                        data['advs'][i]['advid']+"></td></tr>");
                    }
                    else{
                        $('#advListTbl').append("<tr style='background-color:"+styleStr+
                        ";' style='height:50px;'><td><input type='checkbox' value='"+
                        data['advs'][i]['advid']+"'></td><td><img src='/media/"+data['advs'][i]['defaultimgpath']+"' height='70px' width='80px'/></td><td>"+
                        data['advs'][i]['height']+"</td><td>"+
                        data['advs'][i]['width']+"</td><td>"+
                        data['advs'][i]['advregno']+"</td><td style='text-align:left;width:160px;'>"+
                        data['advs'][i]['addressline1']+"</td><td style='font-weight:bold'>"+
                        data['advs'][i]['subcategory_subcatid_id']+"</td><td>"+
                        data['advs'][i]['area_areaid']+"</td><td>"+
                        data['advs'][i]['city_cityid_id']+"</td><td>"+
                        data['advs'][i]['minquantity']+"</td><td>"+
                        data['advs'][i]['auth_user_id']+"</td><td>"+
                        data['advs'][i]['stock']+"</td><td></td></tr>");   
                    }
                }
            }
        });
    });
    $('#advListTbl').on('click','input:checkbox',function(){
        // alert($('#advQntt'+$(this).val()).prop('required'));
        if($('#advQntt'+$(this).val()).prop('required')){
            $('#advQntt'+$(this).val()).prop('required',false);
        }
        else{
            $('#advQntt'+$(this).val()).prop('required',true);
        }
    });
    $('#advListTbl').on('click','.selectAdvInput',function(){
        var row=$(this).parent().parent();
        var adv_id=$(this).val();
        $(this).prop('disabled','true');
        $('.packDtlTbl').append("<tr>"+$(row).html()+"</tr>");
        $('.packDtlTbl tr:last-child').children().first().html("<a href='/adminsite/adv/"+adv_id+"/dtl' target='_blank'><i class='fas fa-eye'></i></a><br><span class='tmpAdvs' style='color:red'>New!<input value='"+adv_id+"' hidden></span>");
        $('.packDtlTbl tr:last-child').append("<td><input style='width:50px;' name='quant"+adv_id+"' type='number' required></td><td><a class='tmpAdvDel' id='delBtn"+adv_id+"'><i class='fas fa-trash'></i></a></td>");
    });
    $(document).on('click','.tmpAdvDel',function(){
        var id=$(this).attr('id').match(/(\d+)/)[0];
        $(this).parent().parent().remove();
        $('.selectAdvInput').each(function(){
            if($(this).val().toString()==id.toString()){
                $(this).prop('disabled','');
                return false;
            }
        });
    });
        /*<!--$('#checkTmpAdv').click(function(){-->
            <!---->
        <!--});-->*/
        // function validate(){
        //     if($('#id_discount').val()<=0 || $('#id_discount').val()>100){
        //         alert('Discount amount should be between 0 to 100');
        //         return false;
        //     }
        //     if($('#id_enddate').val()<$('#id_startdate').val()){
        //         alert('Startdate should be smaller than Enddate');
        //         return false;
        //     }
        //     $('.tmpAdvs').each(function(){
        //         $('#slctdAdvIds').val($('#slctdAdvIds').val()+$(this).children('input').val()+',');
        //     });
        //     $('#slctdAdvIds').val($('#slctdAdvIds').val().trim());
        //     var slctd=$('#slctdAdvIds').val();
        //     //alert(slctd);
        //     $('#dltdAdvIds').val($('#dltdAdvIds').val().trim());
        //     if (slctd=='' && $('#deletedAdvsCnt').val()==$('#alreadyAdvs').val()){
        //         alert('comnig');
        //         if(!confirm('If you proceed than this package will be deleted as there are 0 advertisements')){
        //             return false;
        //         }
        //     }
        //     $('.quantityAlrdy').each(function(){
        //         if($(this).val()!=$(this).next('.duplicate').val()){
        //             var adv_id=$(this).parent().siblings('.advIdTd').children('input').val();
        //             alert(adv_id);
        //             $('#id_changedAdvQnts').val($('#id_changedAdvQnts').val()+adv_id+' ');
        //         }
        //     });
        //     $('#id_changedAdvQnts').val($('#id_changedAdvQnts').val().trim());
        // }
        
        /*function tmpAdvDel(ele){-->
            <!--var id=$(ele).attr('id').match(/(\d+)/)[0];-->
            <!--$(ele).parent().parent().remove();-->
            <!--$('.selectAdvInput').each(function(){-->
                <!--if($(this).val().toString()==id.toString()){-->
                    <!--$(this).prop('disabled','');-->
                    <!--return false;-->
                <!--}-->
            <!--});-->
        <!--}-->*/
});
function saveIdDelInput(ele){
    $('#dltdAdvIds').val($('#dltdAdvIds').val()+$(ele).attr('id').match(/(\d+)/)[0]+' ');
    $(ele).parent().parent().remove();
    $('#deletedAdvsCnt').val(parseInt($('#deletedAdvsCnt').val())+1);
}