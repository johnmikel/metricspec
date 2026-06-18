select
  o.region,
  sum(o.gross_revenue - o.discount - o.tax - coalesce(r.refund_amount, 0)) as net_revenue
from orders o
left join refunds r on r.order_id = o.order_id
where o.is_test_order = false
group by o.region
order by o.region
