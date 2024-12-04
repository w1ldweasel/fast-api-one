from sqlmodel import create_engine, Session


#Boilerplate code to connect to DB
engine = create_engine(
    "sqlite:///carsharing.db", 
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Log generated SQL (don't use in production)
)


def get_session():
    #return Session(engine)
    with Session(engine) as session:
        yield session 
        #session wrapped in with block, using yield here means if exception occurs in session, any db update is rolled back
