Notes
    You will need a Linux system to build an Android Package Kit (APK) or use the windows subsystem for linux.
    This only works for android phones, it should be possible for iphones as buildozer can also make files for IOS but that has not been tested
    During installation errors can occurr, errors that occurred are stated below with the solution I used.

requirements
    python- sudo apt install python3.10
    pip- sudo apt install pip
    buildozer
        git - sudo apt-get install git
        java - sudo apt-get install openjdk-11-jdk
        unzip - sudo apt-get install unzip
        zip - sudo apt-get install zip
        autoconf - sudo apt-get install autoconf
        sudo apt install build-essential libltdl-dev libffi-dev libssl-dev
        *git clone https://github.com/kivy/buildozer.git* in the directory where PokemonNuzlockeTracker is located, it should be a sibling folder
        Use *cd buildozer* to go into the directory and run *sudo python3 setup.py install* to install buildozer
    android debrug bridge(adb), optional- sudo apt install adb for linux and download it here for windows https://dl.google.com/android/repository/platform-tools_r27.0.0-windows.zip

Build APK
    Buildozer needs a *buildozer.spec* which is provided in the root directory of the program. Depending on what you added it could need modification. With most modifications you won't need to modify the .spec file.
    To actually make the APK you would need to run *sudo buildozer android debug* in the root folder, the same place where the *buildozer.spec* is located.
    This command could take several minutes, up to 15 in my experience, if it is the first time you create the APK, after that the command should not be as time consuming.
    the APK should appear in the PokemonNuzlockeTracker/bin directory

transfer APK to phone
    There are multiple ways to transfer the APK to your phone, one is to manually connect your phone to your computer through a USB cable and drag the APK to your phone. Then you can install it to your phone.
    This way however is, in my opinion, tedious for multiple deployments. So I opt for using adb which can install it to your phone through a wifi connection. Both machine and phone need to be connected to the same wifi network for this to work.

    To use adb, first connect your phone to your machine through USB, if asked to allow access to your phone, press yes. Unlock developer options on your phone, usually done by tapping build number 7 times in the settings menu. Then enable usb debugging and wireless debugging. Also take note of the IP address your phone has as we'll need it later.
    On windows unzip the platform tools folder and open a terminal (cmd) there, NO powershell as that doesn't work. Use left shift + right click in the folder to get the terminal option.
    In the terminal run *adb devices*, it should show your device connected through USB, now run *adb tcpip 5555* to start the service on port 5555 and you can remove the USB cable. The windows terminal can now be closed.

    On Linux run *adb connect PHONE_IP:5555* to connect to your phone, this should start a new service and also ask for permission on your phone. Allow the connection.
    Navigate to PokemonNuzlockeTracker/bin, the location where the APK is and run *adb -s PHONE_IP:5555 install APK_NAME*, both PHONE_IP and APK_NAME can be autocompleted using the TAB key. It should now install to your phone. When you want to deploy again you only have to use the linux commands to connect and to install.




ERRORS
    Error trying to create APK gradle error message
    Run *buildozer android clean* and try to build it again. If that does not work, uninstall java using *sudo apt remove openjdk-11-jdk* and install a newer version if applicable

    SDK error, remove the folder at /.buildozer/android/platform called android-sdk this is in the same directory where the buildozer folder is located. remove the android sdk folder by using *sudo rm -r android-sdk* and try the command again

    streaming to phone
    Failure [INSTALL_FAILED_UPDATE_INCOMPATIBLE: Existing package org.test.nuzlocketracker signatures do not match newer version; ignoring!]
    Remove the application from your phone and retry