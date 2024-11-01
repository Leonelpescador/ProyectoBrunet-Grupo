document.addEventListener('DOMContentLoaded', function () {
    const mesas = document.querySelectorAll('.mesa');

    mesas.forEach(mesa => {
        mesa.addEventListener('click', function (event) {
            event.stopPropagation();
            closeAllMenus();

            const menu = mesa.querySelector('.menu-desplegable');
            if (menu) {
                menu.style.display = 'block';
            }
        });
    });

    document.addEventListener('click', function () {
        closeAllMenus();
    });

    function closeAllMenus() {
        const menus = document.querySelectorAll('.menu-desplegable');
        menus.forEach(menu => {
            menu.style.display = 'none';
        });
    }
});

