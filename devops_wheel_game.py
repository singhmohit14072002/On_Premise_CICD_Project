import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import threading
import random
from datetime import datetime

class DevOpsWheelGame:
    def __init__(self, root):
        self.root = root
        self.root.title("DevOps Tools Wheel Game")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        
        # Game variables
        self.is_spinning = False
        self.spin_thread = None
        self.current_angle = 0
        self.target_angle = 0
        self.spin_speed = 0
        self.selected_tool = None
        
        # DevOps tools data
        self.devops_tools = [
            {'name': 'Docker', 'color': '#2496ED', 'icon': '🐳', 'description': 'Containerization Platform'},
            {'name': 'Kubernetes', 'color': '#326CE5', 'icon': '☸️', 'description': 'Container Orchestration'},
            {'name': 'Jenkins', 'color': '#D33833', 'icon': '🤖', 'description': 'CI/CD Automation'},
            {'name': 'Git', 'color': '#F05032', 'icon': '📚', 'description': 'Version Control System'},
            {'name': 'Ansible', 'color': '#EE0000', 'icon': '⚙️', 'description': 'Configuration Management'},
            {'name': 'Terraform', 'color': '#7B42BC', 'icon': '🏗️', 'description': 'Infrastructure as Code'},
            {'name': 'Prometheus', 'color': '#E6522C', 'icon': '📊', 'description': 'Monitoring & Alerting'},
            {'name': 'Grafana', 'color': '#F46800', 'icon': '📈', 'description': 'Data Visualization'},
            {'name': 'Helm', 'color': '#0F1689', 'icon': '⚓', 'description': 'Kubernetes Package Manager'},
            {'name': 'Istio', 'color': '#466BB0', 'icon': '🛡️', 'description': 'Service Mesh'},
            {'name': 'ArgoCD', 'color': '#326CE5', 'icon': '🔄', 'description': 'GitOps Continuous Delivery'},
            {'name': 'Vault', 'color': '#000000', 'icon': '🔐', 'description': 'Secrets Management'}
        ]
        
        self.setup_ui()
        self.start_animation()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎯 DevOps Tools Wheel Game",
            font=('Arial', 24, 'bold'),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(0, 20))
        
        # Game controls
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Spin button
        self.spin_btn = tk.Button(
            control_frame,
            text="🎲 SPIN THE WHEEL",
            command=self.spin_wheel,
            bg='#ff6b35',
            fg='white',
            font=('Arial', 14, 'bold'),
            relief=tk.RAISED,
            bd=3,
            width=20
        )
        self.spin_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Auto spin toggle
        self.auto_spin_var = tk.BooleanVar()
        self.auto_spin_check = tk.Checkbutton(
            control_frame,
            text="Auto Spin",
            variable=self.auto_spin_var,
            bg='#2d2d2d',
            fg='white',
            font=('Arial', 12),
            selectcolor='#1e1e1e'
        )
        self.auto_spin_check.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Spin speed control
        speed_label = tk.Label(control_frame, text="Spin Speed:", bg='#2d2d2d', fg='white', font=('Arial', 10))
        speed_label.pack(side=tk.LEFT, padx=(20, 5), pady=15)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(
            control_frame,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#2d2d2d',
            fg='white',
            highlightbackground='#2d2d2d',
            length=150
        )
        speed_scale.pack(side=tk.LEFT, padx=5, pady=15)
        
        # Status display
        self.status_label = tk.Label(
            control_frame,
            text="Ready to spin!",
            bg='#2d2d2d',
            fg='#00ff88',
            font=('Arial', 12, 'bold')
        )
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Game canvas
        self.canvas = tk.Canvas(
            main_frame,
            bg='#0a0a0a',
            highlightthickness=0,
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Result display
        result_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        result_frame.pack(fill=tk.X)
        
        # Selected tool display
        self.selected_tool_label = tk.Label(
            result_frame,
            text="🎯 Selected Tool: None",
            bg='#2d2d2d',
            fg='#ffffff',
            font=('Arial', 16, 'bold')
        )
        self.selected_tool_label.pack(pady=10)
        
        # Tool description
        self.tool_desc_label = tk.Label(
            result_frame,
            text="Spin the wheel to select a DevOps tool!",
            bg='#2d2d2d',
            fg='#888888',
            font=('Arial', 12)
        )
        self.tool_desc_label.pack(pady=(0, 10))
        
        # History frame
        history_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        history_frame.pack(fill=tk.X, pady=(10, 0))
        
        history_label = tk.Label(
            history_frame,
            text="📋 Spin History:",
            bg='#2d2d2d',
            fg='#ffffff',
            font=('Arial', 12, 'bold')
        )
        history_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # History text widget
        self.history_text = tk.Text(
            history_frame,
            height=4,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Arial', 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def spin_wheel(self):
        """Start spinning the wheel"""
        if not self.is_spinning:
            self.is_spinning = True
            self.spin_btn.config(state=tk.DISABLED, text="🎲 SPINNING...")
            self.status_label.config(text="Spinning...", fg='#ffff00')
            
            # Random target angle
            self.target_angle = random.uniform(0, 360)
            
            # Start spin thread
            self.spin_thread = threading.Thread(target=self.spin_animation, daemon=True)
            self.spin_thread.start()
    
    def spin_animation(self):
        """Animate the wheel spinning"""
        initial_speed = 20 * self.speed_var.get()
        current_speed = initial_speed
        deceleration = 0.98
        
        while self.is_spinning and current_speed > 0.1:
            try:
                # Update angle
                self.current_angle += current_speed
                if self.current_angle >= 360:
                    self.current_angle -= 360
                
                # Decelerate
                current_speed *= deceleration
                
                # Check if we should stop
                if current_speed < 0.5:
                    self.is_spinning = False
                    self.select_tool()
                
                time.sleep(0.05)
                
            except Exception as e:
                print(f"Spin animation error: {e}")
                break
        
        # Ensure we're stopped
        self.is_spinning = False
        self.root.after(0, self.finish_spin)
    
    def finish_spin(self):
        """Finish the spin and update UI"""
        self.spin_btn.config(state=tk.NORMAL, text="🎲 SPIN THE WHEEL")
        self.status_label.config(text="Spin complete!", fg='#00ff88')
    
    def select_tool(self):
        """Select the tool that the pointer is pointing to"""
        # Calculate which tool is selected based on current angle
        tools_count = len(self.devops_tools)
        angle_per_tool = 360 / tools_count
        
        # Adjust angle so 0 degrees points to the top
        adjusted_angle = (360 - self.current_angle + 90) % 360
        
        # Find the selected tool
        tool_index = int(adjusted_angle / angle_per_tool) % tools_count
        self.selected_tool = self.devops_tools[tool_index]
        
        # Update UI
        self.root.after(0, self.update_selection_display)
    
    def update_selection_display(self):
        """Update the selection display"""
        if self.selected_tool:
            self.selected_tool_label.config(
                text=f"🎯 Selected Tool: {self.selected_tool['icon']} {self.selected_tool['name']}",
                fg=self.selected_tool['color']
            )
            self.tool_desc_label.config(
                text=f"Description: {self.selected_tool['description']}",
                fg='#cccccc'
            )
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {self.selected_tool['icon']} {self.selected_tool['name']}\n"
            
            self.history_text.config(state=tk.NORMAL)
            self.history_text.insert(tk.END, history_entry)
            self.history_text.see(tk.END)
            self.history_text.config(state=tk.DISABLED)
    
    def start_animation(self):
        """Start the continuous animation loop"""
        self.animation_loop()
    
    def animation_loop(self):
        """Main animation loop"""
        try:
            # Clear canvas
            self.canvas.delete("all")
            
            # Draw wheel
            self.draw_wheel()
            
            # Draw pointer
            self.draw_pointer()
            
            # Schedule next frame
            self.root.after(50, self.animation_loop)
            
        except Exception as e:
            print(f"Animation error: {e}")
    
    def draw_wheel(self):
        """Draw the wheel with DevOps tools"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        wheel_radius = min(width, height) // 3
        
        # Draw wheel background
        self.canvas.create_oval(
            center_x - wheel_radius, center_y - wheel_radius,
            center_x + wheel_radius, center_y + wheel_radius,
            fill='#2a2a2a', outline='#444444', width=3
        )
        
        # Draw inner circle
        inner_radius = wheel_radius - 20
        self.canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            fill='#1a1a1a', outline='#333333', width=2
        )
        
        # Draw tool segments
        tools_count = len(self.devops_tools)
        angle_per_tool = 360 / tools_count
        
        for i, tool in enumerate(self.devops_tools):
            start_angle = i * angle_per_tool
            end_angle = (i + 1) * angle_per_tool
            
            # Convert angles to radians
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)
            
            # Calculate segment points
            points = [center_x, center_y]  # Center point
            
            # Add points along the arc
            for angle in range(int(start_angle), int(end_angle) + 1, 5):
                rad = math.radians(angle)
                x = center_x + wheel_radius * math.cos(rad)
                y = center_y - wheel_radius * math.sin(rad)
                points.extend([x, y])
            
            # Draw segment
            self.canvas.create_polygon(
                points,
                fill=tool['color'],
                outline='#ffffff',
                width=2
            )
            
            # Draw tool icon and name
            mid_angle = (start_angle + end_angle) / 2
            mid_rad = math.radians(mid_angle)
            icon_radius = wheel_radius - 60
            
            icon_x = center_x + icon_radius * math.cos(mid_rad)
            icon_y = center_y - icon_radius * math.sin(mid_rad)
            
            # Draw icon
            self.canvas.create_text(
                icon_x, icon_y,
                text=tool['icon'],
                font=('Arial', 20, 'bold'),
                fill='white'
            )
            
            # Draw tool name
            name_radius = wheel_radius - 30
            name_x = center_x + name_radius * math.cos(mid_rad)
            name_y = center_y - name_radius * math.sin(mid_rad)
            
            self.canvas.create_text(
                name_x, name_y,
                text=tool['name'],
                font=('Arial', 10, 'bold'),
                fill='white'
            )
    
    def draw_pointer(self):
        """Draw the spinning pointer"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        wheel_radius = min(width, height) // 3
        
        # Calculate pointer position
        pointer_angle = math.radians(self.current_angle)
        pointer_x = center_x + (wheel_radius + 20) * math.cos(pointer_angle)
        pointer_y = center_y - (wheel_radius + 20) * math.sin(pointer_angle)
        
        # Draw pointer triangle
        triangle_size = 15
        angle_offset = math.radians(30)
        
        # Calculate triangle points
        p1_x = pointer_x + triangle_size * math.cos(pointer_angle)
        p1_y = pointer_y - triangle_size * math.sin(pointer_angle)
        
        p2_x = pointer_x + triangle_size * math.cos(pointer_angle + angle_offset)
        p2_y = pointer_y - triangle_size * math.sin(pointer_angle + angle_offset)
        
        p3_x = pointer_x + triangle_size * math.cos(pointer_angle - angle_offset)
        p3_y = pointer_y - triangle_size * math.sin(pointer_angle - angle_offset)
        
        # Draw pointer
        self.canvas.create_polygon(
            p1_x, p1_y, p2_x, p2_y, p3_x, p3_y,
            fill='#ff0000',
            outline='#ffffff',
            width=2
        )
        
        # Draw center dot
        self.canvas.create_oval(
            center_x - 5, center_y - 5,
            center_x + 5, center_y + 5,
            fill='#ffffff',
            outline='#000000',
            width=2
        )

def main():
    root = tk.Tk()
    app = DevOpsWheelGame(root)
    
    # Handle window close
    def on_closing():
        app.is_spinning = False
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 