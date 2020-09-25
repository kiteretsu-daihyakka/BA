$(function(){
    $('#id_areaid').hide();
    $('#id_email').attr('type','email');
    $('#id_first_name').attr('pattern','[a-zA-Z]*');
    $('#id_first_name').attr('title','Name should have only alphabets(a-z).');
    $('#id_last_name').attr('pattern','[a-zA-Z]*');
    $('#id_last_name').attr('title','Name should have only alphabets(a-z).');
    $('#id_mobileno').attr('type','text');
    $('#id_mobileno').attr('pattern','[6789][0-9]{9}');
    $('#id_mobileno').attr('title','Please enter 10 digit mobile number. Also it should start with 6/7/8/9.');
    // $('#id_mobileno').attr('min','10');
    // $('#id_email').attr('pattern','[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}');
    // $('#id_email').attr('title','Mail Id should have pattern.');
    // $('#id_first_name').attr('oninvalid',"this.setCustomValidity('Please enter a valid name!')");
    // $('#id_first_name').attr('oninput',"this.setCustomValidity('')");
    $('#cnclBtn,#updtBtn').hide();
    $('.inputFields').hide();
    $('.detailTable select').hide();

    // $('.detailTable input').prop('readonly',true);
    // $('.detailTable textarea').prop('readonly',true);
    // $('.viewBtn').click(function(){
        // alert();
    // });
    // $('#updtBtn').click(function(e){
    //     // var flag={};
    //     $.ajax({
    //         url:chckPwdUrl,
    //         data:{
    //             'pwd':prompt("Enter your password:"),
    //         },
    //         dataType:'json',
    //         // _async: false,
    //         success: function(data){
    //             console.log(data['result']);
    //             if(data['result']==1){
    //                 $('#detailTableForm').submit();
    //             }
    //             else{
    //                 alert('Incorrect Password.');
    //             }
    //             // $('#pwdFlag').val(data['result']);  
    //             // func(data['result']);
    //             // func();
    //         }
    //     });

        // console.log(flag);
        // return false;
        // function func(){
        // if($('#pwdFlag').val()==1){
            // console.log('yeah');
            
            // e.preventDefault();
            // e.stopPropagatoin();
        // }
        // }
        // alert(flag);
        // if(flag==false){
        //     return false;
        // }
        // $('#id_first_name').attr('oninvalid',"this.setCustomValidity('Please enter a valid name!')");
        // e.preventDefault();
        // alert();
        // if($('#id_first_name').val()=='Sahil'){
            // e=$('#id_first_name');
            // $('#id_first_name').focus(function(e){
                // e.target.setCustomValidity('what..');
            // });
        // }
    // });
    $('#sellerDocsForm').submit(function(e){
        if(!confirm('You can not change documents once uploaded, Are you sure to proceed?')){
            return false;
        }
        // e.preventDefault();
        // if(this.files && this.files[0]){
        //     var reader=new FileReader();
        //     // alert('coming in if');
        //     reader.onload=function(e){
        //         // alert('onload');
        //         $('.imagesOfAdv').append("<img class='adv_image' src='"+e.target.result+"' alt='adv img' height='80px' width='110px' ><i class='fas fa-times' style='cursor:pointer;margin-left:-17px;opacity:80%;font-size:20px;background-color:white;' onclick='removeImg(this)'></i> ");
        //         $('#tmpInputForImgRequired').prop('required',false);
        //         var imgs=$('#tmpInputForImgRequired').val();
        //         if(imgs==''){
        //             imgs=0;
        //         }
        //         $('#tmpInputForImgRequired').val(++imgs);
        //         // alert($('#tmpInputForImgRequired').val());
        //         // alert($('#tmpInputForImgRequired').prop('required'));
        //     }
        //     <!--alert('readDAttaUrl');
        //     reader.readAsDataURL(this.files[0]);
        //     $('#imgInputContainer').append("<input class='imgInput' type='file' accept='images/*' name='advImg"+$('.imgInput').length+1+"' hidden>");
        // }
    });
    $('#editBtn').click(function(){
        $('#cnclBtn,#updtBtn').show();
        $(this).hide();
        // $('.detailTable input').css('border:1px solid black');
        // $('textarea').css('border:1px solid black');
        // $('.detailTable textarea').attr('readonly',false);
        $('.inputFields').show();
        $(".detailTable select:not('#id_areaid')").show();
            
        // $.ajax({
        //     url:stObjUrl,
        //     dataType:'json',
        //     success: function(data){
        //         console.log(data);
        //         $('#states').empty();
        //         $('#states').append("<option value=''>Select</option>");
        //         for(var i=0;i<data['stObjs'].length;i++){
        //             $('#states').append("<option value="+data['stObjs'][i]['id'].toString()+">"+data['stObjs'][i]['statename']+"</option>");
        //         }
        //     }
        // });
    });

    $('#cnclBtn').click(function(){
        $('.inputFields').hide();
        $('#cnclBtn,#updtBtn').hide();
        $('#editBtn').show();
        // $('.detailTable input').css('border:none');
        // $('.detailTable textarea').css('border:none');
        // $('.detailTable textarea').attr('readonly',true);
        // $(".detailTable select:not(#states)").html("<option value=''>-----</option>");
        $(".detailTable select").hide();
    });

    $('#states').change(function(){
        $('#cities').empty();
        $('#cities').append("<option value=''>Select</option>");

        var stateId=$(this).val();
        if (stateId==''){
            return;
        }
        $.ajax({
            url:ctObjUrl,
            data:{
                'id':stateId,
            },
            dataType:'json',
            success: function (data){
                console.log(data);
                $('#cities').empty();
                $('#cities').append("<option value=''>Select</option>");
                for(var i=0;i<data['ctObjs'].length;i++){
                    $('#cities').append("<option value='"+data['ctObjs'][i]['id']+"' >"+data['ctObjs'][i]['cityname']+"</option>");
                }
            }
        });
    });
    $('#cities').change(function(){
        $('#areas').empty();
        $('#areas').append("<option value=''>Select</option>");

        var ctId=$(this).val();
        if (ctId==''){
            return;
        }
        $.ajax({
            url:arObjUrl,
            data:{
                'id':ctId,
            },
            dataType:'json',
            success: function (data){
                console.log(data);
                $('#areas').empty();
                $('#areas').append("<option value='' >Select</option>");
                for(var i=0;i<data['arObjs'].length;i++){
                    $('#areas').append("<option value='"+data['arObjs'][i]['id']+"' >"+data['arObjs'][i]['areaname']+"</option>");
                }
            }
        });
    });
    $('#areas').change(function(){
        $('#id_areaid').html("<option value='"+$(this).val()+"' selected></option>");
    });

    // alert(id);
    // alert(color);
    $('#imgUpld').change(function (e) { 
        // alert('seleccted');
        $('#imageForm').submit();
        var slctr=this;
//        console.log('coming in submit func');
//        e.preventDefault();
        if(this.files && this.files[0]){
            var reader=new FileReader();
            // alert('coming in if');
            reader.onload=function(e){
                // alert(e.target.result);
                $('.avatar').html('');
                $('.avatar').css("background-image","url("+e.target.result+")");

                $('.hasPhoto').show();

                $('.viewLink').attr('href','/media/'+slctr.files.item(0).name);
                $('.hasntPhoto').hide();
                $('.dropdownMenu').hide();
            }
            // alert('readDAttaUrl');
            reader.readAsDataURL(this.files[0]);
            // alert(this.files[0]);
         }
        // $('.imagesOfAdv').append("<img src='"+$(this).val()+"' alt='adv img' height='100px' width='130px'>");
    });
    $('#imageForm').submit(function(e){
        e.preventDefault();
        var fd=new FormData(this);
            // fd.append('profile_pic',this.files[0]);
            $.ajax({
                url: imgUpldUrl,
                type:'post',
                data: fd,
                contentType: false,
                processData: false,
                success: function (response) {
                    // if(response==1){
                    //alert(response.rslt);
                    console.log('image upload status '+response.rslt);
                    // }
                    // else{
                        // alert(0);
                    // }
                }
            });
    });
    $('.removeLink').click(function(){
        alert();
        //var fd=new FormData(this);
        // fd.append('profile_pic',this.files[0]);
        $.ajax({
            url: imgDelUrl,
            success: function (response) {
                // if(response==1){
                //alert(response.rslt);
                console.log('image remove status '+response.rslt);
                $('.avatar').css("background-image","url('')");
                $('.hasntPhoto').show();
                $('.hasPhoto').hide();
                $('.dropdownMenu').hide();
                // }
                // else{
                    // alert(0);
                // }
            }
        });
    });

    $('.avatar').click(function () {
        $('.dropdownMenu').toggle();
    });
//    alert();
//    $('#initialLetter').parent().css('background-color',color);
//    $('#initialLetter').html(initial);
//    $('tbody input').css('border','none');
//    $('tbody input').css('outline','none');
//    $('tbody input').prop('readonly',true);
//    $('.postBtns').hide();

    $('#editBtn').click(function(){
        $('tbody input').css('border','1px solid');
        $('tbody input').css('outline','default');
        $('tbody input').prop('readonly',false);
        $('.postBtns').show();
        $(this).hide();
    });

    $('#cnclBtn').click(function(){
        $('tbody input').css('border','none');
        $('tbody input').css('outline','none');
        $('tbody input').prop('readonly',true);
        $('.postBtns').hide();
        $('#editBtn').show();
    });
    //alert();
});