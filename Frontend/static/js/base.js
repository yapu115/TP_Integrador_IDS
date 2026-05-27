//Espera a que todo el HTML de la página esté completamente cargado (js carga mas rapido que el html de la pagina)
document.addEventListener('DOMContentLoaded', function() {
    
    const boton = document.querySelector('.topbar__menu-btn');
    const barraLateral = document.querySelector('.sidebar');

    //Verificamos que ambos elementos existan en la página actual
    if (boton && barraLateral) {
        // Se espera a que el usuario haga click 
        boton.addEventListener('click', function() {
            // Alternamos la clase que estira la barra lateral
            barraLateral.classList.toggle('sidebar--active');
        });
        
    } else {
        console.log("No se encontró el botón o la barra lateral en esta página.");
    }
});