import streamlit as st
from app import init_app
from app.pages import overview, reports, production, sales, products, customers

# Configure the Streamlit page
st.set_page_config(
    page_title="Brewery Inventory System",
    page_icon="🍻",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize the application
    init_app()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Navigation options with icons
    pages = {
        "Overview": {"icon": "📊", "module": overview},
        "Reports": {"icon": "📈", "module": reports},
        "Production": {"icon": "🏭", "module": production},
        "Orders": {"icon": "💰", "module": sales},
        "Products": {"icon": "📦", "module": products},
        "Customers": {"icon": "👥", "module": customers}
    }
    
    # Create selection box with icons
    selection = st.sidebar.selectbox(
        "",
        options=list(pages.keys()),
        format_func=lambda x: f"{pages[x]['icon']} {x}"
    )
    
    # Render the selected page
    try:
        pages[selection]['module'].show()
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.write("Please make sure all required page modules are implemented.")

    # Add sidebar footer with version info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("v1.0.0")
    st.sidebar.markdown("© 2025 Brewery Inventory System")

if __name__ == "__main__":
    main()