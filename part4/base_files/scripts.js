document.addEventListener('DOMContentLoaded', () => {

    /************* DATA *************/
    // Exemple de places
    let places = [
        { id: 1, name: "Cozy Apartment", price: 120 },
        { id: 2, name: "Beach House", price: 250 },
        { id: 3, name: "Mountain Cabin", price: 150 }
    ];

    // Exemple de place détaillée et reviews
    let placeDetails = {
        1: {
            name: "Cozy Apartment",
            host: "Alice Johnson",
            price: 120,
            description: "A modern apartment in the city center with all amenities included.",
            amenities: ["Wi-Fi", "Air Conditioning", "Kitchen", "Washer"],
            reviews: [
                { user: "Bob", rating: 5, comment: "Great location, very clean!" },
                { user: "Clara", rating: 4, comment: "Perfect for a short stay." }
            ]
        },
        2: {
            name: "Beach House",
            host: "John Smith",
            price: 250,
            description: "A beautiful house by the beach with sea view.",
            amenities: ["Wi-Fi", "Pool", "Beach Access"],
            reviews: []
        },
        3: {
            name: "Mountain Cabin",
            host: "Emma White",
            price: 150,
            description: "Cozy cabin in the mountains for nature lovers.",
            amenities: ["Fireplace", "Hiking Trails", "Pets Allowed"],
            reviews: []
        }
    };

    /************* INDEX.HTML *************/
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    function renderPlaces(maxPrice = 0) {
        if (!placesList) return; // Page index only
        placesList.innerHTML = '';
        const filtered = maxPrice > 0 ? places.filter(p => p.price <= maxPrice) : places;
        filtered.forEach(place => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.innerHTML = `
                <h3>${place.name}</h3>
                <p>Price per night: $${place.price}</p>
                <a href="place.html?place_id=${place.id}" class="details-button">View Details</a>
            `;
            placesList.appendChild(card);
        });
    }

    if (placesList) {
        renderPlaces();
        priceFilter.addEventListener('change', () => {
            const max = parseInt(priceFilter.value, 10);
            renderPlaces(max);
        });
    }

    /************* PLACE.HTML *************/
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id') || 1; // default to 1
    const placeSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');
    const reviewForm = document.getElementById('review-form');

    function renderPlace(placeId) {
        if (!placeSection) return; // Not on place.html
        const place = placeDetails[placeId];
        if (!place) return;
        placeSection.innerHTML = `
            <div class="place-card">
                <h1>${place.name}</h1>
                <p><strong>Host:</strong> ${place.host}</p>
                <p><strong>Price per night:</strong> $${place.price}</p>
                <p><strong>Description:</strong> ${place.description}</p>
                <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
            </div>
        `;
    }

    function renderReviews(placeId) {
        if (!reviewsSection) return;
        const place = placeDetails[placeId];
        reviewsSection.innerHTML = '<h2>Reviews</h2>';
        if (!place.reviews || place.reviews.length === 0) {
            reviewsSection.innerHTML += "<p>No reviews yet.</p>";
            return;
        }
        place.reviews.forEach(r => {
            const card = document.createElement('div');
            card.className = 'review-card';
            card.innerHTML = `
            <p><strong>${r.user}:</strong></p>
                <p>${r.comment}</p>
                <p>Rating: ${r.rating}⭐</p>
            `;
            reviewsSection.appendChild(card);
        });
    }

    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const user = document.getElementById('user') ? document.getElementById('user').value.trim() : "Current User";
            const comment = document.getElementById('review') ? document.getElementById('review').value.trim() : "";
            const rating = document.getElementById('rating') ? parseInt(document.getElementById('rating').value) : 5;

            if (!comment) return;

            placeDetails[placeId].reviews.push({ user, rating, comment });

            // Reset form
            if (reviewForm) reviewForm.reset();
            // Refresh reviews
            renderReviews(placeId);
        });
    }

    // Initial render
    renderPlace(placeId);
    renderReviews(placeId);

    /************* ADD_REVIEW.HTML *************/
    const addReviewForm = document.getElementById('review-form');
    const placeIdInput = document.getElementById('place-id');

    if (addReviewForm && placeIdInput) {
        // Populate rating select
        const ratingSelect = document.getElementById('rating');
        for (let i = 1; i <= 5; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `${i} ⭐`;
            ratingSelect.appendChild(option);
        }

        addReviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const user = document.getElementById('user').value.trim() || "Current User";
            const comment = document.getElementById('review').value.trim();
            const rating = parseInt(document.getElementById('rating').value);
            const pid = parseInt(placeIdInput.value);

            if (!comment || !rating) return;

            if (!placeDetails[pid].reviews) placeDetails[pid].reviews = [];
            placeDetails[pid].reviews.push({ user, rating, comment });

            alert("Review submitted!");
            addReviewForm.reset();
        });
    }

});
