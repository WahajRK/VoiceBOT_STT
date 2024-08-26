from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Database setup - use your MySQL instance details
DATABASE_URL = "mysql+pymysql://root:root@DESKTOP-2ED4NK2:3306/file_uploads_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a model for the uploaded files
class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    upload_time = Column(TIMESTAMP, default=datetime.utcnow)

# Create tables in the database
Base.metadata.create_all(bind=engine)

@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile]):
    db = SessionLocal()
    
    try:
        for file in files:
            # Save file metadata to the database
            db_file = UploadedFile(filename=file.filename)
            db.add(db_file)
            db.commit()
            db.refresh(db_file)

            # Optionally, save the file to the disk
            with open(f"/path/to/save/{file.filename}", "wb") as f:
                f.write(file.file.read())

        return {"Uploaded Files": [file.filename for file in files]}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="File upload failed")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
