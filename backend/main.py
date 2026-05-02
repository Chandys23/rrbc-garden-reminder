from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
import sys

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, get_connection, get_cursor
from reminders import schedule_reminders
from import_gardeners import BulkImporter

# Initialize FastAPI app
app = FastAPI(title="RRBC Garden Reminder API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Gardener(BaseModel):
    date: str  # Format: YYYY-MM-DD
    name: str
    task: str  # Front, Back, or Trimming
    email: str
    mobile: str

class GardenerUpdate(BaseModel):
    date: str
    name: str
    task: str
    email: str
    mobile: str

class GardenerResponse(Gardener):
    id: int

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database and start scheduler"""
    init_db()
    print("✓ Database initialized")
    
    # Start background scheduler for reminders
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_reminders, 'interval', hours=1)
    scheduler.start()
    print("✓ Reminder scheduler started")
    
    # Shut down the scheduler when the app exits
    atexit.register(lambda: scheduler.shutdown())

# ============ API Routes ============

@app.get("/api/gardeners", response_model=list[GardenerResponse])
def get_all_gardeners():
    """Get all gardeners"""
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        
        cursor.execute("SELECT * FROM gardeners ORDER BY date ASC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/gardeners/{gardener_id}", response_model=GardenerResponse)
def get_gardener(gardener_id: int):
    """Get a specific gardener"""
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        
        cursor.execute("SELECT * FROM gardeners WHERE id = %s", (gardener_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Gardener not found")
        
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gardeners", response_model=dict)
def create_gardener(gardener: Gardener):
    """Add a new gardener"""
    try:
        # Validate date format
        datetime.strptime(gardener.date, '%Y-%m-%d')
        
        conn = get_connection()
        cursor = get_cursor(conn)
        
        cursor.execute("""
            INSERT INTO gardeners (date, name, task, email, mobile)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (gardener.date, gardener.name, gardener.task, gardener.email, gardener.mobile))
        
        result = cursor.fetchone()
        gardener_id = result['id'] if result else None
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"id": gardener_id, "message": "Gardener added successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/gardeners/{gardener_id}")
def update_gardener(gardener_id: int, gardener: GardenerUpdate):
    """Update gardener details"""
    try:
        # Validate date format
        datetime.strptime(gardener.date, '%Y-%m-%d')
        
        conn = get_connection()
        cursor = get_cursor(conn)
        
        cursor.execute("""
            UPDATE gardeners 
            SET date = %s, name = %s, task = %s, email = %s, mobile = %s
            WHERE id = %s
        """, (gardener.date, gardener.name, gardener.task, gardener.email, gardener.mobile, gardener_id))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Gardener not found")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": "Gardener updated successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/gardeners/{gardener_id}")
def delete_gardener(gardener_id: int):
    """Delete a gardener"""
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        
        cursor.execute("DELETE FROM gardeners WHERE id = %s", (gardener_id,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Gardener not found")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": "Gardener deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reimport")
def reimport_gardeners():
    """Re-import all gardeners from Schedule.xlsx - clears existing data"""
    try:
        # Clear existing records
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("DELETE FROM gardeners")
        conn.commit()
        deleted_count = cursor.rowcount
        cursor.close()
        conn.close()
        
        # Re-import fresh data
        importer = BulkImporter()
        success = importer.import_from_excel()
        
        if success:
            return {
                "status": "success",
                "message": f"Successfully cleared {deleted_count} old records and imported {importer.imported_count} gardeners",
                "deleted": deleted_count,
                "imported": importer.imported_count
            }
        else:
            return {
                "status": "error",
                "message": f"Import completed with {importer.error_count} errors",
                "imported": importer.imported_count,
                "failed": importer.error_count
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reimport failed: {str(e)}")

# Serve frontend
@app.get("/")
def serve_frontend():
    """Serve the main HTML file"""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
