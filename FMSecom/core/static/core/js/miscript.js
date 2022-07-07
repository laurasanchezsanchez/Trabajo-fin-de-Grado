$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('#whatsapp').fadeIn();
        } else {
            $('#whatsapp').fadeOut();
        }
    });
});