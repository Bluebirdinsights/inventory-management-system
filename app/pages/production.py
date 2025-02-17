import streamlit as st
from datetime import datetime, timedelta
from sqlalchemy import text
import pandas as pd

def initialize_production_state():
    """Initialize session state variables for multi-product production"""
    if 'current_production_items' not in st.session_state:
        st.session_state.current_production_items = []
    if 'production_date' not in st.session_state:
        st.session_state.production_date = datetime.now()
    if 'editing_production_index' not in st.session_state:    
        st.session_state.editing_production_index = None      

def validate_dates(production_date, expiry_date):
    """Validate production dates"""
    if production_date < datetime.now().date() - timedelta(days=7):  # Allow backdating up to a week
        st.error("Production date cannot be more than 7 days in the past")
        return False
    
    return True
    

def add_product_to_production(product_id, product_name, product_desc, category, quantity, unit, production_date, expiry_date):
    """Add a product to the current production batch"""
    st.session_state.current_production_items.append({
        'product_id': product_id,
        'product_name': product_name,
        'product_desc': product_desc,
        'category': category,
        'quantity': quantity,
        'unit': unit,
        'production_date': production_date,
        'expiry_date': expiry_date
    })

def clear_current_production():
    """Clear the current production from session state"""
    st.session_state.current_production_items = []

def show_recent_production(db, days_ago=30):
    """Display recent production records"""
    try:
        query = text("""
            SELECT i.id, i.production_date, i.expiry_date, p.name as product,
                   c.name as category, i.quantity, i.unit
            FROM inventory i
            JOIN products p ON i.product_id = p.id
            JOIN categories c ON p.category = c.name
            WHERE i.production_date >= :start_date
            ORDER BY i.production_date DESC, i.id DESC
            LIMIT 10
        """)
        
        start_date = datetime.now() - timedelta(days=days_ago)
        production_records = db.execute(query, {"start_date": start_date}).fetchall()
        
        if production_records:
            st.write("### Recent Production")
            st.dataframe({
                "ID": [r.id for r in production_records],
                "Production Date": [r.production_date.strftime("%Y-%m-%d") for r in production_records],
                "Expiry Date": [r.expiry_date.strftime("%Y-%m-%d") for r in production_records],
                "Product": [r.product for r in production_records],
                "Category": [r.category for r in production_records],
                "Quantity": [f"{r.quantity} {r.unit}" for r in production_records],
            })
        else:
            st.info("No recent production records found")
    except Exception as e:
        st.error(f"Error loading production records: {str(e)}")

def new_production_form(db):
    """Form for creating new production records with multiple products"""
    st.subheader("New Production")
    
    # Initialize session state
    initialize_production_state()
    
    # Only show date selection if no items added yet
    if not st.session_state.current_production_items:
        st.session_state.production_date = st.date_input(
            "Production Date", 
            datetime.now(),
            key="new_prod_date"
        )
    else:
        st.info(f"Production Date: {st.session_state.production_date.strftime('%Y-%m-%d')}")

    # Product search and selection
    st.write("### Add Product to Production")
    search_term = st.text_input("Search Product (ID, product, or category)", 
                               key="product_search_prod")
    if search_term:
        products = db.execute(text("""
            SELECT p.id, p.name, p.description, c.name as category_name, p.days_to_expiration
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
                    quantity = st.number_input("Quantity", min_value=0.1, 
                                            step=0.1, key="new_prod_quantity")
                with col2:
                    unit = st.selectbox("Unit", ["L"], 
                                    key="new_prod_unit")
                
                col3, col4 = st.columns(2)
                with col3:
                    production_date = st.date_input("Production Date",
                                                st.session_state.production_date,
                                                key="prod_date")
                with col4:
                    # Get days_to_expiration from products results
                    days_to_expiration = next(p.days_to_expiration for p in products if p.id == product_id)
                    # Calculate expiry date based on production date and days_to_expiration
                    default_expiry = production_date + timedelta(days=days_to_expiration)
                    expiry_date = st.date_input("Expiry Date",
                                            default_expiry,
                                            key="expiry_date",
                                            disabled=True)  # Make it read-only
                
                if st.button("Add to Production", key="add_prod_button"):
                    if validate_dates(production_date, expiry_date):
                        add_product_to_production(
                            product_id, parts[1].strip(), product_desc, category,
                            quantity, unit, production_date, expiry_date
                        )
                        st.success("Product added to production batch!")
                        st.rerun()

    # Show current items in production
    st.markdown("---")
    if st.session_state.current_production_items:
        st.write("### Current Production Items")
        
        # Display each item with edit option
        for idx, item in enumerate(st.session_state.current_production_items):
            col1, col2, col3 = st.columns([6, 2, 2])
            
            with col1:
                item_text = (f"{item['product_desc']} ({item['category']}) - "
                            f"{item['quantity']} {item['unit']}\n"
                            f"Production: {item['production_date'].strftime('%Y-%m-%d')}, "
                            f"Expiry: {item['expiry_date'].strftime('%Y-%m-%d')}")
                st.text(item_text)
            
            with col2:
                if st.button("Edit", key=f"edit_prod_item_{idx}"):
                    st.session_state.editing_production_index = idx
            
            with col3:
                if st.button("Remove", key=f"remove_prod_item_{idx}"):
                    st.session_state.current_production_items.pop(idx)
                    st.rerun()
            
            # Show edit form if this item is being edited
            if st.session_state.editing_production_index == idx:
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        new_quantity = st.number_input(
                            "New Quantity",
                            value=float(item['quantity']),
                            min_value=0.1,
                            step=0.1,
                            key=f"edit_prod_quantity_{idx}"
                        )
                        new_unit = st.selectbox(
                            "New Unit",
                            ["L"],
                            index=["L"].index(item['unit']),
                            key=f"edit_prod_unit_{idx}"
                        )
                    with col2:
                        new_production_date = st.date_input(
                            "New Production Date",
                            value=item['production_date'],
                            key=f"edit_prod_date_{idx}"
                        )
                        new_expiry_date = st.date_input(
                            "New Expiry Date",
                            value=item['expiry_date'],
                            key=f"edit_expiry_date_{idx}"
                        )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save Changes", key=f"save_prod_edit_{idx}"):
                            st.session_state.current_production_items[idx].update({
                                'quantity': new_quantity,
                                'unit': new_unit,
                                'production_date': new_production_date,
                                'expiry_date': new_expiry_date
                            })
                            st.session_state.editing_production_index = None
                            st.rerun()
                    with col2:
                        if st.button("Cancel", key=f"cancel_prod_edit_{idx}"):
                            st.session_state.editing_production_index = None
                            st.rerun()
        
        st.markdown("---")

    # Submit or clear production
    if st.session_state.current_production_items:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Complete Production", 
                        key="submit_prod_button", 
                        type="primary"):
                try:
                    # Insert each production item
                    for item in st.session_state.current_production_items:
                        db.execute(text("""
                            INSERT INTO inventory 
                            (product_id, quantity, unit, production_date, expiry_date)
                            VALUES (:product_id, :quantity, :unit, :prod_date, :exp_date)
                        """), {
                            "product_id": item['product_id'],
                            "quantity": item['quantity'],
                            "unit": item['unit'],
                            "prod_date": item['production_date'],
                            "exp_date": item['expiry_date']
                        })
                    db.commit()
                    st.success("Production batch recorded successfully!")
                    clear_current_production()
                    st.rerun()
                except Exception as e:
                    db.rollback()
                    st.error(f"Error recording production: {str(e)}")
        
        with col2:
            if st.button("Clear Production", 
                        key="clear_prod_button", 
                        type="secondary"):
                clear_current_production()
                st.rerun()

    # Show recent production at the bottom
    st.markdown("---")
    show_recent_production(db)

def edit_delete_production(db):
    """Interface for editing or deleting production records"""
    st.subheader("Edit or Delete Production")
    
    # Production ID input for editing
    production_id = st.text_input("Enter Production ID to edit", 
                                 key="edit_prod_id")
    if production_id:
        try:
            production = db.execute(text("""
                SELECT i.*, p.description as product_name,
                       c.name as category_name
                FROM inventory i
                JOIN products p ON i.product_id = p.id
                JOIN categories c ON p.category = c.name
                WHERE i.id = :prod_id
            """), {"prod_id": production_id}).fetchone()
            
            if production:
                # Get days_to_expiration for this product
                product_info = db.execute(text("""
                    SELECT days_to_expiration
                    FROM products
                    WHERE id = :product_id
                """), {"product_id": production.product_id}).fetchone()
                
                days_to_expiration = product_info.days_to_expiration

                st.write(f"Editing production for {production.product_name} "
                        f"({production.category_name})")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_quantity = st.number_input("Quantity", 
                                                value=float(production.quantity),
                                                key="edit_prod_quantity")
                    new_unit = st.selectbox("Unit", ["L"],
                                        index=["L"].index(production.unit),
                                        key="edit_prod_unit")
                
                with col2:
                    new_production_date = st.date_input("Production Date",
                                                    production.production_date,
                                                    key="edit_prod_date")
                    # Calculate new expiry date based on production date
                    new_expiry_date = new_production_date + timedelta(days=days_to_expiration)
                    st.date_input("Expiry Date",
                                new_expiry_date,
                                key="edit_expiry_date",
                                disabled=True)
                
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("Update Production", key="update_prod_button"):
                        try:
                            db.execute(text("""
                                UPDATE inventory
                                SET quantity = :quantity, unit = :unit,
                                    production_date = :prod_date,
                                    expiry_date = :exp_date
                                WHERE id = :prod_id
                            """), {
                                "quantity": new_quantity,
                                "unit": new_unit,
                                "prod_date": new_production_date,
                                "exp_date": new_expiry_date,
                                "prod_id": production_id
                            })
                            db.commit()
                            st.success("Production record updated successfully!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error updating production: {str(e)}")
                
                with col4:
                    delete_confirmed = st.checkbox("I confirm I want to delete this production record",
                                                 key="delete_prod_confirm")
                    if delete_confirmed and st.button("Delete Production",
                                                    type="secondary",
                                                    key="delete_prod_button"):
                        try:
                            db.execute(text("DELETE FROM inventory WHERE id = :prod_id"),
                                     {"prod_id": production_id})
                            db.commit()
                            st.success("Production record deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error deleting production: {str(e)}")
            else:
                st.error("Production record not found")
        except Exception as e:
            st.error(f"Error fetching production record: {str(e)}")
    
    # Show recent production at the bottom
    st.markdown("---")
    show_recent_production(db)

def search_production(db):
    st.subheader("Search Production Records")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", key="search_prod_start_date")
        end_date = st.date_input("End Date", key="search_prod_end_date")
    
    with col2:
        categories = db.execute(text("SELECT name FROM categories ORDER BY name")).fetchall()
        category_options = [c.name for c in categories]
        category_options.insert(0, "All Categories")
        selected_category = st.selectbox(
            "Product Category",
            options=category_options,
            key="search_prod_category"
        )
    
    # Add product search field
    search_term = st.text_input("Search by Product Name", key="search_prod_name")
    
    query = """
        SELECT 
            i.id,
            i.production_date,
            i.expiry_date,
            p.name as product,
            c.name as category,
            i.quantity,
            i.unit
        FROM inventory i
        JOIN products p ON i.product_id = p.id
        JOIN categories c ON p.category = c.name
        WHERE i.production_date BETWEEN :start_date AND :end_date
    """
    params = {"start_date": start_date, "end_date": end_date}
    
    if selected_category != "All Categories":
        query += " AND c.name = :category"
        params["category"] = selected_category
    
    if search_term:
        query += " AND p.name ILIKE :search"
        params["search"] = f"%{search_term}%"
    
    query += " ORDER BY i.production_date DESC"
    
    try:
        results = db.execute(text(query), params).fetchall()
        if results:
            df = pd.DataFrame([{
                "ID": r.id,
                "Production Date": r.production_date.strftime("%Y-%m-%d"),
                "Expiry Date": r.expiry_date.strftime("%Y-%m-%d"),
                "Product": r.product,
                "Category": r.category,
                "Quantity": f"{r.quantity} {r.unit}"
            } for r in results])
            
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "ID": st.column_config.Column(width="small"),
                    "Production Date": st.column_config.Column(width="medium"),
                    "Expiry Date": st.column_config.Column(width="medium"),
                    "Product": st.column_config.Column(width="large"),
                    "Category": st.column_config.Column(width="medium"),
                    "Quantity": st.column_config.Column(width="medium")
                }
            )
            st.write(f"Found {len(results)} production records")
            total_quantity = sum(r.quantity for r in results)
            st.write(f"Total Production: {total_quantity:,.2f}")
        else:
            st.info("No production records found matching your criteria")
    except Exception as e:
        st.error(f"Error searching production records: {str(e)}")

def show():
    """Main production page"""
    st.title("Production Management")
    
    # Tab selection
    tab1, tab2, tab3, = st.tabs(["New Production", "Edit/Delete Production", "Search"])
    
    with tab1:
        new_production_form(st.session_state.db)
    
    with tab2:
        edit_delete_production(st.session_state.db)
    
    with tab3:
        search_production(st.session_state.db)