SELECT CONCAT(s.first_name, ' ', s.last_name) AS seller,
    ARRAY_AGG(
        json_build_object(
            'buyer', b.first_name || ' ' || b.last_name,
            'total', total
        ) 
    ) AS buyer_infos
FROM (
    SELECT l.seller_id, d.buyer_id, SUM(d.amount * fp.price) AS total 
    FROM deals d 
    JOIN lots l ON l.id = d.lot_id
    JOIN (
        select p.flower_id, p.price from flower_prices p
        where now() >= p.start_date and now() < p.end_date
    ) fp ON fp.flower_id = l.flower_id
    GROUP BY l.seller_id, d.buyer_id
) i 
JOIN users s ON s.id = i.seller_id
JOIN users b ON b.id = i.buyer_id
GROUP BY CONCAT(s.first_name, ' ', s.last_name);
