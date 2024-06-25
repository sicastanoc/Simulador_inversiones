// Función para enviar datos al servidor
async function enviarDatos() {
  event.preventDefault(); // Prevenir el envío del formulario por defecto
  
  const nombreUsuario = document.getElementById('nombreUsuario').value;
  const url = `http://127.0.0.1:8000/users/${nombreUsuario}`; // URL de la API
  
  try {
      const response = await fetch(url);
      
      if (!response.ok) {
          throw new Error('Usuario no encontrado');
      }
      const username = document.getElementById("nombreUsuario").value;

      // Redireccionar a trading.html con el nombre de usuario como parámetro de consulta
      window.location.href = `trading.html?username=${encodeURIComponent(username)}`;
      
  } catch (error) {
      // Capturar y manejar errores de la API
      document.getElementById('result').textContent = error.message;
  }

}