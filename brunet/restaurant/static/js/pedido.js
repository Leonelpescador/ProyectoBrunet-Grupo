document.addEventListener('DOMContentLoaded', function() {
    const resumenPedido = document.getElementById('resumenPedido');
    const categoriaFiltro = document.getElementById('categoriaFiltro');
    let pedido = [];

    // Filtrar platos por categoría
    categoriaFiltro.addEventListener('change', function() {
        const categoriaId = this.value;
        fetch(`/filtrar_platos_por_categoria/?categoria_id=${categoriaId}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('platosContainer').innerHTML = html;
            addEventListenersToPlatos(); // Volvemos a asignar los eventos
        });
    });

    // Añadir evento a los botones de "Agregar al Pedido"
    function addEventListenersToPlatos() {
        document.querySelectorAll('.agregar-pedido').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const platoId = this.getAttribute('data-id');
                const platoPrecio = parseFloat(this.getAttribute('data-precio'));
                const platoNombre = this.closest('.card').querySelector('.card-title').innerText;

                // Verificar si el plato ya existe en el pedido
                const itemExistente = pedido.find(p => p.plato_id == platoId);
                if (itemExistente) {
                    itemExistente.cantidad += 1;
                } else {
                    pedido.push({ plato_id: platoId, nombre: platoNombre, cantidad: 1, precio_unitario: platoPrecio });
                }

                renderPedido();

                // Mostrar notificación debajo del botón
                const notificacion = this.closest('.card-body').querySelector('.notificacion-agregado');
                mostrarNotificacion(notificacion);
            });
        });
    }

    // Añadir controladores de eventos a los platos al cargar la página
    addEventListenersToPlatos();

    // Función para mostrar la notificación
    function mostrarNotificacion(element) {
        element.style.display = 'inline';  // Mostrar la notificación

        // Desaparecer la notificación después de 3 segundos
        setTimeout(() => {
            element.style.display = 'none';
        }, 3000);
    }

    // Función para mostrar el resumen del pedido y ajustar cantidades
    function renderPedido() {
        resumenPedido.innerHTML = '';
        pedido.forEach(plato => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${plato.nombre} 
                <button class="btn-cantidad btn-restar">➖</button> 
                ${plato.cantidad} unidades 
                <button class="btn-cantidad btn-sumar">➕</button> 
                $${(plato.precio_unitario * plato.cantidad).toFixed(2)}
            `;
            resumenPedido.appendChild(li);

            // Botones para sumar y restar
            li.querySelector('.btn-sumar').addEventListener('click', () => {
                plato.cantidad += 1;
                renderPedido();
            });

            li.querySelector('.btn-restar').addEventListener('click', () => {
                if (plato.cantidad > 1) {
                    plato.cantidad -= 1;
                    renderPedido();
                } else {
                    pedido = pedido.filter(p => p.plato_id !== plato.plato_id);
                    renderPedido();
                }
            });
        });
    }

    // Manejo del envío del formulario
    document.getElementById('pedidoForm').addEventListener('submit', function(e) {
        e.preventDefault();  // Evitar el envío normal del formulario

        if (pedido.length === 0) {
            alert("Por favor, agrega al menos un plato al pedido.");
            return;
        }

        // Enviar los datos del pedido al servidor
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Incluye el CSRF token
            },
            body: JSON.stringify({ platos: pedido })  // Enviar datos
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Pedido creado con éxito. Número de comanda: ' + data.numero_comanda);
                  window.location.href = '/';  // Redirigir después de crear el pedido
              } else {
                  alert('Hubo un error al crear el pedido');
              }
          }).catch(error => console.error('Error:', error));
    });

    // Obtener el CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
