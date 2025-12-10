from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta
from typing import Optional
import secrets

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))

# Mount static files
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Mock Users Database
USERS = {
    "customer@demo.com": {
        "id": "1",
        "name": "Demo Customer",
        "email": "customer@demo.com",
        "password": "customer123",
        "role": "customer"
    },
    "staff@demo.com": {
        "id": "2",
        "name": "Demo Staff",
        "email": "staff@demo.com",
        "password": "staff123",
        "role": "staff"
    },
    "manager@demo.com": {
        "id": "3",
        "name": "Demo Manager",
        "email": "manager@demo.com",
        "password": "manager123",
        "role": "manager"
    }
}

# Helper function to check authentication
def get_current_user(request: Request):
    user_email = request.session.get("user_email")
    if user_email and user_email in USERS:
        return USERS[user_email]
    return None

# Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url=f"/{user['role']}")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = USERS.get(email)
    if user and user["password"] == password:
        request.session["user_email"] = email
        return JSONResponse({"success": True, "role": user["role"]})
    return JSONResponse({"success": False, "message": "Invalid credentials"}, status_code=401)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/customer", response_class=HTMLResponse)
async def customer_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "customer":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("customer.html", {"request": request, "user": user})

@app.get("/staff", response_class=HTMLResponse)
async def staff_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "staff":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("staff.html", {"request": request, "user": user})

@app.get("/manager", response_class=HTMLResponse)
async def manager_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "manager":
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("manager.html", {"request": request, "user": user})

# API Endpoints for data operations
@app.get("/api/menu-items")
async def get_menu_items():
    return {
        "items": [
            {"id": "1", "name": "Espresso", "category": "Hot Coffee", "price": 3.50, "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6df5bee?w=400"},
            {"id": "2", "name": "Cappuccino", "category": "Hot Coffee", "price": 4.50, "image": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400"},
            {"id": "3", "name": "Latte", "category": "Hot Coffee", "price": 4.75, "image": "https://images.unsplash.com/photo-1561882468-9110e03e0f78?w=400"},
            {"id": "4", "name": "Americano", "category": "Hot Coffee", "price": 3.75, "image": "https://images.unsplash.com/photo-1532004491497-ba35c367d634?w=400"},
            {"id": "5", "name": "Iced Coffee", "category": "Cold Coffee", "price": 4.25, "image": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=400"},
            {"id": "6", "name": "Cold Brew", "category": "Cold Coffee", "price": 4.50, "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400"},
            {"id": "7", "name": "Croissant", "category": "Pastries", "price": 3.25, "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400"},
            {"id": "8", "name": "Blueberry Muffin", "category": "Pastries", "price": 3.50, "image": "https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=400"},
        ]
    }

@app.get("/api/orders")
async def get_orders(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401)
    
    # Mock orders based on role
    if user["role"] == "customer":
        return {
            "orders": [
                {"id": "ORD-001", "date": "2025-11-15", "items": ["Cappuccino", "Croissant"], "total": 7.75, "status": "completed"},
                {"id": "ORD-002", "date": "2025-11-18", "items": ["Latte"], "total": 4.75, "status": "pending"},
            ]
        }
    else:
        return {
            "orders": [
                {"id": "ORD-101", "customer": "John Doe", "items": ["Espresso x2"], "total": 7.00, "status": "pending", "time": "10:30 AM"},
                {"id": "ORD-102", "customer": "Jane Smith", "items": ["Latte", "Muffin"], "total": 8.25, "status": "in_preparation", "time": "10:45 AM"},
                {"id": "ORD-103", "customer": "Bob Johnson", "items": ["Cold Brew"], "total": 4.50, "status": "completed", "time": "11:00 AM"},
            ]
        }

@app.get("/api/tables")
async def get_tables():
    return {
        "tables": [
            {"id": "1", "number": 1, "capacity": 2, "status": "available"},
            {"id": "2", "number": 2, "capacity": 4, "status": "occupied"},
            {"id": "3", "number": 3, "capacity": 4, "status": "available"},
            {"id": "4", "number": 4, "capacity": 6, "status": "reserved"},
            {"id": "5", "number": 5, "capacity": 2, "status": "available"},
            {"id": "6", "number": 6, "capacity": 8, "status": "available"},
        ]
    }

@app.get("/api/inventory")
async def get_inventory():
    return {
        "items": [
            {"id": "1", "name": "Coffee Beans (Arabica)", "quantity": 45, "unit": "kg", "minStock": 20, "supplier": "Premium Beans Co."},
            {"id": "2", "name": "Milk", "quantity": 15, "unit": "liters", "minStock": 30, "supplier": "Local Dairy Farm"},
            {"id": "3", "name": "Sugar", "quantity": 25, "unit": "kg", "minStock": 10, "supplier": "Sweet Supply Inc."},
            {"id": "4", "name": "Paper Cups (12oz)", "quantity": 500, "unit": "pieces", "minStock": 200, "supplier": "Packaging Pro"},
            {"id": "5", "name": "Croissants", "quantity": 8, "unit": "pieces", "minStock": 20, "supplier": "Baker's Delight"},
        ]
    }

@app.get("/api/staff")
async def get_staff():
    return {
        "staff": [
            {"id": "1", "name": "Sarah Johnson", "role": "Barista", "email": "sarah@coffee.com", "phone": "(555) 123-4567", "status": "active", "schedule": "Mon-Fri, 6AM-2PM"},
            {"id": "2", "name": "Mike Chen", "role": "Cashier", "email": "mike@coffee.com", "phone": "(555) 234-5678", "status": "active", "schedule": "Tue-Sat, 10AM-6PM"},
            {"id": "3", "name": "Emily Rodriguez", "role": "Barista", "email": "emily@coffee.com", "phone": "(555) 345-6789", "status": "active", "schedule": "Wed-Sun, 7AM-3PM"},
        ]
    }

@app.get("/api/promotions")
async def get_promotions():
    return {
        "promotions": [
            {"id": "1", "name": "Happy Hour", "description": "20% off all drinks", "discount": 20, "type": "percentage", "startDate": "2025-11-01", "endDate": "2025-11-30", "status": "active"},
            {"id": "2", "name": "Weekend Special", "description": "Buy 2 Get 1 Free", "discount": 0, "type": "bogo", "startDate": "2025-11-15", "endDate": "2025-12-15", "status": "active"},
        ]
    }

@app.get("/api/customers")
async def get_customers():
    return {
        "customers": [
            {"id": "1", "name": "John Doe", "email": "john.doe@email.com", "phone": "(555) 111-2222", "totalOrders": 24, "totalSpent": 387.50, "status": "active"},
            {"id": "2", "name": "Jane Smith", "email": "jane.smith@email.com", "phone": "(555) 222-3333", "totalOrders": 18, "totalSpent": 295.75, "status": "active"},
            {"id": "3", "name": "Bob Johnson", "email": "bob.j@email.com", "phone": "(555) 333-4444", "totalOrders": 32, "totalSpent": 512.25, "status": "active"},
        ]
    }

@app.get("/api/feedback")
async def get_feedback():
    return {
        "feedback": [
            {"id": "1", "customer": "John Doe", "date": "2025-11-08", "foodRating": 5, "serviceRating": 5, "comment": "Excellent coffee and very friendly staff!", "status": "pending"},
            {"id": "2", "customer": "Jane Smith", "date": "2025-11-07", "foodRating": 5, "serviceRating": 5, "comment": "Best coffee shop in town!", "status": "responded", "response": "Thank you for your support!"},
            {"id": "3", "customer": "Bob Johnson", "date": "2025-11-06", "foodRating": 3, "serviceRating": 4, "comment": "Good service, but my latte was a bit cold.", "status": "pending"},
        ]
    }

@app.get("/api/revenue")
async def get_revenue():
    return {
        "daily": [
            {"date": "2025-11-13", "revenue": 1245.50, "orders": 87},
            {"date": "2025-11-14", "revenue": 1398.25, "orders": 92},
            {"date": "2025-11-15", "revenue": 1156.75, "orders": 78},
            {"date": "2025-11-16", "revenue": 1520.00, "orders": 105},
            {"date": "2025-11-17", "revenue": 1687.50, "orders": 115},
            {"date": "2025-11-18", "revenue": 1823.25, "orders": 128},
            {"date": "2025-11-19", "revenue": 945.00, "orders": 62},
        ],
        "totals": {
            "today": 945.00,
            "week": 9776.25,
            "month": 42350.00,
            "orders_today": 62,
            "orders_week": 667,
            "avg_order": 14.65
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
