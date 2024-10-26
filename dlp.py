import streamlit as st
import hashlib
import json
from datetime import datetime

# Blockchain class to manage blocks and chain
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        # Convert block contents to a JSON string and encode it
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        # Initialize with a genesis block
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Create a block with a fixed initial index and data
        return Block(0, str(datetime.now()), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        # Create a new block and add it to the chain
        previous_block = self.get_last_block()
        new_block = Block(index=previous_block.index + 1,
                          timestamp=str(datetime.now()),
                          data=data,
                          previous_hash=previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Check that each block's hash matches its contents and the previous hash matches the chain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Initialize the blockchain
blockchain = Blockchain()

# Streamlit App Title
st.title("P2P Digital Land Certificate System (Blockchain-Backed)")

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
    
    # Register button to submit certificate
    if st.button("Register Certificate"):
        if owner_name and land_id and location and area:
            # Create certificate data to store in the blockchain
            certificate_data = {
                "Owner Name": owner_name,
                "Land ID": land_id,
                "Location": location,
                "Area (acres)": area,
                "Date Registered": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Add the certificate as a new block in the blockchain
            blockchain.add_block(certificate_data)
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
        # Search for the certificate by Land ID in the blockchain
        matching_block = next((block for block in blockchain.chain if block.data.get("Land ID") == verify_land_id), None)
        
        if matching_block:
            # Display certificate details if found
            st.write("Certificate Found:")
            st.json(matching_block.data)
        else:
            st.error("Certificate not found. Please check the Land ID.")

# Display blockchain validity
st.subheader("Blockchain Integrity Check")
if blockchain.is_chain_valid():
    st.success("The blockchain is valid.")
else:
    st.error("The blockchain has been compromised!")

# Display entire blockchain (for demonstration)
st.subheader("Blockchain Ledger")
for block in blockchain.chain:
    st.write(f"Block {block.index}:")
    st.json(block.__dict__)
