from auth.auth_database import Base, engine
from auth import model

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")