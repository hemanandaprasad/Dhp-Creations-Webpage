const form = document.getElementById("form");
const messageEl = document.getElementById("message");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Gather form data
  const data = {
    name: form.name.value,
    age: form.age.value,
    location: form.location.value,
    role: form.role.value,
    skills: form.skills.value,
    email: form.email.value,
    phone: form.phone.value,
    portfolio: form.portfolio.value,
  };

  try {
    const response = await fetch("/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      // Success
      messageEl.style.color = "lightgreen";
      messageEl.textContent = result.message;
      form.reset();
    } else {
      // Error (like duplicate submission)
      messageEl.style.color = "red";
      messageEl.textContent = result.error || "Submission failed!";
    }
  } catch (err) {
    messageEl.style.color = "red";
    messageEl.textContent = "Server error. Please try again later.";
    console.error(err);
  }
});