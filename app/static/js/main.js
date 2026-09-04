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

    // Suporte a arraste horizontal com o mouse/touch nas fotos panorâmicas
    function enableHorizontalDrag(selector) {
        const slider = document.querySelector(selector);
        if (!slider) return;

        let isDown = false;
        let startX;
        let scrollLeft;

        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            slider.style.cursor = 'grabbing';
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });

        slider.addEventListener('mouseleave', () => {
            isDown = false;
            slider.style.cursor = 'grab';
        });

        slider.addEventListener('mouseup', () => {
            isDown = false;
            slider.style.cursor = 'grab';
        });

        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 1.5;
            slider.scrollLeft = scrollLeft - walk;
        });
    }

    enableHorizontalDrag('#heroCoverContainer');
    enableHorizontalDrag('.dashboard-banner');
});
