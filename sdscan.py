#Author : Nemuel Wainaina
'''
    This is a simple python script that is handy for Information Gathering as it
    can be used to scan for the available subdomains on a target URL
'''

import requests
import os
from colorama import init, Fore

# initialize some colors
init()
GREEN = Fore.GREEN
BLUE = Fore.BLUE
RED = Fore.RED
GRAY = Fore.LIGHTBLACK_EX
RESET = Fore.RESET

# obtain the information from the user
target = input(f"[*] Enter Target URL: ")
file = input(f"[*] Enter file containing potential subdomains: ")

# check whether the file exists
if not os.path.exists(file):
    print(f"{RED}[!] The file {file} does not exist!{RESET}\n")
    exit(0)
    
# check whether we have permissions to read the file
if not os.access(file, os.R_OK):
    print(f"{RED}[!] Access to the file is denied!{RESET}")
    exit(0)
    
total = len(open(file, "r").read().splitlines()) # total number of potential subdomains from the specified file
valid_subdomains = [] # list to hold the valid subdomains before writing them to a file
valid = 0 # to keep track of valid subdomains

# Checks whether the subdomain exists or not
def check_sd(sd):
    url = f"https://{sd}.{target}"
    try:
        requests.get(url)
    except requests.ConnectionError:
        print(f"{GRAY}[-] Invalid : http://{sd}.{target}{RESET}")
    else:
        valid_subdomains.append(sd)
        print(f"{GREEN}[+] Valid : http://{sd}.{target}{RESET}")
        global valid
        valid += 1
        
# read list of names from the specified file
sd_list = open(file, "r").read().splitlines()

print(f"\n{BLUE}[$~] Starting scan for {target} : {RESET}\n")
for sd in sd_list:
    check_sd(sd)
    
print(f"\n[*] Done!")
print(f"{BLUE}=> Found {valid} valid subdomains out of the {total}{RESET}")

# writing the valid subdomains to a file
out_file = target + ".txt"
with open(out_file, "w") as of:
    for sd in valid_subdomains:
        of.write(sd + "\n")
print(f"{GREEN}=> Valid Subdomains saved to : {target}.txt{RESET}\n")