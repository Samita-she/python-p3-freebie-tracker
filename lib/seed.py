#!/usr/bin/env python3

# Script goes here!
from models import Company, Dev, Freebie
from database import session

c1 = Company(name="Google", founding_year=1998)
c2 = Company(name="Microsoft", founding_year=1975)

d1 = Dev(name="Alice")
d2 = Dev(name="Bob")

f1 = Freebie(item_name="Sticker", value=1, company=c1, dev=d1)
f2 = Freebie(item_name="Mug", value=10, company=c2, dev=d1)
f3 = Freebie(item_name="T-shirt", value=20, company=c1, dev=d2)

session.add_all([c1, c2, d1, d2, f1, f2, f3])
session.commit()

