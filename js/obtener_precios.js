async function fetchAccion(accionId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/acciones/${accionId}`);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';
        data.forEach(item => {
            const p = document.createElement('p');
            p.textContent = `Acción: ${item.nombre_accion} (${item.nombre_abreviado}), Fecha: ${new Date(item.fecha).toLocaleDateString()}, Precio: $${item.precio}`;
            resultDiv.appendChild(p);
        });
    } catch (error) {
        console.error('Hubo un problema con la petición Fetch:', error);
    }
}

window.onload = function() {
    // Reemplaza con el ID de la acción que deseas obtener
    const accionId = 1;
    fetchAccion(accionId);
};