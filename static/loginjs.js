const loginBtn = document.getElementById("loginBtn");
const authContainer = document.getElementById("authContainer");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const tabLogin = document.getElementById("tabLogin");
const tabSignup = document.getElementById("tabSignup");
const switchToSignup = document.getElementById("switchToSignup");
const mainContent = document.getElementById("mainContent");
const authWrapper = document.getElementById("authButtonWrapper");
const profileDropdown = document.getElementById("profileDropdown");
let redirectAfterLogin = false;

function showLogin() {
    authContainer.classList.remove("hidden");
    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");
    tabLogin.classList.add("active");
    tabSignup.classList.remove("active");
}

function showSignup() {
    signupForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    tabSignup.classList.add("active");
    tabLogin.classList.remove("active");
}

loginBtn.addEventListener("click", showLogin);
tabLogin.addEventListener("click", showLogin);
tabSignup.addEventListener("click", showSignup);
switchToSignup.addEventListener("click", (e) => {
    e.preventDefault();
    showSignup();
});

// Sign Up Logic
signupForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("signupEmail").value;
    const user = {
        name: document.getElementById("signupName").value,
        profession: document.getElementById("signupProfession").value,
        email: email,
        password: document.getElementById("signupPassword").value,
        avatar: getGravatarUrl(email)
    };

    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("loggedIn", "true");
    updateUIAfterLogin(user);
});

// Login Logic
loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const savedUser = JSON.parse(localStorage.getItem("user"));
    if (savedUser && savedUser.email === email && savedUser.password === password) {
        localStorage.setItem("loggedIn", "true");
        updateUIAfterLogin(savedUser);
    } else {
        alert("Invalid email or password");
    }
});

// Update UI after login/signup

function updateUIAfterLogin(user) {
    authContainer.classList.add("hidden");
    mainContent.classList.remove("hidden");

    const img = document.createElement("img");
    img.src = user.avatar;
    img.alt = "Profile";
    img.className = "profile-img";
    img.onclick = () => profileDropdown.classList.toggle("hidden");

    authWrapper.innerHTML = "";
    authWrapper.appendChild(img);

    if (redirectAfterLogin) {
        window.location.href = "dashboard.html";
    }
}


// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("loggedIn");
    location.reload();
});

// Check on load
window.onload = () => {
    const loggedIn = localStorage.getItem("loggedIn") === "true";
    const user = JSON.parse(localStorage.getItem("user"));
    if (loggedIn && user) {
        updateUIAfterLogin(user);
    }
};

function getGravatarUrl(email) {
    const trimmedEmail = email.trim().toLowerCase();
    const hash = md5(trimmedEmail);
    return `https://www.gravatar.com/avatar/${hash}?d=identicon`;
}

// Close auth popup
document.getElementById("closeAuth").addEventListener("click", () => {
    authContainer.classList.add("hidden");
});

// Show/hide password
document.querySelectorAll(".toggle-password").forEach(icon => {
  icon.addEventListener("click", () => {
    const input = document.getElementById(icon.dataset.target);
    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";
    icon.classList.toggle("fa-eye");
    icon.classList.toggle("fa-eye-slash");
  });
});

// jump to top for login 
const getStartedBtn = document.getElementById("getStartedBtn");

getStartedBtn.addEventListener("click", () => {
    const isLoggedIn = localStorage.getItem("loggedIn") === "true";
    if (isLoggedIn) {
        window.location.href = "dashboard.html";
    } else {
        redirectAfterLogin = true;
        showLogin();

        // Smooth scroll to top
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
});



// let redirectAfterLogin = false;

// getStartedBtn.addEventListener("click", () => {
//     const isLoggedIn = localStorage.getItem("loggedIn") === "true";
//     if (isLoggedIn) {
//         window.location.href = "dashboard.html";
//     } else {
//         redirectAfterLogin = true;
//         showLogin();
//     }
// });

// animation 
window.addEventListener('load', () => {
  const animatedElements = document.querySelectorAll('.animate-slide-up');
  animatedElements.forEach((el, index) => {
    setTimeout(() => {
      el.classList.add('active');
    }, 150 * index); // Stagger animations by 150ms each
  });
});

// Scroll-triggered animation
document.addEventListener("DOMContentLoaded", () => {
    const animatedItems = document.querySelectorAll(".animate-slide-up");

    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                    observer.unobserve(entry.target); // Animate once
                }
            });
        },
        { threshold: 0.15 }
    );

    animatedItems.forEach(item => observer.observe(item));
});


