import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="AERORENT UK",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to hide Streamlit elements
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Read and display the HTML file
def load_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

# Main app
def main():
    try:
        html_content = load_html()
        components.html(html_content, height=800, scrolling=True)
    except FileNotFoundError:
        st.error("HTML file not found. Please make sure 'index.html' exists in the same directory.")
        st.info("You can create a simple HTML file or upload your existing HTML website.")

if __name__ == "__main__":
    main() 