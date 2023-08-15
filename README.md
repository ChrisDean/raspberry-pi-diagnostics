# raspberry-pi-diagnostics
This a script to run hardware diagnostics against most models of raspberry pi (I've not checked all features across 
the board but happy to take feedback.

It was written due to a need to batch test a set of about 200 raspberry pis with no quick and easy non-commercial 
option to do so.

It should just run and work. If it doesn't do feel free to submit a bug report and then attempt to fix it and submit 
a PR for your fix.

Usage:
clone this repo and: 

#1 Run the following to install necessary tools and libraries
```
python ./dependencies_check.py
```

#2 Run the following to perform the diagnostics
```
python ./diagnostics.py
```

#3 Optional: Run the following to install the diagnotics script as a service
so it runs on boot (good for plugin, test board, and go)
```
python ./install_as_service.py
```

## Limitations
The latest raspbian removes access to vcgencmd which has meant workarounds to attempt to aquire similar information 
to that which vcgencmd returned originally - the tests here are fine for my use case but you may want to exand on them.
If you do, please submit a PR!

## Sponsors
This project currently has no sponsors so is only maintained as I need or as PR's come in. If you are an industrial 
or similar user and want specific adaptions or support, raise an issue requesting that I contact you.

## License
Standard Apache 2.0 license.
Please fork and reference the project if used elsewhere - I'm always interested to know who has found it useful. 