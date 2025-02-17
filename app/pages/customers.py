import streamlit as st
from sqlalchemy import text
import pandas as pd

def show_customers(db):
    """Display all customers"""
    try:
        query = text("""
            SELECT id, name, contact_info
            FROM customers
            ORDER BY name
        """)
        customers = db.execute(query).fetchall()
        
        if customers:
            st.write("### All Customers")
            st.dataframe({
                "ID": [c.id for c in customers],
                "Name": [c.name for c in customers],
                "Contact Info": [c.contact_info for c in customers]
            }, hide_index=True)
        else:
            st.info("No customers found")
    except Exception as e:
        st.error(f"Error loading customers: {str(e)}")

def new_customer_form(db):
    """Form for creating a new customer"""
    st.subheader("New Customer")

    # Customer details
    name = st.text_input("Customer Name")
    contact_info = st.text_area("Contact Information")
    
    if st.button("Add Customer", type="primary"):
        if name:  # Basic validation
            try:
                # Check if customer already exists
                existing = db.execute(
                    text("SELECT id FROM customers WHERE name = :name"),
                    {"name": name}
                ).fetchone()
                
                if existing:
                    st.error("A customer with this name already exists")
                else:
                    # Insert new customer
                    db.execute(
                        text("""
                            INSERT INTO customers (name, contact_info)
                            VALUES (:name, :contact_info)
                        """),
                        {"name": name, "contact_info": contact_info}
                    )
                    db.commit()
                    st.success("Customer added successfully!")
                    st.rerun()
            except Exception as e:
                db.rollback()
                st.error(f"Error adding customer: {str(e)}")
        else:
            st.error("Customer name is required")

def edit_delete_customer(db):
    """Interface for editing or deleting customers"""
    st.subheader("Edit or Delete Customer")
    
    # Get all customers for selection
    customers = db.execute(text("""
        SELECT id, name, contact_info 
        FROM customers 
        ORDER BY name
    """)).fetchall()
    
    if customers:
        customer_options = {c.name: (c.id, c.contact_info) for c in customers}
        selected_customer = st.selectbox(
            "Select Customer",
            options=list(customer_options.keys()),
            key="edit_customer"
        )
        
        if selected_customer:
            customer_id, current_contact = customer_options[selected_customer]
            
            # Edit form
            new_name = st.text_input("Name", value=selected_customer)
            new_contact = st.text_area("Contact Information", value=current_contact)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Customer", key="update_customer"):
                    try:
                        db.execute(text("""
                            UPDATE customers
                            SET name = :name, contact_info = :contact
                            WHERE id = :id
                        """), {
                            "name": new_name,
                            "contact": new_contact,
                            "id": customer_id
                        })
                        db.commit()
                        st.success("Customer updated successfully!")
                        st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Error updating customer: {str(e)}")
            
            with col2:
                # Check if customer has any sales before allowing deletion
                sales = db.execute(text("""
                    SELECT COUNT(*) as count
                    FROM sales
                    WHERE customer_id = :id
                """), {"id": customer_id}).scalar()
                
                delete_confirmed = st.checkbox(
                    "I confirm I want to delete this customer",
                    key="delete_customer_confirm"
                )
                
                delete_button = st.button(
                    "Delete Customer",
                    key="delete_customer",
                    type="secondary",
                    disabled=sales > 0
                )
                
                if sales > 0:
                    st.warning(
                        "This customer cannot be deleted because they have "
                        f"{sales} sales records"
                    )
                
                if delete_confirmed and delete_button:
                    try:
                        db.execute(
                            text("DELETE FROM customers WHERE id = :id"),
                            {"id": customer_id}
                        )
                        db.commit()
                        st.success("Customer deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Error deleting customer: {str(e)}")

def search_customers(db):
    st.subheader("Search Customers")
    
    search_term = st.text_input("Search by Name or Contact Info")
    
    query = """
        SELECT 
            c.id,
            c.name,
            c.contact_info,
            COUNT(DISTINCT s.id) as total_orders,
            SUM(s.quantity * s.price_per_unit) as total_revenue
        FROM customers c
        LEFT JOIN sales s ON c.id = s.customer_id
        WHERE 1=1
    """
    params = {}
    
    if search_term:
        query += """
            AND (
                c.name ILIKE :search 
                OR c.contact_info ILIKE :search
            )
        """
        params["search"] = f"%{search_term}%"
    
    query += " GROUP BY c.id, c.name, c.contact_info ORDER BY c.name"
    
    try:
        results = db.execute(text(query), params).fetchall()
        if results:
            df = pd.DataFrame([{
                "ID": r.id,
                "Name": r.name,
                "Contact Info": r.contact_info,
                "Total Orders": r.total_orders,
                "Total Revenue": f"${r.total_revenue:.2f}" if r.total_revenue else "$0.00"
            } for r in results])
            
            st.dataframe(df, hide_index=True)
            st.write(f"Found {len(results)} customers")
        else:
            st.info("No customers found matching your criteria")
    except Exception as e:
        st.error(f"Error searching customers: {str(e)}")

def show():
    """Main customers page"""
    st.title("Customer Management")
    
    # Tab selection
    tab1, tab2, tab3 = st.tabs(["New Customer", "Edit/Delete Customer", "Search Customer"])
    
    with tab1:
        new_customer_form(st.session_state.db)
        st.markdown("---")
        show_customers(st.session_state.db)
    
    with tab2:
        edit_delete_customer(st.session_state.db)
        st.markdown("---")
        show_customers(st.session_state.db)
    with tab3:
        search_customers(st.session_state.db)
        
