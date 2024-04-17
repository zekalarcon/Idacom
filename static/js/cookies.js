var cookieAlert = document.querySelector(".cookie-alert");
var acceptCookies = document.querySelector(".accept-cookies");

if (!getCookie("acceptCookies")) {
    cookieAlert.classList.add("show");
}

acceptCookies.addEventListener("click", function () {
    setCookie("acceptCookies", true, 1);
    cookieAlert.classList.remove("show");
});

// Cookie functions stolen from w3schools
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

//console.log(document.cookie)