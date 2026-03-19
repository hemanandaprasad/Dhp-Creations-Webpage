const form = document.getElementById("form");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
        name: form.name.value,
        age: form.age.value,
        location: form.location.value,
        role: form.role.value,
        skills: form.skills.value,
        email: form.email.value,
        phone: form.phone.value,
        portfolio: form.portfolio.value
    };

    try {
        const response = await fetch("https://dhp-creations-webpage.onrender.com/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        alert(data.message);
        form.reset();
    } catch (err) {
        console.error(err);
        alert("Failed to submit. Please try again.");
    }
});