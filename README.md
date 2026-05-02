# Automatic_SQL_Injection_Testing_Tool
Automatic Find  Any Website Sql and Auto Exploit site access easily


(![image](https://i.ibb.co.com/Z1mwqSwT/2026-05-02-140213.png)


```bash
INSTALL COMMAND
git clone https://github.com/chowdhuryvai/Automatic_SQL_Injection_Testing_Tool.git
cd Automatic_SQL_Injection_Testing_Tool
python Automatic_SQL_Injection_Testing_Tool.py
```


```bash
🎯 Tool Features:
✅ 500 SQL Injection Payloads

✅ Auto-Exploit Feature

✅ Professional UI with Tkinter

✅ Real-time Terminal Output

✅ Vulnerability Detection

✅ Multi-threaded Scanning
```


```bash
🛡️ IMPORTANT DISCLAIMER:
This tool is for educational and ethical hacking purposes only!

⚖️ Legal Uses:
Testing your own website

Testing websites with written permission

Participating in bug bounty programs

Using in local testing environments

Using in CTF (Capture The Flag) competitions

⛔ Illegal Uses:
Scanning a website without permission is a crime

Testing SQL injection on another website is a cyber crime

Accessing a database without permission is punishable by law

🔴 Bangladesh Laws:
Information and Communication Technology (ICT) Act 2006

Digital Security Act 2018 (DSA)

Unauthorized hacking is punishable by a maximum of 14 years in prison or a fine of Tk 1 crore or both
```

```bash
🎯 Testing Target (Practice Site):
Use the following legal practice sites to test the tool:
http://testphp.vulnweb.com/artists.php?artist=1
http://testphp.vulnweb.com/listproducts.php?cat=1
```



```bash
📋 In the terminal you will see:

==============================================================
   SQLiFinder Pro v3.0 - Starting Scan
   SC-ETHICAL HACKER IN BANGLADESH
==============================================================
Target URL: http://testphp.vulnweb.com/artists.php?artist=1
Parameter: artist
Total Payloads: 500
Auto-Exploit: Enabled
==============================================================

[12:30:45] Testing payload: ' OR '1'='1...
[12:30:46] 🚨 VULNERABILITY FOUND: ' OR '1'='1
[12:30:46]    Type: Error-based SQL Injection
[12:30:46]    ⚡ Attempting auto-exploit...
[12:30:47]    ✅ Exploit successful!
```

```bash
# First check if Python is installed
python --version
# or
python3 --version

# Install the required libraries
pip install requests
pip install python-tk
pip install urllib3

# or install all together
pip install requests urllib3

# Tkinter is usually built-in with Python
# If not:

# Ubuntu/Debian/Linux Mint:
sudo apt-get update
sudo apt-get install python3-tk

# Kali Linux:
sudo apt-get install python3-tk

# Windows:
# Tkinter is usually installed automatically when installing Python
# If not, reinstall Python and select tkinter

# MacOS:
brew install python-tk

# Save the file
nano Automatic_SQL_Injection_Testing_Tool.py
# or
gedit Automatic_SQL_Injection_Testing_Tool.py
# or
code Automatic_SQL_Injection_Testing_Toolr.py
# Paste the code and save (Ctrl+S)

# Run the tool
python Automatic_SQL_Injection_Testing_Tool.py
# or
python3 Automatic_SQL_Injection_Testing_Tool.py

# If Permission denied error appears:
chmod +x Automatic_SQL_Injection_Testing_Tool.py
python3 Automatic_SQL_Injection_Testing_Tool.py

# In Windows Command Prompt or PowerShell:
python Automatic_SQL_Injection_Testing_Tool.py

# If there is more than one Python version:
python3 Automatic_SQL_Injection_Testing_Tool.py
# or
py Automatic_SQL_Injection_Testing_Tool.py
```
