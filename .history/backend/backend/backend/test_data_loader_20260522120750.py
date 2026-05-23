from backend.data_loader import load_csv_to_db

result = load_csv_to_db(
    "data/sales_data.csv"
)

print(result)