// Join form: no partner field when the player is looking for a partner (service 3)
const serviceSelect = document.getElementById("service_id");
const partnerInput = document.querySelector("#join-form input[name=partner]");
if (serviceSelect && partnerInput) {
  const partnerGroup = partnerInput.closest(".mb-3");
  const matchHint = document.getElementById("match-hint");
  const syncPartner = () => {
    const lookingForPartner = serviceSelect.value === "3";
    partnerGroup.hidden = lookingForPartner;
    partnerInput.disabled = lookingForPartner;
    if (lookingForPartner) partnerInput.value = "";
    if (matchHint) matchHint.hidden = !lookingForPartner;
  };
  serviceSelect.addEventListener("change", syncPartner);
  syncPartner();
}

// Stop double joining: disable the button once the form is submitted
const joinForm = document.getElementById("join-form");
if (joinForm) {
  joinForm.addEventListener("submit", () => {
    const button = joinForm.querySelector("button[type=submit]");
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });
}