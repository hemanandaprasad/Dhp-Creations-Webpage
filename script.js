const form = document.getElementById("form");
const dataDiv = document.getElementById("data");
const msg = document.getElementById("message");

const API = "http://127.0.0.1:5000";

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: form.name.value,
        age: form.age.value,
        location: form.location.value,
        role: form.role.value,
        skills: form.skills.value,
        email: form.email.value,
        phone: form.phone.value,
        portfolio: form.portfolio.value
    };

    const res = await fetch(API + "/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    msg.innerText = "✅ Application Submitted Successfully!";
    form.reset();

    loadData();
});