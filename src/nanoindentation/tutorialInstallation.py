"""
Linux
=====

1. Clone this github repository (ensure git is installed)::

	git clone https://github.com/micromechanics/main.git

2. Install packages using requirements (contains numpy, matplotlib, scipy etc).
Make sure you are typing the command in the correct folder (requirements.txt is in "main" after successful cloning) ::

	cd main
	pip3 install -r requirements.txt

If pip has not been installed::

   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # download pip script
   sudo python3 get-pip.py

If pip is installed, make sure it is the latest version::

	python3 -m pip install --upgrade pip

3. Add the folder with the source code to the pythonpath. Open and edit with text editor (e.g. gedit).
Type in the terminal in home directory::

	gedit .bashrc

and add in the end for pythonpath the location of the folder, for example::

	export PYTHONPATH=$PYTHONPATH:/home/*USER*/...../main

where "*USER*" is your user name and "....." is the folder where you cloned this repository.
Save and close. To test whether it is working, open new terminal and in interactive python console (e.g ipython3) type::

	ipython3
	from nanoindentation import Indentation, Tip

It should not report back any errors.

Windows
=======

1. Install git. Go to http://git-scm.com/download/win and download '64-bit Git for Windows Setup' (mostlikely choice).
Install git using:

	- under "Adjusting your PATH environment" choose:  Git from the command line and also from 3rd-party software
	- under "Choosing the ssh executable" choose:  use OpenSSH
	- under "Choosing the HTTPS transport backend" choose:  Use the OpenSSL library
	- under "Configuring the line ending conversions" choose:  Checkout Windows-Style, commit Unix-Style line endings
	- under "Configuring the terminal emulator to use with Git bash" choose:  Use minTTY
	- under "Choose the default behavior of 'git pull'" choose:  Default
	- under "Choose credential helper" choose:  Git credential Manager Core
	- under "Configure extra options" choose:  Enable filesystem caching and Enable symbolic links

2. Using the command-line tool "CMD.exe":

	- change to your "MyDocuments"
	- type "git clone git@github.com:micromechanics/main.git"

3. Adopt the "System Variables" or "Environment Variables" (search "systemvariables" in the Windows search bar) and edit
the variables "for your account". Edit the entry path and add::

	C:\\Users*USER*\\Documents\\Micromechanics

Mac OS
=======

1. Clone this github repository (ensure git is installed)::

	git clone git@github.com:micromechanics/main.git

2. Install packages using requirements (contains numpy, matplotlib, scipy etc) ::

	pip3 install -r requirements.txt

3. Add the directory /Users/'username'/.../main to the PYTHONPATH

	- open Terminal.app

	- open the file .bash_profile with text editor (for example, atom)::

		atom ~/.bash_profile

	- Add the following line to the end::

		export PYTHONPATH="/Users/'username'/.../main"

	- Save the file.

	- Type the following command in Terminal::

		source ~/.bash_profile

	- check the PYTHONPATH::

		echo $PYTHONPATH
	It should show something like /Users/'username'/.../main

4. Checking system environment variables in Python::

	import os
	os.environ['PYTHONPATH']
	/Users/'username'/.../main

"""
