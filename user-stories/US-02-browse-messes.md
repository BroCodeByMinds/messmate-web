# US-02: Browse Messes by City

## 🎯 Goal
As a user, I want to browse messes in a selected city so that I can compare options and choose the best mess based on price, food type, and menu before subscribing.

---

## 📚 Description
The user should be able to select a city or allow location access to view available messes. Each mess listing should provide key details like name, meal type (veg/non-veg), price, rating, and weekly menu. The user can then click on a mess to view its full profile and choose to subscribe.

---

## ✅ Acceptance Criteria

- [ ] User can select a city from a dropdown or input field.
- [ ] All messes in that city are listed in cards/grid format.
- [ ] Each mess card displays:
  - Mess name
  - Meal type (Veg/Non-Veg)
  - Monthly price
  - Rating (optional)
  - "View Menu" and "Subscribe" buttons
- [ ] Filters:
  - Veg / Non-Veg toggle
  - Sort by Price (low-high, high-low)
- [ ] Clicking "View Menu" opens the weekly menu (handled in US-03).
- [ ] Clicking "Subscribe" takes the user to the subscription process (US-04).

---

## 🛠 Tasks

### Frontend
- [ ] Build city selection dropdown or search input
- [ ] Create mess card UI with key info
- [ ] Integrate API to fetch messes by city
- [ ] Implement filters and sorting options
- [ ] Display message if no messes found

### Backend (FastAPI)
- [ ] Endpoint: `GET /api/messes?city={city}`
- [ ] Optional query params:
  - `type=veg/non-veg`
  - `sort=price_asc/price_desc`
- [ ] Validate city name input
- [ ] Fetch mess records from DB with filters

---

## 📦 API Design

**Endpoint:** `GET /api/messes`

**Query Params:**
| Name  | Type   | Required | Description             |
|-------|--------|----------|-------------------------|
| city  | string | ✅ Yes    | City name to filter     |
| type  | string | ❌ No     | Filter by veg/non-veg   |
| sort  | string | ❌ No     | Sorting preference      |

---

## 🔐 Security
- Use authentication for users accessing mess details (optional in MVP).
- Rate limit the browse endpoint to avoid abuse (future).

---

## 📝 Notes

- Add fallback UI for when no messes are available in the selected city.
- Reuse this screen to enable city-based recommendations in future.
- Ensure data is cached or paginated to prevent performance issues with many messes.
- Extend later with:
  - Google Maps integration (optional)
  - "Show messes near me" with location permission

---
