# Ty's XSS Fuzzer

Semi-intelligent fuzzing tool. Program analyzes html output and constructs attack strings based on the output. If desired, the program will modify each character to attempt to bypass filtering. 

One advantage of this fine-tuned approach is fewer network connections, so you don't have to flood the target network. 

Program interface is a unix-like command prompt (Think msfconsole).

Multithreaded Support - Set thread count when spidering or fuzzing

Connection Delay - Set connection delays to avoid flooding the target or to avoid any mechanisms that prevent frequent connections.

##Todo: Additions

###Large 
Stored XSS analysis

###Medium 
Handle JS reflect context
Handle unique attribute reflect content
Improve Spider: Consider beautifulsoup, check 'src' attr
Check forms/input for URLs (currently only check a tags)

###Small 
Spider output when finished 
Handle printing to sdout without disrupting the cmd line


