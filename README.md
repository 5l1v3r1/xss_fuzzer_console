# Ty's XSS Fuzzer

Note0: Still a WIP <br>
Note1: This is my first python program so the code may not be high quality stuff <br>

Semi-intelligent fuzzing tool. Program analyzes html output and constructs attack strings based on the output. If desired, the program will modify each character to attempt to bypass filtering. <br>

One advantage of this fine-tuned approach is fewer network connections, so you don't have to flood the target network. <br>

Program interface is a unix-like command prompt (Think msfconsole). <br>

Multithreaded Support - Set thread count when spidering or fuzzing. <br>

Connection Delay - Set connection delays to avoid flooding the target or to avoid any mechanisms that prevent frequent connections.<br>

##Todo: Additions

###Large 
Stored XSS analysis<br>
Right now only the spider has been implemented; initial version of fuzzer not added yet <br>

###Medium 
Handle JS reflect context<br>
Handle unique attribute reflect content<br>
Improve Spider: Consider beautifulsoup, check 'src' attr<br>
Check forms/input for URLs (currently only check a tags)<br>
Make attack on main thread with a whole lot of progress output <br>

###Small 
Spider output when finished <br>
Handle printing to sdout without disrupting the cmd line<br>
Implement show command to show current attack urls <br>
For showing specific url data show snippet of reflection and current fuzzer characters, and the target string<br>


