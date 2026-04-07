// mapa simples
const SIMULACOES = {
    queda: {
        titulo: "Queda Livre",
        arquivo: "queda.js"
    },
    molas: {
        titulo: "Sistema de Molas",
        arquivo: "molas.js"
    },
    orbitas: {
        titulo: "Órbitas Planetárias",
        arquivo: "orbitas.js"
    }
};


// pega simulação atual
const sim = SIMULACOES[SIMULACAO];

if (sim) {

    // muda título
    document.getElementById("titulo").innerText = sim.titulo;

    // carrega script da simulação
    let script = document.createElement("script");
    script.src = "/static/sim/" + sim.arquivo;

    document.body.appendChild(script);

} else {
    document.getElementById("titulo").innerText = "Simulação não encontrada";
}

// ===== GERAR DROPDOWN =====
const dropdown = document.getElementById("dropdown-simulacoes");

if (dropdown) {
    for (let key in SIMULACOES) {

        let a = document.createElement("a");
        a.href = "/simulacao/" + key;
        a.innerText = SIMULACOES[key].titulo;

        dropdown.appendChild(a);
    }
}
