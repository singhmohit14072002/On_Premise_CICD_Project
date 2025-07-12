#!/usr/bin/env python3
"""
DevOps Animation Launcher
Choose between Basic and Advanced versions of the DevOps Tools Animation Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class DevOpsAnimationLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("DevOps Animation Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🚀 DevOps Animation Launcher",
            font=('Arial', 24, 'bold'),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(0, 30))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Choose your preferred animation experience",
            font=('Arial', 12),
            fg='#888888',
            bg='#1e1e1e'
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Version selection frame
        selection_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=3)
        selection_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Basic version
        basic_frame = tk.Frame(selection_frame, bg='#2d2d2d')
        basic_frame.pack(fill=tk.X, padx=20, pady=20)
        
        basic_title = tk.Label(
            basic_frame,
            text="🎯 Basic Version",
            font=('Arial', 16, 'bold'),
            fg='#00aa44',
            bg='#2d2d2d'
        )
        basic_title.pack(anchor=tk.W)
        
        basic_desc = tk.Label(
            basic_frame,
            text="• Circular rotating DevOps tools\n• Animated connections and particles\n• Real-time status updates\n• Simple and elegant design",
            font=('Arial', 10),
            fg='#cccccc',
            bg='#2d2d2d',
            justify=tk.LEFT
        )
        basic_desc.pack(anchor=tk.W, pady=(5, 10))
        
        basic_btn = tk.Button(
            basic_frame,
            text="Launch Basic Version",
            command=self.launch_basic,
            bg='#00aa44',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            width=20
        )
        basic_btn.pack(anchor=tk.W)
        
        # Separator
        separator = tk.Frame(selection_frame, bg='#444444', height=2)
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Advanced version
        advanced_frame = tk.Frame(selection_frame, bg='#2d2d2d')
        advanced_frame.pack(fill=tk.X, padx=20, pady=20)
        
        advanced_title = tk.Label(
            advanced_frame,
            text="🌟 Advanced Version",
            font=('Arial', 16, 'bold'),
            fg='#ff8800',
            bg='#2d2d2d'
        )
        advanced_title.pack(anchor=tk.W)
        
        advanced_desc = tk.Label(
            advanced_frame,
            text="• Multiple animation modes (circular, matrix, network, spiral)\n• Enhanced particle system\n• Detailed metrics and descriptions\n• Advanced visual effects and 3D-like animations\n• FPS counter and performance monitoring",
            font=('Arial', 10),
            fg='#cccccc',
            bg='#2d2d2d',
            justify=tk.LEFT
        )
        advanced_desc.pack(anchor=tk.W, pady=(5, 10))
        
        advanced_btn = tk.Button(
            advanced_frame,
            text="Launch Advanced Version",
            command=self.launch_advanced,
            bg='#ff8800',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            width=20
        )
        advanced_btn.pack(anchor=tk.W)
        
        # Bottom info
        info_frame = tk.Frame(main_frame, bg='#1e1e1e')
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_label = tk.Label(
            info_frame,
            text="💡 Tip: Both versions use only Python built-in modules - no external dependencies required!",
            font=('Arial', 9),
            fg='#888888',
            bg='#1e1e1e'
        )
        info_label.pack()
        
        # Exit button
        exit_btn = tk.Button(
            main_frame,
            text="Exit Launcher",
            command=self.root.destroy,
            bg='#444444',
            fg='white',
            font=('Arial', 10),
            relief=tk.RAISED,
            bd=2
        )
        exit_btn.pack(pady=(20, 0))
    
    def launch_basic(self):
        """Launch the basic version of the DevOps animation app"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'devops_animation_app.py')
            if os.path.exists(script_path):
                subprocess.Popen([sys.executable, script_path])
                messagebox.showinfo("Success", "Basic version launched successfully!")
            else:
                messagebox.showerror("Error", "Basic version script not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch basic version: {str(e)}")
    
    def launch_advanced(self):
        """Launch the advanced version of the DevOps animation app"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'devops_animation_advanced.py')
            if os.path.exists(script_path):
                subprocess.Popen([sys.executable, script_path])
                messagebox.showinfo("Success", "Advanced version launched successfully!")
            else:
                messagebox.showerror("Error", "Advanced version script not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch advanced version: {str(e)}")

def main():
    root = tk.Tk()
    app = DevOpsAnimationLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 