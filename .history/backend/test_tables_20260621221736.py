from backend.insight_generator import generate_insights
import pandas as pd

df = pd.DataFrame({
    "region": ["South", "East", "North", "West"],
    "total_sales": [3200, 2600, 2375, 2000]
})

print(
    generate_insights(
        "Show total sales by region",
        df
    )
)