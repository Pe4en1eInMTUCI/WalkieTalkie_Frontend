
function login() {

    let phone = document.getElementById('phone').value
    let password = document.getElementById('password').value

    const requestOptions = {
        method: 'POST',
        body: {
            "phone": phone,
            "password": password
        }
    };

    fetch('http://127.0.0.1:1232/api/login', requestOptions)
        .then(response => response.json())
        .then(data => console.log(data) );
}