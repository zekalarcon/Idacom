
function getCookie(c_name) {
    if(document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if(c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if(c_end == -1) c_end = document.cookie.length;
            return document.cookie.substring(c_start,c_end);
        }
    }
    return "";
};


function calificar(t) {

    const inputOptions = new Promise((resolve) => {
            resolve({
            '1': '★',
            '2': '★',
            '3': '★',
            '4': '★',
            '5': '★'
            })	
    })
    Swal.fire({
        title: 'Que te parecio el producto' + ' ' + $(t).data('name') + ' ' +'?',
        icon: 'question',
        input: 'radio',	
        inputOptions: inputOptions,
        inputValidator: (value) => {
            if (!value) {
            return 'Tenes que elegir una opcion!'
            }
        }		
    })
    .then((data) => {
        //console.log(data.value)

        fetch("/calificar_producto/", {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':getCookie("csrftoken"),
            }, 
            body:JSON.stringify({
                'producto_id': $(t).data('productoid'),
                'compra_id': $(t).data('compraid'),
                'calificacion': data.value
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

            if(out[0]['mensaje'] == 'guardado'){

                Toast.fire({
                    icon: 'success',
                    title: 'Producto calificado correctamente!',  
                })

            }else{ 
                    Toast.fire({
                        icon: 'error',
                        title: 'Ups intenta nuevamente',  
                    });
                
            };
        })
        .catch(error => console.log('error', error));
        
    });        

};

$("#eliminar-cuenta").click(function() {
    let cliente = $(this).attr('data-cliente')

    Swal.fire({
        title: 'Estas seguro que queres eliminar tu cuenta?',
        text: "Vas a tener que volver a crearla para ver esta seccion nuevamente!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#1d1f1de7',
        cancelButtonColor: ' #6d6b6b',
        confirmButtonText: 'Si, eliminar!',
        cancelButtonText: 'Cancelar'
    })
    .then((result) => {
        if (result.isConfirmed) {
  
            fetch("/eliminar_cuenta/", {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':getCookie("csrftoken"),
                }, 
                body:JSON.stringify({
                    'cliente': cliente,
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

                if(out[0]['mensaje'] == 'eliminado'){

                    Toast.fire({
                        icon: 'success',
                        title: 'Cuenta eliminada con exito\nTe vamos a extrañar!',  
                    }).then((result) => {
                        if (result.dismiss === Swal.DismissReason.timer || result.dismiss === Swal.DismissReason.backdrop || result.dismiss === Swal.DismissReason.confirm ) {
                            window.location = "https://www.idacom.com.ar/salir";
                        }
                    })  

                }else{ 
                    Toast.fire({
                        icon: 'error',
                        title: 'Ups intenta nuevamente',  
                    });
                
                };
            })
            .catch(error => console.log('error', error));
        }
    })
});
