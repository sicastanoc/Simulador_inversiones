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

function nombreUsuario(){
    // Función para obtener el valor del parámetro de consulta 'username' de la URL
    function getParameterByName(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    // Obtener el nombre de usuario de la URL
    const username = getParameterByName('username');

    // Mostrar el mensaje de bienvenida
    document.getElementById('nombreUsuarioActivo').textContent = `${username}`;
}

async function comprarAccion() {        
    // Obtiene el valor del input
    var nombreUsuario = document.getElementById('nombreUsuarioActivo').value;
    var cantidadAcciones = document.getElementById('cantidadAcciones').value;
    var tipo_transaccion = 'Compra';
    var nombre_abreviado = document.getElementById('acciones').value;

    // Prepara el cuerpo de la solicitud con el texto extraído
    var data = {
        nombre_usuario: nombreUsuario,
        accion_id: nombre_abreviado,
        tipo_transaccion: tipo_transaccion,
        cantidad: cantidadAcciones
    };

    // Envía la solicitud POST a la API usando Fetch
    fetch('http://127.0.0.1:8000/transactions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                throw new Error('Bad Request');
            } else {
                throw new Error('Network response was not ok');
            }
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        document.getElementById('result').innerText = JSON.stringify(data, null, 2);
        alert('Transaccion creada correctamente');
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error: ' + error;
        if (error.message === 'Bad Request') {
            alert('Fallo al crear transaccion');
        } else {
            alert('Fallo al crear transaccion' + error.message);
        }
    });
}

async function venderAccion() {        
    // Obtiene el valor del input
    var nombreUsuario = document.getElementById('nombreUsuarioActivo').value;
    var cantidadAcciones = document.getElementById('cantidadAcciones').value;
    var tipo_transaccion = 'Venta';
    var nombre_abreviado = document.getElementById('acciones').value;

    // Prepara el cuerpo de la solicitud con el texto extraído
    var data = {
        nombre_usuario: nombreUsuario,
        accion_id: nombre_abreviado,
        tipo_transaccion: tipo_transaccion,
        cantidad: cantidadAcciones
    };

    // Envía la solicitud POST a la API usando Fetch
    fetch('http://127.0.0.1:8000/transactions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                throw new Error('Bad Request');
            } else {
                throw new Error('Network response was not ok');
            }
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        document.getElementById('result').innerText = JSON.stringify(data, null, 2);
        alert('Transaccion creada correctamente');
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error: ' + error;
        if (error.message === 'Bad Request') {
            alert('Fallo al crear transaccion');
        } else {
            alert('Fallo al crear transaccion' + error.message);
        }
    });
}
