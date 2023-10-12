import streamlit as st
from sklearn.linear_model import LinearRegression
import streamlit.components.v1 as components
# import sqlite3
import re
import matplotlib.pyplot as plt
import numpy as np
import io
import pandas as pd
import requests
import json

st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header('Investeringsspil for Varmestrup', divider='grey')
st.write("Vælg kapaciteter/størrelser i sliders og omkostningen for det enkelte anlæg vil komme op. Scrol igennem og fyldt ud til investeringsloftet er nået. "
         "Husk du maks bruge for 30 mio. DKK, og husk at skrive navn og email, og klik send")
# streamlit run "c:/Users/sba/OneDrive - EMD International A S/energygame - Jonathan Refsgaards filer/main_local.py"
# streamlit run "c/Users/sba/Documents/Git_repo/ta_energypro/examples/competition_landsmoede/streamlit_setup.py"
# streamlit run "c:/Users/sba/Documents/Git_repo/ta_energypro/examples/competition_landsmoede/streamlit_setup.py"


#path = "C:/Users/jr/OneDrive - EMD International A S/Python Projects/jr_projects/energygame/"
#path = "C:/Users/jr/OneDrive - EMD International A S/Python Projects/jr_projects/energygame/"
# path = "./examples/competition_landsmoede/"
# conn = sqlite3.connect(path + "forslag.db")
# conn.execute("DROP TABLE IF EXISTS SETTINGS")
# conn.execute("CREATE TABLE SETTINGS (NAME CHAR(50), EMAIL CHAR(50), VARMEPUMPE, ELKEDEL, AKKU, FLIS, SOL)")
# conn.commit()
# conn.close()

def price_function(x,y, cap):
    # Convert the data to NumPy arrays and reshape x
    x_1 = np.array(x).reshape(-1, 1)
    y_1 = np.array(y)
    # Create a Linear Regression model
    model = LinearRegression()
    # Fit the model to the data
    model.fit(x_1, y_1)

    # Make a prediction using the model for the stated capacity cap
    input_value = np.array([[cap]])

    # Calculate the predicted price - if the cap is zero then the price is zero (If the price curve does not end in zero)
    if cap == 0:
        price = 0
    else:
        price = model.predict(input_value)[0]

    return price

def ChangeWidgetFontSize(wgt_txt, wch_font_size = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('p'), i;
                for (i = 0; i < elements.length; ++i) 
                    { if (elements[i].textContent.includes(|wgt_txt|)) 
                        { elements[i].style.fontSize ='""" + wch_font_size + """'; } }</script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

st.markdown(
    """<style>
div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 24px;
}
    </style>
    """, unsafe_allow_html=True)


vp = st.slider("Varmepumpe", min_value=0.0, max_value=4.0, step=0.25)

# Create the price curve of the unit
x_vppricecurve = [0.5, 1, 1.5, 2, 2.5, 3]  # heat effect (MW)
y_vppricecurve = [9, 13, 17, 21, 25, 29]  # prices (mio. DKK)

# Calculate the price of the unit
vp_price = round(price_function(x_vppricecurve, y_vppricecurve, vp), 1)
# Shown calculated price
st.write("Samlet pris Varmepumpe: "+str(vp_price) + " mio. DKK")

# Create a checkbox to toggle the visibility of the section
show_section_vp = st.checkbox("Vis information om Varmepumpe")

# Check if the checkbox is checked to determine whether to display the section
if show_section_vp:
    # Content of the collapsible section
    st.write("Varmepumpen antages til at have en fast COP uanset størrelsen på 2.7")

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Scatter plot (markers)
    ax.scatter(x_vppricecurve, y_vppricecurve, label='Scatter Points', color='blue', marker='o')

    # Line plot (lines connecting the points)
    ax.plot(x_vppricecurve, y_vppricecurve, label='Line Connecting Points', color='blue', linestyle='-')

    ax.set_xlabel('Varmeffekt [MW]')
    ax.set_ylabel('Pris [mio. DKK]')
    ax.set_title('Omkostning som funktion af varmeeffekt')

    # Save the Matplotlib plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Save as PNG format
    buffer.seek(0)

    # Display the Matplotlib plot as an image with specified dimensions
    st.image(buffer, width=1000)

ek = st.slider("Elkedel", min_value=0.0, max_value=10.0, step=0.25)


# Create the price curve of the unit
x_ekpricecurve = [2, 4, 6, 8, 10, 12, 14, 16]            # heat effect (MW)
y_ekpricecurve = [1.2, 2.4, 3.6, 4.8, 6, 7.2, 8.4, 9.6]  # prices (mio. DKK)

# Calculate the price of the unit
ek_price = round(price_function(x_ekpricecurve, y_ekpricecurve, ek), 1)

st.write("Samlet pris elkedel: "+str(ek_price) + " mio. DKK")

# Create a checkbox to toggle the visibility of the section
show_section_elb = st.checkbox("Vis information om Elkedel")

# Check if the checkbox is checked to determine whether to display the section
if show_section_elb:
    # Content of the collapsible section
    st.write("Elkedlen antages til at have effektivitet på 100%")

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Scatter plot (markers)
    ax.scatter(x_ekpricecurve, y_ekpricecurve, label='Scatter Points', color='blue', marker='o')

    # Line plot (lines connecting the points)
    ax.plot(x_ekpricecurve, y_ekpricecurve, label='Line Connecting Points', color='blue', linestyle='-')

    ax.set_xlabel('Varmeffekt [MW]')
    ax.set_ylabel('Pris [mio. DKK]')
    ax.set_title('Omkostning som funktion af varmeeffekt')

    # Save the Matplotlib plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Save as PNG format
    buffer.seek(0)

    # Display the Matplotlib plot as an image with specified dimensions
    st.image(buffer, width=1000)


ak = st.slider("Varmeakkumuleringstank", min_value=0.0, max_value=10000.0, step=50.0)

# Create the price curve of the unit
x_akpricecurve = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]            # Storage capacity (m3)
y_akpricecurve = [1.35, 2.15, 2.82, 3.42, 3.97, 4.49, 4.97, 5.44]                      # prices (mio. DKK)

# Calculate the price of the unit
ak_price = round(price_function(x_akpricecurve, y_akpricecurve, ak),1)

st.write("Samlet pris VAK: "+str(ak_price) + " mio. DKK")

# Create a checkbox to toggle the visibility of the section
show_section_vak = st.checkbox("Vis information om VAK")



# Check if the checkbox is checked to determine whether to display the section
if show_section_vak:
    # Content of the collapsible section
    st.write("VAK antages at kunne bruges af alle enheder")
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Scatter plot (markers)
    ax.scatter(x_akpricecurve, y_akpricecurve, label='Scatter Points', color='blue', marker='o')

    # Line plot (lines connecting the points)
    ax.plot(x_akpricecurve, y_akpricecurve, label='Line Connecting Points', color='blue', linestyle='-')

    ax.set_xlabel('Lagerkapacitet [m3]')
    ax.set_ylabel('Pris [mio. DKK]')
    ax.set_title('Omkostning som funktion af lagerstørrelse')

    # Save the Matplotlib plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Save as PNG format
    buffer.seek(0)

    # Display the Matplotlib plot as an image with specified dimensions
    st.image(buffer, width=1000)


fk = st.slider("Fliskedel", min_value=0.0, max_value=10.0, step=0.5)

# Create the price curve of the unit
x_fkpricecurve = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]                                          # Heat effect (MW)
y_fkpricecurve = [5.25, 8, 10.75, 13.5, 16.25, 19, 21.75, 24.5, 27.25]                      # prices (mio. DKK)

# Calculate the price of the unit
fk_price = round(price_function(x_fkpricecurve, y_fkpricecurve, fk),1)

st.write("Samlet pris fliskedel: "+str(fk_price) + " mio. DKK")

# Create a checkbox to toggle the visibility of the section
show_section_fk = st.checkbox("Vis information om fliskedlen")

# Check if the checkbox is checked to determine whether to display the section
if show_section_fk:
    # Content of the collapsible section
    st.write("Fliskedlen antages til at have effektivitet på 96%")
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Scatter plot (markers)
    ax.scatter(x_fkpricecurve, y_fkpricecurve, label='Scatter Points', color='blue', marker='o')

    # Line plot (lines connecting the points)
    ax.plot(x_fkpricecurve, y_fkpricecurve, label='Line Connecting Points', color='blue', linestyle='-')

    ax.set_xlabel('Varmeffekt [MW]')
    ax.set_ylabel('Pris [mio. DKK]')
    ax.set_title('Omkostning som funktion af varmeeffekt')

    # Save the Matplotlib plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Save as PNG format
    buffer.seek(0)

    # Display the Matplotlib plot as an image with specified dimensions
    st.image(buffer, width=1000)


so = st.slider("Solvarmeanlæg areal", min_value=0.0, max_value=25000.0, step=500.0)

# Create the price curve of the unit
x_sopricecurve = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]                              # Solar collector area (m2)
y_sopricecurve = [1.3, 2.6, 3.9, 5.2, 6.5, 7.8, 9.1, 10.4]                                     # prices (mio. DKK)

# Calculate the price of the unit
so_price = round(price_function(x_sopricecurve, y_sopricecurve, so), 1)

st.write("Samlet pris solvarmeanlæg: "+str(so_price) + " mio. DKK")


# Create a checkbox to toggle the visibility of the section
show_section_so = st.checkbox("Vis information om solanlæg")

# Check if the checkbox is checked to determine whether to display the section
if show_section_so:
    # Content of the collapsible section
    st.write("Solpanelerne antages også at kunne levere ind til VAKen")

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Scatter plot (markers)
    ax.scatter(x_sopricecurve, y_sopricecurve, label='Scatter Points', color='blue', marker='o')

    # Line plot (lines connecting the points)
    ax.plot(x_sopricecurve, y_sopricecurve, label='Line Connecting Points', color='blue', linestyle='-')

    ax.set_xlabel('Solfanger areal [m2]')
    ax.set_ylabel('Pris [mio. DKK]')
    ax.set_title('Omkostning som funktion af solfanger areal')

    # Save the Matplotlib plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')  # Save as PNG format
    buffer.seek(0)

    # Display the Matplotlib plot as an image with specified dimensions
    st.image(buffer, width=1000)

# Total investment of the project
cost = vp_price + ek_price + ak_price + fk_price + so_price

# Define a CSS style for the highlighted text
highlighted_text_style = """
    background-color: lightgrey;
    padding: 5px;
    border: 1px solid black;
    border-radius: 5px;
"""

# Define the text you want to highlight
text_to_highlight = "Samlet foreløbig investering " + str(round(cost,1)) + " mio. DKK"

# Use Markdown to display the text with the specified style
st.markdown(f'<div style="{highlighted_text_style}">{text_to_highlight}</div>', unsafe_allow_html=True)


# email checker
def is_valid_email(em):
    # Regular expression for a valid email address
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Use the re.match function to match the email pattern
    if re.match(email_pattern, em):
        return True
    else:
        return False

# def is_unique_email(em):
#     path = "c:/Users/sba/Documents/Git_repo/ta_energypro/examples/competition_landsmoede/"
#     # c:\Users\sba\Documents\Git_repo\ta_energypro\examples\competition_landsmoede\forslag.db
#     # Establish a connection to the SQLite database
#     conn = sqlite3.connect(path + "forslag.db")
#     cursor = conn.cursor()
#
#     # Use the "SELECT EMAIL FROM" query to retrieve EMAIL column from the "SETTINGS" table
#     query = "SELECT EMAIL FROM SETTINGS"
#
#     # Read the data into a DataFrame
#     df = pd.read_sql_query(query, conn)
#     df["EMAIL"] = df["EMAIL"].str.lower()
#     # See if email exists in dataframe
#     em = str(em)
#     em = em.lower()
#     if em in df["EMAIL"].values:
#         return False
#     else:
#         return True

def is_unique_email(em):
    response = requests.get('https://www3.emd.dk/admin/simon/')
    if response.status_code == 200:
        json_data = response.json()

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(json_data)

    df_email = df["email"].str.lower()
    # See if email exists in dataframe
    em = str(em)
    em = em.lower()
    if em in df_email.values:
        return False
    else:
        return True


if cost > 30:
    st.markdown("Investering må ikke samlet være større end 30 mio. DKK")
else:
    navn = st.text_input("Navn")
    email = st.text_input("E-mail")
    if  navn != "" and email != "":
        if is_valid_email(email):
            if is_unique_email(email):
                send = st.button("Send forslag")
                if send:
                    # Skriv data

                    input_data = {'navn': navn, 'email': email, 'varmepumpe': vp, 'elkedel': ek, 'akku': ak,
                                 'flis': fk, 'sol': so}

                    response = requests.post('https://www3.emd.dk/admin/simon/', data=json.dumps(input_data))
                    if response.status_code == 200:
                        print('Write successfull')
                        print(response.text)

                    # path = "c:/Users/sba/Documents/Git_repo/ta_energypro/examples/competition_landsmoede/"
                    # conn = sqlite3.connect(path + "forslag.db")
                    # # Define the SQL query with placeholders for data
                    # query = "INSERT INTO SETTINGS (NAME, EMAIL, VARMEPUMPE, ELKEDEL, AKKU, FLIS, SOL) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    # conn.execute(query, (navn, email, vp, ek, ak, fk, so))
                    # conn.commit()
                    # conn.close()
                    st.markdown("Forslag indsendt")
                    # Display some content
                    st.write("Genstart side for nyt forslag")
            else:
                st.markdown("Der er desværre allerede afgivet et svar med den E-mail. Kontakt nærmeste EMD medarbejder ved fejl!")
        else:
            st.markdown("E-mail ser ikke ud til at være skrevet korrekt?")







