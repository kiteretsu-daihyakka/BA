<script>

    $(document).ready(function(){
        $('.upd').click(function(){
            var idNum=$(this).attr('id').match(/(\d+)/))[0];
            $('#actNameInput').val($('#activityName'+idNum).html());
            $('#actIdInput').val(idNum);
            $('#updForm').slideToggle();
        });
    });

</script>


<form action='' id='updForm'>
    <input id='actIdInput' name='whatever'>
    <input id='actNameInput' name='whatever'>
    <input type='submit'>
</form>