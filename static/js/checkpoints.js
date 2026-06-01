document.addEventListener("click", (e) => {

    if (!e.target.classList.contains("alternativa")) {
        return;
    }

    const botao = e.target;

    const bloco = botao.closest(".checkpoint");

    const botoes = bloco.querySelectorAll(
        ".alternativa"
    );

    const feedback = bloco.querySelector(
        ".checkpoint-feedback"
    );

    botoes.forEach(b => {

        b.disabled = true;

        if (
            b.dataset.correta === "1"
        ) {
            b.classList.add(
                "correta"
            );
        }
    });

    if (
        botao.dataset.correta === "1"
    ) {

        botao.classList.add(
            "selecionada"
        );

        feedback.textContent =
            "✅ Resposta correta!";

    } else {

        botao.classList.add(
            "errada"
        );

        feedback.textContent =
            "❌ Resposta incorreta.";
    }
});
