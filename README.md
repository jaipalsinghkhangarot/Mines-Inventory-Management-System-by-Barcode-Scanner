A Simple Database Management System to monitor Inoventory via barcode!

To start using the inventory DBS, download the file and Unzip in a folder of your choice.

Use a Python source code editor or IDE and set your workspace to the file you unzipped to (my preferred one is Visual Studio Code)

You will need to have some libraries installed, the command is:
pip install tkinter, sqlite3, pillow, pandas, SQLAlchemy

This code was made using Python 3.9.5 but any version 3.9 and above should work.

First Run create_db.py

Next run dashboard.py

dashboard.py your main program and you can add/modify/delete inventory by clicking on 'Admin Only' and putting in the password. The default password is 12345.

The timestamp for when items are added or modified are added to the 'inventory' table

-----------
I use DB Browser (SQLite) to look at the the database outside of Excel. While there shouldn't be bugs, this should be a helpful tool in looking at the SQLite tables when trying to change or debug the code.
https://sqlitebrowser.org/

-----------

To take off the Footer message with my name and contact, click the gray area underneath.
