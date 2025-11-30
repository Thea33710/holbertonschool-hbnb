/*--------===> GESTION DU L'API <===------- */
const API_BASE_URL = 'http://localhost:5000/api/v1';
const API_LOGIN_ENDPOINT = `${API_BASE_URL}/auth/login`;

/*----===> Chargement de la page <===------ */
document.addEventListener('DOMContentLoaded', async () => {
    const currentPage = window.location.pathname.split('/').pop();

    /*---===> GESTION PAGE INDEX.HTML <===-----*/
    const priceFilter = document.getElementById('price-filter');
    
    if (currentPage === 'index.html') {
        console.log('Page index');
        checkAuthentication();
        loadPriceFilterOptions();
        fetchPlaces();
        
        if (priceFilter) {
            priceFilter.addEventListener('change', filterPlacesByPrice);
        }

        window.viewPlaceDetails = (placeId) => {
            window.location.href = `place.html?place_id=${encodeURIComponent(placeId)}`;
        };
    }

    /*--------===> GESTION PLACE.HTML <===------- */
    if (currentPage === 'place.html') {
        const placeId = new URLSearchParams(window.location.search).get('place_id');
        if (placeId) loadPlaceDetails(placeId);
    }

    /*--------===> GESTION DU LOGIN <===------- */
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        // Soumission du formulaire
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                alert('Merci de remplir tous les champs !');
                return;
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Merci d\'entrer une adresse email valide !');
                return;
            }
            
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Connexion en cours...';
            submitButton.disabled = true;

            try {
                const success = await loginUser(email, password);

                if (success) {
                    show('Connexion réussie! Redirection...');
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                }
            } catch (error) {
                console.error('Erreur lors de la connexion:', error);
                show('Une erreur est survenue. Veuillez réessayer.');
            } finally {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
            
        });
    }

    /*-----===> FORMULAIRE ADD REVIEW <===-----*/
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        const floating = document.createElement('div');
        floating.id = 'floating-confirmation';
        floating.textContent = "Votre avis a été ajouté.";
        floating.style.cssText = `
            position: fixed;
            top: 50px;
            right: 100px;
            background: #559c65ff;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            opacity: 0;
        `;
        document.body.appendChild(floating);

        const showMessage = () => {
            floating.style.opacity = '1';
            setTimeout(() => {
                floating.style.opacity = '0';
            }, 3000);
        };

        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            showMessage();
            reviewForm.reset();
        });
    }
});

/**
 * Redirige vers place.html et affiche les détails + reviews
 */
async function loadPlaceDetails(placeId) {
    const placeDetailsContainer = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews');
    const token = getCookie('token');

    if (!placeDetailsContainer || !reviewsContainer) return;

    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        });

        if (!response.ok) {
            placeDetailsContainer.innerHTML = `<p style="color:red;">Erreur : place non trouvée</p>`;
            return;
        }

        const place = await response.json();

        placeDetailsContainer.innerHTML = `
            <h2>${place.title || place.name}</h2>
            <p>${place.description}</p>
            <p><strong>Prix:</strong> ${place.price}€</p>
            <p><strong>Localisation:</strong> ${place.latitude}, ${place.longitude}</p>
        `;

         const reviewsResponse = await fetch(`${API_BASE_URL}/places/${placeId}/reviews/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        });

        if (!reviewsResponse.ok) {
            reviewsContainer.innerHTML = `<p style="color:red;">Impossible de récupérer les avis</p>`;
            return;
        }

        const reviews = await reviewsResponse.json();

        reviewsContainer.innerHTML = `<h3>Avis des utilisateurs</h3><ul id="reviews-list" style="padding-left:20px;"></ul>`;
        const reviewsList = document.getElementById('reviews-list');

        if (reviews.length === 0) {
            reviewsList.innerHTML = '<li>Aucun avis pour le moment.</li>';
        } else {
            reviews.forEach(async (r) => {
                const li = document.createElement('li');
                user_name = await getUserName(r.user_id);
                li.textContent = `${user_name} : ${r.comment || r.text}`;
                reviewsList.appendChild(li);
            });
        }
    } catch (error) {
        console.error('Erreur réseau: ', error);
        placeDetailsContainer.innerHTML = `<p style="color:red;">Impossible de récupérer les détails.</p>`;
    }
}

/*-===> Fonction pour récupérer le nom d'utilisateur <==-*/
async function getUserName(user_id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${user_id}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) return 'Utilisateur inconnu';
        const user = await response.json();
        return user.name || 'Utilisateur inconnu';
    } catch (err) {
        console.error('Erreur récupération nom utilisateur: ', err);
        return 'Utilisateur inconnu';
    }
}

/*-===> Fonction de la connexion à l'Api <==-*/
/**
 * Envoie les identifiants à l'API backend
 */
async function loginUser(email, password) {
    try {
        const response = await fetch(API_LOGIN_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (response.ok) {
            const data = await response.json();
            
            if (data.access_token) {
                saveTokenToCookie(data.access_token);
                return true;
            } else {
                console.error('Token manquant dans la réponse');
                show('Erreur serveur: token manquant');
                return false;
            }
        } else {
            let errorMessage = 'Email ou mot de passe incorrect';
            
            try {
                const errorData = await response.json();
                if (errorData.message) {
                    errorMessage = errorData.message;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                }
            } catch (e) {
                console.error('Impossible de parser le message d erreur JSON: ', e);
            }
            
            console.error('Connexion échouée: ', errorMessage);
            show(errorMessage);
            return false;
        }
    } catch (error) {
        console.error('Erreur réseau: ', error);        
        return false;
    }
}

/*===== GESTION DE LA PAGE INDEX =============*/
/**
 * Vérifie l'authentification et affiche/cache le bouton login
 */
function checkAuthentication() {
    const token = getCookie('token');
    const loginButton = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    
    if (loginButton) {
        if (token) {
            // Utilisateur connecté : cacher le bouton login
            if (loginButton) loginButton.style.display = 'none';
            if (logoutButton) logoutButton.style.display = 'inline-block';
        } else {
            // Utilisateur non connecté : afficher le bouton login
            if (loginButton) loginButton.style.display = 'inline-block';
            if (logoutButton) logoutButton.style.display = 'none';
        }
    }
}

/**
 * Charge les options du filtre de prix
 */
function loadPriceFilterOptions() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    const options = [
        { value: 'all', text: 'All' },
        { value: '10', text: '10€' },
        { value: '50', text: '50€' },
        { value: '100', text: '100€' }
    ];

    priceFilter.innerHTML = '';
    
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.text;
        priceFilter.appendChild(option);
    });
}

/**
 * Récupère la liste des places depuis l'API
 */
async function fetchPlaces() {
    const token = getCookie('token');
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        });
        
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Erreur lors de la récupération des places: ', response.status);
            show('Impossible de charger les logements');
        }
    } catch (error) {
        console.error('Erreur réseau: ', error);
        show('Erreur de connexion au serveur');
    }
}

/**
 * Affiche les places dans le DOM
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesList.appendChild(placeCard);
    });
}

/**
 * Crée une carte HTML pour une place avec gestion intelligente des images
 */
function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price;
    
    card.innerHTML = `
        <h2>${place.title}</h2>
        <p>${place.description || 'Aucune description disponible'}</p>
        <p class="prix">${place.price}€ / nuit</p>
        <p class="location">${place.latitude.toFixed(4)}, ${place.longitude.toFixed(4)}</p>
        <button class="details-button" onclick="viewPlaceDetails('${place.id}')">Plus d'infos</button>
    `;
    
    return card;
}

/**
 * Filtre les places affichées selon le prix sélectionné
 */
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    const selectedPrice = priceFilter.value;

    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const placePrice = parseFloat(card.dataset.price);
        
        if (selectedPrice === 'all') {
            card.style.display = 'block';
        } else {
            const maxPrice = parseFloat(selectedPrice);
            if (placePrice <= maxPrice) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

/**
 * Redirige vers la page de détails d'une place
 */
function viewPlaceDetails(placeId) {
    const token = getCookie('token');
    const container = document.getElementById('place-details');
    container.style.display = 'block';

    fetch(`${API_BASE_URL}/places/${placeId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    })
    .then(res => {
        if (!res.ok) throw new Error('Place non trouvée');
        return res.json();
    })
    .catch(err => {
        container.innerHTML = `<p style="color:red;">Erreur : ${err.message}</p>`;
    });
}

/*===== GESTION DES COOKIES ==================*/
/**
 * Sauvegarde le JWT token dans un cookie
 */
function saveTokenToCookie(token) {
    const expirationDays = 7;
    const date = new Date();
    date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;

    document.cookie = `token=${token}; ${expires}; path=/; SameSite=Lax`;
}

/**
 * Récupère un cookie par son nom
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

/**
 * Vérifie si l'utilisateur est connecté
 */
function isUserLoggedIn() {
    return getCookie('token') !== null;
}

/**
 * Déconnecte l'utilisateur (supprime le cookie)
 */
function logoutUser() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = 'login.html';
}

/*===== AFFICHAGE DES MESSAGES ===============*/
/**
 * Affiche un message d'erreur
 */
function show(message) {
    alert(message);
}
