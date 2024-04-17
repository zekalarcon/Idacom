var updateBtns = document.getElementsByClassName('update-cart');
var cardAdd = document.getElementsByClassName('add-card');

function addProducto(d){
    d.classList.add('clicked'); 
    var productId = d.getAttribute("data-product")
    var action = d.getAttribute("data-action")

    if (user == 'AnonymousUser') { 
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1};
        }else{
            cart[productId]['quantity'] += 1 ; 
        };   
        document.cookie = 'cart=' + JSON.stringify(cart) + ";expires=Fri, 31 Dec 9999 23:59:59 GMT;domain=;path=/";
    }
    else {
        var url = '/update_item/';

        fetch(url, {
            method: 'POST',
            headers:{
                'Content-type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'productId': productId, 'quantity': null, 'action':action})
        })
        .then(console.log('updated'))
    }
    
    $("#menubar").load(location.href + " #menubar>*", "");
    
    setTimeout(function(){  
        $("#kits").load(location.href + " #kits>*", "");
        $("#arma-tu-kit").load(location.href + " #arma-tu-kit>*", "");
    }, 1900)
    
}

function botonTabla(d){

    var productId = d.getAttribute("data-product")
    var action = d.getAttribute("data-action")
    var info = d.getAttribute("data-info")
    var div = d.getAttribute("data-div")
    
    if (user == 'AnonymousUser') {
        if (info == 'detail' || info == 'home' || info == 'carrito'){
            d.classList.add('clicked');
	        addCookieItem(productId, null, action, info, d, div);      
        }else{
            addCookieItem(productId, null, action, info, d, div);
        }   
    }
    else {
        if (info == 'detail' || info == 'home' || info == 'carrito'){
            d.classList.add('clicked');
            updateUserOrder(productId, null, action, info, d, div);
        }else{
            updateUserOrder(productId, null, action, info, d, div);
        }   
    }
 
};


$(document).on('click', '#cantidad', function(){  

    var cantidad = document.querySelectorAll("#cantidad");
    actualizarInputs(cantidad)

});

function actualizarInputs(cantidad){
    cantidad.forEach(function(elem){
    
        elem.addEventListener("input", function() {
            console.log(elem.value);
            
            var productId = elem.dataset.product
            var quantity = elem.value;
            let info = 'carrito'
            let action = 'input-change'

            if (user == 'AnonymousUser') {
                if( quantity != ''){
                    setTimeout(function(){
                        addCookieItem(productId, quantity, action, info, null, null);          
                    }, 500);
                }
            }
            else {
                if( quantity != ''){
                    setTimeout(function(){
                        updateUserOrder(productId, quantity, action, info, null, null); 
                    }, 500);
                }
            }
        
        });
    
    });
};

function addCookieItem(productId, quantity, action, info, d, div){
    //console.log('Usuario no registrado ..');

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1};
        }else{
            cart[productId]['quantity'] += 1 ; 
        }
    }
    else if(action == 'remove'){
        cart[productId]['quantity'] -= 1;

        if(cart[productId]['quantity'] <= 0){
            //console.log('Remove item');
            delete cart[productId];
        }
    }
    else if(quantity == 0 || action == 'delete'){
        delete cart[productId];
    }
    else{
        cart[productId]['quantity'] = parseInt(quantity);
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";expires=Fri, 31 Dec 9999 23:59:59 GMT;domain=;path=/";
    //location.reload();
    $("#menubar").load(location.href + " #menubar>*", ""); 


    if(Object.keys(cart).length === 0){

        location.reload()

    }else if(info == 'carrito'){

        $("#carrito").load(location.href + " #carrito>*", "");
        

        if(div = 'slider-carrito'){
            setTimeout(function(){
                d.classList.remove('clicked');
                actualizarCarrito();
            }, 2000); 
        }else{
            actualizarCarrito();   
        };

    }else{

        setTimeout(function(){
            d.classList.remove('clicked');
            actualizarSlider(info); 
        }, 2000);     
    };
};

function updateUserOrder(productId, quantity, action, info, d, div){
    //console.log('Usuario registrado..');
    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'quantity': quantity, 'action':action})
    })
    .then((response) =>{
        return response.json();
    })
    .then((out) =>{
        //console.log('data:', out[0]);
        //$(".cart-icon").toggleClass("down");
        //location.reload();
        $("#menubar").load(location.href + " #menubar>*", "");

        if(out[0]['data'] == '0'){

            location.reload()

        }else if(info == 'carrito'){

            $("#carrito").load(location.href + " #carrito>*", "");

            if(div = 'slider-carrito'){
                setTimeout(function(){
                    d.classList.remove('clicked');
                    actualizarCarrito();
                }, 2000); 
            }else{
                actualizarCarrito();   
            };

        }else{

            setTimeout(function(){
                d.classList.remove('clicked');
                actualizarSlider(info);
            }, 2000);             
        };
    });
};

function actualizarSlider(info){

    fetch("/update_slider/", {
        method:'GET'
    })
    .then(response => response.json())
    .then(out => {   

        if(out['total'] == 'mayor'){
            //console.log('mayor')

            if(info == 'home'){

                var kits1 = document.getElementById('kits-home-slider');
                var kits2 = document.getElementById('kits-home-slider2');

                var productos1 = document.getElementById('productos-home-slider');
                var productos2 = document.getElementById('productos-home-slider2');

                if(kits2.style.display == 'none'){

                    kits1.style.display = 'none';
                    kits2.style.display = 'block';   
                    swiper2();

                    productos1.style.display = 'none';
                    productos2.style.display = 'block';
                    swiper4();
                    
                }else{
                    
                };

            }else{

                $("#detail-precio").load(location.href + " #detail-precio>*", "");
                $("#detail-mini-precio").load(location.href + " #detail-mini-precio>*", "");

                var noTeVa1 = document.getElementById('slider-no-te-olvides');
                var noTeVa2 = document.getElementById('slider-no-te-olvides2');

                if(noTeVa2.style.display == 'none'){

                    noTeVa1.style.display = 'none';
                    noTeVa2.style.display = 'block'; 
                    swiperDetail2();

                }else{
                    
                };
        
            }

        }else if(out['total'] == 'menor'){

            //console.log('menor')
            
        }else{

            console.log('error');

        }
        
    })
    .catch(error => console.log('error', error));
}

function actualizarCarrito(){
    
    var sliderCart1 = document.getElementById('slider-cart1');
    var sliderCart2 = document.getElementById('slider-cart2');
    var sliderCart3 = document.getElementById('slider-cart3');

    fetch("/update_slider/", {
        method:'GET'
    })
    .then(response => response.json())
    .then(out => {   

        if(out['total'] == 'mayor'){
            //console.log('mayor')
 
            if(sliderCart2.style.display == 'none'){

                sliderCart3.style.display = 'none' 
                sliderCart1.style.display = 'none'
                $('#slider-cart2').fadeIn( 1000 )
                sliderCart2.style.display = 'block'   
                swiperCarrito2()
                 
            }else{
                
            }      
           
        }else if(out['total'] == 'menor' || out['total'] == '0'){ 
            //console.log('menor')

            if(sliderCart3.style.display == 'none'){

                sliderCart1.style.display = 'none'
                sliderCart2.style.display = 'none'
                $('#slider-cart3').fadeIn( 1000 )
                sliderCart3.style.display = 'block' 
                swiperCarrito3()   
                 
            }else{
                
            }      
                      
        }else{
            console.log('error')
        }
        
    })
    .catch(error => console.log('error', error));
}