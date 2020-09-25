$(document).ready(function(){
    $('.role_Name').dblclick(function(){
                $(this).prop('readonly',false);
            });;
            $('.role_Name').change(function(){
                var tmp=$(this).next('a').attr('href');
                $(this).next('a').attr('href',tmp+$(this).val());
                $(this).next('a')[0].click();
            });
});