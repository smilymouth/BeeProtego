import tkinter as tk
import tkinter.ttk as ttk
import requests
import json 
import hashlib
import subprocess
import platform
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Preformatted
from datetime import date, datetime
import os
import threading
from tkinter import filedialog
import time

os.makedirs(os.path.expanduser("~/logs"), exist_ok=True)

root = tk.Tk()
root.title("Bee Protego")
root.state("zoomed")
root.configure(bg="#231f20")
root.iconbitmap("favicon.ico")


root.grid_columnconfigure(0, weight=0, minsize=220)  
root.grid_columnconfigure(1, weight=1)               
root.grid_columnconfigure(2, weight=0, minsize=270)

center_frame = tk.Frame(root, bg="#1f1c1d")
center_frame.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)

home_page = tk.Frame(center_frame, bg="#231f20")
scan_page = tk.Frame(center_frame, bg="#231f20")
logs_page = tk.Frame(center_frame, bg="#231f20")
ask_ai_page = tk.Frame(center_frame, bg="#231f20")

scan_paused = False
scan_stop = False
stop_requested = False

def run_scan_thread(target_func):
    threading.Thread(target=target_func, daemon=True).start()

def browse_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def browse_directory():
    folder = filedialog.askdirectory()
    if folder:
        selected_directory.set(folder)


models = [
  
    "gemma3:1b",
    "gemma3:2b",
    "gemma3:3b",
    "gemma3:4b",
    "gemma3:7b",

   
    "qwen-7b",
    "qwen-14b",
    "qwen-7b-chat",
    "qwen-14b-chat",

    
    "GPT-Neo 1.3B",
    "GPT-Neo 2.7B",
    "GPT-J 6B",
    "GPT-NeoX 20B",
    "Pythia 70M",
    "Pythia 160M",
    "Pythia 410M",
    "Pythia 1B",
    "Pythia 2.8B",
    "Pythia 6.9B",
    "Pythia 12B",
    "LLaMA 7B",
    "LLaMA 13B",
    "LLaMA 65B",
    "Falcon 7B",
    "Falcon 40B",
    "Alpaca 7B"
]


def ask_ollama_thread():
    user_input = input_box.get("1.0", "end").strip()
    selected_model = model_combo.get()

    if not user_input:
        return

    output_box.insert(tk.END, "🐝 Buzzy AI is thinking...\n")
    output_box.see(tk.END)

    threading.Thread(
        target=run_ollama,
        args=(selected_model, user_input),
        daemon=True
    ).start()


def run_ollama(selected_model, user_input):
    try:
        process = subprocess.Popen(
            ["ollama", "run", selected_model, user_input],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for line in process.stdout:
            output_box.after(0, lambda l=line: output_box.insert(tk.END, l))

        process.wait()

    except Exception as e:
        output_box.after(0, lambda: output_box.insert(tk.END, f"Error: {e}\n"))


def add_placeholder(entry, placeholder_text):
    def on_focus_in(event):
        if event.widget.get() == placeholder_text:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="#FFF600")

    def on_focus_out(event):
        if not event.widget.get():
            event.widget.insert(0, placeholder_text)
            event.widget.config(fg="gray")

    entry.insert(0, placeholder_text)
    entry.config(fg="gray")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def get_file_path():
    path = file_entry.get().strip()

def get_file_path():
    path = file_entry.get().strip()

    if not path:
        log_box2.insert(tk.END, "[ERROR] File path not entered.\n")
        log_box2.insert(tk.END, "👉 Please enter the file path in Scan window.\n\n")
        log_box2.see(tk.END)

        log_box.insert(tk.END, "[ERROR] File path not entered.\n")
        log_box.insert(tk.END, "👉 Please enter the file path in Scan window.\n\n")
        log_box.see(tk.END)

        return None

    if not os.path.exists(path):
        log_box2.insert(tk.END, "[ERROR] File does not exist.\n\n")
        log_box2.see(tk.END)

        log_box.insert(tk.END, "[ERROR] File does not exist.\n\n")
        log_box.see(tk.END)

        return None

    return path

yara_exe = os.path.abspath("yara64.exe")          
yara_rules = ["malware_index.yar",
              "maldocs_index.yar",
              "cve_rules_index.yar" ]


def write_log(text):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
    line = timestamp + text + "\n"

  
    log_box2.insert(tk.END, line)
    log_box2.see(tk.END)

    logfile = datetime.now().strftime("logs/%Y-%m-%d.log")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line)


def export_logs_to_pdf():
    log_text = log_box2.get("1.0", tk.END).strip()
    if not log_text:
        return

    os.makedirs("pdf_logs", exist_ok=True)
    

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"pdf_logs/BeeProtego_Report_{timestamp}.pdf"
    
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCenter",
        parent=styles["Heading1"],
        alignment=TA_CENTER
    )

    story = []

    story.append(Paragraph("Bee Protego – Malware Scan Report", title_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Scan Date:</b> {datetime.now()}", styles["Normal"]))
    story.append(Paragraph(f"<b>Target File:</b> {get_file_path()}", styles["Normal"]))
    story.append(Spacer(1, 15))

  
    malware_hits = log_text.count("MALWARE DETECTED")
    yara_hits = log_text.count("YARA MATCH")

    if malware_hits > 0 or yara_hits > 0:
        verdict = "MALICIOUS"
        severity = "HIGH"
        verdict_text = "⚠️ Malware activity detected. Immediate action recommended."
    else:
        verdict = "CLEAN"
        severity = "LOW"
        verdict_text = "✅ No malicious activity detected in this scan."

    story.append(Paragraph("<b>Scan Summary</b>", styles["Heading2"]))
    story.append(Paragraph(f"Verdict: <b>{verdict}</b>", styles["Normal"]))
    story.append(Paragraph(f"Severity: <b>{severity}</b>", styles["Normal"]))
    story.append(Paragraph(f"Malware Hits: {malware_hits}", styles["Normal"]))
    story.append(Paragraph(f"YARA Matches: {yara_hits}", styles["Normal"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Important Findings</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    important_lines = []
    keywords = ["DETECTED", "ERROR", "WARNING", "YARA MATCH"]

    for line in log_text.split("\n"):
        if any(keyword in line for keyword in keywords):
            important_lines.append(line)

    if important_lines:
        for line in important_lines[:50]: 
            safe = (
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )
            story.append(Preformatted(safe, styles["Code"]))
    else:
        story.append(Paragraph("No suspicious entries found.", styles["Normal"]))

    story.append(Spacer(1, 20))

   
    story.append(Paragraph("<b>Final Verdict</b>", styles["Heading2"]))
    story.append(Paragraph(verdict_text, styles["Normal"]))

    doc.build(story)

    log_box2.insert(tk.END, f"\nPDF Report Generated:\n{pdf_filename}")
    log_box2.see(tk.END)

print("Loading signatures...")

TXT_url = "https://raw.githubusercontent.com/Bee-Protego/beeprotego-signatures/main/beeprotego-signatures/malicious-hash/full-hash-sha256-aa.txt"
Json_url = "https://raw.githubusercontent.com/Bee-Protego/beeprotego-signatures/main/hashes/malware_hashes.json"
Local_hash = "ful_sha256"

print("Signatures loaded successfully.")

def run_all_yara_rules(yara_path, yara_rules_list, target_file):
    global stop_requested

    log_box2.insert(tk.END, f"[YARA] Scanning: {target_file}\n")
    log_box2.see(tk.END)

    for rule_file in yara_rules_list:

        if stop_requested:
            return False

        rule_path = os.path.abspath(rule_file)

        cmd = [yara_path, rule_path, target_file]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        while process.poll() is None:
            if stop_requested:
                process.terminate()
                return False
            while scan_paused:
                time.sleep(0.2)
                
            time.sleep(0.1)
        output = process.stdout.read()

        if output.strip():
            log_box2.insert(
                tk.END,
                f"🚨 YARA MATCH ({os.path.basename(rule_file)})\n{output}\n",
                "red_text"
            )
            return True

    log_box2.insert(tk.END, "[YARA] No match\n", "green_text")
    return False
def start_full_scan():
    global scan_paused, stop_requested

    scan_paused = False
    stop_requested = False

    dir_path = selected_directory.get()

    threading.Thread(
        target=full_directory_scan,
        args=(dir_path,),
        daemon=True
    ).start()



def full_directory_scan(dir_path):
    global scan_paused, stop_requested

    log_box2.insert(tk.END, f"\n[+] FULL SCAN STARTED\n{dir_path}\n\n")

    for root_dir, _, files in os.walk(dir_path):
        for file in files:

            if stop_requested:
                log_box2.insert(tk.END, "\n[!] Scan stopped by user\n")
                return


            while scan_paused:
                time.sleep(0.2)
                if stop_requested:
                    log_box2.insert(tk.END, "\n[!] Scan stopped by user\n")
                    return

            file_path = os.path.join(root_dir, file)
            log_box2.insert(tk.END, f"\n📄 {file_path}\n")

            file_hash = sha256_file(file_path)
            if file_hash in load_local_hashes("full_sha256.txt"):
                log_box2.insert(
                    tk.END,
                    f"🚨 HASH MATCH FOUND\n{file_path}\n",
                    "red_text"
                )
                scan_paused = True
                continue   


            if scan_file_with_rules(file_path, rules):
                log_box2.insert(
                    tk.END,
                    "⚠️ Suspicious strings detected\n",
                    "red_text"
                )

           
            if run_all_yara_rules(yara_exe, yara_rules, file_path):
                log_box2.insert(
                    tk.END,
                    "🚨 YARA MATCH FOUND\n",
                    "red_text"
                )
                scan_paused = True
                continue

    log_box2.insert(tk.END, "\n[✓] FULL SCAN COMPLETED\n")


def load_rules():
    return [
        "MZ",
        "PK",
        "7z",
        "Rar!",
        "cab",
        "exe",
        "dll",
        "scr",
        "pif",
        "bat",
        "cmd",
        "vbs",
        "js",
        "wsf",
        "jar",
        "cmd.exe",
        "powershell",
        "WScript.Shell",
        "Shell.Application",
        "regsvr32",
        "mshta",
        "rundll32",
        "cscript",
        "wscript",
        "schtasks",
        "at.exe",
        "CreateRemoteThread",
        "VirtualAllocEx",
        "WriteProcessMemory",
        "ReadProcessMemory",
        "OpenProcess",
        "GetProcAddress",
        "LoadLibrary",
        "LoadLibraryA",
        "LoadLibraryW",
        "GetModuleHandle",
        "GetModuleHandleA",
        "GetModuleHandleW",
        "ExitProcess",
        "CreateProcess",
        "NtCreateThreadEx",
        "ZwCreateThreadEx",
        "SetWindowsHookEx",
        "VirtualProtect",
        "ZwProtectVirtualMemory",
        "NtQueryInformationProcess",
        "NtQuerySystemInformation",
        "GetAsyncKeyState",
        "SetTimer",
        "SendMessage",
        "GetForegroundWindow",
        "GetWindowThreadProcessId",
        "CreateMutex",
        "IsDebuggerPresent",
        "FindWindow",
        "GetKeyState",
        "VkKeyScan",
        "mouse_event",
        "keybd_event",
        "BlockInput",
        "GetKeyboardState",
        "GetCursorPos",
        "SetCursorPos",
        "SendInput",
        "ShellExecute",
        "WinExec",
        "URLDownloadToFile",
        "InternetOpen",
        "InternetOpenUrl",
        "HttpOpenRequest",
        "InternetReadFile",
        "WinHttpOpen",
        "WinHttpConnect",
        "WinHttpSendRequest",
        "WinHttpReceiveResponse",
        "Base64Decode",
        "CryptAcquireContext",
        "CryptEncrypt",
        "CryptDecrypt",
        "CryptImportKey",
        "CryptExportKey",
        "XOR",
        "AES",
        "RSA",
        "RC4",
        "Obfuscate",
        "ReflectiveLoader",
        "HeapSpray",
        "Shellcode",
        "CodeInjection",
        "DllMain",
        "RunOnce",
        "RunServices",
        "RunServicesOnce",
        "StartupFolder",
        "SetServiceStatus",
        "OpenSCManager",
        "CreateService",
        "StartService",
        "OpenService",
        "ControlService",
        "QueryServiceStatus",
        "RegOpenKeyEx",
        "RegQueryValueEx",
        "RegCreateKeyEx",
        "RegSetValueEx",
        "RegDeleteValue",
        "RegDeleteKey",
        "TaskScheduler",
        "ScheduledTask",
        "socket",
        "connect",
        "send",
        "recv",
        "bind",
        "listen",
        "accept",
        "WSAStartup",
        "InternetConnect",
        "InternetWriteFile",
        "WinSock",
        "C2",
        "CommandAndControl",
        "DebugBreak",
        "DbgPrint",
        "NtSetInformationThread",
        "NtQueryInformationThread",
        "ZwQueryInformationThread",
        "CheckRemoteDebuggerPresent",
        "OutputDebugString",
        "NtClose",
        "Trojan",
        "Ransom",
        "Exploit",
        "Botnet",
        "Keylogger",
        "Backdoor",
        "Rootkit",
        "Cryptominer",
        "Dropper",
        "Spyware",
        "Adware",
        "Worm",
        "Virus",
        "Payload",
        "Infect",
        "Downloader",
        "Loader",
        "ExploitKit",
        "msfvenom",
        "Metasploit",
        "Empire",
        "CobaltStrike",
        "PowerSploit",
        "Veil",
        "Mimikatz",
        "Netcat",
        "Ncat",
        "Tor",
        "Proxy",
        "VPN",
        "Zloader",
        "Emotet",
        "TrickBot",
        "Dridex",
        "Formbook",
        "Azorult",
        "CopyFile",
        "MoveFile",
        "DeleteFile",
        "WriteFile",
        "ReadFile",
        "CreateFile",
        "eval(",
        "Invoke-Expression",
        "Invoke-WebRequest",
        "Invoke-Command",
        "System.Net.WebClient",
        "System.Management.Automation",
        "Add-Type",
        "Get-Process",
        "Get-Service",
        "Stop-Service",
        "Start-Process",
        "Start-Job"
    ]

rules = load_rules()


def scan_file_with_rules(file_path, rules):
    
    suspicious_found = []

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                chunk = chunk.lower()

                for rule in rules:
                    rule_bytes = rule.encode("utf-8").lower()

                    if rule_bytes in chunk and rule not in suspicious_found:
                        suspicious_found.append(rule)

    except Exception as e:
        print(f"Error Bro: {e}")
        return False

    if suspicious_found:
        log_box2.tag_configure("red_text", foreground="red")

        log_box2.insert(tk.END, f"Suspicious patterns found in {file_path}:\n", "red_text")
        log_box.insert(tk.END, f"Suspicious patterns found in {file_path}:\n", "red_text")

        for s in suspicious_found:
            log_box2.insert(tk.END, f"{s}\n")
            log_box.insert(tk.END, f"{s}\n")

        return True

    else:
        log_box2.insert(tk.END, f"No suspicious patterns found in {file_path}\n")
        log_box.insert(tk.END, f"No suspicious patterns found in {file_path}\n")

        return False   
def load_txt_hashes(url):
    r = requests.get(url)
    r.raise_for_status()
    return{line.strip() for line in r.text.splitlines() if line.strip()}


def load_json_signatures(url):  
    r = requests.get(url)
    r.raise_for_status()
    return json.loads(r.text)  

def load_local_hashes(file_path):
    try:
        with open(file_path, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"Error loading local hashes: {e}")
        return set()

def sha256_file(file_path):
    h = hashlib.sha256()
    with open(file_path,"rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def Scan_file():
    log_box2.tag_configure("red_text", foreground="red")
    log_box2.insert(tk.END, "Scan Started\n","red_text")
    log_box2.see(tk.END)
    log_box.insert(tk.END, "Scan Started\n","red_text")
    log_box.see(tk.END)

    path = get_file_path()
    if not path:
      return
    file_hash = sha256_file(path)



    log_box2.insert(tk.END, f"Hash: {file_hash}\n")
    log_box2.see(tk.END)
    log_box.insert(tk.END, f"Hash: {file_hash}\n")
    log_box.see(tk.END)

    txt_hash = load_txt_hashes(TXT_url)
    json_sigs = load_json_signatures(Json_url)
    hash =  load_local_hashes("full_sha256.txt")

    log_box2.insert(tk.END, "Signatures Loaded\n")
    log_box2.see(tk.END)
    log_box.insert(tk.END, "Signatures Loaded\n")
    log_box.see(tk.END)

    if file_hash in hash:
        log_box2.insert(tk.END, "[!] MALWARE DETECTED (HASH SIGNATURE)\n")
        log_box2.insert(tk.END, f"SHA256        : {file_hash}\n")
        log_box2.insert(tk.END, "Details       : Not available (TXT-only signature)\n\n")
        log_box2.see(tk.END)
        log_box.insert(tk.END, "[!] MALWARE DETECTED (HASH SIGNATURE)\n")
        log_box.insert(tk.END, f"SHA256        : {file_hash}\n")
        log_box.insert(tk.END, "Details       : Not available (TXT-only signature)\n\n")
        log_box.see(tk.END)
        return      

    for sig in json_sigs:
        if sig.get("sha256") == file_hash:
           log_box2.insert(tk.END, "[!] MALWARE DETECTED (JSON SIGNATURE)\n")
           log_box2.insert(tk.END, f"SHA256        : {sig['sha256']}\n")
           log_box2.insert(tk.END, f"Family        : {sig['malware_family']}\n")
           log_box2.insert(tk.END, f"File Name     : {sig['file_name']}\n")
           log_box2.insert(tk.END, f"Source        : {sig['source']}\n")
           log_box2.insert(tk.END, f"Fetched On    : {sig['fetched_on']}\n\n")
           log_box2.see(tk.END)
           log_box.insert(tk.END, "[!] MALWARE DETECTED (JSON SIGNATURE)\n")
           log_box.insert(tk.END, f"SHA256        : {sig['sha256']}\n")
           log_box.insert(tk.END, f"Family        : {sig['malware_family']}\n")
           log_box.insert(tk.END, f"File Name     : {sig['file_name']}\n")
           log_box.insert(tk.END, f"Source        : {sig['source']}\n")
           log_box.insert(tk.END, f"Fetched On    : {sig['fetched_on']}\n\n")
           log_box.see(tk.END)           
           return
    if file_hash in txt_hash:
        log_box2.insert(tk.END, "[!] MALWARE DETECTED (HASH SIGNATURE)\n")
        log_box2.insert(tk.END, f"SHA256        : {file_hash}\n")
        log_box2.insert(tk.END, "Details       : Not available (TXT-only signature)\n\n")
        log_box2.see(tk.END)
        log_box.insert(tk.END, "[!] MALWARE DETECTED (HASH SIGNATURE)\n")
        log_box.insert(tk.END, f"SHA256        : {file_hash}\n")
        log_box.insert(tk.END, "Details       : Not available (TXT-only signature)\n\n")
        log_box.see(tk.END)
        return
    else:
        log_box2.insert(tk.END, "No Virus Found in hash detection.\n")
        log_box2.see(tk.END)
        log_box.insert(tk.END, "No Virus Found in hash detection\n")
        log_box.see(tk.END)
    if not os.path.exists(get_file_path()):
        log_box2.insert(tk.END, "File not found\n")
        log_box.insert(tk.END, "File not found\n")
        return

for page in (home_page, scan_page, logs_page, ask_ai_page):
    page.place(relwidth=1, relheight=1)

def pause_scan():
    global scan_paused
    scan_paused = True
    log_box2.after(0, lambda: (
        log_box2.insert(tk.END, "[||] Scan paused\n"),
        log_box2.see(tk.END)
    ))

def resume_scan():
    global scan_paused
    scan_paused = False
    log_box2.after(0, lambda: (
        log_box2.insert(tk.END, "[+] Scan resumed by user\n"),
        log_box2.see(tk.END)
    ))


def stop_scan():
    global stop_requested, scan_paused
    stop_requested = True
    scan_paused = False

    log_box2.after(0, lambda: (
        log_box2.insert(tk.END, "[!] Scan stopped by user\n"),
        log_box2.see(tk.END)
    ))

top_frame = tk.Frame(root, bg="#231f20")
top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

title = tk.Label(
    top_frame,
    text="Bee Protego",
    font=("Josefin Sans", 30, "bold"),
    fg="#FFF600",
    bg="#231f20"
)
title.pack(anchor="w", padx=20, pady=15)

line = tk.Frame(top_frame, bg="white", height=1)
line.pack(fill="x", padx=20)

sidebar_frame = tk.Frame(root, bg="#231f20", width=160)
sidebar_frame.grid(row=1, column=0, sticky="ns")
sidebar_frame.grid_propagate(False)




button_1 = tk.Button(sidebar_frame, text="Home",fg="#231f20",bg="#FFF600",font=("Josefin Sans",24), relief="flat",bd=0,highlightthickness=0)
button_1.pack(pady=50, fill="x",padx=50)

button_2 = tk.Button(sidebar_frame, text="Scan",fg="#231f20",bg="#FFF600",font=("Josefin Sans",24) ,relief="flat",
    bd=0,
    highlightthickness=0)
button_2.pack(pady=50, fill="x",padx=50)

button_3 = tk.Button(sidebar_frame, text="Logs",fg="#231f20",bg="#FFF600",font=("Josefin Sans",24) ,relief="flat",
    bd=0,
    highlightthickness=0)
button_3.pack(pady=50, fill="x",padx=50)

button_4 = tk.Button(sidebar_frame, text="Ask AI",fg="#231f20",bg="#FFF600",font=("Josefin Sans",24), relief="flat", bd=0,highlightthickness=0)
button_4.pack(pady=50, fill="x",padx=50)


scan_btn = tk.Button(
    home_page,
    text="SCAN",
    font=("Josefin Sans", 22, "bold"),
    bg="#FFF600",
    fg="black",
    height=2,
    width=14,
    relief="flat",
    command=lambda: (scan_file_with_rules(get_file_path(), rules),Scan_file())   
)
scan_btn.pack(pady=(20, 30))


def clear_output():
    log_box2.delete("1.0", "end")
    log_box.delete("1.0", "end")

clear_btn = tk.Button(
    home_page,
    text="Clear Output",
    command=clear_output,
    bg="yellow",
    fg="black",
    font=("Josefin Sans",4,"bold"),
    relief="flat",
    padx=10,
    pady=5,
    height=1,
    width=3
)
clear_btn.pack(anchor="e", padx=10, pady=5)


log_box = tk.Text(
   home_page,
    bg="black",
    fg="white",
    height=14,
    relief="flat"
)
log_box.pack(fill="both", expand=True)


right_frame = tk.Frame(root, bg="#1b1819", width=270)  
right_frame.grid(row=1, column=2, sticky="nsew")
right_frame.grid_propagate(False)

ai_container = tk.Frame(right_frame, bg="#231f20",width=500)
ai_container.pack(fill="both", expand=True, padx=5, pady=5)



Lbl_2 = tk.Label(
    ai_container,
    text="Buzzy AI",
    font=("Josefin Sans", 28, "bold"),
    fg="#FFF600",
    bg="#231f20"
)
Lbl_2.pack(anchor="w", pady=(8, 15))

prompt_lbl = tk.Label(
    ai_container,
    text="Ask anything",
    font=("Josefin Sans", 10),
    fg="#9e9e9e",
    bg="#231f20"
)
prompt_lbl.pack(anchor="w", pady=(0, 4))

input_box = tk.Text(
    ai_container,
    height=6,
    width=22, 
    bg="black",
    fg="white",
    insertbackground="white",
    font=("Consolas", 10),
    relief="flat",
    wrap="word"
)

input_box.pack(fill="x", padx=10)

ask_btn = tk.Button(
    ai_container,
    text="Ask",
    bg="#FFF600",
    fg="#000000",
    font=("Josefin Sans", 11, "bold"),
    relief="flat",
    cursor="hand2",
     command=ask_ollama_thread
)
ask_btn.pack(fill="x", padx=10, pady=10)



output_box = tk.Text(
    ai_container,
    height=22,
    width=22, 
    bg="black",
    fg="white",
    insertbackground="white",
    font=("Consolas", 10),
    relief="flat",
    wrap="word"
)

output_box.pack(fill="x", padx=10)


clear_btn = tk.Button(
    ai_container,
    text="✖",
    width=2,
    bg="#FFF600",
    fg="#000000",
    height=1,
    font=("Segoe UI", 9),
    command=lambda: output_box.delete("1.0", tk.END)
)
clear_btn.place(relx=0.96, rely=0.02, anchor="ne")

button_1.config(command=lambda: home_page.tkraise())
button_2.config(command=lambda: scan_page.tkraise())
button_3.config(command=lambda: (logs_page.tkraise()))
button_4.config(command=lambda: ask_ai_page.tkraise())

scan_btn_frame = center_frame = tk.Frame(scan_page, bg="#1f1c1d")
scan_btn_frame.pack()


Full_scan = tk.Button(
    scan_btn_frame,
    text="Full Scan",
    font=("Josefin Sans", 10),
    fg="black",
    bg="#FFF600",
    height=5,
    width=30,
    command=lambda: run_scan_thread(
        lambda: start_full_scan())
    )

Full_scan.pack(fill="x", padx=10, pady=10,side="left")

Quick_scan = tk.Button(
    scan_btn_frame,
    text="Quick Scan",
    font=("Josefin Sans", 10),
    fg="black",
    bg="#FFF600",
    height=5,
    width=30,
    command=lambda: run_scan_thread(
        lambda: (scan_file_with_rules(get_file_path(), rules), Scan_file())
    )
)
Quick_scan.pack(fill="x", padx=10, pady=10,side="left")

Target_scan = tk.Button(
    scan_btn_frame,
    text="Targetted Scan",
    font=("Josefin Sans", 10),
    fg="black",
    bg="#FFF600",
    height=5,
    width=30,
    command=lambda: run_scan_thread(
        lambda: (
            scan_file_with_rules(get_file_path(), rules),
            Scan_file(),
            run_all_yara_rules(yara_exe, yara_rules, get_file_path())
        )
    )
)
Target_scan.pack(fill="x", padx=10, pady=10,side="left")


file_frame = tk.Frame(scan_page, bg="#231f20")
file_frame.pack(fill="x", padx=10, pady=8)

dir_frame = tk.Frame(scan_page, bg="#231f20")
dir_frame.pack(fill="x", padx=10, pady=8)

file_entry = tk.Entry(file_frame, bg="#000000", fg="#FFF600", insertbackground="#FFF600", font=("Consolas", 12), relief="flat")
file_entry.pack(side="left", fill="x", expand=True, padx=(0,8))

dir_entry = tk.Entry(dir_frame, bg="#1a1a1a", fg="#FFF600", insertbackground="#FFF600", font=("Consolas", 12), relief="flat")
dir_entry.pack(side="left", fill="x", expand=True, padx=(0,8))



add_placeholder(file_entry, "Enter file path...")
add_placeholder(dir_entry, "Enter directory path...")

def on_enter(e):
    e.widget['background'] = '#444444'

def on_leave(e):
    e.widget['background'] = '#2a2a2a'

btn_style = {
    "bg": "#2a2a2a",
    "fg": "#FFF600",
    "font": ("Josefin Sans", 12, "bold"),
    "relief": "flat",
    "padx": 15,
    "pady": 6,
    "cursor": "hand2",
}

file_browse_btn = tk.Button(file_frame, text="Browse", command=browse_file, **btn_style)
file_browse_btn.pack(side="left")
file_browse_btn.bind("<Enter>", on_enter)
file_browse_btn.bind("<Leave>", on_leave)

selected_directory = tk.StringVar()

dir_browse_btn = tk.Button(dir_frame, text="Browse", command=browse_directory, **btn_style)
dir_browse_btn.pack(side="left")
dir_browse_btn.bind("<Enter>", on_enter)
dir_browse_btn.bind("<Leave>", on_leave)

button_frame = tk.Frame(scan_page, bg="#231f20")
button_frame.pack(fill="x", padx=10, pady=(5, 15))


btn_style = {
    "font": ("Josefin Sans", 8, "bold"),
    "relief": "flat",
    "padx": 10,
    "pady": 5,
    "height": 1,
    "width": 8,
    "bd": 0,
    "cursor": "hand2"
}

resume_btn = tk.Button(button_frame, text="Resume", bg="#4CAF50", fg="white", command=resume_scan, **btn_style)
pause_btn = tk.Button(button_frame, text="Pause", bg="#FF9800", fg="white", command=pause_scan, **btn_style)
stop_btn = tk.Button(button_frame, text="Stop", bg="#F44336", fg="white", command=stop_scan, **btn_style)
clear_btn = tk.Button(button_frame, text="Clear Output", bg="#FFC107", fg="black", command=clear_output, **btn_style)
export_btn = tk.Button(button_frame, text="Export PDF", bg="#2196F3", fg="white", command=export_logs_to_pdf, **btn_style)

resume_btn.pack(side="right", padx=5)
pause_btn.pack(side="right", padx=5)
stop_btn.pack(side="right", padx=5)
clear_btn.pack(side="right", padx=5)
export_btn.pack(side="right", padx=5)

log_box2 = tk.Text(
    scan_page,
    bg="black",
    fg="#00ff9c",         
    font=("Consolas", 13), 
    height=16,
    relief="flat"
)
log_box2.pack(fill="both", expand=True, padx=10, pady=(0,10))



scan_page.grid_rowconfigure(1, weight=1)
scan_page.grid_columnconfigure(0, weight=1)

model_label = tk.Label(
    home_page,
    text="Select Ollama Model:",
    font=("Josefin Sans", 12),
    fg="#FFF600",
    bg="#231f20"
)
model_label.pack(anchor="w", padx=10, pady=(10, 0))
model_combo = ttk.Combobox(
    home_page,
    values=models,
    state="readonly",
    font=("Josefin Sans", 12),
    width=15
)
model_combo.configure(state="normal")
model_combo.pack(anchor="w", padx=10, pady=(0, 10))
model_combo.set("gemma") 

Buzzy = tk.Label(ask_ai_page,text="Buzzy AI", font=("Josefin Sans", 28),  fg="#FFF600",bg="#231f20")
Buzzy.pack(fill="x", padx=10, pady=10)

buzzy_intro = tk.Label(
    ask_ai_page,
    text="Buzzy AI is an intelligent AI assistant built into Bee Protego.\n"
         "It helps protect your desktop from dangerous and freak viruses.\n"
         "It acts like your personal cybersecurity buddy - ready to analyze, explain, and guide.",
    font=("Josefin Sans", 16),
    fg="#ffffff",
    bg="#231f20",
    justify="left",
    wraplength=900
)
buzzy_intro.pack(anchor="w", padx=20, pady=10)

buzzy_features_title = tk.Label(
    ask_ai_page,
    text="With Buzzy AI, you can:",
    font=("Josefin Sans", 20, "bold"),
    fg="#FFF600",
    bg="#231f20"
)
buzzy_features_title.pack(anchor="w", padx=20, pady=(10, 5))

features = [
    "🦠 Detect & analyze viruses and suspicious files",
    "❓ Ask doubts related to malware, hacking, or system behavior",
    "📊 Get analysis reports in simple language",
    "📝 Review scan results and security status",
    "🔐 Receive tips to improve computer security"
]

for item in features:
    lbl = tk.Label(
        ask_ai_page,
        text="• " + item,
        font=("Josefin Sans", 15),
        fg="#ffffff",
        bg="#231f20",
        justify="left"
    )
    lbl.pack(anchor="w", padx=40, pady=2)

buzzy_purpose = tk.Label(
    ask_ai_page,
    text="The main purpose of Buzzy AI is to make cybersecurity easy — even for beginners.\n"
         "It explains complex threats clearly and helps you understand, fix, and secure your system confidently.",
    font=("Josefin Sans", 16),
    fg="#cccccc",
    bg="#231f20",
    justify="left",
    wraplength=900
)
buzzy_purpose.pack(anchor="w", padx=20, pady=15)

log_box2.tag_configure("green_text", foreground="#00ff9d")
log_box2.tag_configure("yellow_text", foreground="#fff600")
log_box2.tag_configure("red_text", foreground="#ff4d4d")

LOG_FOLDER = "pdf_logs"

def load_pdf_logs():
    
    tree.delete(*tree.get_children())

    if not os.path.exists(LOG_FOLDER):
        return

    files = [f for f in os.listdir(LOG_FOLDER) if f.endswith(".pdf")]

    files.sort(reverse=True)

    for i, file in enumerate(files, start=1):

        path = os.path.join(LOG_FOLDER, file)

        timestamp = os.path.getmtime(path)

        date = datetime.fromtimestamp(timestamp).strftime("%d/%m/%y %I:%M %p")

        tree.insert(
            "",
            "end",
            values=(i, file, date),
            tags=("row",)
        )
refresh_btn = tk.Button(
    logs_page,
    text="Refresh",
    command=load_pdf_logs,
    bg="green",
    fg="black",
    font=("Josefin Sans",4,"bold"),
    relief="flat",
    padx=10,
    pady=5,
    height=1,
    width=3
)
refresh_btn.pack(anchor="e", padx=10, pady=5)
columns = ("sno", "name", "date")

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#231f20",
    foreground="#FFF600",
    fieldbackground="#231f20",
    rowheight=55,
    font=("Josefin Sans", 14)
)
style.configure(
    "Treeview.Heading",
    background="#231f20",
    foreground="#FFF600",
    font=("Josefin Sans", 16, "bold")
)
tree = ttk.Treeview(logs_page, columns=columns, show="headings")

tree.heading("sno", text="S.No")
tree.heading("name", text="Report Name")
tree.heading("date", text="Date")

tree.column("sno", width=80, anchor="center")
tree.column("name", width=450)
tree.column("date", width=200)




tree.pack(fill="both", expand=True, padx=20, pady=20)

home_page.tkraise()

root.mainloop()
