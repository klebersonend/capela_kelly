$(document).ready(function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $(".alert").fadeOut("slow", function() {
            $(this).remove();
        });
    }, 5000);

    // Smooth scroll for anchor links
    $("a[href^='#']").on("click", function(e) {
        var target = $(this.getAttribute("href"));
        if (target.length) {
            e.preventDefault();
            $("html, body").stop().animate({
                scrollTop: target.offset().top - 85
            }, 600);
        }
    });
});
