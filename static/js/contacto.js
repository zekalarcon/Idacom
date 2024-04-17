let captchaValue
const dataKey = JSON.parse(document.getElementById('site_key').textContent);

grecaptcha.ready(function() {
    $('#form-contacto').submit(function(e){
        e.preventDefault()
        grecaptcha.execute(dataKey).then(function(token) {
            captchaValue = token;
            mandarMensaje();
        });
    })

});
    

function mandarMensaje(){

    let emailContacto = $('#id_email_contacto').val();
    let mensaje = $('#id_mensaje').val();
    

    fetch("/mandar_mensaje/", {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({
                'email':emailContacto,
                'mensaje': mensaje,
                'captcha': captchaValue
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
        

        if (out[0]['mensaje'] == 'enviado'){

            Toast.fire({
                icon: 'success',
                title: 'Mensaje enviado con exito. Gracias por contactarse con IDACOM.',  
            }).then((result) => {
                if (result.dismiss === Swal.DismissReason.timer || result.dismiss === Swal.DismissReason.backdrop || result.dismiss === Swal.DismissReason.confirm ) {
                    location.reload();
                }
            })  
             
        }else if(out[0]['mensaje'] == 'error'){

            Toast.fire({
                icon: 'error',
                title: 'Ups algo salio mal, volve a intentar.'
            });

        }else if(out[0]['mensaje'] == 'email invalido'){

            Toast.fire({
                icon: 'error',
                title: 'Email invalido!'
            });
           
        }else{

            Toast.fire({
                icon: 'error',
                title: 'Robot!'
            });
        }   
    })
    .catch(error => console.log('error', error));
}
 