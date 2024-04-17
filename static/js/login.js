var form = document.getElementById('form-login');
const keyLogin = JSON.parse(document.getElementById('key_login').textContent);
csrftoken = form.getElementsByTagName("input")[0].value;


grecaptcha.ready(function() {
    $('#form-login').submit(function(e){
        e.preventDefault()
        grecaptcha.execute(keyLogin).then(function(token) {
            
            fetch("/loguearse/", {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrftoken,
                }, 
                body:JSON.stringify({
                        'captcha': token,
                        'usuario':document.querySelector('[name="username"]').value,
                        'password':document.querySelector('[name="password"]').value
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

                if(out[0]['mensaje'] == 'logueado'){

                    window.location = "https://idacom.com.ar?Bienvenido";

                }else if(out[0]['mensaje'] == 'error'){

                    Toast.fire({
                        icon: 'error',
                        title: 'Usuario o contraseña icorrecta',  
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
    });

});