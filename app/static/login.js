const form = document.getElementById("loginForm");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const res = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    document.getElementById("response").innerText = result.message || result.error;

    // ✅ Redirect after login
    if (res.status === 200) {
    window.location.href = result.role === "admin" ? "/admin" : "/";
}
});