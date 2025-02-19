# slack-wlan-status-updater
Sets the Slack status on Windows OS depending on the active wifi network

## Credits

The repo is mainly based on [slack-wlan-status-updater](https://github.com/martin-ueding/slack-wlan-status-updater) - martin-ueding deserves all credits!
I just adapated the code so that is runs on Windows OS.


## Requirements

See 'requirements.txt'


## Configuration

See 'config.toml'


### Optional environment variable

These environment variables are required

* "HTTPS_PROXY" = "your_company's_https_proxy_url_and_port"


## Sample 'config.toml'

The repo comes with the sample config file 'config-sample.toml' with the
following content

```
[slack.Work]
token = "xxxx-xxxx"  # Token of the Slack instance with the name 'Work'; requires users.profile.set API method

[environments.Home]
network = "home-wifi"  # SSID of the wifi network at home
emoji = "house_with_garden"  # name of the emoji in Slack
text = "Working @ Home"
until = "17:30"

[environments.Work]
network = "work-wifi"
emoji = "office"
text = "Working in the office"
until = "17:00"
```


## Questions & Answers

Here are some common questions and answers.


### How can I run the tool?

Create a batch file with the following command:
```
python __main__.py
```
Put the batch file into the startup folder of Windows.


Or create an executable with the following command:
```
make_exe.bat
```
Then, put the executable 'slack-wlan-status-updater.exe' into the startup folder of Windows.


### Where to put the config file?

Create the config file 'config.toml' and keep it in the same folder as the files '__main__.py'
or 'slack-wlan-status-updater.exe', respectively.