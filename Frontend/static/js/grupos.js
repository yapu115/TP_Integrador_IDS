function mostrarInfoAlumnos(){
    const infoAlumnos = document.getElementById("info-alumno-grupo");

    infoAlumnos.setAttribute('aria-hidden', 'false');
}

function ocultarInfoAlumnos(){
    const infoAlumnos = document.getElementById("info-alumno-grupo");

    infoAlumnos.setAttribute('aria-hidden', 'true');
}
