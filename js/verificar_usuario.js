async function enviarDatos() {
    const nombreUsuario = document.getElementById('nombreUsuario').value;
    const url = `http://127.0.0.1:8000/users/${nombreUsuario}`;
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        // Si la respuesta no es exitosa (código de estado no está en el rango 200-299)
        if (response.status === 404) {
          throw new Error('Usuario no encontrado');
        } else {
          throw new Error('Error en la solicitud: ' + response.status);
        }
      }
      
      // Redirigir a la página trading.html solo si la respuesta es exitosa
      window.location.href = 'trading.html';
      
    } catch (error) {
      // Manejar errores
      if (error.message.includes('404')) {
        document.getElementById('result').textContent = 'Usuario no encontrado';
        // No redirigir automáticamente en caso de error 404
      } else {
        document.getElementById('result').textContent = error.message;
      }
    }
  }