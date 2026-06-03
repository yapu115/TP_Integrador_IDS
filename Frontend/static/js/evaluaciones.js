//Funcion que cambia de estado el boton eliminar y cambia la visibilidad de .form-delete,
// que contiene un boton para eliminar 
document.addEventListener('DOMContentLoaded', () => {
    const btnEliminar = document.querySelector('.btn.btn--delete');
    
    let EdicionActiva = false;
    
    if (btnEliminar) {
        btnEliminar.addEventListener('click', function(e) {
            e.preventDefault();
            
            const formulariosEliminar = document.querySelectorAll('.form-delete');
            
            EdicionActiva = !EdicionActiva;
            
            if (EdicionActiva) {
                this.innerText = "Finalizar Edición";
                
                formulariosEliminar.forEach(form => {
                    form.style.display = "block";
                    form.style.opacity = "1";
                    form.style.visibility = "visible";
                    
                });
                
            } else {
                this.innerText = "Eliminar actividad";
                
                formulariosEliminar.forEach(form => {
                    form.style.visibility = "hidden";
                    form.style.display = "none";
                });
            }
        });
    }

    //Funcion que cambia de estado el boton modificar y abilita la visibilidad de .link-edit
    // que muestra un lapiz que redirige hacia otro endpoint para editar
    const btnEditar = document.querySelector('.btn.btn--edit');
    let EditarActivo = false;

    if (btnEditar) {
        btnEditar.addEventListener('click', function(e) {
            e.preventDefault();
            const linksEditar = document.querySelectorAll('.link-edit');
            EditarActivo = !EditarActivo;

            if (EditarActivo) {
                this.innerText = "Finalizar Cambios";

                linksEditar.forEach(link => {
                    link.style.display = "inline-block";
                    link.style.opacity = "1";
                    link.style.visibility = "visible";
                });
            } else {
                this.innerText = "Modificar actividad";

                linksEditar.forEach(link => {
                    link.style.opacity = "0";
                    link.style.visibility = "hidden";
                    link.style.display = "none";
                });
            }
        });
    }
});