import streamlit as st
from sqlalchemy import text
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

def get_summary_metrics(db, start_date, end_date):
    """Get summary metrics for the period"""
    try:
        query = text("""
            SELECT 
                COUNT(*) as total_sales,
                COALESCE(SUM(s.quantity * s.price_per_unit), 0) as total_revenue,
                COALESCE(SUM(s.quantity * p.base_price), 0) as total_cogs
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.sale_date BETWEEN :start_date AND :end_date
        """)
        
        result = db.execute(query, {
            "start_date": start_date,
            "end_date": end_date
        }).fetchone()
        
        db.commit()
        
        revenue = float(result.total_revenue)
        cogs = float(result.total_cogs)
        gross_profit = revenue - cogs
        
        return {
            "total_sales": result.total_sales,
            "total_revenue": revenue,
            "total_cogs": cogs,
            "gross_profit": gross_profit
        }
    except Exception as e:
        db.rollback()
        st.error(f"Error fetching summary metrics: {str(e)}")
        return {
            "total_sales": 0, 
            "total_revenue": 0, 
            "total_cogs": 0,
            "gross_profit": 0
        }

def get_daily_data(db, start_date, end_date):
    """Get daily revenue and COGS data"""
    try:
        query = text("""
            SELECT 
                s.sale_date,
                COALESCE(SUM(s.quantity * s.price_per_unit), 0) as revenue,
                COALESCE(SUM(s.quantity * p.base_price), 0) as cogs
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.sale_date BETWEEN :start_date AND :end_date
            GROUP BY s.sale_date
            ORDER BY s.sale_date;
        """)
        
        results = db.execute(query, {
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()
        
        dates = [r.sale_date.strftime('%Y-%m-%d') for r in results]
        revenues = [float(r.revenue) for r in results]
        cogs = [float(r.cogs) for r in results]
        
        return dates, revenues, cogs
    except Exception as e:
        db.rollback()
        st.error(f"Error fetching daily data: {str(e)}")
        return [], [], []

def get_sales_by_group(db, start_date, end_date):
    """Get daily sales data by product category"""
    try:
        query = text("""
            SELECT 
                s.sale_date,
                c.name as category_name,
                COALESCE(SUM(s.quantity * s.price_per_unit), 0) as revenue
            FROM sales s
            JOIN products p ON s.product_id = p.id
            JOIN categories c ON p.category = c.name
            WHERE s.sale_date BETWEEN :start_date AND :end_date
            GROUP BY s.sale_date, c.name
            ORDER BY s.sale_date, c.name;
        """)
        
        results = db.execute(query, {
            "start_date": start_date,
            "end_date": end_date
        }).fetchall()
        
        data = {
            'date': [r.sale_date.strftime('%Y-%m-%d') for r in results],
            'group': [r.category_name for r in results],
            'revenue': [float(r.revenue) for r in results]
        }
        
        return data
    except Exception as e:
        db.rollback()
        st.error(f"Error fetching group sales data: {str(e)}")
        return {'date': [], 'group': [], 'revenue': []}

def show():
    """Main reports page"""
    st.title("Projected Sales Overview")
    
    # Get first and last day of current month
    today = datetime.now()
    first_day = today.replace(day=1)
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    
    # Date range selection
    st.sidebar.header("Date Range")
    start_date = st.sidebar.date_input(
        "Start Date", 
        value=first_day,
        min_value=datetime(2024, 1, 1),
        max_value=datetime(2025, 12, 31)
    )
    end_date = st.sidebar.date_input(
        "End Date", 
        value=last_day,
        min_value=datetime(2024, 1, 1),
        max_value=datetime(2025, 12, 31)
    )
    
    # Get summary metrics
    metrics = get_summary_metrics(st.session_state.db, start_date, end_date)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Orders", f"{metrics['total_sales']:,}")
    with col2:
        st.metric("Total Projected Revenue", f"${metrics['total_revenue']:,.2f}")
    with col3:
        st.metric("Total Projected COGS", f"${metrics['total_cogs']:,.2f}")
    with col4:
        st.metric("Projected Gross Profit", f"${metrics['gross_profit']:,.2f}")
    
    # Get daily data
    dates, revenues, cogs = get_daily_data(st.session_state.db, start_date, end_date)
    
    # Revenue Trend
    st.subheader("Daily Revenue")
    if dates and revenues:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=dates,
            y=revenues,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#2E86C1', width=2),
            marker=dict(size=8)
        ))
        
        fig1.update_layout(
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    # COGS Trend
    st.subheader("Daily COGS")
    if dates and cogs:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=dates,
            y=cogs,
            mode='lines+markers',
            name='COGS',
            line=dict(color='#E74C3C', width=2),
            marker=dict(size=8)
        ))
        
        fig2.update_layout(
            xaxis_title="Date",
            yaxis_title="COGS ($)",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Sales by Product Category
    st.subheader("Orders by Product Category")
    group_data = get_sales_by_group(st.session_state.db, start_date, end_date)
    
    if group_data['date']:
        fig3 = px.bar(
            group_data,
            x='date',
            y='revenue',
            color='group',
            title="Daily Sales by Product Category",
            labels={'date': 'Date', 
                   'revenue': 'Revenue ($)', 
                   'group': 'Product Category'}
        )
        
        fig3.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            barmode='stack'
        )
        
        st.plotly_chart(fig3, use_container_width=True)

if __name__ == "__main__":
    show()