function mostrarModalAlumnos(id){
    const modal = document.getElementById(id);

    modal.classList.add('modal--open');
    modal.setAttribute('aria-hidden', 'false');
}

function ocultarModalAlumnos(id){
    const modal = document.getElementById(id);

    modal.classList.remove('modal--open');
    modal.setAttribute('aria-hidden', 'true');
}

function mostrarInfoAlumnos(nombre, legajo, email){
    document.getElementById('detalleAlumnoNombre').textContent = nombre;
    document.getElementById('detalleAlumnoLegajo').textContent = legajo;
    document.getElementById('detalleAlumnoEmail').textContent = email;

    mostrarModalAlumnos('modalAlumnos');
}

window.addEventListener('click', function (event) {
    document.querySelectorAll('.modal--open').forEach(m => {
        if (event.target === m) ocultarModalAlumnos(m.id);
    });
});