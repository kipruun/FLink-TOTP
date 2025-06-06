from totp import TOTPElement
from colorama import init, Fore
import os


init(autoreset=True)  




def config_load():
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(path, "config.cfg")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                config = {}
                if line.startswith("TIMEZONE="):
                    config["timezone"] = line.split("=")[1].strip()
                    print(f"Timezone loaded: {config['timezone']}")
                if line.startswith("SECRET="):
                    config["secret"] = line.split("=")[1].strip()
                    print(f"Secret loaded: {config['secret']}")
        return config
    return {}


def config_save(timezone=False, secret=False):
    config = []
    if timezone != False:
        config.append(f"TIMEZONE={timezone}")
    if secret != False:
        config.append(f"SECRET={secret}")
    if len(config) > 0:
        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path, "config.cfg")
        with open(file_path, "w") as file:
            for line in config:
                file.write(line + "\n")
        return True
    return False




print(f"""{Fore.CYAN}   ___ _ _       _      _____  ___  _____  ___ 
  / __\\ (_)_ __ | | __ /__   \\/___\\/__   \\/ _ \\
 / _\\ | | | '_ \\| |/ /   / /\\//  //  / /\\/ /_)/
/ /   | | | | | |   <   / / / \\_//  / / / ___/ 
\\/    |_|_|_| |_|_|\\_\\  \\/  \\___/   \\/  \\/{Fore.RESET}

Creator: Kipruun
This module generates TOTP codes for a given secret key.
Please reffer to the documentation for more information.

{Fore.CYAN}[0]{Fore.RESET} - Generate codes for all hours of the current day
{Fore.CYAN}[1]{Fore.RESET} - Generate code for the current hour
{Fore.CYAN}[2]{Fore.RESET} - Configuration
{Fore.CYAN}[3]{Fore.RESET} - Show configuration
{Fore.CYAN}[4]{Fore.RESET} - Exit
""")
config = config_load()
if "secret" in config:
    secret = config["secret"]
else:
    print(f"\n{Fore.RED}We couldn't find the secret in the config file. We recommend you to set it up in the configuration menu.{Fore.RESET}")    
    secret = input("Enter the family link's code: ")



# Check if timezone is set in config
if "timezone" in config:
    time_zone = config["timezone"]
else:
    time_zone = ""
totp_element = TOTPElement(secret)


while True:
    choice = input(f"{Fore.CYAN}[?]> {Fore.RESET} ")

    if choice == "0":
        print("\nGenerating codes for all hours of the current day...")
        if time_zone == "":
            codes = totp_element.get_a_day_codes()
        else:
            codes = totp_element.get_a_day_codes(time_zone)
        for hour, code in codes:
            print(f"Hour: {hour:02d}:00 - Code: {code}")
        print("\nThe code for this hour is: " + totp_element.get_totp_code())
        
    elif choice == "1":
        print("\nThe code for this hour is: " + Fore.CYAN + totp_element.get_totp_code() + Fore.RESET)

    elif choice == "2":
        print(f"\n{Fore.CYAN}Configuration Menu{Fore.RESET}")
        print(f"Current timezone: {time_zone if time_zone else 'Not set'}")
        time = input("Enter the timezone (e.g., Europe/Paris) or leave empty to use the default: ")
        secret = input("Enter the secret key or leave empty to keep the current one: ")
        config_save(timezone=time if time else False, secret=secret)
        print(f"\n{Fore.GREEN}Configuration saved successfully!{Fore.RESET}")
        
    elif choice == "3":
        print(f"\n{Fore.CYAN}Current Configuration{Fore.RESET}")
        print(f"Timezone: {config.get('timezone', 'Not set')}")
        print(f"Secret: {config["secret"]}")

    elif choice == "4":
        print(f"\n{Fore.RED}Exiting...{Fore.RESET}")
        break

