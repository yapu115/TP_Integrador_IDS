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