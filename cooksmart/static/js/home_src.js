document.addEventListener("DOMContentLoaded", function() {
    if(document.getElementById('welcome')){
        document.getElementById('welcome').textContent = welcome[Math.floor(Math.random() * welcome.length)];
    }
    
    if(window.loggedIn){
        document.getElementById('loginBtn').textContent = window.lastName;
    }
});

function checkInput() {
    const input = document.getElementById("user-input");
    const btn = document.getElementById("submit-btn");
    if (input.value.trim().length > 0) {
        btn.style.display = "inline-block";
    } else {
        btn.style.display = "none";
    }
}

function handleLogin() {
    const btn = document.getElementById('loginBtn');
    if (!window.loggedIn) {
        window.location.href = "/login";
    } else {
        if (confirm('Bạn có chắc chắn muốn đăng xuất ?')) {
            document.getElementById("logoutForm").submit()
        }
    }
}