from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a la base de datos usada por la aplicación.
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost:5432/mascotas_db"

# Motor compartido para ejecutar las operaciones SQL.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fábrica de sesiones con control explícito de transacciones y cierre.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base común para definir los modelos ORM.
Base = declarative_base()

def get_db():
    # Dependencia de FastAPI para abrir y cerrar una sesión por request.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()