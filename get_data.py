from settings import SessionFactory
import models as m
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, func
import pprint



def main()-> None:
    session: Session = SessionFactory()
    Buyer = aliased(m.User)
    Seller = aliased(m.User)
    active_prices = (
        select(m.FlowerPrice.flower_id, m.FlowerPrice.price)
        .where(m.FlowerPrice.start_date <= func.now(), m.FlowerPrice.end_date > func.now())
        .subquery()
    )
    buyers_info = (
        select(
            m.Lot.seller_id, m.Deal.buyer_id, func.sum(m.Deal.amount * active_prices.c.price).label("total")
        )
        .select_from(m.Deal)
        .join(m.Lot, onclause=m.Lot.id == m.Deal.lot_id)
        .join(active_prices, onclause=active_prices.c.flower_id==m.Lot.flower_id)
        .group_by(m.Lot.seller_id, m.Deal.buyer_id)
    ).subquery()
    stmt = (
        select(
            func.concat(
                Seller.first_name, " ", Seller.last_name
            ).label("seller"),
            func.array_agg(
                func.json_build_object(
                    "buyer", func.concat(Buyer.first_name, " ", Buyer.last_name),
                    "total", buyers_info.c.total,
                )
            )
        ).select_from(
            buyers_info
        ).join(Seller, onclause=Seller.id == buyers_info.c.seller_id)
        .join(Buyer, onclause=Buyer.id == buyers_info.c.buyer_id)
        .group_by(
            func.concat(Seller.first_name, " ", Seller.last_name)
        )
    )
    try:
        result = session.execute(stmt)
        data = result.fetchall()
    except Exception as e:
        pass
    finally:
        session.close()
    pprint.pprint(data)
    
if __name__ == "__main__":
    main()