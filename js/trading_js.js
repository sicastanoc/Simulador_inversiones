// Función para obtener y mostrar los precios de las acciones
async function mostrarPrecios(accion_id,id_precio_accion) {
    const response = await fetch(`http://127.0.0.1:8000/acciones/${accion_id}`); // Reemplaza {accion_id} con el ID de la acción específica
    const data = await response.json();

    const preciosContainer = document.getElementById(`${id_precio_accion}`);
    preciosContainer.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevos datos

    data.forEach(precio => {
        const precioHTML = `
            <div class="precio-item">
                <h5>${precio.nombre_accion} (${precio.nombre_abreviado}) </h5>
                <p>Precio: ${precio.precio}</p>
            </div>
        `;
        preciosContainer.innerHTML += precioHTML;
    });
}

// Función para obtener y mostrar los precios de las acciones
function cerrarSesion() {
    var logoutBtn = document.getElementById('logoutBtn');
    logoutBtn.addEventListener('click', function () {
        window.location.href = 'index.html'; // Redireccionar a la página de inicio
    });
    document.addEventListener('DOMContentLoaded', function() {
        cerrarSesion();
    });
}
