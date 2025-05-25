#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

if __name__ == '__main__':
    # Set up database connection
    engine = create_engine('sqlite:///freebies.db')
    
    # Create a session class and instance
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Make session available in debugger's global namespace
    import __main__
    __main__.session = session
    
    # Start debugger with all variables available
    import ipdb; ipdb.set_trace()