# Ecommerce ELT Pipeline

Portfolio project: ELT pipeline (dbt + BigQuery) over the Olist Brazilian e-commerce public dataset, feeding a downstream review-score prediction notebook. Built to demonstrate data-engineering + data-science skills for a student targeting a data scientist role.

## Language

**Customer**:
A real, distinct buyer, identified by `customer_unique_id`. Used for any customer-level analysis (lifetime behavior, repeat purchases).
_Avoid_: `customer_id` — that field is order-scoped (a new one is issued per order), not a stable person identifier.

**Order**:
A single checkout event placed by a Customer, identified by `order_id`. May contain multiple Order Items from different Sellers, and may have multiple payments.
_Avoid_: Purchase, transaction.

**Order Item**:
One product line within an Order, identified by (`order_id`, `order_item_id`). The unit at which price, freight, and Seller are recorded — not the Order as a whole.
_Avoid_: Line item, cart item.

**Seller**:
The merchant fulfilling a given Order Item, identified by `seller_id`. Distinct from Olist itself (the marketplace).
_Avoid_: Vendor, merchant.

**Delivery Delay**:
Derived metric: actual delivery date (`order_delivered_customer_date`) minus estimated delivery date (`order_estimated_delivery_date`) for an Order. Positive = late. Central input feature for the review-score prediction model. Null when the order was never delivered.
_Avoid_: Shipping time, lateness (without a precise definition).

**Review Score**:
The 1-5 rating a Customer leaves on an Order via `review_score`. The prediction target for the companion ML notebook.
_Avoid_: Rating, satisfaction score.
