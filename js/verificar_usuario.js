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
      
      // Si la respuesta es exitosa (código 200), redirigir a trading.html
      window.location.href = 'trading.html';
      
  } catch (error) {
      // Capturar y manejar errores de la API
      document.getElementById('result').textContent = error.message;
  }
}