# ZAKA — Data Analytics in Commerce
## Predicting Customer Demand to Help UAE Retailers Plan Their Inventory

Professional interactive dashboard based on the verified capstone outputs.

### Interface
- Icon-based top navigation; no left sidebar.
- ZAKA-inspired orange → amber → yellow visual system.
- Interactive customer filters and verified inventory-planning outputs.
- Week 4, Week 6 and Week 7 verified CSV outputs integrated.
- Public-data evidence, assumptions, limitations and future UAE implementation are clearly separated.

### Pages
Overview · Sales · Products · Customers · Demand Forecast · Inventory Insights · Strategy · Data Quality · About

### Export a whole page to PDF
Use the **Export current page as PDF** control at the top. It opens the browser print dialog for the full current dashboard page. Select **Save as PDF**, use Landscape when helpful, and enable Background graphics.

### Run on Windows
Double-click `run_app.bat`.

### Run on macOS
Double-click `run_app.command`.

### Terminal
`python3 launcher.py`

Python 3 is required; the launcher installs missing Python packages automatically.


### Final accuracy corrections before deployment
- Products / ABC uses **unit-demand-based ABC**, not the earlier revenue-based classification.
- Demand Forecast uses the **final product-level 4-Week Moving Average** results and the final aggregate Category A comparison against Prophet.
- Inventory is named **Inventory Insights** and only verified Week 6 summary/backtest outputs are shown. The older product-level JSON calculations were removed.
- Customer segmentation validation values and the data-quality ledger are rendered explicitly for reliable PDF export.
- The official project title is used consistently throughout the app.

### Important scope note
Online Retail II is public international retail data used as a proof of concept. It is not UAE retailer transaction data. A real UAE deployment requires local retailer sales, stock, supplier, ERP/POS and operational data.
