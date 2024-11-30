const logout = document.getElementById("logout");

//evento de click para fazer logout
logout.addEventListener('click', (event) => {
    event.preventDefault()
    window.location.href = '/index';
});