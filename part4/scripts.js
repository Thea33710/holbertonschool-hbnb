
/* 
  scripts.js - Handles login, index page (places), place details, reviews, filtering, and review submission
*/

// ------------------------------
// SAMPLE DATA (for testing without API)
// ------------------------------
const samplePlaces = [
  { id: 1, name: "Cozy Apartment", price: 90 },
  { id: 2, name: "Modern Loft", price: 120 },
  { id: 3, name: "Beach House", price: 200 }
];

const samplePlaceData = {
  1: {
    id: 1,
    name: "Cozy Apartment",
    host: "Alice",
    price: 90,
    description: "A warm, welcoming apartment in the city center.",
    amenities: ["WiFi", "Air Conditioning", "Kitchen"],
    reviews: [
      { user: "John", rating: 5, comment: "Great stay!" },
      { user: "Maria", rating: 4, comment: "Very cozy!" }
    ]
  },
  2: {
    id: 2,
    name: "Modern Loft",
    host: "Bob",
    price: 120,
    description: "Stylish loft in downtown with amazing views.",
    amenities: ["WiFi", "Elevator", "Coffee Machine"],
    reviews: []
  },
  3: {
    id: 3,
    name: "Beach House",
    host: "Carol",
    price: 200,
    description: "Spacious house right on the beach.",
    amenities: ["WiFi", "Pool", "Kitchen", "Parking"],
    reviews: [
      { user: "Anna", rating: 5, comment: "Loved it!" }
    ]
  }
};

// ------------------------------
// UTILITY FUNCTIONS
// ------------------------------
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

let userLoggedIn = getCookie("token") !== null;

// ------------------------------
// LOGIN FUNCTIONS
// ------------------------------
async function loginUser(email, password) {
  try {
    const response = await fetch('https://your-api-url/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/; max-age=${60*60*24}`;
      userLoggedIn = true;
      window.location.href = 'index.html';
    } else {
      const errorData = await response.json();
      alert('Login failed: ' + (errorData.message || response.statusText));
    }
  } catch (error) {
    alert('Login failed: ' + error.message);
  }
}

function updateLoginButton() {
  const loginButton = document.querySelector('.login-button');
  if (!loginButton) return;

  if (userLoggedIn) {
    loginButton.textContent = 'Logout';
    loginButton.href = '#';
    loginButton.addEventListener('click', () => {
      document.cookie = 'token=; path=/; max-age=0';
      userLoggedIn = false;
      window.location.reload();
    });
  }
}

// ------------------------------
// INDEX PAGE FUNCTIONS
// ------------------------------
async function fetchPlaces(token) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch('https://your-api-url/places', { method: 'GET', headers });

    let placesData = samplePlaces; // fallback
    if (response.ok) {
      placesData = await response.json();
    }

    displayPlaces(placesData);
    setupPriceFilter(placesData);
  } catch (error) {
    console.error(error);
    displayPlaces(samplePlaces);
    setupPriceFilter(samplePlaces);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;

  container.innerHTML = '';
  places.forEach(place => {
    const card = document.createElement('div');
    card.classList.add('place-card');
    card.dataset.price = place.price;

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    container.appendChild(card);
  });
}

function setupPriceFilter(places) {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.innerHTML = `
    <option value="10">$10</option>
    <option value="50">$50</option>
    <option value="100">$100</option>
    <option value="All">All</option>
  `;

  filter.addEventListener('change', (event) => {
    const selected = event.target.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseInt(card.dataset.price, 10);
      card.style.display = (selected === 'All' || price <= parseInt(selected, 10)) ? 'block' : 'none';
    });
  });
}

// ------------------------------
// PLACE PAGE FUNCTIONS
// ------------------------------
async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`https://your-api-url/places/${placeId}`, { method: 'GET', headers });
    let place = samplePlaceData[placeId] || samplePlaceData[1];

    if (response.ok) {
      place = await response.json();
    }

    displayPlaceDetails(place);
  } catch (error) {
    console.error(error);
    const place = samplePlaceData[placeId] || samplePlaceData[1];
    displayPlaceDetails(place);
  }
}

function displayPlaceDetails(place) {
  const detailsContainer = document.getElementById("place-details");
  const reviewsContainer = document.getElementById("reviews");
  const addReviewSection = document.getElementById("add-review");
  if (!detailsContainer) return;

  detailsContainer.innerHTML = `
    <h2>${place.name}</h2>
    <div class="place-info">
      <p><strong>Host:</strong> ${place.host}</p>
      <p><strong>Price:</strong> $${place.price} per night</p>
      <p><strong>Description:</strong> ${place.description}</p>
      <p><strong>Amenities:</strong> ${place.amenities.join(", ")}</p>
    </div>
  `;

  reviewsContainer.innerHTML = "<h3>Reviews</h3>";
  if (!place.reviews || place.reviews.length === 0) {
    reviewsContainer.innerHTML += "<p>No reviews yet.</p>";
  } else {
    place.reviews.forEach(r => {
      const card = document.createElement("div");
      card.classList.add("review-card");
      card.innerHTML = `
        <p><strong>${r.user}</strong> – Rating: ${r.rating}/5</p>
        <p>${r.comment}</p>
      `;
      reviewsContainer.appendChild(card);
    });
  }

  // Show review form only if user is logged in
  if (!userLoggedIn) {
    addReviewSection.innerHTML = `<a href="login.html" class="login-button">Login to add a review</a>`;
  } else {
    addReviewSection.innerHTML = `
      <form id="review-form">
        <input type="text" id="review-comment" placeholder="Your comment" required>
        <input type="number" id="review-rating" min="1" max="5" placeholder="Rating" required>
        <button type="submit">Add Review</button>
      </form>
    `;

    document.getElementById('review-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const comment = document.getElementById('review-comment').value.trim();
      const rating = parseInt(document.getElementById('review-rating').value, 10);

      if (!comment || !rating || rating < 1 || rating > 5) {
        alert('Please enter a valid comment and rating (1-5).');
        return;
      }

      submitReview(getCookie('token'), place.id, comment, rating);
    });
  }
}

// ------------------------------
// SUBMIT REVIEW FUNCTION
// ------------------------------
async function submitReview(token, placeId, comment, rating) {
  try {
    const response = await fetch(`https://your-api-url/places/${placeId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ comment, rating })
    });

    if (response.ok) {
      alert('Review submitted successfully!');
      document.getElementById('review-form').reset();
      fetchPlaceDetails(token, placeId); // refresh reviews
    } else {
      const errorData = await response.json();
      alert('Failed to submit review: ' + (errorData.message || response.statusText));
    }
  } catch (error) {
    alert('Failed to submit review: ' + error.message);
  }
}

// ------------------------------
// INITIALIZE
// ------------------------------
document.addEventListener('DOMContentLoaded', () => {
  // Login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      if (!email || !password) {
        alert('Please enter both email and password.');
        return;
      }
      await loginUser(email, password);
    });
  }

  // Update login button
  updateLoginButton();

  // Index page
  const token = getCookie('token');
  const placesList = document.getElementById('places-list');
  if (placesList) {
    const loginLink = document.getElementById('login-link');
    if (!token) {
      if (loginLink) loginLink.style.display = 'block';
      displayPlaces(samplePlaces);
      setupPriceFilter(samplePlaces);
    } else {
      if (loginLink) loginLink.style.display = 'none';
      fetchPlaces(token);
    }
  }

  // Place page
  const placeDetails = document.getElementById('place-details');
  if (placeDetails) {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get("id");
    fetchPlaceDetails(token, placeId);
  }
});
