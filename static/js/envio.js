let formDatosPersonales = document.getElementById('form-datos-personales');
let formDatosEnvio = document.getElementById('form-datos-envio');
let formDatosTarjeta = document.getElementById('form-card-decidir');
let email = document.getElementById("email-checkout");
let pTag = document.getElementById("p-tag");
let cp, correo;
let shipping = true;
let currentPrice = parseFloat($("#currentSubtotal").data("other").replace(',', '.'));
let totalCheck = parseInt($('#total_check').attr('data-other'));
let current_price = Math.ceil(currentPrice * 100) / 100
let address = '';
let currentActive = 1;
const progress = document.getElementById('progress');
const circles = document.querySelectorAll('.circle');
const dataKey = JSON.parse(document.getElementById('site_key').textContent);


csrftoken = formDatosPersonales.getElementsByTagName("input")[0].value;
//console.log('Newtoken:', form.getElementsByTagName("input")[0].value);

if (user != 'AnonymousUser'){
    document.getElementById('user-info').innerHTML = '';
};

let userFormData = {
    'name':null,
    'last_name':null,
    'phone':null,
    'email':null  
}

let shippingInfo = {
    'address':null,
    'city':null,
    'state':null,
    'zipcode':null,
    'directions':'',
    'correo':''
}
function datosPersonales(){
  
    if (user == 'AnonymousUser'){
        userFormData.name      = document.querySelector('[name="name"]').value;
        userFormData.last_name = document.querySelector('[name="last_name"]').value;
        userFormData.phone     = document.querySelector('[name="phone"]').value;
        userFormData.email     = document.querySelector('[name="email"]').value;

        localStorage.setItem("user_name", userFormData.name);
        localStorage.setItem("user_last_name", userFormData.last_name);
        localStorage.setItem("user_phone", userFormData.phone);
        localStorage.setItem("user_email", userFormData.email);
        localStorage.setItem("user_dni_cuit", formDatosPersonales.dni_cuit.value);
    }else{
        localStorage.setItem("user_dni_cuit", formDatosPersonales.dni_cuit.value);
    }
}

function datosEnvio(){
    let floor = document.getElementById('floor').value
    let indicaciones = formDatosEnvio.indicaciones.value
    let addressSeparated = address.split(',')

    if(floor == ''){
        shippingInfo.address   = addressSeparated[0];
    }else{
        shippingInfo.address   = addressSeparated[0] + ' ' + floor;
    }
    shippingInfo.city      = addressSeparated[1].replace(' ', '');
    shippingInfo.state     = addressSeparated[2].replace(' ', '');
    shippingInfo.zipcode   = cp;
    if(indicaciones == ''){
        shippingInfo.directions = '-';
    }else{
        shippingInfo.directions = indicaciones;
    }
    shippingInfo.correo    = correo;

    localStorage.setItem("shipping_address", address);
    //console.log("FLOOR:",shippingInfo.address );
    //console.log('INDICACIONES:', indicaciones)
    //console.log("DIRECCION COMPLETA:", shippingInfo.address)
    //console.log('DIRECCION SEPARADA:', addressSeparated)
    //console.log("CODIGO POSTAL:", cp)
}


$(document).ready(function() { 
    
    //console.log('PROVINCIA:', localStorage.getItem("shipping_state"))

    if (user == 'AnonymousUser'){
        document.querySelector('[name="name"]').value = localStorage.getItem("user_name");
        document.querySelector('[name="last_name"]').value = localStorage.getItem("user_last_name"); 
        document.querySelector('[name="phone"]').value = localStorage.getItem("user_phone");
        document.querySelector('[name="email"]').value = localStorage.getItem("user_email");      
    }

    formDatosPersonales.dni_cuit.value = localStorage.getItem("user_dni_cuit");
    //formDatosEnvio.direccion.value = localStorage.getItem("shipping_address");
    //formDatosEnvio.ciudad.value = localStorage.getItem("shipping_city");
    //if(localStorage.getItem("shipping_state") != null){
        //formDatosEnvio.provincia.value = localStorage.getItem("shipping_state");
        
    //}
});


//             Correos checkbox
/*
$('.correo').click(function(){
    //Get Data-Amount String & Convert to a Number
    var getAmt = parseInt($(this).attr("data-amount"));
    var getCorreo = $(this).attr("name");
    var price = parseInt($('#currentprice').data("other"));
    console.log(getAmt)
    console.log(getCorreo)
    console.log(price)

    if($(this).is(":checked")){
        var total = (price + getAmt).toString();
        correo = getCorreo.toString();
        $('.currentPrice').text("Total $" + total);
    
    }
    else if($(this).is(":not(:checked)")){
        total = (price - getAmt).toString();
        correo = '';
      
        $('.currentPrice').text("Subtotal $" + total);
    }
});

$(function(){

    var requiredCheckboxes = $(':checkbox[required]');

    requiredCheckboxes.change(function(){

        if(requiredCheckboxes.is(':checked')) {
            requiredCheckboxes.removeAttr('required');
        }

        else {
            requiredCheckboxes.attr('required', 'required');
        }
    });

});

*/
/*
$(document).ready(function () {
    $('#form-button').click(function(e) {
    checked = $("input[type=checkbox]:checked").length;

    if(!checked) {
        e.preventDefault();
        alert("Te olvidaste de elegir el metodo de envio!");
        return false;
    }

    });
});
*/


grecaptcha.ready(function() {
    $('#form-datos-personales').submit(function(e){
        e.preventDefault()
        grecaptcha.execute(dataKey).then(function(token) {

            if (user != 'AnonymousUser'){
                siguiente();
            }else{
                fetch("/email_validador/", {
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken':csrftoken,
                    }, 
                    body:JSON.stringify({
                        'captcha': token,
                        'email_checkout':document.querySelector('[name="email"]').value
                        }),  
                })
            
                .then(response => response.json())
                .then(out => {   

                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 2000,
                        timerProgressBar: true,
                    });

                    if(out[0]['email'] == true){

                        datosPersonales();
                        siguiente();

                    }else if(out[0]['email'] == false){

                        Toast.fire({
                            icon: 'error',
                            title: 'Correo electronico invalido.',  
                        })

                    }else{
            
                            Toast.fire({
                                icon: 'error',
                                title: 'Robot!',  
                            })
                        
                    };
                })
                .catch(error => console.log('error', error));
            }
        });
    });

});

formDatosEnvio.addEventListener('submit', function(e){
    e.preventDefault();
    //console.log('Form Submitted...');
    $("#contenedor-mp").load(location.href + " #contenedor-mp>*", "");
    datosEnvio();
    mercadopago();
    siguiente()

});

formDatosTarjeta.addEventListener('submit', function(e){
    e.preventDefault();
    //console.log('Form Submitted...');
    
    decidir()
});


function siguiente() {
            
    currentActive++

    if(currentActive > circles.length) {
        currentActive = circles.length
    };

    if(currentActive == 2){
        document.getElementById('datos-personales').classList.remove("doFadeOut");
        document.getElementById('datos-personales').classList.add("doFadeIn");
        document.getElementById('datos-personales').classList.remove("hidden");
        document.getElementById('detalle-compra').classList.add("hidden");
    };

    if(currentActive == 3){
        document.getElementById('datos-envio').classList.remove("doFadeOut");
        document.getElementById('datos-envio').classList.add("doFadeIn");
        document.getElementById('datos-personales').classList.add("hidden");
        document.getElementById('datos-envio').classList.remove("hidden");

    };

    if(currentActive == 4){
        document.getElementById('datos-pago').classList.add("doFadeIn");
        document.getElementById('datos-envio').classList.add("hidden");
        document.getElementById('datos-pago').classList.remove("hidden");

    };
    
    update();

};


function anterior(){
    
    currentActive--

    if(currentActive < 1) {
        currentActive = 1
    };

    if(currentActive == 1){
        document.getElementById('detalle-compra').classList.add("doFadeOut");
        document.getElementById('datos-personales').classList.add("hidden");
        document.getElementById('detalle-compra').classList.remove("hidden");
    };

    if(currentActive == 2){
        document.getElementById('datos-personales').classList.add("doFadeOut");
        document.getElementById('datos-envio').classList.add("hidden");
        document.getElementById('datos-personales').classList.remove("hidden");
    };

    if(currentActive == 3){
        document.getElementById('datos-envio').classList.add("doFadeOut");
        document.getElementById('datos-pago').classList.add("hidden");
        document.getElementById('datos-envio').classList.remove("hidden");

        document.getElementById('id_cuotas').selectedIndex = 0 ;

        if(totalCheck >= 9000){
            pTag.style.display = "block";
            $("#total-interest").text("")
        }else{    
            $("#currentSubtotal").css( 'color', '#000000');
            $("#currentPrice").text(" $" + (currentPrice + parseInt($("#correo_oca").data("amount"))).toString()).css( 'color', '#000000');
        }
            
    };

    update();

};


function update() {
    circles.forEach((circle, idx) => {
        if(idx < currentActive) {
            circle.classList.add('active')
        } else {
            circle.classList.remove('active')
        }
    });

    const actives = document.querySelectorAll('.active');

    progress.style.width = (actives.length - 1) / (circles.length - 1) * 100 + '%';

};


$(document).ready(function() {

    email.addEventListener("input", function() {
        //console.log(email.value);
        fetch("/email_verification/", {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            }, 
            body:JSON.stringify({
                    'email':email.value
                }),  
        })
        .then(response => response.json())
        .then(out => {   
            if (out[0]['cliente'] === true){
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                });

                Toast.fire({
                icon: 'info',
                title: 'Usuario registrado. Inicie sesion si lo desea.'
                });  
                //email.value = '';                       
            }else{
                //console.log(email.value);
            }    
        })
        .catch(error => console.log('error', error))  
    });
});

/*
$(document).ready(function() {
    console.log('Buscando direccion')
    
    listAddresses.innerHTML = "";
    inputAddress.addEventListener("input", function() {
        //console.log(address.value);
        fetch("/address_finder/", {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            }, 
            body:JSON.stringify({
                    'address':inputAddress.value
                }),  
        })
        .then(res => res.json())
        .then(data => {
            var counter = 1
            console.log(data[0]['nomenclaturas'])
            
            data[0]['nomenclaturas'].forEach(item => {
            
                let option = document.createElement("option");
                option.setAttribute("data-id", counter);
                option.value = item;
                console.log('counter:', counter)
                listAddresses.appendChild(option);
                counter++
                
            });
            listAddresses.click();
        })
        .catch(error => console.log('error', error))  
             
    });    
});
*/

function onInput() {
    var val = inputAddress.value;
    var opts = listAddresses.childNodes;
    for (var i = 0; i < opts.length; i++) {
        if (opts[i].value === val) {
            // An item was selected from the list!
            // yourCallbackHere()
            address = opts[i].value;
            codeAddress(opts[i].value)  
            
            setTimeout(function() {
                showMail(cp);
            }, 200);
            
            alert(correo);
            
            
            
        }
    }
};


function prisma(){
    var x = document.getElementById("prisma-tarjeta");
    var y = document.getElementById("mercadopago-tarjeta");
    if (x.style.display === "none") {
        x.style.display = "block";
        y.style.display = "none";
    } else {
        x.style.display = "none";
    }
};

function mercado(){

    document.getElementById('id_cuotas').selectedIndex = 0 ;

    if(totalCheck >= 9000){
        pTag.style.display = "block";
        $("#total-interest").text("")
    }else{    
        $("#currentSubtotal").css( 'color', '#000000');
        $("#currentPrice").text(" $" + (currentPrice + parseInt($("#correo_oca").data("amount"))).toString()).css( 'color', '#000000');
    }

    var x = document.getElementById("mercadopago-tarjeta");
    var y = document.getElementById("prisma-tarjeta");
    if (x.style.display === "none") {
        x.style.display = "block";
        y.style.display = "none";
    } else {
        x.style.display = "none";
    }
};



// showing loading
function displayLoading() {
    document.getElementById('cart-view-wrapper').style.display = 'none';
    document.getElementById('loading').classList.remove("hidden");  
};

// hiding loading 
function hideLoading() {
    document.getElementById('cart-view-wrapper').style.display = 'block';
    document.getElementById('loading').classList.add("hidden");
};


function decidir(){
    
    //console.log('Decidir')
    displayLoading()

    var expiry = formDatosTarjeta.expiry.value;
    var fields = expiry.split('/');
    var month = fields[0].replace(' ', '');
    var year = fields[1].replace(' ', '');
   

    //console.log("mes", month)
    //console.log("ano", year)
    //console.log("DNI", document.querySelector('[name="numero_documento"]').value)
    var tarjetaForm = JSON.stringify({
        "card_number": document.querySelector('[name="number"]').value,
        "card_expiration_month": month,
        "card_expiration_year": year, 
        "security_code": document.querySelector('[name="cvc"]').value, 
        "card_holder_name": document.querySelector('[name="name"]').value, 
        "card_holder_identification": {
            "type": 'DNI',
            "number": document.querySelector('[name="numero_documento"]').value,
        },
    });
    
    var installments = document.querySelector('[name="cuotas"]').value;

    fetch("https://developers.decidir.com/api/v2/tokens", {
        method:'POST',
        headers:{
            "apikey": "4ae76f00234843d1af5994ed4674fd76",
            'Content-Type':'application/json',
            
        }, 
        body:tarjetaForm,   
    })
    .then(response => response.json())
    .then(result => {
        
        fetch("/decidir/", {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
                
            }, 
            body:JSON.stringify({
                'result': result, 
                'user_info': userFormData,
                'shipping_info': shippingInfo,
                'installments': installments,
                'dni_cuit': formDatosPersonales.dni_cuit.value,
              
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            //console.log(data);
            if(data == 'error'){
                console.log('error decidir backend')
            }else if (data === 'approved'){
                hideLoading()
                let timerInterval
                Swal.fire({
                    icon: 'success',
                    title: 'Compra realizada con exito!',
                    text: 'En breve recibiras un correo electronico. Muchas gracias!',
                    timer: 8000,
                    timerProgressBar: true,
                    confirmButtonText: 'Entendido',
                    willClose: () => {
                        clearInterval(timerInterval)
                    }
                    }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.timer || result.dismiss === Swal.DismissReason.backdrop || result.dismiss === Swal.DismissReason.confirm ) {
                        //console.log('I was closed by the timer');
                        cart = {};
                        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
                        window.location = "https://www.idacom.com.ar";
                    }
                })
            }else{
                hideLoading()
                let timerInterval
                Swal.fire({
                    icon: 'error',
                    title: 'Error!',
                    text: data,
                    timer: 5000,
                    timerProgressBar: true,
                    confirmButtonText: 'Entendido',
                    willClose: () => {
                        clearInterval(timerInterval)
                    }
                })
            }

        })
        .catch(error => console.log('error', error));
    })
    .catch(error => console.log('error', error));
    
};


function mercadopago(){

    //console.log('Mercadopago') 

    fetch("/create_preference/", {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({
            'user_info': userFormData,
            'shipping_info': shippingInfo,
            'dni_cuit': formDatosPersonales.dni_cuit.value,
          
        }),   
    })
    .then((response) => response.json())
    .then((preference) => {

        if(preference == 'error'){
            console.log('error mp backend')
        }else{
            // Agrega credenciales de SDK
            const mp = new MercadoPago('APP_USR-648d6757-a1b0-4d71-b3fd-b72b1cce8d32', {
                locale: 'es-AR'
            });
    
            // Inicializa el checkout
            mp.checkout({
                
                preference: {
                    id: preference.id
                },
                render: {
                    container: '.cho-container', // Indica dónde se mostrará el botón de pago
                    label: 'Mercado Pago', // Cambia el texto del botón de pago (opcional)
                
                },
                    
            });
        }
            
    });   

};

function showCheckOut(t){
    var cartDiv = document.getElementById("cart-div");
    var checkOutDiv = document.getElementById("wrapper-finalizar-compra");
    var sliderCart = document.getElementById('slider-cart');
    var sliderCart1 = document.getElementById('slider-cart1');
    var sliderCart2 = document.getElementById('slider-cart2');
    var sliderCart3 = document.getElementById('slider-cart3');
    
    if (checkOutDiv.style.display == "none") {
        
        t.innerHTML = 'EDITAR CARRITO';
        cartDiv.style.display = "none";
        sliderCart.style.display = "none";
        sliderCart1.style.display = "none";
        sliderCart2.style.display = "none";
        sliderCart3.style.display = "none";
        checkOutDiv.style.display = "block";
    } else {
       
        t.innerHTML = 'FINALIZAR COMPRA';
        $('#cart-div').fadeIn( 1000 )
        cartDiv.style.display = "block";
        sliderCart.style.display = "block";
        actualizarCarrito();
        checkOutDiv.style.display = "none";
        document.getElementById('detalle-compra').classList.remove("doFadeOut");
        document.getElementById('datos-personales').classList.remove("doFadeIn");
        document.getElementById('datos-envio').classList.remove("doFadeIn")
        document.getElementById('datos-personales').classList.remove("doFadeOut");
        document.getElementById('datos-envio').classList.remove("doFadeOut")
        document.getElementById('datos-pago').classList.remove("doFadeIn");
        
    };
};

//    CORREOS OCA, CABA, BARILOCHE

/*
$(document).ready(function() {
    cp.addEventListener("input", function() {
        console.log(cp.value);
        if(cp.value >= 1000 & cp.value <= 1245 || cp.valu == 1675 || cp.value == 1703 || 
        cp.value == 1751 || cp.value == 1824 || cp.value == 1827 || cp.value == 2942 || cp.value == 8109){
            var correo_amount = parseInt($("#correo_caba").data("amount"))
            correo = document.getElementById('correo_caba').getAttribute("name")
            $("#currentprice").text("TOTAL:")
            $("#envio-total").text("$" + (correo_amount + current_price).toString()).css('font-family', 'Roboto)
            document.getElementById('correo-caba').classList.remove("hidden");
            document.getElementById('correo-oca').classList.add("hidden");
            document.getElementById('correo-bariloche').classList.add("hidden");
        }else if(cp.value == 1663 || cp.value == 8400 || cp.value == 4140){
            var correo_amount = parseInt($("#correo_bariloche").data("amount"))
            correo = document.getElementById('correo_bariloche').getAttribute("name")
            $("#currentprice").text("TOTAL:")
            $("#envio-total").text("$" + (correo_amount + current_price).toString()).css('font-family', 'Roboto')
            document.getElementById('correo-bariloche').classList.remove("hidden");
            document.getElementById('correo-oca').classList.add("hidden");
            document.getElementById('correo-caba').classList.add("hidden");
        }else if(cp.value == '' || cp.value <= 999){
            $("#currentprice").text("SUBTOTAL:")
            $("#envio-total").text("$" + (current_price).toString()).css('font-family', 'Roboto')
            correo = '';
            document.getElementById('correo-oca').classList.add("hidden");
            document.getElementById('correo-bariloche').classList.add("hidden");
            document.getElementById('correo-caba').classList.add("hidden");
        }else {
            var correo_amount = parseInt($("#correo_oca").data("amount"))
            $("#currentprice").text("TOTAL:")
            $("#envio-total").text("$" + (correo_amount + current_price).toString()).css('font-family', 'Roboto')
            correo = document.getElementById('correo_oca').getAttribute("name")
            document.getElementById('correo-oca').classList.remove("hidden");
            document.getElementById('correo-bariloche').classList.add("hidden");
            document.getElementById('correo-caba').classList.add("hidden");
        }
    });
});
*/

// CORREO OCA SOLAMENTE

function showMail(value){
        //console.log(cp.value);
        var indicaciones =document.getElementById('id_indicaciones')

        if(value == '' || value <= 999){
            $("#currentSubtotal").text("SUBTOTAL:")
            $("#currentPrice").text("$" + (current_price).toString()).css('font-family', 'Roboto')
            $("#envio-else").text("MAS GASTOS DE ENVIO").css('color', '#bb1b1b')
            correo = '';
            document.getElementById('correo-oca').classList.add("hidden");
            document.getElementById('correo-bariloche').classList.add("hidden");
            document.getElementById('correo-caba').classList.add("hidden");
            indicaciones.style.display = "none"
        }else {
            var correo_amount = parseInt($("#correo_oca").data("amount"))
            $("#currentSubtotal").text("TOTAL:")
            $("#currentPrice").text("$" + (correo_amount + current_price).toString()).css('font-family', 'Roboto')
            $("#envio-else").text("GASTOS DE ENVIO INCLUIDOS").css('color', '#b68500')
            correo = 'OCA';
            document.getElementById('correo-oca').classList.remove("hidden");
            document.getElementById('correo-bariloche').classList.add("hidden");
            document.getElementById('correo-caba').classList.add("hidden");    
            indicaciones.style.display = "block"
        }
};


function interest(){
    let selectBox = document.getElementById("id_cuotas");
    let cuotas = selectBox.options[selectBox.selectedIndex].value;
    let index = selectBox.options[selectBox.selectedIndex].index;
    let total = (current_price + parseFloat($("#correo_oca").data("amount"))).toFixed(0)
    let cuotaPS = '';
    let inter = ''
    let nameId = '';
    let t = '';
    let totalInterest = 0;
    let cuotaInterest = 0;

    if(cuotas == 1){
        cuotaPS = " CUOTA DE $"
    }else{
        cuotaPS = " CUOTAS DE $"
    }
    
    if(totalCheck >= 9000){
        nameId = "#total-interest"
        pTag.style.display = "none";
        t = 'TOTAL: '
    }else{
        nameId = "#currentPrice"
        $("#currentSubtotal").css( 'color', '#D6A200')
        t = '';
    } 

    if(cuotas == '1' || cuotas == '3' || cuotas == '6'){      
        totalInterest = parseInt(total)
        inter = '0.00%'
        cuotaInterest = (totalInterest / parseInt(cuotas)).toFixed(2)
    }else if(cuotas == '12'){
        let interes = (18.18 * total) / 100
        totalInterest = parseInt(total) + interes
        inter = '18.18%'
        cuotaInterest = (totalInterest / parseInt(cuotas)).toFixed(2)
    }else if(cuotas == '18'){
        let interes = (28.84 * total) / 100
        totalInterest = (parseInt(total) + interes)
        inter = '28.84%'
        cuotaInterest = (totalInterest / parseInt(cuotas)).toFixed(2)
    }else{
        let interes = (35.83 * total) / 100
        totalInterest = parseInt(total) + interes
        inter = '35.83%'
        cuotaInterest = (totalInterest / parseInt(cuotas)).toFixed(2)
    }
   
    let spans = ["<span>" + (t).toString() + " " + "<span style='color:#E2002691;'> $" + (totalInterest.toFixed(2)).toString() + "</span>",
    "</span>", "<span> EN " + "</span>", "<span style='color:#E2002691;'>" + (cuotas).toString() + " " + "</span>", "<span>" + (cuotaPS).toString() + " " + "</span>",
    "<span style='color:#E2002691;'>" + (cuotaInterest).toString() + " " + "<span> CFT " + "</span>", "</span>","<span style='color:#E2002691;'>" + (inter).toString() + "</span>"];

    $(nameId).html(spans.join(" "))
    
    if(index == 0){
        pTag.style.display = "block";
        $("#total-interest").text("")
    }

}


if (window.location.href.indexOf("success") > -1) {
    let timerInterval
    Swal.fire({
        icon: 'success',
        title: 'Compra realizada con exito!',
        text: 'En breve recibiras un correo electronico. Muchas gracias!',
        timer: 8000,
        timerProgressBar: true,
        confirmButtonText: 'Entendido',
        willClose: () => {
            clearInterval(timerInterval)
        }
        }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer || result.dismiss === Swal.DismissReason.backdrop || result.dismiss === Swal.DismissReason.confirm ) {
            //console.log('I was closed by the timer');
            cart = {};
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
            window.location = "https://www.idacom.com.ar";
        };
    });
};

if (window.location.href.indexOf("pending") > -1) {
    let timerInterval
    Swal.fire({
        icon: 'warning',
        title: 'Compra pendiente!',
        text: 'Una vez acreditado el pago recibiras un correo electonico. Muchas gracias!',
        timer: 8000,
        timerProgressBar: true,
        confirmButtonText: 'Entendido',
        willClose: () => {
            clearInterval(timerInterval)
        }
        }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer || result.dismiss === Swal.DismissReason.backdrop || result.dismiss === Swal.DismissReason.confirm ) {
            //console.log('I was closed by the timer');
            cart = {};
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
            window.location = "https://www.idacom.com.ar";
        };
    });  
  
};

if (window.location.href.indexOf("failure") > -1) {
    let timerInterval
    Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'Pago rechazado',
        timer: 5000,
        timerProgressBar: true,
        confirmButtonText: 'Entendido',
        willClose: () => {
            clearInterval(timerInterval)
        }
    });  
};


$('#form-card-decidir').card({
    // a selector or DOM element for the container
    // where you want the card to appear
    container: '.card-wrapper', // *required*

    // all of the other options from above
    width: 320, // optional — default 350px
    formatting: true, // optional - default true

    // Strings for translation - optional
    messages: {
        validDate: 'hasta\nthru', // optional - default 'valid\nthru'
        monthYear: 'mm/aa', // optional - default 'month/year'
    },

    // Default placeholders for rendered fields - optional
    placeholders: {
        number: '1234 5678 9101 1121',
        name: 'CARLOS GONZALES',
        expiry: '••/••',
        cvc: '•••'
    },

    masks: {
        cardNumber: '•' // optional - mask card number
    },

    // if true, will log helpful messages for setting up Card
    debug: true // optional - default false
});



//    Google maps 


var buttonNext = document.getElementById("button-seguir-envio");
var extraZipCode = document.getElementById("zip-code");

function inicioGoogleMaps() {

    const ARGENTINA_BOUNDS = {
        north: -20.603781336016716,
        south: -56.41124018961127,
        west: -75.25527275168552,
        east: -53.39580233978408,
      };

    const ARG = { lat: -35.177247907485516, lng: -65.46096581635403};
    
    const mapOptions = {
        zoom: 5,
        center: ARG,
        disableDefaultUI: true,
        restriction: {
            latLngBounds: ARGENTINA_BOUNDS,
            //strictBounds: false,
        },
    };

    const options = {
        componentRestrictions: {
            country: 'AR'
        },   
        fields: ["address_components", "formatted_address", "geometry", "name"],
        type:["address"]
    };

    const input = document.getElementById('address');
    const autocomplete = new google.maps.places.Autocomplete(input, options);
    const map = new google.maps.Map(document.getElementById('mapa'), mapOptions);
    autocomplete.bindTo("bounds", map);
    const infowindow = new google.maps.InfoWindow();
    const infowindowContent = document.getElementById("infowindow-content");

    infowindow.setContent(infowindowContent);

    const marker = new google.maps.Marker({
        map,
        anchorPoint: new google.maps.Point(0, -29),
    });
    
    autocomplete.addListener("place_changed", () => {
        infowindow.close();
        marker.setVisible(false);

        $(document).ready(function() {
           
            input.addEventListener("input", function() {
                if(input.value == ''){
                    extraZipCode.style.display = 'none';
                    buttonNext.setAttribute("disabled", "disabled");
                    showMail('');
                    infowindow.close();
                    marker.setVisible(false);
                    cp =undefined;
                    zcode =undefined;
                }
            });
        });

        const place = autocomplete.getPlace();
        //console.log('PLACE:', place)
        let streetName, streetNumber, zcode, locality, pro;
        let typs = []

        for(var j=0;j < place.address_components.length; j++){
            typs.push(place.address_components[j].types[0])
        }
        //console.log('typs list:', typs)

        if(place.address_components[0].types[0] != "street_number"){
            
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
            });

            Toast.fire({
            icon: 'info',
            title: 'Direccion inexistente o sin numero, intente nuevamente.'
            });  

            input.value = '';
            extraZipCode.style.display = "none";
            buttonNext.setAttribute("disabled", "disabled");
            showMail('')

        }else{

            cp =undefined;
            zcode =undefined;
   
            for(var j=0;j < place.address_components.length; j++){
                for(var k=0; k < place.address_components[j].types.length; k++){
                    //console.log("tipos:", place.address_components[j].types[k])
                    
                    if(place.address_components[j].types[k] == "route"){
                        streetName= place.address_components[j].long_name;
                        //console.log("street name:", streetName)
                    };

                    if(place.address_components[j].types[k] == "street_number"){
                        streetNumber = place.address_components[j].short_name;
                        //console.log("street number:", streetNumber)
                    };

                    if(place.address_components[j].types[k] == "locality"){
                        locality = place.address_components[j].long_name;
                        //console.log("locality:", locality)
                    }else{
                        if(place.address_components[j].types[k] == "sublocality_level_1"){
                            locality = place.address_components[j].long_name;
                            //console.log("locality:", locality)
                        };
                    };

                    if(place.address_components[j].types[k] == "administrative_area_level_1"){

                        if (place.address_components[j].long_name.startsWith('Provincia de')){
                            pro = place.address_components[j].long_name.replace("Provincia de ","");
                        }else{
                            pro = place.address_components[j].long_name;
                        }

                        //console.log("provin:", pro)
                    };

                    if(place.address_components[j].types[k] == "postal_code"){
                        zcode = place.address_components[j].short_name.substr(1);
                        //console.log("ZIPCODE LOOP:", zcode)
                    }
                }
            }


            /*
            if (!place.geometry || !place.geometry.location) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                });

                Toast.fire({
                icon: 'info',
                title: 'Direccion inexistente o sin numero, intente nuevamente.'
                });
            return;
            }
            */


            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                map.setCenter(place.geometry.location);
                map.setZoom(17);
            }
            infowindowContent.children["place-address"].textContent = place.formatted_address;
            marker.setPosition(place.geometry.location);
            marker.setVisible(true);
        
            infowindow.open(map, marker);

            if(zcode == undefined){

                fetch("/address_finder/", {
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken':csrftoken,
                    }, 
                    body:JSON.stringify({
                            'city':locality,
                            'state':pro
                        }),  
                })
                .then(res => res.json())
                .then(data => {
                    //console.log("DATA:", data[0]['zipcode'])
                    if(data[0]['zipcode'] != 'none'){
                        cp = data[0]['zipcode'];
                        showMail(cp)
                    }else{
                        extraZipCode.style.display = "block";
                        extraZipCode.setAttribute("required", "");
                        extraZipCode.addEventListener("input", function() {
                            cp = extraZipCode.value;
                            showMail(cp);
                        });
                    }
                   
                })
                .catch(error => console.log('error', error))  
            
            }else{
                extraZipCode.style.display = "none";
                extraZipCode.removeAttribute("required");
                cp =zcode
                showMail(cp);
            }

            address = streetName + ' ' + streetNumber + ',' + ' ' + locality + ',' + ' ' + pro
            
            //console.log("ADDRESS, ZC", address, cp)
            buttonNext.removeAttribute("disabled");
            
            /*
            breakme: if (place.address_components.length == 6){
                if(parseInt(place.address_components[0]['short_name']) != 'NaN'){
        
                    if (extraZipCode.style.display === "none") {
                        extraZipCode.style.display = "block";
                    };

                    if (place.address_components[4]['long_name'].startsWith('Provincia de')){
                        var provincia = place.address_components[4]['long_name'].replace("Provincia de ","");
                    }else{
                        var provincia = place.address_components[4]['long_name'];
                    }

                    address = place.name + ',' + ' '+ place.address_components[2]['short_name'] + ',' + ' '+ provincia;

                    extraZipCode.addEventListener("input", function() {
                        cp = extraZipCode.value;
                        showMail(cp);
                    });

                    console.log("ADDRESS:", address)
                    
                }

            }else if (place.address_components.length == 7){
                
        
                if (extraZipCode.style.display === "none") {
                    extraZipCode.style.display = "block";
                };

                if (place.address_components[5]['short_name'].startsWith('Provincia de')){
                    var provincia = place.address_components[5]['short_name'].replace("Provincia de ","");
                }else{
                    var provincia = place.address_components[5]['short_name'];
                }

                address = place.name + ',' + ' '+ place.address_components[3]['short_name'] + ',' + ' '+ provincia;

                extraZipCode.addEventListener("input", function() {
                    cp = extraZipCode.value;
                    showMail(cp);
                });

                console.log("ADDRESS:", address)
                
            }else if(place.address_components.length == 8 || place.address_components.length == 9){

                
                if (extraZipCode.style.display === "block") {
                    extraZipCode.style.display = "none";
                };

                if (place.address_components[6]['short_name'] == 'AR'){
                    if (place.address_components[5]['long_name'].startsWith('Provincia de')){
                        var provincia = place.address_components[5]['long_name'].replace("Provincia de ","");
                    }else{
                        var provincia = place.address_components[5]['long_name'];
                    }
        
                    address = place.name + ',' + ' '+ place.address_components[3]['long_name'] + ',' + ' '+ provincia;
                    cp =  place.address_components[7]['long_name'].substr(1)
                }else{

                    if (place.address_components[4]['long_name'].startsWith('Provincia de')){
                        var provincia = place.address_components[4]['long_name'].replace("Provincia de ","");
                    }else{
                        var provincia = place.address_components[4]['long_name'];
                    }

                    address = place.name + ',' + ' '+ place.address_components[2]['long_name'] + ',' + ' '+ provincia;
                    cp =  place.address_components[6]['long_name'].substr(1)
                }

                console.log("ADDRESS:", address)
                showMail(cp);

            }else{
                alert("No se encuentra esa direccion");
                input.value = '';
                break breakme
                
            }

            


        */  
        }; 
    });     
              
};

window.addEventListener('load', inicioGoogleMaps())