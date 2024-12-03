// fetch('https://meu-app.herokuapp.com/organize', {
//     method: 'GET'
// })

// .then(response => response.json())
// .then(data => {
//     console.log(data);
// })
// .catch(error => {
//     console.error('Erro', error);
// });

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('login-form').addEventListener('submit', function(event){
        event.preventDefault();
    
        // dados do formulário
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
    
        // cria objetos com os dados
        const loginData = {
            email: email,
            senha: senha
        };
        
        //faz requisição  fetch para o servidor flask (login)
        fetch('https://meu-app.herokuapp.com/organize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData) //envia os dados em json 
        })
        .then(response => response.json()) //converte a resposta para json
        .then(data => {
            if(data.sucess) {
                //caso o login seja bem sucedido, redireciona para o dashboard
                window.location.href = '/dashboard';
            }else {
                //caso haja erro no login, exibe uma mensagem erro
                alert('Erro ao fazer o login:' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
        }); 
    });
})



// função para fazer uma requisição GET para a rota /organize
function organizeData() {
    fetch('https://meu-app.herokuapp.com/organize', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error', error);
    });
}

organizeData();