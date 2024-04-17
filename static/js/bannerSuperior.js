var text = ["10% OFF En compras superiores a $9000", "6 CUOTAS SIN INTERES", "Envio gratis en ordenes superiores a $4000"];
var counter = 0;
var elem = document.getElementById("changeText");
var inst = setInterval(change, 5000);

function change() {
    elem.innerHTML = text[counter];
    counter++;
    if (counter >= text.length) {
        counter = 0;
        // clearInterval(inst); // uncomment this if you want to stop refreshing after one cycle
    }
}