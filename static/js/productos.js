$(document).ready(function() {
    document.title = 'Productos IDACOM';
});

if (window.location.href.indexOf("#") > -1) {
    $(".tab-pane").removeClass("show active");
    $("#arma-tu-kit").addClass("show active");
    $(".nav-link").removeClass("active");
    $("#B").addClass("active");	 
    window.history.replaceState({}, document.title, "/" + 'productos/' );
};