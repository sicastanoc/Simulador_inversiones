// Función para obtener el valor del parámetro de consulta 'username' de la URL
function getParameterByName(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Obtener el nombre de usuario de la URL
const username = getParameterByName('username');

// Mostrar el mensaje de bienvenida
document.getElementById('nombreUsuarioActivo').textContent = `${username}`;