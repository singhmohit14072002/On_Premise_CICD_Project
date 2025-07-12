import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import threading
import random
from datetime import datetime

class AdvancedDevOpsWheelGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced DevOps Tools Wheel Game")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Game variables
        self.is_spinning = False
        self.spin_thread = None
        self.current_angle = 0
        self.target_angle = 0
        self.spin_speed = 0
        self.selected_tool = None
        self.game_mode = "random"  # random, learning, challenge
        self.score = 0
        self.spins_count = 0
        
        # DevOps tools data with categories
        self.devops_tools = [
            # Containerization
            {'name': 'Docker', 'color': '#2496ED', 'icon': '🐳', 'description': 'Containerization Platform', 'category': 'Containerization'},
            {'name': 'Kubernetes', 'color': '#326CE5', 'icon': '☸️', 'description': 'Container Orchestration', 'category': 'Containerization'},
            {'name': 'Helm', 'color': '#0F1689', 'icon': '⚓', 'description': 'Kubernetes Package Manager', 'category': 'Containerization'},
            
            # CI/CD
            {'name': 'Jenkins', 'color': '#D33833', 'icon': '🤖', 'description': 'CI/CD Automation', 'category': 'CI/CD'},
            {'name': 'GitLab CI', 'color': '#FC6D26', 'icon': '🦊', 'description': 'GitLab CI/CD Pipeline', 'category': 'CI/CD'},
            {'name': 'GitHub Actions', 'color': '#2088FF', 'icon': '🐙', 'description': 'GitHub CI/CD Workflows', 'category': 'CI/CD'},
            
            # Version Control
            {'name': 'Git', 'color': '#F05032', 'icon': '📚', 'description': 'Version Control System', 'category': 'Version Control'},
            {'name': 'SVN', 'color': '#809CC9', 'icon': '📖', 'description': 'Subversion Version Control', 'category': 'Version Control'},
            
            # Configuration Management
            {'name': 'Ansible', 'color': '#EE0000', 'icon': '⚙️', 'description': 'Configuration Management', 'category': 'Configuration Management'},
            {'name': 'Chef', 'color': '#F09820', 'icon': '👨‍🍳', 'description': 'Infrastructure Automation', 'category': 'Configuration Management'},
            {'name': 'Puppet', 'color': '#FFAE1A', 'icon': '🎭', 'description': 'Configuration Management', 'category': 'Configuration Management'},
            
            # Infrastructure as Code
            {'name': 'Terraform', 'color': '#7B42BC', 'icon': '🏗️', 'description': 'Infrastructure as Code', 'category': 'Infrastructure as Code'},
            {'name': 'CloudFormation', 'color': '#FF9900', 'icon': '☁️', 'description': 'AWS Infrastructure as Code', 'category': 'Infrastructure as Code'},
            
            # Monitoring
            {'name': 'Prometheus', 'color': '#E6522C', 'icon': '📊', 'description': 'Monitoring & Alerting', 'category': 'Monitoring'},
            {'name': 'Grafana', 'color': '#F46800', 'icon': '📈', 'description': 'Data Visualization', 'category': 'Monitoring'},
            {'name': 'Nagios', 'color': '#1A472A', 'icon': '👁️', 'description': 'Network Monitoring', 'category': 'Monitoring'},
            
            # Service Mesh
            {'name': 'Istio', 'color': '#466BB0', 'icon': '🛡️', 'description': 'Service Mesh', 'category': 'Service Mesh'},
            {'name': 'Linkerd', 'color': '#2BED70', 'icon': '🔗', 'description': 'Lightweight Service Mesh', 'category': 'Service Mesh'},
            
            # GitOps
            {'name': 'ArgoCD', 'color': '#326CE5', 'icon': '🔄', 'description': 'GitOps Continuous Delivery', 'category': 'GitOps'},
            {'name': 'Flux', 'color': '#0B5D1E', 'icon': '🌊', 'description': 'GitOps Kubernetes Operator', 'category': 'GitOps'},
            
            # Security
            {'name': 'Vault', 'color': '#000000', 'icon': '🔐', 'description': 'Secrets Management', 'category': 'Security'},
            {'name': 'Falco', 'color': '#00D4AA', 'icon': '🦅', 'description': 'Cloud Native Security', 'category': 'Security'}
        ]
        
        # Categories for filtering
        self.categories = list(set(tool['category'] for tool in self.devops_tools))
        
        self.setup_ui()
        self.start_animation()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with score
        title_frame = tk.Frame(main_frame, bg='#0a0a0a')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🎯 Advanced DevOps Tools Wheel Game",
            font=('Arial', 28, 'bold'),
            fg='#00ff88',
            bg='#0a0a0a'
        )
        title_label.pack(side=tk.LEFT)
        
        # Score display
        self.score_label = tk.Label(
            title_frame,
            text="Score: 0 | Spins: 0",
            font=('Arial', 14, 'bold'),
            fg='#ffff00',
            bg='#0a0a0a'
        )
        self.score_label.pack(side=tk.RIGHT, pady=10)
        
        # Game controls
        control_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=3)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left controls
        left_controls = tk.Frame(control_frame, bg='#1a1a1a')
        left_controls.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Spin button
        self.spin_btn = tk.Button(
            left_controls,
            text="🎲 SPIN THE WHEEL",
            command=self.spin_wheel,
            bg='#ff6b35',
            fg='white',
            font=('Arial', 16, 'bold'),
            relief=tk.RAISED,
            bd=3,
            width=18
        )
        self.spin_btn.pack(side=tk.LEFT, padx=5)
        
        # Game mode selector
        mode_label = tk.Label(left_controls, text="Mode:", bg='#1a1a1a', fg='white', font=('Arial', 10))
        mode_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.mode_var = tk.StringVar(value="random")
        mode_combo = ttk.Combobox(
            left_controls,
            textvariable=self.mode_var,
            values=["random", "learning", "challenge"],
            state="readonly",
            width=12
        )
        mode_combo.pack(side=tk.LEFT, padx=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
        
        # Center controls
        center_controls = tk.Frame(control_frame, bg='#1a1a1a')
        center_controls.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Category filter
        category_label = tk.Label(center_controls, text="Category:", bg='#1a1a1a', fg='white', font=('Arial', 10))
        category_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(
            center_controls,
            textvariable=self.category_var,
            values=["All"] + self.categories,
            state="readonly",
            width=15
        )
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.bind('<<ComboboxSelected>>', self.on_category_change)
        
        # Spin speed control
        speed_label = tk.Label(center_controls, text="Speed:", bg='#1a1a1a', fg='white', font=('Arial', 10))
        speed_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(
            center_controls,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#1a1a1a',
            fg='white',
            highlightbackground='#1a1a1a',
            length=150
        )
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Right controls
        right_controls = tk.Frame(control_frame, bg='#1a1a1a')
        right_controls.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Reset button
        reset_btn = tk.Button(
            right_controls,
            text="🔄 Reset Score",
            command=self.reset_score,
            bg='#444444',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.RAISED,
            bd=2
        )
        reset_btn.pack(side=tk.RIGHT, padx=5)
        
        # Status display
        self.status_label = tk.Label(
            right_controls,
            text="Ready to spin!",
            bg='#1a1a1a',
            fg='#00ff88',
            font=('Arial', 12, 'bold')
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)
        
        # Game canvas
        self.canvas = tk.Canvas(
            main_frame,
            bg='#000000',
            highlightthickness=0,
            relief=tk.SUNKEN,
            bd=3
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Result display
        result_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        result_frame.pack(fill=tk.X)
        
        # Selected tool display
        self.selected_tool_label = tk.Label(
            result_frame,
            text="🎯 Selected Tool: None",
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Arial', 18, 'bold')
        )
        self.selected_tool_label.pack(pady=10)
        
        # Tool description and category
        self.tool_desc_label = tk.Label(
            result_frame,
            text="Spin the wheel to select a DevOps tool!",
            bg='#1a1a1a',
            fg='#888888',
            font=('Arial', 12)
        )
        self.tool_desc_label.pack(pady=(0, 5))
        
        self.tool_category_label = tk.Label(
            result_frame,
            text="",
            bg='#1a1a1a',
            fg='#cccccc',
            font=('Arial', 10)
        )
        self.tool_category_label.pack(pady=(0, 10))
        
        # History frame
        history_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        history_frame.pack(fill=tk.X, pady=(10, 0))
        
        history_label = tk.Label(
            history_frame,
            text="📋 Spin History:",
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Arial', 12, 'bold')
        )
        history_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # History text widget with scrollbar
        history_text_frame = tk.Frame(history_frame, bg='#1a1a1a')
        history_text_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.history_text = tk.Text(
            history_text_frame,
            height=5,
            bg='#0a0a0a',
            fg='#ffffff',
            font=('Arial', 10),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.history_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Scrollbar for history
        history_scrollbar = tk.Scrollbar(history_text_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=history_scrollbar.set)
    
    def on_mode_change(self, event=None):
        """Handle game mode changes"""
        self.game_mode = self.mode_var.get()
        if self.game_mode == "learning":
            messagebox.showinfo("Learning Mode", "Learning Mode: Each spin will focus on a specific category to help you learn DevOps tools systematically!")
        elif self.game_mode == "challenge":
            messagebox.showinfo("Challenge Mode", "Challenge Mode: Try to get tools from different categories. Score points for variety!")
    
    def on_category_change(self, event=None):
        """Handle category filter changes"""
        # This will be used to filter tools in the wheel
        pass
    
    def reset_score(self):
        """Reset the game score"""
        self.score = 0
        self.spins_count = 0
        self.update_score_display()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        messagebox.showinfo("Score Reset", "Score and history have been reset!")
    
    def update_score_display(self):
        """Update the score display"""
        self.score_label.config(text=f"Score: {self.score} | Spins: {self.spins_count}")
    
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
        """Animate the wheel spinning with enhanced effects"""
        initial_speed = 25 * self.speed_var.get()
        current_speed = initial_speed
        deceleration = 0.985
        
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
                
                time.sleep(0.04)
                
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
        self.spins_count += 1
        self.update_score_display()
    
    def select_tool(self):
        """Select the tool that the pointer is pointing to"""
        # Get filtered tools based on category
        filtered_tools = self.get_filtered_tools()
        
        # Calculate which tool is selected based on current angle
        tools_count = len(filtered_tools)
        angle_per_tool = 360 / tools_count
        
        # Adjust angle so 0 degrees points to the top
        adjusted_angle = (360 - self.current_angle + 90) % 360
        
        # Find the selected tool
        tool_index = int(adjusted_angle / angle_per_tool) % tools_count
        self.selected_tool = filtered_tools[tool_index]
        
        # Update score based on game mode
        self.update_score()
        
        # Update UI
        self.root.after(0, self.update_selection_display)
    
    def get_filtered_tools(self):
        """Get tools filtered by selected category"""
        selected_category = self.category_var.get()
        if selected_category == "All":
            return self.devops_tools
        else:
            return [tool for tool in self.devops_tools if tool['category'] == selected_category]
    
    def update_score(self):
        """Update score based on game mode and selected tool"""
        if self.game_mode == "challenge":
            # In challenge mode, score points for variety
            recent_tools = self.get_recent_tools(5)
            categories_seen = set(tool['category'] for tool in recent_tools)
            
            if self.selected_tool['category'] not in categories_seen:
                self.score += 10
                messagebox.showinfo("Bonus!", f"New category! +10 points for {self.selected_tool['category']}")
            else:
                self.score += 1
        else:
            # In other modes, just add 1 point per spin
            self.score += 1
    
    def get_recent_tools(self, count):
        """Get recent tools from history"""
        # This is a simplified version - in a real implementation, you'd track recent selections
        return []
    
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
            self.tool_category_label.config(
                text=f"Category: {self.selected_tool['category']}",
                fg='#888888'
            )
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {self.selected_tool['icon']} {self.selected_tool['name']} ({self.selected_tool['category']})\n"
            
            self.history_text.config(state=tk.NORMAL)
            self.history_text.insert(tk.END, history_entry)
            self.history_text.see(tk.END)
            self.history_text.config(state=tk.DISABLED)
    
    def start_animation(self):
        """Start the continuous animation loop"""
        self.animation_loop()
    
    def animation_loop(self):
        """Main animation loop with enhanced effects"""
        try:
            # Clear canvas
            self.canvas.delete("all")
            
            # Draw enhanced background
            self.draw_background()
            
            # Draw wheel
            self.draw_wheel()
            
            # Draw pointer
            self.draw_pointer()
            
            # Draw effects
            if self.is_spinning:
                self.draw_spin_effects()
            
            # Schedule next frame
            self.root.after(40, self.animation_loop)
            
        except Exception as e:
            print(f"Animation error: {e}")
    
    def draw_background(self):
        """Draw enhanced background with effects"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Draw gradient-like background
        for i in range(0, height, 20):
            alpha = i / height
            color = f'#{int(10 + 20 * alpha):02x}{int(10 + 20 * alpha):02x}{int(10 + 20 * alpha):02x}'
            self.canvas.create_line(0, i, width, i, fill=color, width=20)
    
    def draw_wheel(self):
        """Draw the wheel with DevOps tools"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        wheel_radius = min(width, height) // 3
        
        # Draw wheel background with glow effect
        for i in range(3):
            glow_radius = wheel_radius + i * 5
            glow_color = f'#{int(40 + i * 10):02x}{int(40 + i * 10):02x}{int(40 + i * 10):02x}'
            self.canvas.create_oval(
                center_x - glow_radius, center_y - glow_radius,
                center_x + glow_radius, center_y + glow_radius,
                fill='', outline=glow_color, width=2
            )
        
        # Draw main wheel
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
        
        # Get filtered tools
        filtered_tools = self.get_filtered_tools()
        tools_count = len(filtered_tools)
        angle_per_tool = 360 / tools_count
        
        # Draw tool segments
        for i, tool in enumerate(filtered_tools):
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
            
            # Draw segment with enhanced styling
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
            
            # Draw icon with shadow
            self.canvas.create_text(
                icon_x + 2, icon_y + 2,
                text=tool['icon'],
                font=('Arial', 20, 'bold'),
                fill='#000000'
            )
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
        """Draw the spinning pointer with enhanced effects"""
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
        
        # Draw pointer shadow
        shadow_offset = 3
        self.canvas.create_polygon(
            pointer_x + shadow_offset, pointer_y + shadow_offset,
            pointer_x + shadow_offset + 15, pointer_y + shadow_offset,
            pointer_x + shadow_offset + 7.5, pointer_y + shadow_offset - 15,
            fill='#000000', outline='#000000', width=2
        )
        
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
        
        # Draw center dot with glow
        self.canvas.create_oval(
            center_x - 8, center_y - 8,
            center_x + 8, center_y + 8,
            fill='#ffffff',
            outline='#000000',
            width=2
        )
        self.canvas.create_oval(
            center_x - 5, center_y - 5,
            center_x + 5, center_y + 5,
            fill='#ff0000',
            outline='#ffffff',
            width=1
        )
    
    def draw_spin_effects(self):
        """Draw additional effects while spinning"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        wheel_radius = min(width, height) // 3
        
        # Draw spinning particles
        for i in range(5):
            particle_angle = math.radians(self.current_angle + i * 72)
            particle_radius = wheel_radius + 30 + random.randint(0, 20)
            
            particle_x = center_x + particle_radius * math.cos(particle_angle)
            particle_y = center_y - particle_radius * math.sin(particle_angle)
            
            self.canvas.create_oval(
                particle_x - 2, particle_y - 2,
                particle_x + 2, particle_y + 2,
                fill='#ffff00', outline='#ffffff'
            )

def main():
    root = tk.Tk()
    app = AdvancedDevOpsWheelGame(root)
    
    # Handle window close
    def on_closing():
        app.is_spinning = False
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 