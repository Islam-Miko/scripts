from sqlalchemy import insert, text
from sqlalchemy.orm import Session

import models as m
from settings import SessionFactory


def insert_entities(session: Session)-> None:
    user_stmt = insert(m.User).values([
        {
            "id": 1,
            "first_name": "first",
            "last_name": "firstov",
            "role": m.UserRole.SELLER
        },
        {
            "id": 2,
            "first_name": "second",
            "last_name": "secondov",
            "role": m.UserRole.SELLER
        },
        {
            "id": 3,
            "first_name": "third",
            "last_name": "thirdov",
            "role": m.UserRole.BUYER
        },
        {
            "id": 4,
            "first_name": "fourth",
            "last_name": "fourthov",
            "role": m.UserRole.BUYER
        },
        {
            "id": 5,
            "first_name": "Fifth",
            "last_name": "Fifthov",
            "role": m.UserRole.BUYER
        },
    ])
    flower_stmt = insert(m.Flower).values([
        {
            "id": 1,
            "type": "Tulips"
        },
        {
            "id":2,
            "type": "Roses"
        }
    ])
    shade_stmt =insert(m.Shade).values([
        {
            "id": 1,
            "color": "#FF69B4"
        }, 
        {
            "id": 2,
            "color": "#5F51FE"
        },    
        {
            "id": 3,
            "color": "#FD3412"
        }
    ])
    session.execute(user_stmt)
    session.execute(flower_stmt)
    session.execute(shade_stmt)
    session.commit()

def insert_satelites(session: Session)-> None:
    shades_stmt = insert(m.FlowerShade).values([
        {
            "flower_id": 1,
            "shade_id": 1,
        },
        {
            "flower_id": 1,
            "shade_id": 2,
        },
        {
            "flower_id": 2,
            "shade_id": 3,
        },
        {
            "flower_id": 2,
            "shade_id": 1,
        }
    ])
    amount_stmt = insert(m.FlowerAmount).values([
        {
            "amount": 10,
            "flower_id": 1,
        },        {
            "amount": 10,
            "flower_id": 2,
        }
    ]) 
    price_stmt = insert(m.FlowerPrice).values([
        {
            "price": text("ROUND(200.00, 2)"),
            "flower_id": 1,
        },        {
            "price":  text("ROUND(100.00, 2)"),
            "flower_id": 2,
        }
    ])
    session.execute(price_stmt)
    session.execute(amount_stmt)
    session.execute(shades_stmt)
    session.commit()
    
def insert_links(session: Session)-> None:
    lot_stmt = insert(m.Lot).values([
        {
            "id": 1,
            "flower_id": 1,
            "seller_id": 1,
        },        {
            "id": 2,
            "flower_id": 2,
            "seller_id": 1,
        },        {
            "id": 3,
            "flower_id": 1,
            "seller_id": 2,
        },
    ])
    deal_stmt = insert(m.Deal).values([
        {
            "lot_id": 1,
            "buyer_id": 3,
            "amount": 1,
        },
        {
            "lot_id": 2,
            "buyer_id": 4,
            "amount": 3,
        },
        {
            "lot_id": 3,
            "buyer_id": 5,
            "amount": 2,
        },
        {
            "lot_id": 3,
            "buyer_id": 3,
            "amount": 6,
        }
    ])
    session.execute(lot_stmt)
    session.execute(deal_stmt)
    session.commit()
    
if __name__ == "__main__":
    session = SessionFactory()
    insert_entities(session)
    insert_satelites(session)
    insert_links(session)
    session.close()