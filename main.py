#!/usr/local/bin/python3.10

from main_platform import *
import sys, os, termcolor

def openEditor(file):
    file = os.path.abspath(file)

    a = open(file)
    content = a.read()
    a.close()

    foundEditor = False
    for i in ("nano", "vim", "vi", "gedit -w"):
        if os.system(i + " " + repr(file)) == 0:
            foundEditor = True
            break

    a = open(file)
    new_content = a.read()
    a.close()

    if foundEditor:
        if content == new_content:
            if askYesOrNo("Are you sure not to modify this file?"):
                return openEditor(file)
            else:
                return False
    else:
        raise OSError("couldn't found any editor")
    
    return True

def askYesOrNo(prompt):
    a = input(prompt + " (y/n) ").lower()
    while not a in ("y", "n"):
        print("Please write y or n")
        a = input(prompt).lower()
    return a == "y"

def playInstallation(platform):
    if askYesOrNo("Do you want to modify the configuration files?"):
        try:
            for file in ("mail", "i18n", "owner", "verbosePolicy"):
                path = platform.configuration().confDirectory + "/" + file + ".conf"
                print("Editing the configuration file", termcolor.colored(path, "green"))
                openEditor(path)
        except OSError:
            print(termcolor.colored("Couldn't find any editor. Please install nano, vi or vim"))

    if askYesOrNo("Do you want to install the microportal background service?"):
        a = open("/etc/systemd/system/microportal.service", "w")
        a.write("""[Unit]
Description=Microportal domotic project
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=python3 {path} --run
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target""".format(path = os.path.abspath(__file__)))
        a.close()
        os.system("systemctl enable microportal.service")
    

def printHelp():
    print("""usage : {PATH} [--server|--help|-h]

Options : 
    	--run :
                make the platform handling
        
        --install :
                runs the install programm

    	--help|-h :
                displays this help

""".format(PATH = sys.argv[0]))

def main(args):
    platform = Platform()
    if not args[ 1 : ]:
        return printHelp()
    command = args[1]
    if  command in ("--run",):
        platform.handle()
        print()
    elif command in ("--help","-h"):
        return printHelp()
    elif command in ("--install"):
        return playInstallation(platform)
    else:
        printHelp()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
