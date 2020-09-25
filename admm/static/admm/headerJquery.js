$(document).ready(function () {
    $('#myAc').click(function(){
        $('#myAcPanel').fadeToggle('fast');
        $('article').click(function(){
            $('#myAcPanel').hide();
        });
    });
});