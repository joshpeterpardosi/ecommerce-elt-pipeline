# Customer grain uses `customer_unique_id`, not `customer_id`

Olist's `customer_id` looks like a customer primary key but is actually issued per order — the same real person gets a new `customer_id` on every purchase. All customer-level marts and ML features (repeat-purchase counts, lifetime value, RFM-style aggregates) are built on `customer_unique_id` instead. Getting this wrong silently inflates customer counts and hides repeat buyers, and the mistake is easy to make since `customer_id` reads as the obvious key — worth recording so it isn't "fixed" back later.
