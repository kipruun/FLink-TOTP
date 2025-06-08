"""
FamilyLink TOTP Generator
Creator: Kipruun
Packtage: pyotp, pytz

Description: This module generates TOTP codes for a given secret key.
It allows you to generate codes for specific hours of the day or for all hours of the current day.
"""

import pyotp
import datetime
import base64
import pytz



class TOTPElement:
    def __init__(self, secret: str, timezone=""):
        """Initialize the TOTPElement with a secret.

        Args:
            secret (str): The secret key used to generate TOTP codes. 
                          It should be a string of characters. 
                          Follow this tutorial to get it : https://gist.github.com/rifting/732a45adf8ebacfa0e1fda0a66662570#guide-computer
        """
        self.secret = secret
        self.timezone = ""
        self.base32_secret = base64.b32encode(bytes(secret, encoding="utf-8")).decode('utf-8') # Convert the secret to base32 format
    
    def get_totp_code(self, hour=None) -> str:
        """Generate a TOTP code for a specific hour.

        Args:
            hour (int, optional): The hour for which to generate the TOTP code.

        Returns:
            str: The generated TOTP code for the specified hour.
        """
              
        if self.timezone != "":
            tz = pytz.timezone(self.timezone)
            date = datetime.datetime.now().astimezone(tz)
        else:
            date = datetime.datetime.now()

        if not hour:
            hour = date.hour # Use the current hour if no hour is provided
      
        target_time = datetime.datetime(date.year, date.month, date.day, hour, 0, 0) # Create a target time with the specified hour and current date
        timestamp = int(target_time.timestamp()) # Convert the target time to a timestamp
        totp = pyotp.TOTP(self.base32_secret, interval=60) # Create a TOTP object with the base32 secret and a 60-second interval
        code = totp.at(timestamp) # Generate the TOTP code for the target time
        return code

    def get_a_day_codes(self) -> list:
        """Generate TOTP codes for all hours of the current day.

        Returns:
            list: A list of tuples, each containing the hour and the corresponding TOTP code for that hour.
        """
        codes = []
        for hour in range(24):
            code = self.get_totp_code(hour)
            codes.append((hour, code))
        return codes





                    
        

        
if __name__ == "__main__":
    os.system("python cli-flink.py")