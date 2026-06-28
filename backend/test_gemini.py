import pandas as pd

from backend.insight_generator import generate_insights

df = pd.DataFrame({

    "region": [
        "South",
        "East",
        "North",
        "West"
    ],

    "total_sales": [
        3200,
        2600,
        2375,
        2000
    ]

})

result = generate_insights(

    "Show total sales by region",

    df

)

print("\nINSIGHTS:\n")

print(result)