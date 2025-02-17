import streamlit as st
from datetime import datetime
from sqlalchemy import text
import pandas as pd

def initialize_sale_state():
    """Initialize session state variables for multi-product sales"""
    if 'current_sale_items' not in st.session_state:
        st.session_state.current_sale_items = []
    if 'sale_customer_id' not in st.session_state:
        st.session_state.sale_customer_id = None
    if 'sale_date' not in st.session_state:
        st.session_state.sale_date = datetime.now()
    if 'editing_item_index' not in st.session_state:
        st.session_state.editing_item_index = None

def add_product_to_sale(product_id, product_desc, category, quantity, unit, price):
    """Add a product to the current sale"""
    st.session_state.current_sale_items.append({
        'product_id': product_id,
        'product_desc': product_desc,
        'category': category,
        'quantity': quantity,
        'unit': unit,
        'price': price,
        'total': quantity * price
    })

def clear_current_sale():
    """Clear the current sale from session state"""
    st.session_state.current_sale_items = []
    st.session_state.sale_customer_id = None

def show_recent_sales(db, customer_id=None):
    """Display recent sales, optionally filtered by customer"""
    try:
        if customer_id:
            query = text("""
                SELECT s.id, s.sale_date, c.name as customer, p.name as product,
                       cat.name as category, s.quantity, s.unit, s.price_per_unit
                FROM sales s
                JOIN customers c ON s.customer_id = c.id
                JOIN products p ON s.product_id = p.id
                JOIN categories cat ON p.category = cat.name
                WHERE s.customer_id = :customer_id
                ORDER BY s.sale_date DESC, s.id DESC
                LIMIT 10
            """)
            sales = db.execute(query, {"customer_id": customer_id}).fetchall()
        else:
            query = text("""
                SELECT s.id, s.sale_date, c.name as customer, p.name as product,
                       cat.name as category, s.quantity, s.unit, s.price_per_unit
                FROM sales s
                JOIN customers c ON s.customer_id = c.id
                JOIN products p ON s.product_id = p.id
                JOIN categories cat ON p.category = cat.name
                ORDER BY s.sale_date DESC, s.id DESC
                LIMIT 10
            """)
            sales = db.execute(query).fetchall()
        
        if sales:
            st.write("### Recent Orders")
            st.dataframe({
                "ID": [s.id for s in sales],
                "Date": [s.sale_date.strftime("%Y-%m-%d") for s in sales],
                "Customer": [s.customer for s in sales],
                "Product": [s.product for s in sales],
                "Category": [s.category for s in sales],
                "Quantity": [f"{s.quantity} {s.unit}" for s in sales],
                "Price/Unit": [f"${s.price_per_unit:.2f}" for s in sales],
                "Total": [f"${s.quantity * s.price_per_unit:.2f}" for s in sales],
            })
        else:
            st.info("No recent orders found")
    except Exception as e:
        st.error(f"Error loading recent orders: {str(e)}")

def new_sale_form(db):
    """Form for creating a new sale with multiple products"""
    st.subheader("New Order")
    
    # Initialize session state
    initialize_sale_state()
    
    # Customer selection
    customers = db.execute(text("SELECT id, name FROM customers ORDER BY name")).fetchall()
    customer_options = {c.name: c.id for c in customers}
    
    # Only show customer selection if no items added yet
    if not st.session_state.current_sale_items:
        selected_customer_name = st.selectbox(
            "Select Customer", 
            options=list(customer_options.keys()), 
            key="new_sale_customer"
        )
        st.session_state.sale_customer_id = customer_options[selected_customer_name]
        st.session_state.sale_date = st.date_input("Sale Date", datetime.now(), key="new_sale_date")
    else:
        # Show selected customer and date
        customer_name = [k for k, v in customer_options.items() 
                        if v == st.session_state.sale_customer_id][0]
        st.info(f"Customer: {customer_name}")
        st.info(f"Order Date: {st.session_state.sale_date.strftime('%Y-%m-%d')}")

    # Product search and selection
    st.write("### Add Product to Order")
    search_term = st.text_input("Search Product (ID, name, or category)", key="product_search")
    if search_term:
        products = db.execute(text("""
            SELECT p.id, p.name, p.description, c.name as category_name
            FROM products p 
            JOIN categories c ON p.category = c.name
            WHERE p.description ILIKE :search 
            OR CAST(p.id AS TEXT) LIKE :search
            OR c.name ILIKE :search
            OR p.name ILIKE :search
            ORDER BY p.description
        """), {"search": f"%{search_term}%"}).fetchall()

        if products:
            product_options = [
                f"{p.id} | {p.name} | {p.description} | {p.category_name}" 
                for p in products
            ]
            selected_product = st.selectbox(
                "Select Product", 
                product_options, 
                key="new_prod_product"
            )
            
            if selected_product:
                # Split the selected string into parts
                parts = selected_product.split(" | ")
                product_id = int(parts[0])
                product_desc = parts[2].strip()
                category = parts[3].strip()
                
                col1, col2 = st.columns(2)
                with col1:
                    quantity = st.number_input("Quantity", min_value=0.1, step=0.1, key="new_item_quantity")
                with col2:
                    unit = st.selectbox("Unit", ["L"], key="new_item_unit")
                
                price = st.number_input("Price per unit", min_value=0.1, step=0.1, key="new_item_price")
                
                if st.button("Add to Order", key="add_item_button"):
                    add_product_to_sale(product_id, product_desc, category, quantity, unit, price)
                    st.success("Product added to order!")
                    st.rerun()

    # Show current items in sale
    st.markdown("---")
    if st.session_state.current_sale_items:
        st.write("### Current Order Items")
        
        # Display each item with edit option
        for idx, item in enumerate(st.session_state.current_sale_items):
            col1, col2, col3 = st.columns([6, 2, 2])
            
            with col1:
                item_text = (f"{item['product_desc']} ({item['category']}) - "
                            f"{item['quantity']} {item['unit']} @ ${item['price']:.2f}/unit = "
                            f"${item['total']:.2f}")
                st.text(item_text)
            
            with col2:
                if st.button("Edit", key=f"edit_item_{idx}"):
                    st.session_state.editing_item_index = idx
            
            with col3:
                if st.button("Remove", key=f"remove_item_{idx}"):
                    st.session_state.current_sale_items.pop(idx)
                    st.rerun()
            
            # Show edit form if this item is being edited
            if st.session_state.editing_item_index == idx:
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        new_quantity = st.number_input(
                            "New Quantity",
                            value=float(item['quantity']),
                            min_value=0.1,
                            step=0.1,
                            key=f"edit_quantity_{idx}"
                        )
                        new_unit = st.selectbox(
                            "New Unit",
                            ["L"],
                            index=["L"].index(item['unit']),
                            key=f"edit_unit_{idx}"
                        )
                    with col2:
                        new_price = st.number_input(
                            "New Price per unit",
                            value=float(item['price']),
                            min_value=0.1,
                            step=0.1,
                            key=f"edit_price_{idx}"
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save Changes", key=f"save_edit_{idx}"):
                            st.session_state.current_sale_items[idx].update({
                                'quantity': new_quantity,
                                'unit': new_unit,
                                'price': new_price,
                                'total': new_quantity * new_price
                            })
                            st.session_state.editing_item_index = None
                            st.rerun()
                    with col2:
                        if st.button("Cancel", key=f"cancel_edit_{idx}"):
                            st.session_state.editing_item_index = None
                            st.rerun()
        
        total_sale = sum(item['total'] for item in st.session_state.current_sale_items)
        st.write(f"**Total Order Value:** ${total_sale:.2f}")
        st.markdown("---")

    # Submit or clear sale
    if st.session_state.current_sale_items:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Complete Order", key="submit_sale_button", type="primary"):
                try:
                    # Insert each sale item
                    for item in st.session_state.current_sale_items:
                        db.execute(text("""
                            INSERT INTO sales 
                            (product_id, customer_id, quantity, unit, price_per_unit, sale_date)
                            VALUES (:product_id, :customer_id, :quantity, :unit, :price, :sale_date)
                        """), {
                            "product_id": item['product_id'],
                            "customer_id": st.session_state.sale_customer_id,
                            "quantity": item['quantity'],
                            "unit": item['unit'],
                            "price": item['price'],
                            "sale_date": st.session_state.sale_date
                        })
                    db.commit()
                    st.success("Complete order recorded successfully!")
                    clear_current_sale()
                    st.rerun()
                except Exception as e:
                    db.rollback()
                    st.error(f"Error recording order: {str(e)}")
        
        with col2:
            if st.button("Clear Order", key="clear_sale_button", type="secondary"):
                clear_current_sale()
                st.rerun()

    # Show recent sales at the bottom
    st.markdown("---")
    show_recent_sales(db, st.session_state.sale_customer_id)

def edit_delete_sale(db):
    """Interface for editing or deleting sales"""
    st.subheader("Edit or Delete Order")
    
    # Customer selection for filtering
    customers = db.execute(text("SELECT id, name FROM customers ORDER BY name")).fetchall()
    customer_options = {c.name: c.id for c in customers}
    selected_customer_name = st.selectbox(
        "Select Customer",
        options=list(customer_options.keys()),
        key="edit_customer"
    )
    selected_customer_id = customer_options[selected_customer_name]
    
    # Sale ID input for editing
    sale_id = st.text_input("Enter Order ID to edit", key="edit_sale_id")
    if sale_id:
        try:
            sale = db.execute(text("""
                SELECT s.*, p.name as product_name, c.name as customer_name,
                       cat.name as category_name
                FROM sales s
                JOIN products p ON s.product_id = p.id
                JOIN customers c ON s.customer_id = c.id
                JOIN categories cat ON p.category = cat.name
                WHERE s.id = :sale_id
            """), {"sale_id": sale_id}).fetchone()
            
            if sale:
                st.write(f"Editing order for {sale.product_name} ({sale.category_name})")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_quantity = st.number_input("Quantity", value=float(sale.quantity), key="edit_quantity")
                    new_unit = st.selectbox("Unit", ["L"], 
                                          index=["L"].index(sale.unit),
                                          key="edit_unit")
                
                with col2:
                    new_price = st.number_input("Price per unit", 
                                              value=float(sale.price_per_unit),
                                              key="edit_price")
                
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("Update Order", key="update_sale_button"):
                        try:
                            db.execute(text("""
                                UPDATE sales
                                SET quantity = :quantity, unit = :unit, price_per_unit = :price
                                WHERE id = :sale_id
                            """), {
                                "quantity": new_quantity,
                                "unit": new_unit,
                                "price": new_price,
                                "sale_id": sale_id
                            })
                            db.commit()
                            st.success("Order updated successfully!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error updating order: {str(e)}")
                
                with col4:
                    delete_confirmed = st.checkbox("I confirm I want to delete this order",
                                                 key="delete_sale_confirm")
                    if delete_confirmed and st.button("Delete Order", 
                                                    type="secondary",
                                                    key="delete_sale_button"):
                        try:
                            db.execute(text("DELETE FROM sales WHERE id = :sale_id"), 
                                     {"sale_id": sale_id})
                            db.commit()
                            st.success("Order deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error deleting order: {str(e)}")
            else:
                st.error("Order not found")
        except Exception as e:
            st.error(f"Error fetching order: {str(e)}")
    
    # Show recent sales at the bottom
    st.markdown("---")
    show_recent_sales(db, selected_customer_id)

def search_sales(db):
    """Interface for searching sales records"""
    st.subheader("Search Orders")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        start_date = st.date_input("Start Date", key="search_start_date")
        end_date = st.date_input("End Date", key="search_end_date")
    
    with col2:
        # Customer filter
        customers = db.execute(text("SELECT id, name FROM customers ORDER BY name")).fetchall()
        customer_options = {"All Customers": None}  # Put "All" first
        customer_options.update({c.name: c.id for c in customers})  # Add other customers
        selected_customer = st.selectbox(
            "Customer",
            options=list(customer_options.keys()),
            key="search_customer"
        )
    
    with col3:
        # Product category filter
        categories = db.execute(text("SELECT name FROM categories ORDER BY name")).fetchall()
        category_options = [c.name for c in categories]
        category_options.insert(0, "All Categories")
        selected_category = st.selectbox(
            "Product Category",
            options=category_options,
            key="search_category"
        )
    
    # Build query based on filters
    query = """
        SELECT 
            s.id,
            s.sale_date,
            c.name as customer,
            p.name as product,
            cat.name as category,
            s.quantity,
            s.unit,
            s.price_per_unit,
            (s.quantity * s.price_per_unit) as total
        FROM sales s
        JOIN customers c ON s.customer_id = c.id
        JOIN products p ON s.product_id = p.id
        JOIN categories cat ON p.category = cat.name
        WHERE s.sale_date BETWEEN :start_date AND :end_date
    """
    params = {"start_date": start_date, "end_date": end_date}
    
    if selected_customer != "All Customers":
        query += " AND s.customer_id = :customer_id"
        params["customer_id"] = customer_options[selected_customer]
    
    if selected_category != "All Categories":
        query += " AND cat.name = :category"
        params["category"] = selected_category
    
    query += " ORDER BY s.sale_date DESC"
    
    # Execute search
    try:
        results = db.execute(text(query), params).fetchall()
        if results:
            # Convert to DataFrame for better display
            df = pd.DataFrame([{
                "ID": r.id,
                "Date": r.sale_date.strftime("%Y-%m-%d"),
                "Customer": r.customer,
                "Product": r.product,
                "Category": r.category,
                "Quantity": f"{r.quantity} {r.unit}",
                "Price/Unit": f"${r.price_per_unit:.2f}",
                "Total": f"${r.total:.2f}"
            } for r in results])
            
            # Show results
            st.dataframe(df, hide_index=True)
            
            # Show summary
            st.write(f"Found {len(results)} order records")
            total_revenue = sum(r.total for r in results)
            st.write(f"Total Revenue: ${total_revenue:,.2f}")
            
        else:
            st.info("No order records found matching your criteria")
            
    except Exception as e:
        st.error(f"Error searching order records: {str(e)}")

def show():
    """Main sales page"""
    st.title("Order Management")
    
    # Tab selection
    tab1, tab2, tab3 = st.tabs(["New Order", "Edit/Delete Order", "Search Orders"])
    
    with tab1:
        new_sale_form(st.session_state.db)
    
    with tab2:
        edit_delete_sale(st.session_state.db)
        
    with tab3:
        search_sales(st.session_state.db)