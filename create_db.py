import pandas as pd
import sqlite3
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column,
                        Date,
                        DateTime,
                        Index,
                        Integer,
                        PrimaryKeyConstraint,
                        String)

engine = create_engine('sqlite:///tsaclaims.db')

metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)
                            )

Base.query = db_session.query_property()

class Claims(Base):
    __tablename__ = 'tsa_claims'

    __table_args__ = (
        PrimaryKeyConstraint('claim_number', name='Claim Number'),
        Index('Date Received', 'date_received'),
        Index('Incident Date', 'incident_date'),
        Index('Airport Code', 'airport_code'),
        Index('Airport Name', 'airport_name'),
        Index('Airline Name', 'airline_name'),
        Index('Claim Type', 'claim_type'),
        Index('Claim Site', 'claim_site'),
        Index('Item Category', 'item_category'),
        Index('Close Amount', 'close_amount'),
        Index('Disposition', 'disposition')
    )

    claim_number = Column(Integer)
    date_received = Column(Date)
    incident_date = Column(DateTime)
    airport_code = Column(String(3))
    airport_name = Column(String(500))
    airline_name = Column(String(500))
    claim_type = Column(String(500))
    claim_site = Column(String(500))
    item_category = Column(String(500))
    close_amount = Column(Integer)
    disposition = Column(String(500))


def populate_db():
    Base.metadata.create_all(engine)
    conn = sqlite3.connect("tsaclaims.db")
    df = pd.read_csv('/Users/AUCHLY1/SideProjects/tsa-claims/tsa_data/claims-2010-2013_0.csv')
    columns = ['claim_number', 'date_received', 'incident_date', 'airport_code', 'airport_name',
               'airline_name', 'claim_type', 'claim_site', 'item_category', 'close_amount', 'disposition']
    df.columns = columns

    df.to_sql('tsa_claims', conn, if_exists='replace', index=False)

if __name__ == "__main__":
    populate_db()