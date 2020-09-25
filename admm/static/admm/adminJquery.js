$(document).ready(function () {



    //for advList.html where advertisements are listed
    // var advArr=[];
    
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
    $('.owned,.verified').click(function(){
                $(this).css('background-color','lightgray');
                $('.others,.unverified').css('background-color','white');
                $('#id_isowned').val(1);
                $('#submitClick').click();
            });
            $('.others,.unverified').click(function(){
                $('#id_isowned').val(0);
                $(this).css('background-color','lightgray');
                $('.owned,.verified').css('background-color','white');
                $('#submitClick').click();
            });
            

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