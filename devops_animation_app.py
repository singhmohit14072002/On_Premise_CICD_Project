import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import threading
import random
from datetime import datetime
import json

class DevOpsAnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DevOps Tools Animation Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Animation variables
        self.animation_running = False
        self.animation_thread = None
        
        # DevOps tools data
        self.devops_tools = {
            'Docker': {'color': '#2496ED', 'icon': '🐳', 'status': 'running'},
            'Kubernetes': {'color': '#326CE5', 'icon': '☸️', 'status': 'running'},
            'Jenkins': {'color': '#D33833', 'icon': '🤖', 'status': 'building'},
            'Git': {'color': '#F05032', 'icon': '📚', 'status': 'committing'},
            'Ansible': {'color': '#EE0000', 'icon': '⚙️', 'status': 'configuring'},
            'Terraform': {'color': '#7B42BC', 'icon': '🏗️', 'status': 'deploying'},
            'Prometheus': {'color': '#E6522C', 'icon': '📊', 'status': 'monitoring'},
            'Grafana': {'color': '#F46800', 'icon': '📈', 'status': 'visualizing'}
        }
        
        self.setup_ui()
        self.start_animations()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🚀 DevOps Tools Animation Dashboard",
            font=('Arial', 24, 'bold'),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Animation controls
        self.start_btn = tk.Button(
            control_frame,
            text="▶️ Start Animations",
            command=self.start_animations,
            bg='#00aa44',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3
        )
        self.start_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹️ Stop Animations",
            command=self.stop_animations,
            bg='#aa4444',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Animation speed control
        speed_label = tk.Label(control_frame, text="Speed:", bg='#2d2d2d', fg='white', font=('Arial', 10))
        speed_label.pack(side=tk.LEFT, padx=(20, 5), pady=10)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(
            control_frame,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#2d2d2d',
            fg='white',
            highlightbackground='#2d2d2d',
            length=150
        )
        speed_scale.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Status display
        self.status_label = tk.Label(
            control_frame,
            text="Status: Animations Running",
            bg='#2d2d2d',
            fg='#00ff88',
            font=('Arial', 10, 'bold')
        )
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Animation canvas
        self.canvas = tk.Canvas(
            main_frame,
            bg='#0a0a0a',
            highlightthickness=0,
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Metrics panel
        metrics_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        metrics_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create metric displays
        self.metrics = {}
        tools_per_row = 4
        for i, (tool_name, tool_data) in enumerate(self.devops_tools.items()):
            row = i // tools_per_row
            col = i % tools_per_row
            
            metric_frame = tk.Frame(metrics_frame, bg='#2d2d2d')
            metric_frame.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            tool_label = tk.Label(
                metric_frame,
                text=f"{tool_data['icon']} {tool_name}",
                bg='#2d2d2d',
                fg=tool_data['color'],
                font=('Arial', 10, 'bold')
            )
            tool_label.pack()
            
            self.metrics[tool_name] = tk.Label(
                metric_frame,
                text="Status: Ready",
                bg='#2d2d2d',
                fg='#ffffff',
                font=('Arial', 8)
            )
            self.metrics[tool_name].pack()
        
        # Configure grid weights
        for i in range(tools_per_row):
            metrics_frame.columnconfigure(i, weight=1)
    
    def start_animations(self):
        if not self.animation_running:
            self.animation_running = True
            self.status_label.config(text="Status: Animations Running")
            self.animation_thread = threading.Thread(target=self.animation_loop, daemon=True)
            self.animation_thread.start()
    
    def stop_animations(self):
        self.animation_running = False
        self.status_label.config(text="Status: Animations Stopped")
    
    def animation_loop(self):
        angle = 0
        pulse_phase = 0
        wave_offset = 0
        
        while self.animation_running:
            try:
                # Clear canvas
                self.canvas.delete("all")
                
                # Draw animated background
                self.draw_animated_background(angle, pulse_phase, wave_offset)
                
                # Draw DevOps tools with animations
                self.draw_devops_tools(angle, pulse_phase)
                
                # Draw connection lines
                self.draw_connections(angle)
                
                # Draw metrics and status
                self.update_metrics()
                
                # Update animation parameters
                angle += 0.02 * self.speed_var.get()
                pulse_phase += 0.05 * self.speed_var.get()
                wave_offset += 0.03 * self.speed_var.get()
                
                time.sleep(0.05)
                
            except Exception as e:
                print(f"Animation error: {e}")
                break
    
    def draw_animated_background(self, angle, pulse_phase, wave_offset):
        # Draw animated grid
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Animated grid lines
        grid_spacing = 50
        for x in range(0, width, grid_spacing):
            alpha = abs(math.sin(angle + x * 0.01)) * 0.3
            color = f'#{int(100 + 50 * alpha):02x}{int(100 + 50 * alpha):02x}{int(100 + 50 * alpha):02x}'
            self.canvas.create_line(x, 0, x, height, fill=color, width=1)
        
        for y in range(0, height, grid_spacing):
            alpha = abs(math.cos(angle + y * 0.01)) * 0.3
            color = f'#{int(100 + 50 * alpha):02x}{int(100 + 50 * alpha):02x}{int(100 + 50 * alpha):02x}'
            self.canvas.create_line(0, y, width, y, fill=color, width=1)
        
        # Animated waves
        for i in range(5):
            wave_y = height // 2 + math.sin(wave_offset + i * 0.5) * 100
            wave_color = f'#{int(50 + i * 20):02x}{int(100 + i * 15):02x}{int(150 + i * 25):02x}'
            self.canvas.create_line(0, wave_y, width, wave_y, fill=wave_color, width=2)
    
    def draw_devops_tools(self, angle, pulse_phase):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Calculate positions in a circle
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3
        
        for i, (tool_name, tool_data) in enumerate(self.devops_tools.items()):
            # Calculate position
            tool_angle = angle + (i * 2 * math.pi / len(self.devops_tools))
            x = center_x + radius * math.cos(tool_angle)
            y = center_y + radius * math.sin(tool_angle)
            
            # Pulse effect
            pulse = 1 + 0.2 * math.sin(pulse_phase + i * 0.5)
            size = int(40 * pulse)
            
            # Draw tool circle
            color = tool_data['color']
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline='white', width=2
            )
            
            # Draw tool icon
            self.canvas.create_text(
                x, y,
                text=tool_data['icon'],
                font=('Arial', int(20 * pulse), 'bold'),
                fill='white'
            )
            
            # Draw tool name
            self.canvas.create_text(
                x, y + size + 15,
                text=tool_name,
                font=('Arial', 10, 'bold'),
                fill=color
            )
            
            # Draw status indicator
            status_colors = {
                'running': '#00ff00',
                'building': '#ffff00',
                'committing': '#00ffff',
                'configuring': '#ff00ff',
                'deploying': '#ff8800',
                'monitoring': '#8800ff',
                'visualizing': '#ff0088'
            }
            
            status_color = status_colors.get(tool_data['status'], '#ffffff')
            status_size = int(8 * pulse)
            self.canvas.create_oval(
                x + size - 10, y - size + 10,
                x + size - 10 + status_size, y - size + 10 + status_size,
                fill=status_color, outline='white', width=1
            )
    
    def draw_connections(self, angle):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3
        
        # Draw connection lines between tools
        for i in range(len(self.devops_tools)):
            angle1 = angle + (i * 2 * math.pi / len(self.devops_tools))
            angle2 = angle + ((i + 1) * 2 * math.pi / len(self.devops_tools))
            
            x1 = center_x + radius * math.cos(angle1)
            y1 = center_y + radius * math.sin(angle1)
            x2 = center_x + radius * math.cos(angle2)
            y2 = center_y + radius * math.sin(angle2)
            
            # Animated connection line
            alpha = abs(math.sin(angle + i * 0.5)) * 0.7 + 0.3
            color = f'#{int(100 * alpha):02x}{int(150 * alpha):02x}{int(255 * alpha):02x}'
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color, width=3, capstyle=tk.ROUND
            )
            
            # Draw data flow particles
            particle_pos = (angle + i * 0.5) % (2 * math.pi)
            if particle_pos < 0.3:
                particle_x = x1 + (x2 - x1) * particle_pos / 0.3
                particle_y = y1 + (y2 - y1) * particle_pos / 0.3
                self.canvas.create_oval(
                    particle_x - 3, particle_y - 3,
                    particle_x + 3, particle_y + 3,
                    fill='#ffff00', outline='white'
                )
    
    def update_metrics(self):
        # Update tool statuses with random changes
        statuses = ['running', 'building', 'committing', 'configuring', 'deploying', 'monitoring', 'visualizing']
        
        for tool_name in self.devops_tools:
            if random.random() < 0.01:  # 1% chance to change status
                self.devops_tools[tool_name]['status'] = random.choice(statuses)
            
            # Update metric display
            status = self.devops_tools[tool_name]['status']
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.metrics[tool_name].config(
                text=f"Status: {status}\nLast Update: {timestamp}",
                fg='#00ff88' if status == 'running' else '#ffff00'
            )

def main():
    root = tk.Tk()
    app = DevOpsAnimationApp(root)
    
    # Handle window close
    def on_closing():
        app.stop_animations()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 