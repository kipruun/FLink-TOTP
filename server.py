"""
FamilyLink TOTP Generator server
Creator: Kipruun
Packtage: flask (web app), fpdf (PDF generation), requests (HTTP requests), pytz (timezone handling)

Description: This script serves a web application that generates and displays TOTP codes for a given secret key.

!!!! Compatibility with PythonAnywhere python 3.10 !!!!
"""


from flask import Flask, render_template_string, send_file
from fpdf import FPDF
import datetime
from io import BytesIO
from totp import TOTPElement
import requests
from flask import request
import pytz


#------------------------- Configuration -------------------------
SECRET = "YOUR TOKEN HERE" # Replace with your TOTP secret key, follow this tutorial to get it : https://gist.github.com/rifting/732a45adf8ebacfa0e1fda0a66662570#guide-computer
DEFAULT_TIMEZONE = "Europe/Paris" # Default timezone if the user's timezone cannot be determined
#------------------------------------------------------------------



app = Flask(__name__) # Flask app instance

@app.route('/')
def index():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
        </style>
        <title>TOTP Codes</title>
    </head>
    <body>
        """ # Initial HTML structure
    try: # Get user's IP address and timezone
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        timezone = requests.get(f"http://ip-api.com/json/{ip}").json().get("timezone")
        if not timezone:
            raise ValueError("Timezone not found in response")
        html += f"<p>Timezone calculated:  {timezone}</p>"

    except: # If there's an error in getting the timezone, use a default
        timezone = "Europe/Paris"
        html += f"<p>Error in the calcul of the timezone /// {DEFAULT_TIMEZONE} use by default</p>"
    
    try: # Set the timezone and get the current date
        tz = pytz.timezone(timezone)
        date = datetime.datetime.now().astimezone(tz)
        totp_codes = TOTPElement(SECRET).get_a_day_codes(timezone=tz)
    except: # If there's an error in setting the timezone, use the server's time
        date = datetime.datetime.now()
        html += f"<p>Error when the timezone was configured /// Server's time used</p>"
        totp_codes = TOTPElement(SECRET).get_a_day_codes()
    
    html += f"<h1>Codes for the {date.day} - {date.month}</h1>" # Add the date to the HTML

    for heure, code in totp_codes: # Loop through the TOTP codes and add them to the HTML
        html += f"<p><b>Hour: {heure:02d}:00</b> - Code: {code}</p>"

    html += "</body></html>" # Close the HTML structure

    return render_template_string(html) # Render the HTML as a string




@app.route('/pdf')
def pdf():
    html = ""
    try: # Get user's IP address and timezone
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        timezone = requests.get(f"http://ip-api.com/json/{ip}").json().get("timezone")
        if not timezone:
            raise ValueError("Timezone not found in response")
        html += f"<p>Timezone calculated:  {timezone}</p>"

    except: # If there's an error in getting the timezone, use a default
        timezone = "Europe/Paris"
        html += f"<p>Error in the calcul of the timezone /// {DEFAULT_TIMEZONE} use by default</p>"
    
    try: # Set the timezone and get the current date
        tz = pytz.timezone(timezone)
        date = datetime.datetime.now().astimezone(tz)
        totp_codes = TOTPElement(SECRET).get_a_day_codes(timezone=tz)
    except: # If there's an error in setting the timezone, use the server's time
        date = datetime.datetime.now()
        html += f"<p>Error when the timezone was configured /// Server's time used</p>"
        totp_codes = TOTPElement(SECRET).get_a_day_codes()
        
    html += f"""
        <h1>Codes for the {date.day} - {date.month}</h1>
        """ # Add the date to the HTML
    pdf = FPDF() # Create a PDF instance
    pdf.add_page() # Add a new page to the PDF
    pdf.set_font("Arial", size=14) # Set the font for the PDF

    for heure, code in totp_codes:  # Loop through the TOTP codes and add them to the PDF
        html += f"<p> <b>Hour   : {heure:02d}:00</b> - Code: {code}</p>"
    pdf.write_html(html) # Write the HTML content to the PDF
    pdf_output = BytesIO() # Create a BytesIO object to hold the PDF data
    pdf.output(pdf_output) # Save the PDF to the BytesIO object
    pdf_output.seek(0)  # Move the cursor to the beginning of the BytesIO object
    return send_file(pdf_output,mimetype='application/pdf', as_attachment=False, download_name='book_catalog.pdf')

application = app

if __name__ == '__main__':
    app.run(debug=True, port=8081)

