# OrbitLicenses v22.40

### What's this !??
>* A Python Licensing Discord Bot made with [hikari](https://github.com/hikari-py/hikari) and [hikari-lightbulb](https://github.com/tandemdude/hikari-lightbulb), Mainly made for minecraft plugin licensing, although you can use this bot to as licensing system for any other software, as it saves the licenses and data in a MySql database, wich can be use it for whatever you want.

### Installation
First download all the files from the repository, then create a python3 venv in the main folder and actiavte it, to do so first start a shell and go to the main folder directory:

Linux
```shell
python -m venv .venv
source .venv/bin/activate
```
Windows
```shell
python -m venv .venv
.\.venv\Scripts\activate
```
Then your folder should look like this:

![photo of the folder](https://i.imgur.com/iO78MLM.png)


Then install the requirements.txt using [pip](https://pip.pypa.io/en/stable/)

```shell
pip install -r requirements.txt
```

Following this go to "\OrbitLicense\bot\config" open config.json and change "token" to your aplication token and change the [MySql](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) data,  for install mysql on widonws [click here](https://www.apachefriends.org/download.html), you can also change any setting in the configuration.

Then start the launcher script and there you go!
```shell
python ./launcher.py
```
