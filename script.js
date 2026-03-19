const form = document.getElementById('form');
const message = document.getElementById('message');

form.addEventListener('submit', async (e) => {
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
        const response = await fetch('https://dhp-creations-webpage.onrender.com/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
            message.textContent = "Application submitted successfully!";
            form.reset();
        } else {
            message.textContent = "Error: " + result.message;
        }
    } catch (err) {
        message.textContent = "Server error. Try again later.";
        console.error(err);
    }
});