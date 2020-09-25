$(document).ready(function(){
    $('.menuTbl').hide();
    $('.menuBtn').click(function(){
        $('.menuTbl').slideToggle();
    });
});

function newFunction() {
    return '.menuTbl td';
}
