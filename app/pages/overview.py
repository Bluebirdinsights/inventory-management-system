import streamlit as st
from sqlalchemy import text
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import pandas as pd

def get_monthly_revenues(db):
    """Get revenue for current month and next 6 months"""
    try:
        query = text("""
            WITH RECURSIVE months AS (
                SELECT 
                    DATE_TRUNC('month', CURRENT_DATE) as month_start,
                    DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' - INTERVAL '1 day' as month_end
                UNION ALL
                SELECT 
                    month_start + INTERVAL '1 month',
                    month_end + INTERVAL '1 month'
                FROM months
                WHERE month_start < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '6 months'
            )
            SELECT 
                months.month_start,
                COALESCE(SUM(s.quantity * s.price_per_unit), 0) as revenue
            FROM months
            LEFT JOIN sales s ON DATE_TRUNC('month', s.sale_date) = months.month_start
            GROUP BY months.month_start
            ORDER BY months.month_start
        """)
        
        results = db.execute(query).fetchall()
        return [(r.month_start, float(r.revenue)) for r in results]
    except Exception as e:
        st.error(f"Error fetching monthly revenues: {str(e)}")
        return []

def get_daily_revenue_current_month(db):
    """Get daily revenue for current month"""
    try:
        query = text("""
            SELECT 
                sale_date::date,
                COALESCE(SUM(quantity * price_per_unit), 0) as revenue
            FROM sales 
            WHERE DATE_TRUNC('month', sale_date) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY sale_date
            ORDER BY sale_date
        """)
        results = db.execute(query).fetchall()
        
        days = [r.sale_date for r in results]
        revenues = [float(r.revenue) for r in results]
        
        return days, revenues
    except Exception as e:
        st.error(f"Error fetching daily revenue: {str(e)}")
        return [], []

def create_weekly_stock_matrix(stock_data, start_date, search_term=None):
    """Create a matrix of weekly stock levels with search functionality"""
    weekly_data = []
    current_week = int(start_date.strftime('%V'))
    
    # Get the start of current week (Monday)
    week_start = start_date - timedelta(days=start_date.weekday())
    
    for product_id, data in stock_data.items():
        # Apply search filter if provided
        if search_term and search_term.lower() not in (
            str(data['id']).lower() + 
            data['name'].lower() + 
            data['description'].lower() + 
            data['category'].lower()
        ):
            continue
            
        current_stock = data['current_stock']
        
        row_data = {
            'Product ID': str(data['id']),
            'Product': data['name'],
            'Category': data['category'],
            'Current Stock': f"{current_stock}"
        }
        
        # Calculate weekly stock levels
        week_date = week_start
        for week in range(26):
            week_end = week_date + timedelta(days=6)
            
            # Add production for this week
            production = sum(
                p['quantity'] for p in data['future_production']
                if week_date <= p['date'] <= week_end
            )
            
            # Subtract sales for this week
            sales = sum(
                s['quantity'] for s in data['future_sales']
                if week_date <= s['date'] <= week_end
            )
            
            current_stock += production - sales
            row_data[f'Week {week + current_week}'] = f"{current_stock}"
            
            week_date += timedelta(days=7)
        
        weekly_data.append(row_data)
    
    return pd.DataFrame(weekly_data)


def calculate_stock_levels(db, start_date, end_date):
    """Calculate current stock levels and future changes"""
    try:
        # Get all products
        products_query = text("""
            SELECT p.id, p.name, p.description, c.name as category
            FROM products p
            JOIN categories c ON p.category = c.name
            ORDER BY p.id
        """)
        products = db.execute(products_query).fetchall()
        
        stock_data = {}
        for product in products:
            # Get production data
            prod_query = text("""
                SELECT SUM(quantity) as total_production, unit
                FROM inventory
                WHERE product_id = :product_id
                AND production_date <= :today
                GROUP BY unit
            """)
            production = db.execute(prod_query, {
                "product_id": product.id,
                "today": start_date
            }).fetchone()
            
            # Get sales data
            sales_query = text("""
                SELECT SUM(quantity) as total_sales, unit
                FROM sales
                WHERE product_id = :product_id
                AND sale_date <= :today
                GROUP BY unit
            """)
            sales = db.execute(sales_query, {
                "product_id": product.id,
                "today": start_date
            }).fetchone()
            
            # Get future production
            future_prod_query = text("""
                SELECT production_date::date as date,
                       SUM(quantity) as quantity,
                       unit
                FROM inventory
                WHERE product_id = :product_id
                AND production_date > :start_date
                AND production_date <= :end_date
                GROUP BY production_date, unit
                ORDER BY production_date
            """)
            future_production = db.execute(future_prod_query, {
                "product_id": product.id,
                "start_date": start_date,
                "end_date": end_date
            }).fetchall()
            
            # Get future sales
            future_sales_query = text("""
                SELECT sale_date::date as date,
                       SUM(quantity) as quantity,
                       unit
                FROM sales
                WHERE product_id = :product_id
                AND sale_date > :start_date
                AND sale_date <= :end_date
                GROUP BY sale_date, unit
                ORDER BY sale_date
            """)
            future_sales = db.execute(future_sales_query, {
                "product_id": product.id,
                "start_date": start_date,
                "end_date": end_date
            }).fetchall()
            
            # Calculate current stock
            current_stock = (production.total_production if production else 0) - \
                          (sales.total_sales if sales else 0)
            
            stock_data[product.id] = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'category': product.category,
                'current_stock': current_stock,
                'unit': production.unit if production else 'L',  # default to liters
                'future_production': [
                    {'date': p.date, 'quantity': p.quantity} 
                    for p in future_production
                ],
                'future_sales': [
                    {'date': s.date, 'quantity': s.quantity} 
                    for s in future_sales
                ]
            }
        
        return stock_data
    except Exception as e:
        st.error(f"Error calculating stock levels: {str(e)}")
        return {}

def get_low_stock_products(stock_data):
    """Find products that will have negative stock"""
    low_stock = []
    
    for product_id, data in stock_data.items():
        current_stock = data['current_stock']
        min_stock = current_stock
        
        # Create a timeline of all stock changes
        timeline = []
        for prod in data['future_production']:
            timeline.append((prod['date'], prod['quantity']))
        for sale in data['future_sales']:
            timeline.append((sale['date'], -sale['quantity']))
        
        # Sort timeline by date
        timeline.sort(key=lambda x: x[0])
        
        # Calculate running stock level
        for _, change in timeline:
            current_stock += change
            min_stock = min(min_stock, current_stock)
        
        if min_stock < 0:
            low_stock.append({
                'Product ID': data['id'],
                'Product': data['name'],
                'Category': data['category'],
                'Current Stock': f"{data['current_stock']} {data['unit']}",
                'Minimum Future Stock': f"{min_stock} {data['unit']}"
            })
    
    return pd.DataFrame(low_stock) if low_stock else pd.DataFrame()

def get_expiring_products(db):
    """Get products expiring within 30 days"""
    try:
        query = text("""
            SELECT 
                p.id,
                p.name,
                p.description,
                c.name as category,
                i.quantity,
                i.unit,
                i.expiry_date
            FROM inventory i
            JOIN products p ON i.product_id = p.id
            JOIN categories c ON p.category = c.name
            WHERE i.expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
            AND i.quantity > 0
            ORDER BY i.expiry_date
        """)
        
        results = db.execute(query).fetchall()
        
        if results:
            return pd.DataFrame([{
                'Product ID': str(r.id),
                'Product': r.name,
                'Category': r.category,
                'Quantity': f"{r.quantity} {r.unit}",
                'Expiry Date': r.expiry_date.strftime('%Y-%m-%d')
            } for r in results])
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching expiring products: {str(e)}")
        return pd.DataFrame()

def get_weekly_expiry(db, num_weeks=15):
    """Calculate weekly expiring quantities using FIFO principle with product details"""
    try:
        start_date = datetime.now().date()
        current_week = int(start_date.strftime('%V'))
        end_date = start_date + timedelta(weeks=num_weeks)
        
        query = text("""
            WITH ProductionAndSales AS (
                SELECT 
                    p.id as product_id,
                    p.name,
                    p.description,
                    c.name as category,
                    i.production_date,
                    i.expiry_date,
                    i.quantity as prod_quantity,
                    i.unit,
                    COALESCE((
                        SELECT SUM(s.quantity)
                        FROM sales s
                        WHERE s.product_id = p.id
                        AND s.sale_date BETWEEN i.production_date AND i.expiry_date
                    ), 0) as sold_quantity
                FROM inventory i
                JOIN products p ON i.product_id = p.id
                JOIN categories c ON p.category = c.name
                WHERE i.expiry_date BETWEEN :start_date AND :end_date
            )
            SELECT 
                product_id,
                name,
                description,
                category,
                expiry_date,
                GREATEST(prod_quantity - sold_quantity, 0) as remaining_quantity,
                unit
            FROM ProductionAndSales
            WHERE prod_quantity - sold_quantity > 0
            ORDER BY expiry_date
        """)
        
        results = db.execute(query, {
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()
        
        # Create week buckets using actual week numbers
        weeks = []
        quantities = []
        weekly_details = {}  # Store product details for each week
        
        for week_offset in range(num_weeks):
            week_num = current_week + week_offset
            if week_num > 52:
                week_num -= 52
            
            week_start = start_date + timedelta(weeks=week_offset)
            week_end = week_start + timedelta(days=6)
            
            # Get products expiring this week
            week_products = [
                {
                    'Product ID': str(r.product_id),
                    'Product': r.name,
                    'Category': r.category,
                    'Quantity': f"{r.remaining_quantity} {r.unit}",
                    'Expiry Date': r.expiry_date.strftime('%Y-%m-%d')
                }
                for r in results
                if week_start <= r.expiry_date <= week_end
            ]
            
            week_quantity = sum(
                r.remaining_quantity 
                for r in results 
                if week_start <= r.expiry_date <= week_end
            )
            
            week_label = f"Week {week_num}"
            weeks.append(week_label)
            quantities.append(float(week_quantity))
            weekly_details[week_label] = week_products
        
        return weeks, quantities, weekly_details
        
    except Exception as e:
        st.error(f"Error calculating expiry data: {str(e)}")
        return [], [], {}

def show():
    """Main overview page"""
    st.title("Overview")
    
    try:
        # Get monthly revenues
        monthly_revenues = get_monthly_revenues(st.session_state.db)
        
        if monthly_revenues:
            # Create two columns with different widths
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Display current month revenue
                current_month_rev = monthly_revenues[0][1]
                st.metric(
                    "Current Month Revenue", 
                    f"${int(current_month_rev):,}",
                    help="Total revenue for current month"
                )
            
            with col2:
                # Display monthly revenue table horizontally
                st.subheader("Monthly Revenue Projection")
                # Create dictionary with months as columns
                revenue_dict = {
                    r[0].strftime("%b %Y"): f"${int(r[1]):,}" 
                    for r in monthly_revenues
                }
                # Convert to DataFrame with a single row
                revenue_df = pd.DataFrame([revenue_dict])
                
                st.dataframe(
                    revenue_df,
                    hide_index=True,
                    column_config={
                        col: st.column_config.Column(width="small")
                        for col in revenue_df.columns
                    }
                )
        
        # Daily revenue graph
        st.header("Daily Revenue")
        days, revenues = get_daily_revenue_current_month(st.session_state.db)
        
        if days and revenues:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=days,
                y=revenues,
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#2E86C1', width=2),
                marker=dict(size=8),
                hovertemplate=(
                    "<b>Date:</b> %{x}<br>" +
                    "<b>Revenue:</b> $%{y:,.2f}<br>" +
                    "<extra></extra>"  # This removes the trace name from tooltip
                )
            ))
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Revenue ($)",
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data available for current month")
        
        # Calculate date ranges for stock projections
        start_date = datetime.now().date()
        end_date = start_date + timedelta(weeks=26)
        
        # Get stock data
        stock_data = calculate_stock_levels(st.session_state.db, start_date, end_date)
        
        # Low Stock Alert
        st.header("Low Stock Alert")
        low_stock_df = get_low_stock_products(stock_data)
        if not low_stock_df.empty:
            st.dataframe(
                low_stock_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Product ID": st.column_config.Column(width="small"),
                    "Product": st.column_config.Column(width="medium"),
                    "Category": st.column_config.Column(width="medium"),
                    "Current Stock": st.column_config.Column(width="small"),
                    "Minimum Future Stock": st.column_config.Column(width="small")
                }
    )
        else:
            st.info("No products with projected negative stock levels")


        # Weekly Expiring Stock graph
        st.header("Weekly Expiring Stock")
        weeks, quantities, weekly_details = get_weekly_expiry(st.session_state.db)

        if weeks and quantities:
            # Store the weekly details in session state
            if 'expiry_details' not in st.session_state:
                st.session_state.expiry_details = weekly_details
            
            # Create tabs for graph and details
            tab1, tab2 = st.tabs(["Graph", "Details"])
            
            with tab1:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=weeks,
                    y=quantities,
                    name='Expiring Stock',
                    marker_color='#E74C3C',
                    hovertemplate=(
                        "<b>Week:</b> %{x}<br>" +
                        "<b>Expiring:</b> %{y:,.0f} kg<br>" +
                        "<extra></extra>"
                    )
                ))
                
                fig.update_layout(
                    xaxis_title="Week",
                    yaxis_title="Quantity (liters)",
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(showgrid=True),
                    yaxis=dict(showgrid=True)
                )
                
                # Add week selection
                selected_week = st.selectbox(
                    "Select week to see details:",
                    options=weeks,
                    key="expiry_week_select"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show details for selected week
                if selected_week:
                    week_data = weekly_details[selected_week]
                    if week_data:
                        st.write(f"#### Products Expiring in {selected_week}")
                        df = pd.DataFrame(week_data)
                        st.dataframe(
                            df,
                            hide_index=True,
                            use_container_width=True,
                            column_config={
                                "ID": st.column_config.Column(width="small"),
                                "Product": st.column_config.Column(width="medium"),
                                "Category": st.column_config.Column(width="medium"),
                                "Quantity": st.column_config.Column(width="small"),
                                "Expiry Date": st.column_config.Column(width="medium")
                            }
                        )
                    else:
                        st.info(f"No products expiring in {selected_week}")
            
            with tab2:
                # Show all weeks in expandable sections
                for week in weeks:
                    with st.expander(f"{week} - {len(weekly_details[week])} products"):
                        if weekly_details[week]:
                            df = pd.DataFrame(weekly_details[week])
                            st.dataframe(df, hide_index=True)
                        else:
                            st.info("No products expiring this week")
        else:
            st.info("No expiring stock in the next 15 weeks")


         # Weekly Stock Matrix
        st.header("26-Week Stock Projection")
            
        # Add search functionality
        search_term = st.text_input("Search by ID, Product, or Category")

        weekly_matrix = create_weekly_stock_matrix(stock_data, start_date, search_term)
        if not weekly_matrix.empty:
            st.markdown("""
                <style>
                [data-testid="stDataFrame"] {
                    width: 100%;
                }
                [data-testid="stDataFrame"] > div:first-child {
                    overflow: auto;
                }
                [data-testid="stDataFrame"] table {
                    border-collapse: collapse;
                }
                /* Make ID column sticky */
                [data-testid="stDataFrame"] th:nth-child(1),
                [data-testid="stDataFrame"] td:nth-child(1) {
                    position: sticky;
                    left: 0;
                    background-color: white;
                    z-index: 3;
                }
                /* Make Name column sticky and positioned after ID */
                [data-testid="stDataFrame"] th:nth-child(2),
                [data-testid="stDataFrame"] td:nth-child(2) {
                    position: sticky;
                    left: 80px;  /* Adjust based on ID column width */
                    background-color: white;
                    z-index: 2;
                }
                /* Add shadow after second column */
                [data-testid="stDataFrame"] td:nth-child(2),
                [data-testid="stDataFrame"] th:nth-child(2) {
                    box-shadow: 2px 0 5px -2px #888;
                }
                /* Keep headers above data */
                [data-testid="stDataFrame"] th {
                    position: sticky;
                    top: 0;
                    background-color: white;
                    z-index: 4;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Display as a single dataframe
            st.dataframe(
                weekly_matrix,
                hide_index=True,
                height=400,
                use_container_width=True,
                column_config={
                    "ID": st.column_config.Column(width=40),  # Set explicit width for ID column
                    "Product": st.column_config.Column(width=100)  # Set explicit width for Name column
                }
            )
        else:
            st.info("No stock projection data available")
            
    except Exception as e:
        st.error(f"Error loading overview: {str(e)}")

if __name__ == "__main__":
    show()