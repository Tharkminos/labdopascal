document.addEventListener(
    "click",
    function(e){

        if(
            !e.target.classList.contains(
                "alternativa"
            )
        ){
            return;
        }

        let correta =
            e.target.dataset.correta;

        let feedback =
            e.target
            .closest(".checkpoint")
            .querySelector(
                ".checkpoint-feedback"
            );

        if(correta === "1"){

            feedback.innerHTML =
                "✅ Correto";

        }else{

            feedback.innerHTML =
                "❌ Tente novamente";

        }

    }
);
