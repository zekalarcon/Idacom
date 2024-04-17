var form = document.getElementById('form-registro');
var email = document.getElementById("username");
const keyRegistro = JSON.parse(document.getElementById('key_registro').textContent);
csrftoken = form.getElementsByTagName("input")[0].value;


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
                    timer: 2000,
                    timerProgressBar: true,
                });

                Toast.fire({
                    icon: 'error',
                    title: 'El correo electronico ya existe!\nInicie sesion.',  
                })

                email.value = '';
                
            }else{
                //console.log(email.value);
            }    
        })
        .catch(error => console.log('error', error))  
    });
});


$(document).ready(function() {
    // messages timeout for 10 sec 
    setTimeout(function() {
        $('#error').fadeOut('slow');
    }, 6000); // <-- time in milliseconds, 1000 =  1 sec

    // delete message
    $('.del-msg').on('click',function(){
        $('.del-msg').parent().attr('style', 'display:none;');
    })
});


grecaptcha.ready(function() {
    $('#form-registro').submit(function(e){

        e.preventDefault()

        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true,
        });

        if( document.getElementById("pass-1").value != document.getElementById("pass-2").value){

            Toast.fire({
                icon: 'error',
                title: 'El password 1 no coicide con el password 2',  
            })

        }else{

            grecaptcha.execute(keyRegistro).then(function(token) {
                
                fetch("/email_validador/", {
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken':csrftoken,
                    }, 
                    body:JSON.stringify({
                            'captcha': token,
                            'email_checkout':document.querySelector('[name="username"]').value,
                        }),  
                })
                .then(response => response.json())
                .then(out => {   

                    if(out[0]['email'] == true){

                        fetch("/registrar_cliente/", {
                            method:'POST',
                            headers:{
                                'Content-Type':'application/json',
                                'X-CSRFToken':csrftoken,
                            }, 
                            body:JSON.stringify({
                                    'email':document.querySelector('[name="username"]').value,
                                    'nombre':document.querySelector('[name="nombre"]').value,
                                    'apellido':document.querySelector('[name="apellido"]').value,
                                    'telefono':document.querySelector('[name="telefono"]').value,
                                    'password1':document.querySelector('[name="password1"]').value,
                                }),  
                        })
                        .then(response => response.json())
                        .then(out => {   
            
                            if(out[0]['mensaje'] == 'guardado'){
            
                                Toast.fire({
                                    icon: 'success',
                                    title: 'Usuario creado con exito!',  
                                }).then((result) => {
                                    if (result.dismiss === Swal.DismissReason.timer || result.dismiss === Swal.DismissReason.backdrop || result.dismiss === Swal.DismissReason.confirm ) {
                                        window.location = "https://idacom.com.ar/acceso";
                                    };
                                });

                            }else{
            
                                Toast.fire({
                                    icon: 'error',
                                    title: 'Ups algo salio mal, intenta nuevamente',  
                                })
            
                            };
                        })
                        .catch(error => console.log('error', error));

                    }else if(out[0]['email'] == false){

                        Toast.fire({
                            icon: 'error',
                            title: 'Correo electronico invalido!',  
                        })

                    }else{
            
                            Toast.fire({
                                icon: 'error',
                                title: 'Robot!',  
                            })
                        
                    };
                })
                .catch(error => console.log('error', error));
                
            });
        };
    });
});