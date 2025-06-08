
# Family TOTP generator
Thanks to [Rifting](https://gist.github.com/rifting) for the method. ([post used](https://gist.github.com/rifting/732a45adf8ebacfa0e1fda0a66662570?permalink_comment_id=5180196#gistcomment-5180196))

🚧 Time zone should be in this format (tz identifier) : [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)
 
## CLI:
### Installation:
`$ git clone https://github.com/kipruun/FLink-TOTP.git`
`$ python -m pip intall pytz pyotp colorama`
 
### Usage:

    $ cd FLink-TOTP
    $ python cli-flink.py
              ___ _ _       _      _____  ___  _____  ___ 
             / __\ (_)_ __ | | __ /__   \/___\/__   \/ _ \
            / _\ | | | '_ \| |/ /   / /\//  //  / /\/ /_)/
           / /   | | | | | |   <   / / / \_//  / / / ___/ 
           \/    |_|_|_| |_|_|\_\  \/  \___/   \/  \/
          
          Creator: Kipruun
          This module generates TOTP codes for a given secret key.
          Please reffer to the documentation for more information.
          
          [0] - Generate codes for all hours of the current day
          [1] - Generate code for the current hour
          [2] - Configuration
          [3] - Exit
          ...
Configuration menu:

          Configuration Menu
          [0] - Show config
          [1] - Change timezone
          [2] - Change token  


### Config file format:

Name of file : config.json

Format:

    {
     "token": "YOUR_SECRET",
     "timezone": "Europe/Paris"
    }



