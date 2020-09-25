$(document).ready(function () {



    //for advList.html where advertisements are listed
    // var advArr=[];
    $('.formFields').show();
    $('input:checkbox').click(function(){
        if($('#advQntt'+$(this).val()).prop('required')==false){
            $('#advQntt'+$(this).val()).prop('required',true);
        }
        else{
            $('#advQntt'+$(this).val()).prop('required',false);
        }
        // alert(());
        // $('#advQntt'+$(this).val()).focus();
        // $('#advQntt'+$(this).val()).attr('title','Please fill this field.');
        // $('#advQntt'+$(this).val()).mouseoverchro();
    });
//     $(document).scroll(function () {
//         var ele=document.getElementById('headRow');
//         var rect=ele.getBoundingClientRect();
// //        alert(rect.x+' '+rect.y);
// //        var fstRowCoords=document.getElementById('advRows1').getBoundingClientRect();


// //        $('#container').html($(document).scrollTop());
//         if ($(document).scrollTop() > 287) {
// //            alert('gt 100');
// //            $("#headRow").css("color","red");
// //              $('#headRow').addClass('fixIt');
//             $("#headRow").css("position","fixed");
// ////            $("#headRow").addClass("");
//             $("#headRow th").css("height","60px");
//             $("#headRow th").css("width","100px");
//             $("#headRow").css("top","0");
//             $("#headRow").css("margin-top","82px");
// //            $("#headRow th").addClass("advertisementsTh");

// //            return;
// //            $("#headRow").css('width','90%');
// //            $("#headRow th").css("background-color","yellow");

//         }
//         else{
//             $("#headRow").css("position","relative");
// //            $("#headRow").css("color","white");

//         }

//     });
    
            // $('#closePackPopUp').click(function(){
            //     $('#packCreate').find('input,textarea').val('');
            //     $('#packCreate').hide();
            // });
            // $('#packBtn').click(function(){
            //     $('#id_isPack').val(1);
            //     $('#packCreate').toggle();
            //     $('input:checkbox').toggle();
            //     $('.advQntt').toggle();
            //     $('#createBtn').html('Create Package')
            //     $('#id_selectedAdvCnt').val($('input:checkbox:checked').length);
            // });
            // $('#offrBtn').click(function(){
            //     $('#id_isPack').val(0);
            //     $('#packCreate').toggle();
            //     $('input:checkbox').toggle();
            //     // $('.advQntt').toggle();
            //     $('#createBtn').html('Create Offer')
            //     $('#id_selectedAdvCnt').val($('input:checkbox:checked').length);
            // });
            // $('#showChckBoxes').click(function(){
            //     $('input:checkbox').toggle();
            //     $('.advQntt').toggle();
            // });

            // $('#submitClick').click(function(){
            //     $.ajax({
            //         type:'POST',
            //         url:'/adminsite/listadv/',
            //         data:{
            //          isowned:$('#id_isowned').val(),
            //         },
            //         success:function(){
            //             alert('done');
            //         }
            //     });
            // });



  });