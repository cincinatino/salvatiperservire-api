document.addEventListener("DOMContentLoaded", () => {
    const API_BASE = ""; // Percorso relativo per chiamare direttamente il backend FastAPI

    // Elementi DOM
    const authSection = document.getElementById("auth-section");
    const profileSection = document.getElementById("profile-section");
    const navUserInfo = document.getElementById("nav-user-info");
    const userEmailDisplay = document.getElementById("user-email-display");
    const alertContainer = document.getElementById("alert-container");

    // Inizializzazione: Controlla se c'è un Token in localStorage
    const token = localStorage.getItem("jwt_token");
    if (token) {
        caricaProfiloUtente();
    }

    // --- UTILITY: Gestione Alert ---
    function showAlert(message, type = "success") {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show shadow-sm" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }

    // --- FASE 1: REGISTRAZIONE ---
    // document.getElementById("form-register").addEventListener("submit", async (e) => {
    //     e.preventDefault();
    document.getElementById("form-register").addEventListener("submit", async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector("button[type='submit']");
        submitBtn.disabled = true;
        const payload = {
            nome: document.getElementById("reg-nome").value,
            cognome: document.getElementById("reg-cognome").value,
            email: document.getElementById("reg-email").value,
            password: document.getElementById("reg-password").value,
            citta: document.getElementById("reg-citta").value || null,
            chiesa: document.getElementById("reg-chiesa").value || null
        };

        try {
            const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || "Errore durante la registrazione");

            showAlert("Registrazione avvenuta con successo! Ora puoi effettuare l'accesso.", "success");
            // Passa alla scheda Login
            const loginTab = new bootstrap.Tab(document.getElementById("login-tab"));
            loginTab.show();
        } catch (err) {
            showAlert(err.message, "danger");
        }
    });

    // --- FASE 1: LOGIN ---
    document.getElementById("form-login").addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new URLSearchParams();
        formData.append("username", document.getElementById("login-email").value);
        formData.append("password", document.getElementById("login-password").value);

        try {
            const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formData
            });
            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || "Credenziali errate");

            // Salva il Token JWT
            localStorage.setItem("jwt_token", data.access_token);
            showAlert("Login effettuato con successo!", "success");
            caricaProfiloUtente();
        } catch (err) {
            showAlert(err.message, "danger");
        }
    });

    // --- FASE 2: CARICAMENTO DATI PROFILO ---
    async function caricaProfiloUtente() {
        const currentToken = localStorage.getItem("jwt_token");
        try {
            const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
                headers: { "Authorization": `Bearer ${currentToken}` }
            });

            if (!res.ok) {
                logout();
                return;
            }

            const user = await res.json();

            // Aggiorna Interfaccia
            authSection.classList.add("d-none");
            profileSection.classList.remove("d-none");
            navUserInfo.classList.remove("d-none");
            userEmailDisplay.textContent = user.email;

            // Compila i campi del profilo
            document.getElementById("prof-nome").value = user.nome || "";
            document.getElementById("prof-cognome").value = user.cognome || "";
            document.getElementById("prof-cf").value = user.codice_fiscale || "";
            document.getElementById("prof-telefono").value = user.telefono || "";
            document.getElementById("prof-citta").value = user.citta || "";
            document.getElementById("prof-chiesa").value = user.chiesa || "";

            // Badge e Foto
            const badge = document.getElementById("badge-stato-profilo");
            if (user.profilo_completato) {
                badge.className = "badge bg-success px-3 py-2 rounded-pill";
                badge.textContent = "Profilo Completato";
            } else {
                badge.className = "badge bg-warning text-dark px-3 py-2 rounded-pill";
                badge.textContent = "Profilo Incompleto";
            }

            if (user.foto_tessera_url) {
                document.getElementById("img-preview").src = user.foto_tessera_url;
            }

        } catch (err) {
            logout();
        }
    }

    // Preview locale dell'immagine prima del salvataggio
    document.getElementById("foto_tessera").addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            document.getElementById("img-preview").src = URL.createObjectURL(file);
        }
    });

    // --- FASE 2: SALVATAGGIO PROFILO (Form Data + Upload Foto) ---
    document.getElementById("form-profile").addEventListener("submit", async (e) => {
        e.preventDefault();
        const currentToken = localStorage.getItem("jwt_token");

        const formData = new FormData();
        formData.append("nome", document.getElementById("prof-nome").value);
        formData.append("cognome", document.getElementById("prof-cognome").value);
        formData.append("codice_fiscale", document.getElementById("prof-cf").value);
        formData.append("telefono", document.getElementById("prof-telefono").value);
        formData.append("citta", document.getElementById("prof-citta").value);
        formData.append("chiesa", document.getElementById("prof-chiesa").value);

        const fotoInput = document.getElementById("foto_tessera");
        if (fotoInput.files.length > 0) {
            formData.append("foto_tessera", fotoInput.files[0]);
        }

        try {
            const res = await fetch(`${API_BASE}/api/v1/users/me/profile`, {
                method: "PUT",
                headers: { "Authorization": `Bearer ${currentToken}` },
                body: formData // Note: NON impostiamo 'Content-Type', lo fa il browser in automatico per il multipart
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Errore durante l'aggiornamento del profilo");

            showAlert("Profilo aggiornato con successo!", "success");
            caricaProfiloUtente();
        } catch (err) {
            showAlert(err.message, "danger");
        }
    });

    // --- LOGOUT ---
    function logout() {
        localStorage.removeItem("jwt_token");
        authSection.classList.remove("d-none");
        profileSection.classList.add("d-none");
        navUserInfo.classList.add("d-none");
        showAlert("Disconnessione effettuata.", "info");
    }

    document.getElementById("btn-logout").addEventListener("click", logout);
});

// Aggiungi questo in fondo a app/static/js/app.js per forzare il cambio tab
document.addEventListener("DOMContentLoaded", () => {
    const registerTabBtn = document.getElementById("register-tab");
    const loginTabBtn = document.getElementById("login-tab");
    const registerPanel = document.getElementById("register-panel");
    const loginPanel = document.getElementById("login-panel");

    if (registerTabBtn && loginTabBtn) {
        registerTabBtn.addEventListener("click", () => {
            registerTabBtn.classList.add("active");
            loginTabBtn.classList.remove("active");
            registerPanel.classList.add("show", "active");
            loginPanel.classList.remove("show", "active");
        });

        loginTabBtn.addEventListener("click", () => {
            loginTabBtn.classList.add("active");
            registerTabBtn.classList.remove("active");
            loginPanel.classList.add("show", "active");
            registerPanel.classList.remove("show", "active");
        });
    }
});