# Restaurant Sales Dashboard 

## Overview
This project is an interactive sales dashboard for a fast food restaurant (Balaji Fast Food) built with Python and Streamlit. The dashboard provides insights into sales performance, payment methods, and top-selling menu items over a customizable date range.

## Features
- **Interactive Date Filtering**: Select any date range to analyze sales data
- **Key Metrics**: 
  - Total sales amount 
  - Estimated profit (assuming 30% margin)
- **Visualizations**:
  - Daily sales trend line chart
  - Payment method distribution pie chart
  - Top 10 selling items bar chart
- **Data Export**: Download filtered data as CSV
- **Mobile-Friendly**: Responsive design works on all devices

## Installation
1. Clone this repository
2. Install required packages:
   ```
   pip install pandas numpy streamlit plotly
   ```
3. Place your sales data CSV file (`Balaji Fast Food Sales.csv`) in the project directory

## Usage
Run the dashboard with:
```
streamlit run your_script_name.py
```

The dashboard will open in your default browser with:
- Date range filters in the sidebar
- Key metrics at the top
- Interactive charts below
- Raw data table
- Export button

## Data Requirements
The dashboard expects a CSV file with these columns (original names will be automatically renamed):
- `date`: Transaction date (format: YYYY/MM/DD or YYYY-MM-DD)
- `item_name`: Name of the menu item
- `item_type`: Category of the item
- `item_price`: Unit price
- `quantity`: Number of items sold
- `transaction_amount`: Total sale amount
- `transaction_type`: Payment method
- `received_by`: Staff who handled the transaction

## Customization
You can easily modify:
- Profit margin percentage in `calculate_profit()` function
- Chart colors and styles
- Dashboard layout and sections
- Language (currently mixed English/French)

## Screenshots
![sales Data Table](https://github.com/user-attachments/assets/6684b779-5e79-479f-9e6f-3ccff98794ee)
![Top_selling_items](https://github.com/user-attachments/assets/7eca93ee-f500-4613-a29d-2aeddbd59b84)
![Sales_payement_mode](https://github.com/user-attachments/assets/a11e74f9-f038-4e9e-a35c-758a6dd58e54)


## License

---

**Note**: This dashboard assumes a 30% profit margin for calculations. Adjust the `calculate_profit()` function if your actual margin differs.
