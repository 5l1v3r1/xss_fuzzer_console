# Ty's XSS Fuzzer
# NOTE: This is still a WIP, but it should be functioning at a basic level by 1/14/17

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
Handle multiple simultaneous attack sessions (run multiple fuzzers and spiders simultaneously) <br>

###Medium 
Add Options to Scan Robots.txt<br>
Check for /sitemap.html or /sitemap.xml for spider<br>
Handle JS reflect context<br>
Handle unique attribute reflect content<br>
Improve Spider: Consider beautifulsoup, check 'src' attr<br>
Check forms/input for URLs (currently only check a tags)<br>
Make attack on main thread with a whole lot of progress output <br>
Change maximum depth option, so that direct directory children receive the set depth, rather than getting decremented <br> 
Make it so that on first connection, for one of the parameterized url's query parameters, the html response will be saved for that AttackURL (kind of unintelligible). This will reduce at least one network connection per url <br> 
Allow saving config and loading ( set -s _name_ ) <br> 
Consider allowing scope modification -- Expand upon set -target

###Small 
Add spider duration option <br> 
Add Attack Attempt Count option <br>
Add Parameter Limit option <br>
Spider output when finished <br>
Handle printing to sdout without disrupting the cmd line<br>
Implement show command to show current attack urls <br>
For showing specific url data show snippet of reflection and current fuzzer characters, and the target string<br>
Rename DictQueue to something cooler like AttackSession or something <br>

