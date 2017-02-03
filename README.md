# Ty's XSS Fuzzer

How to:
Launch console with python xsshell.py

Note0: Still a WIP <br>
Note1: This is my first python program so the code may not be high quality stuff <br>

Semi-intelligent fuzzing tool. Program analyzes html output and constructs attack strings based on the output. If desired, the program will modify each character to attempt to bypass filtering. <br>

One advantage of this fine-tuned approach is fewer network connections, so you don't have to flood the target network. <br>

Program interface is a unix-like command prompt (Think msfconsole). <br>

Multithreaded Support - Set thread count when spidering or fuzzing. <br>

Connection Delay - Set connection delays to avoid flooding the target or to avoid any mechanisms that prevent frequent connections.<br>

