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
                const platoPrecio = parseFloat(this.getAttribute('data-precio')); // Parsear el precio correctamente
                const platoNombre = this.closest('.card').querySelector('.card-title').innerText;

                // Verificar si el plato ya existe en el pedido
                const itemExistente = pedido.find(p => p.plato_id == platoId);
                if (itemExistente) {
                    itemExistente.cantidad += 1;
                } else {
                    pedido.push({ plato_id: platoId, nombre: platoNombre, cantidad: 1, precio_unitario: platoPrecio });
                }

                renderPedido();
            });
        });
    }

    // Añadir controladores de eventos a los platos al cargar la página
    addEventListenersToPlatos();

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
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ platos: pedido })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Pedido creado con éxito');
                  window.location.href = '/';  // Redirigir después de crear el pedido
              } else {
                  alert('Hubo un error al crear el pedido');
              }
          }).catch(error => console.error('Error:', error));
    });

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
                    // Si la cantidad es 1 y el usuario hace clic en restar, eliminamos el plato del pedido
                    pedido = pedido.filter(p => p.plato_id !== plato.plato_id);
                    renderPedido();
                    alert(`Se sacó el plato ${plato.nombre} del pedido.`);
                }
            });
        });
    }

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
