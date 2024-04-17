const swiper = new Swiper(".mySwiper", {
  loop: true,
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
});

const swiper2 = new Swiper(".mySwiper2", {
  loop: true,
  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  thumbs: {
    swiper: swiper,
  },
});

const swiperMini = new Swiper(".mySwiperMini", {
  loop: true,
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
});

const swiper2Mini = new Swiper(".mySwiper2Mini", {
  loop: true,
  spaceBetween: 10,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  thumbs: {
    swiper: swiperMini,
  },
});


const swiperDetail1 = new Swiper('#swiper-detail-1', {
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

function swiperDetail2(){
  const swiperDetail2 = new Swiper('#swiper-detail-2', {
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