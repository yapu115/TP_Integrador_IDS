const btnGerarQr =document.getElementById("btn-generar-qr");
const qrImagen = document.getElementById("qr-imagen");
const qrMensaje = document.getElementById("qr-mensaje");

btnGerarQr.addEventListener("click", async () => {
   try {
    qrMensaje.textContent = "Generando QR..";
    
    const token = localStorage.getItem("token");

    const respuesta = await fetch("/http://127.0.0.1:5000/asistencia/qr", { 
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            id_alumno: 1,
            fecha: "2026-05-27"
        })
    });

    const datos = await respuesta.json();

    if (!respuesta.ok || datos.error) {
        qrMensaje.textContent = datos.mensaje || "No se pudo generar el QR";
        return; 
    }

        qrImagen.src = datos.qr_base64;
        qrImagen.hidden = false;
        qrMensaje.textContent = "QR generado correctamente";

    } catch (error){
        qrMensaje.textContent = "Ocurrio un error al generar el QR";
        console.error(error);
    }

});

document.addEventListener("DOMContentLoaded", function () {
    const botonesDetalle = document.querySelectorAll(".btn-ver-detalle");
    const modal = document.getElementById("modal-detalle");
    const btnCerrar = document.getElementById("cerrar-modal-detalle");

    const detalleLegajo = document.getElementById("detalle-legajo");
    const detalleNombre = document.getElementById("detalle-nombre");
    const detalleEmail = document.getElementById("detalle-email");
    const detalleEstado = document.getElementById("detalle-estado");
    const detalleCondicion = document.getElementById("detalle-condicion");
    const detalleObservacion = document.getElementById("detalle-observacion-texto");

    botonesDetalle.forEach(function (boton) {
        boton.addEventListener("click", function () {
            const legajo = boton.dataset.legajo || "Sin dato";
            const nombre = boton.dataset.nombre || "Sin dato";
            const email = boton.dataset.email || "Sin dato";
            const estado = boton.dataset.estado || "Pendiente";
            const condicion = boton.dataset.condicion || "Sin definir";

            detalleLegajo.textContent = legajo;
            detalleNombre.textContent = nombre;
            detalleEmail.textContent = email;
            detalleEstado.textContent = estado;
            detalleCondicion.textContent = condicion;

            if (condicion === "Sin definir") {
                detalleObservacion.textContent = "Todavía no hay suficientes clases registradas para calcular la regularidad final.";
            } else {
                detalleObservacion.textContent = "La condición fue calculada según las asistencias registradas del alumno.";
            }

            modal.hidden = false;
            modal.classList.add("is-open");
        });
    });

    if (btnCerrar) {
        btnCerrar.addEventListener("click", function () {
            modal.hidden = true;
        });
    }

    if (modal) {
        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.hidden = true;
            }
        });
    }

    function cerrarDetalleAlumno() {
       const modal = document.getElementById("modal-detalle");
       modal.classList.remove("is-open");
       modal.hidden = true;
    }

    document.addEventListener("DOMContentLoaded", function () {
        const modal = document.getElementById("modal-detalle");
    
        if (modal) {
            modal.classList.remove("is-open");
            modal.hidden = true;
        }
    });

});