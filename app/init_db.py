from app.database import engine, Base
# from app import models
import models

def init_db():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created!")

if __name__ == "__main__":
    init_db()