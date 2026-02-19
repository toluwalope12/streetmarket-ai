# Enrich Policy Setup

To enable the `ENRICH` command in ES|QL, create and execute an enrich policy for the `official_prices` index.

Run these commands in Kibana Dev Tools:

```json
PUT /_enrich/policy/official_prices_policy
{
  "match": {
    "indices": "official_prices",
    "match_field": "product_name",
    "enrich_fields": ["wholesale_price", "retail_price"]
  }
}


POST /_enrich/policy/official_prices_policy/_execute

# Verify the policy exists:
GET /_enrich/policy/official_prices_policy

