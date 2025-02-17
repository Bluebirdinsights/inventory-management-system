# Technical Overview

## System Architecture

### Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Data Visualization**: Plotly, Plotly Express

### Database Schema

#### Core Tables
1. **categories**
   - Primary identifier for product categories
   - Tracks creation timestamp
   - Referenced by products table

2. **products**
   - Stores product information and base pricing
   - Includes expiration calculation (days_to_expiration)
   - Links to categories via foreign key
   - Maintains creation and update timestamps

3. **inventory**
   - Records production batches
   - Automatically calculates expiry_date based on product's days_to_expiration
   - Links to products via foreign key
   - Tracks production and expiry dates

4. **sales** (Orders)
   - Manages customer orders
   - Links to both products and customers
   - Includes quantity and pricing information
   - Maintains order status tracking

5. **customers**
   - Stores customer information
   - Includes contact details
   - Referenced by sales records

## Key Features

### Production Management
- Schedule and track production batches
- Automatic expiry date calculation based on product type
- Multi-product production entry
- Production modification with date constraints
- Activity-based deletion protection

### Inventory Tracking
- Real-time stock levels
- Future stock projections (26-week view)
- Low stock alerts
- Expiry tracking and warnings
- Stock level calculations incorporating:
  - Current inventory
  - Scheduled production
  - Confirmed orders

### Order Management
- Multi-product order entry
- Real-time total calculations
- Order modification capabilities
- Activity-based deletion protection
- Customer-specific order history

## Key Algorithms

### Stock Projection System
```python
def calculate_stock_levels(start_date, end_date):
    1. Get current stock levels
       - Sum all production quantities
       - Subtract all sold quantities
    
    2. Add future production
       - Include all scheduled production
       - Consider production completion dates
    
    3. Subtract future sales
       - Consider all confirmed orders
       - Account for delivery dates
    
    4. Calculate weekly projections
       - Aggregate by week for 26 weeks
       - Track minimum stock levels
       - Generate low stock alerts
```

### Expiry Tracking
```python
def handle_expiry():
    1. Product Setup
       - Define days_to_expiration per product category
       - Store at product level
    
    2. Production Entry
       - Calculate expiry_date automatically
       - expiry_date = production_date + days_to_expiration
    
    3. Expiry Monitoring
       - Track weekly expiring quantities
       - Group by product and category
       - Provide early warnings
```

## Query Optimization
- Use of Common Table Expressions (CTEs) for complex calculations
- Efficient date-based filtering
- Optimized joins for inventory calculations
- Strategic use of indexes on:
  - Primary keys
  - Foreign key relationships
  - Date fields for range queries

## Future Enhancements
- User authentication and authorization
- Multi-tenant support
- Advanced reporting features
- API endpoints for external integration
- Batch import/export capabilities