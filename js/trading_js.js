// Función para obtener y mostrar los precios de las acciones
async function mostrarPrecios(accion_id,id_precio_accion) {
    const response = await fetch(`http://127.0.0.1:8000/acciones/${accion_id}`); // Reemplaza {accion_id} con el ID de la acción específica
    const data = await response.json();
    console.log(data)

    const preciosContainer = document.getElementById(`${id_precio_accion}`);
    preciosContainer.innerHTML = ''; // Limpiar el contenedor antes de agregar nuevos datos

    const precioHTML = `
    <div class="precio-item">
        <h5>${data.nombre_accion} (${data.nombre_abreviado}) </h5>
        <p>Precio: ${data.precio}</p>
    </div>`;
    preciosContainer.innerHTML += precioHTML;
    
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

function getParameterByName(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function nombreUsuario(){

    // Obtener el nombre de usuario de la URL
    const username = getParameterByName('username');

    // Mostrar el mensaje de bienvenida
    document.getElementById('nombreUsuarioActivo').textContent = `${username}`;
}

// Función para obtener y mostrar los precios de las acciones
async function obtenerBalance() {
    const username = getParameterByName('username');
    console.log(username)

    try {
        const response = await fetch(`http://127.0.0.1:8000/users/${username}`);
        if (!response.ok) {
            throw new Error('Error al obtener el balance del usuario');
        }
        
        const data = await response.json();
        console.log(data)

        // Mostrar el balance del usuario
        document.getElementById('balance').textContent = `$${data.balance}`;
        console.log('Balance:', data.balance);

    } catch (error) {
        console.error('Error:', error.message);
        // Manejar el error, por ejemplo, mostrando un mensaje al usuario
        document.getElementById('balance').textContent = 'Error al obtener el balance';
    }
}



async function comprarAccion() {        
    // Obtiene el valor del input
    const nombreUsuario = getParameterByName('username');
    console.log(nombreUsuario)
    var cantidadAcciones = document.getElementById('numero').value;
    console.log(cantidadAcciones)
    var tipo_transaccion = 'Compra';
    var nombre_abreviado = document.getElementById('acciones').value;
    console.log(nombre_abreviado)
    var precio = 0;

    // Prepara el cuerpo de la solicitud con el texto extraído
    var data = {
        nombre_usuario: nombreUsuario,
        nombre_abreviado: nombre_abreviado,
        tipo_transaccion: tipo_transaccion,
        cantidad: cantidadAcciones,
        precio: precio
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
                throw new Error('Balance insuficiente para realizar la compra');
            } else if (response.status === 422) {
                throw new Error('Rellene correctamente todos los campos');
            } else if (response.status === 403) {
                throw new Error('Forbidden');
            } else if (response.status === 404) {
                throw new Error('Not Found');
            } else if (response.status === 500) {
                throw new Error('Internal Server Error');
            } else {
                throw new Error('Network response was not ok');
            }
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Transaccion creada correctamente');
    })
    .catch((error) => {
        console.error('Error:', error);
        if (error.message === 'Bad Request') {
            alert('Fallo al crear transaccion ');
        } else {
            alert('Fallo al crear transaccion ' + error.message);
        }
    });
}

async function venderAccion() {        
    // Obtiene el valor del input
    const nombreUsuario = getParameterByName('username');
    console.log(nombreUsuario)
    var cantidadAcciones = document.getElementById('numero').value;
    console.log(cantidadAcciones)
    var tipo_transaccion = 'Venta';
    var nombre_abreviado = document.getElementById('acciones').value;
    console.log(nombre_abreviado)
    var precio = 0;

    // Prepara el cuerpo de la solicitud con el texto extraído
    var data = {
        nombre_usuario: nombreUsuario,
        nombre_abreviado: nombre_abreviado,
        tipo_transaccion: tipo_transaccion,
        cantidad: cantidadAcciones,
        precio: precio
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
                throw new Error('Cantidad insuficiente de acciones para vender');
            } else if (response.status === 422) {
                throw new Error(' Rellene correctamente todos los campos');
            } else if (response.status === 403) {
                throw new Error('Forbidden');
            } else if (response.status === 404) {
                throw new Error('Not Found');
            } else if (response.status === 500) {
                throw new Error('Internal Server Error');
            } else {
                throw new Error('Network response was not ok');
            }
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Transaccion creada correctamente');
    })
    .catch((error) => {
        if (error.message === 'Bad Request') {
            alert('Fallo al crear transaccion ');
        } else {
            alert('Fallo al crear transaccion ' + error.message);
        }
    });
}
