from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

# Naming convention setup for Alembic compatibility
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

# Database setup
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Relationships
    freebies = relationship("Freebie", back_populates="company")
    devs = association_proxy('freebies', 'dev',
        creator=lambda dev: Freebie(dev=dev))

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie for this company and given dev"""
        freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        session.add(freebie)
        session.commit()
        return freebie

    @classmethod
    def oldest_company(cls):
        """Returns the company with the earliest founding year"""
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationships
    freebies = relationship("Freebie", back_populates="dev")
    companies = association_proxy('freebies', 'company',
        creator=lambda company: Freebie(company=company))

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        """Returns True if dev has any freebie with given item_name"""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """Changes freebie's dev to given dev if it belongs to current dev"""
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    # Relationships
    company = relationship("Company", back_populates="freebies")
    dev = relationship("Dev", back_populates="freebies")

    def __repr__(self):
        return f"<Freebie {self.item_name} (${self.value}) from {self.company.name} to {self.dev.name}>"

    def print_details(self):
        """Returns formatted string with freebie details"""
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

# Create all tables
Base.metadata.create_all(engine)