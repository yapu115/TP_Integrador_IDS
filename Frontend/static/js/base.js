//Funcion para activar la barra lateral del base.html
document.addEventListener('DOMContentLoaded', function() {
    
    const boton = document.querySelector('.topbar__menu-btn');
    const barraLateral = document.querySelector('.sidebar');

    if (boton && barraLateral) {
        boton.addEventListener('click', function() {
            barraLateral.classList.toggle('sidebar--active');
        });
        
    } else {
        console.log("No se encontró el botón o la barra lateral o ocurrio otro error");
    }
});