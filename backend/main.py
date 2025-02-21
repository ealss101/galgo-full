from fastapi import FastAPI
from backend.routes.auth_routes import router as auth_router
from backend.routes.admin_routes import router as admin_router
from backend.routes.user_routes import router as user_router
from backend.routes.chat_history_routes import router as chat_history_router  # ✅ Import new router

app = FastAPI()

# ✅ Explicitly set prefixes for clarity
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(chat_history_router, prefix="/chat_history", tags=["chat_history"])  # ✅ Register new route

@app.get("/")
def root():
    return {"message": "Welcome to the API"}
