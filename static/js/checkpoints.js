let acertos = 0
let erros = 0

document
.querySelectorAll(".alternativa")
.forEach(botao => {

    botao.addEventListener(
        "click",
        () => {

            const checkpoint =
                botao.closest(
                    ".checkpoint"
                )

            if(
                checkpoint.dataset
                .concluido === "true"
            ){
                return
            }

            const correta =
                botao.dataset.correta
                === "1"

            const feedback =
                checkpoint.querySelector(
                    ".checkpoint-feedback"
                )

            if(correta){

                acertos++

                checkpoint.dataset
                .concluido = "true"

                feedback.innerHTML =
                    "✅ Correto"

                botao.classList.add(
                    "correta"
                )

            }else{

                erros++

                feedback.innerHTML =
                    "❌ Tente novamente"

                botao.classList.add(
                    "errada"
                )
            }

        }
    )

})

function etapaConcluida(){

    const checkpoints =
        etapas[etapaAtual]
        .querySelectorAll(
            ".checkpoint"
        )

    if(
        checkpoints.length === 0
    ){
        return true
    }

    return [...checkpoints].every(
        cp =>
        cp.dataset.concluido
        === "true"
    )

}
