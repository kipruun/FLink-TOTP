from totp import TOTPElement
from colorama import init, Fore
import os
import json


def config_load():
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(path, "config.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                json_file = json.loads(file.read())
            except:
                json_file = {}
                f = open(file_path, "w")
                f.write("{}")
                f.close()
            if json_file.get("token"):
                print("Token loadded:", json_file.get("token"))
            else:
                print("Token not found.")
            if json_file.get("timezone"):
                print("Timezone loadded:", json_file.get("timezone")) 
            else:
                print("Timezone not found")
        return json_file
    return {}


def config_save(timezone=False, secret=False):
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(path, "config.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            json_file = json.loads(file.read())
    else:
        json_file = {}
    if secret:
        json_file["token"] = secret
    if timezone:
        json_file["timezone"] = timezone
    
    with open(file_path, "w") as f:
        f.write(json.dumps(json_file))
        

init(autoreset=True)  
os.system('cls' if os.name=='nt' else 'clear')

header = f"""{Fore.CYAN}   ___ _ _       _      _____  ___  _____  ___ 
  / __\\ (_)_ __ | | __ /__   \\/___\\/__   \\/ _ \\
 / _\\ | | | '_ \\| |/ /   / /\\//  //  / /\\/ /_)/
/ /   | | | | | |   <   / / / \\_//  / / / ___/ 
\\/    |_|_|_| |_|_|\\_\\  \\/  \\___/   \\/  \\/{Fore.RESET}

Creator: Kipruun
This module generates TOTP codes for a given secret key.
Please reffer to the documentation for more information.
"""
menu = f"""
{Fore.CYAN}[0]{Fore.RESET} - Generate codes for all hours of the current day
{Fore.CYAN}[1]{Fore.RESET} - Generate code for the current hour
{Fore.CYAN}[2]{Fore.RESET} - Configuration
{Fore.CYAN}[3]{Fore.RESET} - Exit
"""
print(header, menu)


config = config_load()
if config == {} or config.get("token") == None:
    print(f"\n{Fore.RED}We couldn't find the secret in the config file.{Fore.RESET}")    
    secret = input("Enter the family link's code: ")
    config_save(secret=secret)
else:
    secret = config.get("token")
    



if config.get("timezone") != None:
    time_zone = config.get("timezone")
else:
    time_zone = ""
totp_element = TOTPElement(secret, timezone=time_zone)

while True:
    choice = input(f"{Fore.CYAN}[?]> {Fore.RESET} ")
    os.system('cls' if os.name=='nt' else 'clear')
    print(header, menu)
    if choice == "0":
        print("Generating codes for all hours of the current day...")
        codes = totp_element.get_a_day_codes()
        for hour, code in codes:
            print(f"Hour: {hour:02d}:00 - Code: {code}")
        print("\nThe code for this hour is: " + totp_element.get_totp_code())
        
    elif choice == "1":
        print("The code for this hour is: " + Fore.CYAN + totp_element.get_totp_code() + Fore.RESET)

    elif choice == "2":
        os.system('cls' if os.name=='nt' else 'clear')
        print(header, menu)
        print(f"{Fore.CYAN}Configuration Menu{Fore.RESET}")
        print(f"{Fore.CYAN}[0]{Fore.RESET} - Show config")
        print(f"{Fore.CYAN}[1]{Fore.RESET} - Change timezone")
        print(f"{Fore.CYAN}[2]{Fore.RESET} - Change token")
        conf_user_choice = input(f"{Fore.CYAN}[+]>{Fore.RESET}")
        if conf_user_choice == "0":
            config = config_load()
        elif conf_user_choice == "1":
            print("List of timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List (tz identifiers)")
            timezone_user = input("Choose timezone: ")
            config_save(timezone=timezone_user)
        elif conf_user_choice == "2":
            token_user = input("Enter your token: ")
            config_save(secret=token_user)


        
    elif choice == "3":
        print(f"\n{Fore.RED}Exiting...{Fore.RESET}")
        break

        

