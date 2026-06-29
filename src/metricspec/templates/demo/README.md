# MetricSpec Demo

This demo shows one passing metric contract and one intentionally failing
contract for net revenue by region.

Run the passing contract:

```bash
metricspec run contracts/net_revenue_by_region.pass.yaml
```

Run the failing contract to inspect diagnostics:

```bash
metricspec run contracts/net_revenue_by_region.fail.yaml
```

The failing query omits refunds, so MetricSpec reports a result mismatch.
