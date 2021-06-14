# serial tool command line for Windows Terminal

# Dependency
- python 2.7
- pip install pyserial
- pip install pyinstaller

# How to use
- Check the runablity of the script through command line firstly(power shell)
- Generate .exe by run: pyinstaller -y serial_port.py
- Add the serial_port.exe to the windows terminal list, such as:
    >   "profiles":
    >    {
    >        "defaults": {},
    >        "list":
    >        [
    >            {
    >                "guid": "{0caa0dad-35be-5f56-a8ff-afceeeaa610a}",
    >                "hidden": false,
    >                "colorScheme": "One Half Dark",
    >                "name": "serial tool",
    >                "commandline": "C:\\serial_port\\dist\\serial_port\\serial_port.exe"
    >            },
    >        ]
    >    }

# Fuctionality
when the tools run successfully, you should be able to see
>   **** Serial tool v0.0 used for command line ****
>   **** press' + SQ +'to exit or '+ SR+'refresh com port ****
>   no COM port available

Or
>   **** Serial tool v0.0 used for command line ****
>   **** press' + SQ +'to exit or '+ SR+'refresh com port ****
>   select port form list:
>   COM67 - mbed Serial Port (COM67)

# Support command
- Press 'SQ' + enter to terminate the tool
- Press 'SR' + enter to refresh the com port list
- Select COM port: com67 or com67:9600, the default baudrate is 115200.