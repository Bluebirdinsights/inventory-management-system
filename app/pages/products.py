import streamlit as st
from sqlalchemy import text
import pandas as pd

def show_products(db, search_term=None):
    """Display products, optionally filtered by search term"""
    try:
        if search_term:
            query = text("""
                SELECT p.id, p.name, p.description, c.name as category_name, p.base_price
                FROM products p
                JOIN categories c ON p.category = c.name
                WHERE p.description ILIKE :search 
                OR CAST(p.id AS TEXT) LIKE :search
                OR p.name ILIKE :search
                OR c.name ILIKE :search
                ORDER BY p.id
            """)
            products = db.execute(query, {"search": f"%{search_term}%"}).fetchall()
        else:
            query = text("""
                SELECT p.id, p.name, p.description, c.name as category_name, p.base_price
                FROM products p
                JOIN categories c ON p.category = c.name
                ORDER BY p.id
            """)
            products = db.execute(query).fetchall()
        
        if products:
            st.write("### Product List")
            st.dataframe({
                "ID": [str(p.id) for p in products],
                "Name": [p.name for p in products],
                "Description": [p.description for p in products],
                "Category": [p.category_name for p in products],
                "Base Price": [f"${p.base_price:.2f}" for p in products]
            }, hide_index=True)
        else:
            if search_term:
                st.info("No products found matching your search")
            else:
                st.info("No products found")
    except Exception as e:
        st.error(f"Error loading products: {str(e)}")

def get_categories(db):
    """Get list of product categories"""
    try:
        categories = db.execute(text("""
            SELECT name FROM categories ORDER BY name
        """)).fetchall()
        return [c.name for c in categories]
    except Exception as e:
        st.error(f"Error loading categories: {str(e)}")
        return []

def new_product_form(db):
    """Form for creating a new product"""
    st.subheader("New Product")
    
    categories = get_categories(db)
    
    # Product details
    col1, col2 = st.columns(2)
    with col1:
        product_id = st.text_input("Product ID")
        name = st.text_input("Product Name")
    
    with col2:
        category = st.selectbox("Category", options=categories)
        base_price = st.number_input("Base Price", min_value=0.0, step=0.1)
    
    days_to_expiration = st.number_input("Days to Expiration", 
                                    min_value=1,
                                    value=90,  # Default value
                                    step=1,
                                    help="Number of days from production date until the product expires")
    
    description = st.text_area("Description")
    
    if st.button("Add Product", type="primary"):
        if product_id and description:  # Basic validation
            try:
                # Check if product ID already exists
                existing = db.execute(
                    text("SELECT id FROM products WHERE id = :id"),
                    {"id": product_id}
                ).fetchone()
                
                if existing:
                    st.error("A product with this ID already exists")
                else:
                    # Insert new product
                    db.execute(text("""
                        INSERT INTO products (id, name, category, description, base_price, days_to_expiration)
                        VALUES (:id, :name, :category, :description, :base_price, :days_to_expiration)
                    """), {
                        "id": product_id,
                        "name": name,
                        "category": category,
                        "description": description,
                        "base_price": base_price,
                        "days_to_expiration": days_to_expiration

                    })
                    db.commit()
                    st.success("Product added successfully!")
                    st.rerun()
            except Exception as e:
                db.rollback()
                st.error(f"Error adding product: {str(e)}")
        else:
            st.error("Product ID and Description are required")

def edit_delete_product(db):
    """Interface for editing or deleting products"""
    st.subheader("Edit or Delete Product")
    
    # Product search
    search = st.text_input("Search Product (Product ID, product, description, or category)",
                          key="edit_product_search")
    

    if search:
        products = db.execute(text("""
            SELECT p.id, p.name, p.description, c.name as category_name, 
                p.base_price, p.days_to_expiration
            FROM products p
            JOIN categories c ON p.category = c.name
            WHERE p.description ILIKE :search 
            OR CAST(p.id AS TEXT) LIKE :search
            OR p.name ILIKE :search
            OR c.name ILIKE :search
            ORDER BY p.id
        """), {"search": f"%{search}%"}).fetchall()
        
        if products:
            product_options = {
                f"ID: {p.id} - {p.name} ({p.category_name})": p 
                for p in products
            }
            selected_product_name = st.selectbox(
                "Select Product",
                options=list(product_options.keys()),
                key="edit_product"
            )
            
            if selected_product_name:
                product = product_options[selected_product_name]
                categories = get_categories(db)
                
                # Edit form
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Product name", value=product.name)
                    new_category = st.selectbox(
                        "Category",
                        options=categories,
                        index=categories.index(product.category_name)
                    )

                with col2:
                    new_base_price = st.number_input(
                        "Base Price",
                        value=float(product.base_price),
                        min_value=0.0,
                        step=0.1
                    )
                    
                    # Add days_to_expiration here
                    new_days_to_expiration = st.number_input(
                        "Days to Expiration",
                        value=product.days_to_expiration,
                        min_value=1,
                        step=1,
                        help="Number of days from production date until the product expires"
                    )
                
                new_description = st.text_area(
                    "Description",
                    value=product.description
                )
                
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("Update Product", key="update_product"):
                        try:
                            db.execute(text("""
                                UPDATE products
                                SET name = :name,
                                    category = :category,
                                    description = :description,
                                    base_price = :base_price,
                                    days_to_expiration = :days_to_expiration
                                WHERE id = :id
                            """), {
                                "name": new_name,
                                "category": new_category,
                                "description": new_description,
                                "base_price": new_base_price,
                                "days_to_expiration": new_days_to_expiration,
                                "id": product.id
                            })
                            db.commit()
                            st.success("Product updated successfully!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error updating product: {str(e)}")
                
                with col4:
                    # Check if product has any sales or inventory before allowing deletion
                    usage = db.execute(text("""
                        SELECT 
                            (SELECT COUNT(*) FROM sales WHERE product_id = :id) as sales_count,
                            (SELECT COUNT(*) FROM inventory WHERE product_id = :id) as inventory_count
                    """), {"id": product.id}).fetchone()
                    
                    delete_confirmed = st.checkbox(
                        "I confirm I want to delete this product",
                        key="delete_product_confirm"
                    )
                    
                    total_usage = usage.sales_count + usage.inventory_count
                    delete_button = st.button(
                        "Delete Product",
                        key="delete_product",
                        type="secondary",
                        disabled=total_usage > 0
                    )
                    
                    if total_usage > 0:
                        st.warning(
                            f"This product cannot be deleted because it has "
                            f"{usage.sales_count} sales records and "
                            f"{usage.inventory_count} inventory records"
                        )
                    
                    if delete_confirmed and delete_button:
                        try:
                            db.execute(
                                text("DELETE FROM products WHERE id = :id"),
                                {"id": product.id}
                            )
                            db.commit()
                            st.success("Product deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error deleting product: {str(e)}")
        else:
            st.info("No products found matching your search")

def search_products(db):
    st.subheader("Search Products")
    
    # Search options
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search by Product ID, Product Name, or Description")
    
    with col2:
        categories = db.execute(text("SELECT name FROM categories ORDER BY name")).fetchall()
        category_options = [c.name for c in categories]
        category_options.insert(0, "All Categories")
        selected_category = st.selectbox(
            "Category",
            options=category_options,
            key="product_search_category"
        )
    
    query = """
        SELECT 
            p.id,
            p.name,
            p.description,
            c.name as category,
            p.base_price,
            (SELECT COUNT(*) FROM sales s WHERE s.product_id = p.id) as total_sales,
            (SELECT COUNT(*) FROM inventory i WHERE i.product_id = p.id) as total_production
        FROM products p
        JOIN categories c ON p.category = c.name
        WHERE 1=1
    """
    params = {}
    
    if search_term:
        query += """ 
            AND (
                CAST(p.id AS TEXT) ILIKE :search 
                OR p.name ILIKE :search
                OR p.description ILIKE :search
            )
        """
        params["search"] = f"%{search_term}%"
    
    if selected_category != "All Categories":
        query += " AND c.name = :category"
        params["category"] = selected_category
    
    query += " ORDER BY p.id"
    
    try:
        results = db.execute(text(query), params).fetchall()
        if results:
            df = pd.DataFrame([{
                "ID": str(r.id),
                "Name": r.name,
                "Description": r.description,
                "Category": r.category,
                "Base Price": f"${r.base_price:.2f}",
                "Total Sales": r.total_sales,
                "Total Production": r.total_production
            } for r in results])
            
            st.dataframe(df, hide_index=True)
            st.write(f"Found {len(results)} products")
        else:
            st.info("No products found matching your criteria")
    except Exception as e:
        st.error(f"Error searching products: {str(e)}")

def show():
    """Main products page"""
    st.title("Product Management")
    
    # Tab selection
    tab1, tab2, tab3, = st.tabs(["New Product", "Edit/Delete Product", "Search Product"])
    
    with tab1:
        new_product_form(st.session_state.db)
        st.markdown("---")
        show_products(st.session_state.db)
    
    with tab2:
        edit_delete_product(st.session_state.db)
        st.markdown("---")
        show_products(st.session_state.db)

    with tab3:
        search_products(st.session_state.db)