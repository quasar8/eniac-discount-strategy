import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns


 
sns.set_theme(style="whitegrid")
 
TEAL = "#8FA8A3"
RED = "#C0504D"
NAVY = "#1F3B6E"
 
# ------------------------------------------------------------------
# prepare the merged orderlines + products table with revenue and discount
# ------------------------------------------------------------------
 
orderlines_qu_copy = orderlines_qu.copy()
orderlines_qu_copy["unit_price_total"] = orderlines_qu_copy["product_quantity"] * orderlines_qu_copy["unit_price"]
orderlines_qu_copy["date"] = pd.to_datetime(orderlines_qu_copy["date"])
orderlines_qu_copy["month"] = orderlines_qu_copy["date"].dt.to_period("M").astype(str)
 
products_orderlines = orderlines_qu_copy.merge(products_cl, how="inner", on="sku")[
    ["id_order", "sku", "unit_price", "unit_price_total", "product_quantity", "month", "price", "name", "desc", "type"]
]
products_orderlines["discount"] = products_orderlines["price"] - products_orderlines["unit_price"]
products_orderlines["discount_pct"] = (products_orderlines["discount"] / products_orderlines["price"]).clip(lower=0)
 
# attach the primary (first) category from product_category_df to every orderline
category_lookup = product_category_df[["sku", "category"]].copy()
category_lookup["primary_category"] = category_lookup["category"].str.split(",").str[0].str.strip()
products_orderlines = products_orderlines.merge(category_lookup[["sku", "primary_category"]], how="left", on="sku")
 
 
# ------------------------------------------------------------------
# Chart 1: Does discount intensity drive revenue growth? (revenue vs. promo depth over time)
# ------------------------------------------------------------------
 
monthly = products_orderlines.groupby("month", as_index=False).agg(
    total_revenue=("unit_price_total", "sum"),
    promo_investment_depth=("discount", lambda x: x.clip(lower=0).sum()),
).sort_values("month")
 
fig, ax1 = plt.subplots(figsize=(11, 5.5))
sns.barplot(data=monthly, x="month", y="total_revenue", color=TEAL, ax=ax1)
ax1.set_ylabel("Total Revenue Realized (\u20ac)", color=NAVY, fontweight="bold")
ax1.set_xlabel("Trading Month Timeline")
ax1.tick_params(axis="x", rotation=45)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"\u20ac{x:,.0f}"))
 
ax2 = ax1.twinx()
sns.lineplot(data=monthly, x="month", y="promo_investment_depth", color=RED, marker="o",
             linewidth=2, ax=ax2, label="Catalog Markdown Volume")
ax2.set_ylabel("Promotional Investment Depth (\u20ac)", color=RED, fontweight="bold")
ax2.grid(False)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"\u20ac{x:,.0f}"))
 
ax1.set_title("Eniac Strategic Review: Does Discount Intensity Drive Revenue Growth?", fontweight="bold")
ax2.legend(loc="upper right")
fig.tight_layout()
plt.show()

 
 
# ------------------------------------------------------------------
# Chart 2: Strategic Re-Allocation: Revenue vs. Discount Depth by Category
# ------------------------------------------------------------------

category_order = ["storage", "smartphone", "tablet", "smartwatch", "headset", "desktop", "speaker", "case"]
 
by_category = products_orderlines.groupby("primary_category", as_index=False).agg(
    total_revenue=("unit_price_total", "sum"),
    avg_discount_rate=("discount_pct", "mean"),
)
by_category = by_category[by_category["primary_category"].isin(category_order)]
by_category["primary_category"] = pd.Categorical(by_category["primary_category"], categories=category_order, ordered=True)
by_category = by_category.sort_values("primary_category")
by_category["category_label"] = by_category["primary_category"].astype(str).str.capitalize()
 
fig, ax1 = plt.subplots(figsize=(11, 5.5))
sns.barplot(data=by_category, x="category_label", y="total_revenue", color=TEAL, ax=ax1)
ax1.set_ylabel("Total Realized Revenue (\u20ac)", color=NAVY, fontweight="bold")
ax1.set_xlabel("Strategic Product Categories")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"\u20ac{x:,.0f}"))
 
ax2 = ax1.twinx()
sns.lineplot(data=by_category, x="category_label", y=by_category["avg_discount_rate"] * 100,
             color=RED, marker="o", linewidth=2, ax=ax2)
ax2.set_ylabel("Average Discount Rate (%)", color=RED, fontweight="bold")
ax2.grid(False)
 
ax1.set_title("Strategic Re-Allocation: Revenue vs. Discount Depth by Category", fontweight="bold")
fig.tight_layout()
plt.show()

