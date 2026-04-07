// Espera carregar
document.addEventListener("DOMContentLoaded", function () {

    const items = document.querySelectorAll(".menu-item");

    items.forEach(item => {

        item.addEventListener("click", function (e) {

            e.stopPropagation();

            // Fecha outros
            items.forEach(i => {
                if (i !== this) i.classList.remove("open");
            });

            // Alterna
            this.classList.toggle("open");
        });
    });

    // Clique fora fecha tudo
    document.addEventListener("click", function () {
        items.forEach(item => item.classList.remove("open"));
    });

});


// MENU MOBILE
function toggleMenu() {
    document.getElementById("menu").classList.toggle("active");
}


// VOLTAR AO TOPO
function scrollTopo() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}
