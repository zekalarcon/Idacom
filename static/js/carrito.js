$(document).ready(function() {
    document.title = 'Checkout IDACOM';
});

const swiperCarrito1 = new Swiper('#swiper-carrito-1', {
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

function swiperCarrito2(){
    const swiperCrrito2 = new Swiper('#swiper-carrito-2', {
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

function swiperCarrito3(){
    const swiperCarrito3 = new Swiper('#swiper-carrito-3', {
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