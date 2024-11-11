import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(page_title="Annual Benefit Dinner - Donation Dashboard", layout="wide")

# Define the target amount needed for donations
TARGET_DONATION = 100000  # Example total target amount
PRESET_ATTENDEE_COUNT = 350  # Example preset count for attendees

# Load Excel file and read donations data
def load_data():
    # Replace 'donations.xlsx' with your actual Excel file path
    df = pd.read_excel('donations.xlsx')
    return df

# Custom CSS styling
st.markdown("""
    <style>
    /* Background color */
    .main {
        background-color: #F9F4EA; /* Light beige/cream */
    }

    /* Titles and headers */
    h1, h2, h3 {
        color: #014421; /* Dark green for main titles */
        font-family: 'Georgia', serif;
    }

    /* Notification success message */
    .stAlert {
        color: #014421;
        background-color: #DFF0D8;
        border: 1px solid #A9DFBF;
        font-family: 'Verdana', sans-serif;
    }

    /* Donation notifications section */
    .stMarkdown h3 {
        color: #014421; /* Dark green */
    }
    .metric-container {
        background-color: #F9F4EA; /* Light blue background color */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* Latest donation highlight */
    .latest-donation {
        background-color: #014421; /* Dark green */
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }

    /* Center QR code area */
    .qr-code-container {
        text-align: center;
        margin-top: 20px;
    }

    /* Custom footer styling */
    footer {
        font-family: 'Arial', sans-serif;
        color: #555;
        text-align: center;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

import os
from PIL import Image


# Function to display sponsor logos in a grid layout
def display_sponsor_logos():
    st.subheader("Our Sponsors")
    # Define the paths for each sponsor's logo
    sponsor_paths = ["./logos/1", "./logos/2", "./logos/3"]
    max_width = 50  # Maximum width for each logo to ensure uniform size

    # Arrange logos in a grid with one column per logo
    cols = st.columns(len(sponsor_paths))  # Creates as many columns as there are sponsor paths

    for i, (col, path) in enumerate(zip(cols, sponsor_paths), start=1):
        # Check if there's an image file in the directory
        if os.path.exists(path) and os.listdir(path):
            logo_file = os.listdir(path)[0]  # Get the first file in the directory
            logo_path = os.path.join(path, logo_file)
            if logo_file.endswith(('.png', '.jpg', '.jpeg')):
                # Open and resize the logo if necessary
                logo_image = Image.open(logo_path)
                if logo_image.width > max_width:
                    aspect_ratio = logo_image.height / logo_image.width
                    #logo_image = logo_image.resize((max_width, int(max_width * aspect_ratio)))

                # Display the logo in its respective column
                with col:
                    st.markdown(f"### Sponsor {i}")
                    col.image(logo_image, use_container_width=True)
        else:
            col.warning(f"No logo found in {path}")

# Function to create pie chart
def plot_donation_chart(total_donated, target_donation):
    fig, ax = plt.subplots()
    data = [total_donated, max(0, target_donation - total_donated)]
    labels = ['Donated', 'Remaining']
    colors = ['#014421', '#F9F4EA']  # Dark green for Donated and beige for Remaining

    # Define a custom function to display the donation amount
    def absolute_value(val):
        # Calculate the actual donation amount based on the pie slice value
        if val > 0:
            amount = total_donated if val > 50 else target_donation - total_donated
            return f"${amount:,.0f}"
        return ""

    # Plot the pie chart with the custom autopct function
    wedges, texts, autotexts = ax.pie(data, labels=labels, autopct=absolute_value, startangle=90, colors=colors)

    # Set the color of "Donated" text to white for readability
    for i, autotext in enumerate(autotexts):
        if labels[i] == 'Donated':  # If it's the "Donated" portion
            autotext.set_color("white")  # Set text to white for dark green portion
        else:
            autotext.set_color("black")  # Set text to black for beige portion

    return fig

# Display title
st.title("Darul Uloom Austin - Annual Benefit Dinner")
st.write("**Join us in supporting this noble cause!**")
st.write("Event Date: **Sunday, November 17, 2024** | Time: **5 PM** | Location: **Georgetown Community Center**")

# Main refreshable container
dashboard_container = st.empty()

while True:
    with dashboard_container.container():
        # Load and display data
        data = load_data()
        total_donated = data['Donation Amount'].sum()
        donation_count = len(data)  # Count of donations

        # Display metrics with a background
        st.markdown('<div class="metric-row">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="metric-item">', unsafe_allow_html=True)
            st.metric(label="Total Donations", value=f"${total_donated}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-item">', unsafe_allow_html=True)
            st.metric(label="Donation Count", value=donation_count)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-item">', unsafe_allow_html=True)
            st.metric(label="Attendee Count", value=PRESET_ATTENDEE_COUNT)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Create two columns for layout
        col1, col2 = st.columns(2)

        # Left Column: Donation Progress Chart
        with col1:
            st.subheader("Donation Progress")
            fig = plot_donation_chart(total_donated, TARGET_DONATION)
            st.pyplot(fig, clear_figure=True)  # Clear figure to avoid stacking

        # Right Column: Last 5 Donations
        with col2:
            st.subheader("Recent Donations")

            # Show the latest donation with highlighted styling
            latest_donation = data.iloc[-1]
            st.markdown(
                f"<div class='latest-donation'>New donation of ${latest_donation['Donation Amount']} from {latest_donation['Donor Name']}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            # Display the previous four donations in default styling
            previous_donations = data.iloc[-5:-1].iloc[::-1]  # Get the 4 donations before the latest
            for _, row in previous_donations.iterrows():
                st.info(f"${row['Donation Amount']} from {row['Donor Name']}")

        # Footer section with contact information and QR code prompts
        st.subheader("After raising your hand, please fill the card out and pass it to the volunteer closest to you during the fundraiser.") 
        st.subheader("If you choose to donate secretly please text the amount and method to 512-767-4082 e.g ‘5000 Card’ or ‘5000 Zelle’")
        st.markdown("""
            <div class="qr-code-container">
                <p><b></b></p>
                <img src="YOUR_QR_CODE_IMAGE_URL_HERE" alt="QR Code for Tickets" style="width:100px; margin-right:10px;">
                <img src="YOUR_DONATION_QR_CODE_IMAGE_URL_HERE" alt="QR Code for Donations" style="width:100px;">
            </div>
        """, unsafe_allow_html=True)

        # Add this at the end of the app layout to display the sponsors
        display_sponsor_logos()

        # Contact Information Footer
        st.markdown("""
            <footer>
                <p>Contact us at <a href="mailto:info@darululoomaustin.org">info@darululoomaustin.org</a> | Phone: (512) 981-5323 | Visit our website: <a href="http://darululoomaustin.org" target="_blank">darululoomaustin.org</a></p>
            </footer>
        """, unsafe_allow_html=True)


    # Refresh every few seconds to check for updates
    time.sleep(5)