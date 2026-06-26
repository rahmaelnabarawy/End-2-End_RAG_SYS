import streamlit as st

st.set_page_config(
    page_title="Deployment Test",
    page_icon="🚀"
)

st.title("🚀 Deployment Test")

st.success("If you can see this message, the deployment works successfully!")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello {name}! 👋")

if st.button("Test Button"):
    st.balloons()
    st.write("Everything is working correctly!")