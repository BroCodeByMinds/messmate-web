# US-12: Admin Adds a Mess to the System

## 🎯 Goal
As a mess admin, I want to add a new mess to the system under a city so that users can discover it, view menus, and subscribe.

---

## 📚 Description
Mess admins should be able to register or log in to their admin dashboard and fill a form to add their mess details. These messes will be publicly visible to users for browsing (US-02) and subscription (US-04). Each mess can have its own meal types, price, location, description, and images.

---

## ✅ Acceptance Criteria

- [ ] Admin can log in and access the "Add Mess" screen.
- [ ] Admin provides required details:
  - Mess Name
  - City
  - Meal Type (Veg/Non-Veg/Both)
  - Monthly Price
  - Address / Location
  - Description (optional)
  - Contact Number (optional)
- [ ] Backend validates and stores the mess in the database.
- [ ] On success, mess appears in the city listing for users (US-02).
- [ ] Duplicate mess names in the same city should be avoided.

---

## 🛠 Tasks

### Frontend (Admin Panel)
- [ ] Create a mess creation form
- [ ] Fields: name, city, type, price, address, description
- [ ] Validate form fields (required, formats)
- [ ] Call API to create mess
- [ ] Show confirmation message on success

### Backend (FastAPI)
- [ ] API Endpoint: `POST /api/admin/messes`
- [ ] Create `Mess` model:
  - `id`, `name`, `city`, `type`, `price`, `address`, `description`, `created_by`
- [ ] Validate for duplicates (name + city)
- [ ] Save to DB with foreign key to admin
- [ ] Add authentication: only admin role can access this API

---

## 📦 API Design

**Endpoint:** `POST /api/admin/messes`

**Payload:**
```json
{
  "name": "Sairam Mess",
  "city": "Pune",
  "type": "Veg",
  "monthly_price": 2200,
  "address": "Near ABC Hostel, Pune",
  "description": "Home-cooked food with tiffin service"
}

---

## 🔐 Security
- Only users with admin role can access this API.
- oken-based auth via JWT required.
- Input validation to prevent XSS or script injection

---

## 📝 Notes

- Extend model later to include:
  - Geo-coordinates (latitude/longitude)
  - Image upload (optional)
  - Multiple meal plans per mess (e.g., 1-meal, 2-meal)

- Mess data should be used in user-facing modules like:
  - City browsing (US-02)
  - Menu view (US-03)
  - Subscriptions (US-04)
- Future feature: Super admin approval before mess goes live (optional)

---
