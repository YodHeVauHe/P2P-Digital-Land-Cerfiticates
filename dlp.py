import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize an empty list to store certificate data
certificates = []

# Streamlit App Title
st.title("P2P Digital Land Certificate System")

# Tabs for functionality
tab1, tab2 = st.tabs(["Register Land", "Verify Certificate"])

# Register Land Certificate
with tab1:
    st.header("Register a New Land Certificate")
    
    # Inputs for land details
    owner_name = st.text_input("Owner Name")
    land_id = st.text_input("Land ID (e.g., unique land plot identifier)")
    location = st.text_input("Land Location")
    area = st.number_input("Land Area (in acres)", min_value=0.1)
    date_registered = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Register button to submit certificate
    if st.button("Register Certificate"):
        # Check that required fields are filled
        if owner_name and land_id and location and area:
            # Create certificate entry
            certificate = {
                "Owner Name": owner_name,
                "Land ID": land_id,
                "Location": location,
                "Area (acres)": area,
                "Date Registered": date_registered
            }
            # Append certificate to the list
            certificates.append(certificate)
            st.success(f"Certificate registered successfully for {owner_name}!")
        else:
            st.warning("Please fill in all required fields.")

# Verify Land Certificate
with tab2:
    st.header("Verify a Land Certificate")
    
    # Input for certificate verification
    verify_land_id = st.text_input("Enter Land ID to Verify")
    
    # Verify button
    if st.button("Verify Certificate"):
        # Search for the certificate by Land ID
        matching_cert = next((cert for cert in certificates if cert["Land ID"] == verify_land_id), None)
        
        if matching_cert:
            # Display certificate details if found
            st.write("Certificate Found:")
            st.write(pd.DataFrame([matching_cert]))
        else:
            st.error("Certificate not found. Please check the Land ID.")

# Display all certificates (for demonstration purposes)
st.subheader("Registered Certificates")
if certificates:
    st.write(pd.DataFrame(certificates))
else:
    st.write("No certificates registered yet.")
