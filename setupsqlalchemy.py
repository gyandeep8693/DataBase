from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
engine = create_engine("sqlite:////home/Gyandeep/projects/pro1/Bittu.db", echo=True)
 

class TODO(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
 
  
    def __init__(self, task, status):

        self.task = task
        self.status = status
 
def main():
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
 
    session.add_all([
        TODO('Hello World', 0),
        TODO('Task Incomplete', 1),
        TODO('Task Completed', 1),
        TODO('Bye World', 0)
        ])
    session.commit()
 
if __name__ == "__main__":
    main()
