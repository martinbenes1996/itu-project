$(document).ready(function () {
    $('a[href^="#"]').on('click', function(event){
        event.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').animate({
            scrollTop: $target.offset().top
        }, 1000, 'swing');
    });
});

/* Keep the dropdown open !! DELETE DATA-TOQQLE="DROPDOWN"
$('li.dropdown.keep-inside-clicks-open a').on('click', function (event) {
    $(this).parent().toggleClass('open');
});

$('body').on('click', function (e) {
    if (!$('li.dropdown.keep-inside-clicks-open').is(e.target)
        && $('li.dropdown.keep-inside-clicks-open').has(e.target).length === 0
        && $('.open').has(e.target).length === 0
    ) {
        $('li.dropdown.keep-inside-clicks-open').removeClass('open');
    }
});*/