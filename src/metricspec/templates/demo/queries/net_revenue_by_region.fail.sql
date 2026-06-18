select
  o.region,
  sum(o.gross_revenue - o.discount - o.tax) as net_revenue
from orders o
where o.is_test_order = false
group by o.region
order by o.region
