/*------------------------------------------*/
/*--------===> GESTION DU L'API <===------- */
/*------------------------------------------*/

const API_BASE_URL = 'http://localhost:5000/api/v1';
const API_LOGIN_ENDPOINT = `${API_BASE_URL}/auth/login`;

/*------------------------------------------*/
/*----===> Chargement de la page <===------ */
/*------------------------------------------*/

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Site chargé avec succès!');
    const currentPage = window.location.pathname.split('/').pop(); // récupère "index.html" ou "place.html"

    /*------------------------------------------*/
    /*---===> GESTION PAGE INDEX.HTML <===-----*/
    /*------------------------------------------*/

    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    
    if (currentPage === 'index.html') {
        console.log('Page index');
        checkAuthentication();
        loadPriceFilterOptions();
        fetchPlaces();
        
        if (priceFilter) {
            priceFilter.addEventListener('change', filterPlacesByPrice);
        }

        // Fonction de redirection pour les boutons
        window.viewPlaceDetails = (placeId) => {
            window.location.href = `place.html?place_id=${encodeURIComponent(placeId)}`;
        };
    }

    /*---------------------------------------------*/
    /*--------===> GESTION PLACE.HTML <===------- */
    /*-------------------------------------------*/

    if (currentPage === 'place.html') {
        const placeId = new URLSearchParams(window.location.search).get('place_id');
        if (placeId) loadPlaceDetails(placeId);
    }

    /*------------------------------------------*/
    /*--------===> GESTION DU LOGIN <===------- */
    /*------------------------------------------*/
    
    // Vérifie si on est sur la page login
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        // Écoute la soumission du formulaire
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Récupère les valeurs des champs
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validation simple
            if (!email || !password) {
                alert('Merci de remplir tous les champs !');
                return;
            }
            
            // Validation du format email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Merci d\'entrer une adresse email valide !');
                return;
            }
            
            // Désactiver le bouton pendant la requête
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Connexion en cours...';
            submitButton.disabled = true;

            try {
                //Appel à l'API pour test la connexion
                const success = await loginUser(email, password);

                if (success) {
                    showSuccess('Connexion réussie! Redirection...');
                    //Redirection vers index.html
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                }
            } catch (error) {
                console.error('Erreur lors de la connexion:', error);
                showError('Une erreur est survenue. Veuillez réessayer.');
            } finally {
                // Permet de réactiver le bouton
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
            
        });
    }

    /*------------------------------------------*/
    /*-----===> FORMULAIRE ADD REVIEW <===-----*/
    /*------------------------------------------*/

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        // Crée dynamiquement un message flottant de confirmation
        const floating = document.createElement('div');
        floating.id = 'floating-confirmation';
        floating.textContent = "Merci ! Votre avis a été ajouté.";
        floating.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            opacity: 0;
            transform: translateY(-20px);
            transition: opacity 0.4s, transform 0.4s;
            z-index: 9999;
        `;
        document.body.appendChild(floating);

        // Fonction pour afficher le message
        const showMessage = () => {
            floating.style.opacity = '1';
            floating.style.transform = 'translateY(0)';
            setTimeout(() => {
                floating.style.opacity = '0';
                floating.style.transform = 'translateY(-20px)';
            }, 3000);
        };

        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Affiche le message
            showMessage();
            // Réinitialise le formulaire
            reviewForm.reset();
        });
    }
});

/**
 * Redirige vers place.html et affiche les détails + reviews
 * @param {string} placeId 
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

        // Affichage des détails
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
        console.log('Reviews récupérées: ', reviews);

        // Affichage des reviews
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

/*--------------------------------------------------------*/
/*-===> Fonction pour récupérer le nom d'utilisateur <==-*/
/*------------------------------------------------------*/

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

/*-------------------------------------------*/
/*-===> Fonction de la connexion à l'Api <==-*/
/*-------------------------------------------*/

/**
 * Envoie les identifiants à l'API backend
 * @param {string} email - Email de l'utilisateur
 * @param {string} password - Mot de passe de l'utilisateur
 * @returns {Promise<boolean>} - true si connexion réussie, false sinon
 */
async function loginUser(email, password) {
    try {
        // Envoyer la requête POST à l'API
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

        // Vérifier si la requête a réussi
        if (response.ok) {
            // Récupérer les données JSON
            const data = await response.json();
            
            // Vérifier que le token existe
            if (data.access_token) {
                // Sauvegarder le token dans un cookie
                saveTokenToCookie(data.access_token);
                return true;
            } else {
                console.error('Token manquant dans la réponse');
                showError('Erreur serveur: token manquant');
                return false;
            }
        } else {
            // Connexion échouée - essayer de récupérer le message d'erreur
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
            showError(errorMessage);
            return false;
        }
    } catch (error) {
        console.error('Erreur réseau: ', error);        
        return false;
    }
}


/*============================================*/
/*===== GESTION DE LA PAGE INDEX =============*/
/*============================================*/

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
    
    // Vider le select
    priceFilter.innerHTML = '';
    
    // Ajouter les options
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
            showError('Impossible de charger les logements');
        }
    } catch (error) {
        console.error('Erreur réseau: ', error);
        showError('Erreur de connexion au serveur');
    }
}

/**
 * Affiche les places dans le DOM
 * @param {Array} places - Liste des places à afficher
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    if (places.length === 0) {
        placesList.innerHTML = '<p style="text-align: center; color: #666;">Aucun logement disponible pour le moment.</p>';
        return;
    }
    
    // Créer une carte pour chaque place
    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesList.appendChild(placeCard);
    });
}

/**
 * Crée une carte HTML pour une place avec gestion intelligente des images
 * @param {Object} place - Données de la place
 * @returns {HTMLElement} - Element div de la carte
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

    // Récupérer toutes les cartes de places
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
 * @param {string} placeId - ID de la place
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
    .then(place => {
        container.innerHTML = `
            <h2>${place.title || place.name}</h2>
            <p>${place.description}</p>
            <p><strong>Prix:</strong> ${place.price}€</p>
            <p><strong>Localisation:</strong> ${place.latitude}, ${place.longitude}</p>
        `;
    })
    .catch(err => {
        container.innerHTML = `<p style="color:red;">Erreur : ${err.message}</p>`;
    });
}


/*============================================*/
/*===== GESTION DES COOKIES ==================*/
/*============================================*/

/**
 * Sauvegarde le JWT token dans un cookie
 * @param {string} token - Le JWT token à sauvegarder
 */
function saveTokenToCookie(token) {
    // Créer un cookie qui expire dans 7 jours
    const expirationDays = 7;
    const date = new Date();
    date.setTime(date.getTime() + (expirationDays * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    
    // Sauvegarder le cookie
    document.cookie = `token=${token}; ${expires}; path=/; SameSite=Lax`;
}

/**
 * Récupère un cookie par son nom
 * @param {string} name - Le nom du cookie
 * @returns {string|null} - La valeur du cookie ou null
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
 * @returns {boolean} - true si connecté, false sinon
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

/*============================================*/
/*===== AFFICHAGE DES MESSAGES ===============*/
/*============================================*/

/**
 * Affiche un message d'erreur
 * @param {string} message - Le message à afficher
 */
function showError(message) {
    // Utilise alert pour l'instant (simple)
    alert('❌ ' + message);
    
    // Alternative : afficher dans un élément HTML
    // Si tu as un <div id="error-message"></div> dans ton HTML
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        errorElement.style.color = 'red';
        errorElement.style.padding = '10px';
        errorElement.style.marginTop = '10px';
        errorElement.style.backgroundColor = '#ffe0e0';
        errorElement.style.borderRadius = '5px';
        
        // Cacher après 5 secondes
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }
}

/**
 * Affiche un message de succès
 * @param {string} message - Le message à afficher
 */
function showSuccess(message) {
    // Utilise alert pour l'instant
    alert('✅ ' + message);
    
    // Alternative : afficher dans un élément HTML
    const successElement = document.getElementById('success-message');
    if (successElement) {
        successElement.textContent = message;
        successElement.style.display = 'block';
        successElement.style.color = 'green';
        successElement.style.padding = '10px';
        successElement.style.marginTop = '10px';
        successElement.style.backgroundColor = '#e0ffe0';
        successElement.style.borderRadius = '5px';
        
        // Cacher après 3 secondes
        setTimeout(() => {
            successElement.style.display = 'none';
        }, 3000);
    }
}
