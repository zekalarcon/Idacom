$(window).scroll(function () {
    var h = ($(this).scrollTop());
    $('#carousel > div').css({
        'transform': 'scale(' + (1 + h / 2000) + ') translateY(' + h / 15 + '%) rotateZ(-' + (h / 45) + 'deg)'
    });

    $('#carousel > i').css({
        'transform': 'translateY(' + h/2 + '%)'
    });
});

if (window.location.href.indexOf("Bienvenido") > -1) {

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 2500,
    });

    Toast.fire({
        title: 'Bienvenido ' + user,  
    })
  
};

const swiper1 = new Swiper('#swiper1', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    centeredSlides:true,
    autoplay:true,
     // Default parameters
    slidesPerView: 3,
    spaceBetween: 10,
    // Responsive breakpoints
    breakpoints: {
        // when window width is >= 320px
        320: {
        slidesPerView: 2,
        spaceBetween: 5,
        },
        // when window width is >= 480px
        480: {
        slidesPerView: 3,
        spaceBetween: 10
        },
        // when window width is >= 640px
        640: {
        slidesPerView: 3,
        spaceBetween: 10
        }
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

});


function swiper2(){
    const swiper2 = new Swiper('#swiper2', {
        // Optional parameters
        direction: 'horizontal',
        loop: true,
        centeredSlides:true,
        autoplay:true,
        // Default parameters
        slidesPerView: 3,
        spaceBetween: 10,
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 2,
            spaceBetween: 5,
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 3,
            spaceBetween: 10
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 3,
            spaceBetween: 10
            }
        },

        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

    });
}

const swiper3 = new Swiper('#swiper3', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    centeredSlides:true,
    autoplay:true,
     // Default parameters
    slidesPerView: 3,
    spaceBetween: 10,
    // Responsive breakpoints
    breakpoints: {
        // when window width is >= 320px
        320: {
        slidesPerView: 2,
        spaceBetween: 5,
        },
        // when window width is >= 480px
        480: {
        slidesPerView: 3,
        spaceBetween: 10
        },
        // when window width is >= 640px
        640: {
        slidesPerView: 3,
        spaceBetween: 10
        }
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

});

function swiper4(){
    const swiper4 = new Swiper('#swiper4', {
        // Optional parameters
        direction: 'horizontal',
        loop: true,
        centeredSlides:true,
        autoplay:true,
        // Default parameters
        slidesPerView: 3,
        spaceBetween: 10,
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 2,
            spaceBetween: 5,
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 3,
            spaceBetween: 10
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 3,
            spaceBetween: 10
            }
        },

        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

    });
}

const swiperHomeEnd = new Swiper(".mySwiperHome", {
    loop: true,
    spaceBetween: 10,
    slidesPerView: 1,
    autoplay:true,
});

function nextVideo(t){
    let videoNumber = $(t).data('video');
    $(".carousel").carousel("next");
    var vid1 = document.getElementById('video-1');
    var vid2 = document.getElementById('video-2');
    var vid3 = document.getElementById('video-3');

    vid2.currentTime = 0;
    vid3.currentTime = 0;
    vid1.currentTime = 0;

}
