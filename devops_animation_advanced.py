import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import math
import time
import threading
import random
from datetime import datetime
import json
import os

class AdvancedDevOpsAnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced DevOps Tools Animation Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Animation variables
        self.animation_running = False
        self.animation_thread = None
        self.animation_mode = "circular"  # circular, matrix, network
        self.particle_system = []
        
        # DevOps tools data with enhanced information
        self.devops_tools = {
            'Docker': {
                'color': '#2496ED', 'icon': '🐳', 'status': 'running',
                'description': 'Containerization Platform',
                'metrics': {'containers': 0, 'images': 0, 'networks': 0}
            },
            'Kubernetes': {
                'color': '#326CE5', 'icon': '☸️', 'status': 'running',
                'description': 'Container Orchestration',
                'metrics': {'pods': 0, 'services': 0, 'nodes': 0}
            },
            'Jenkins': {
                'color': '#D33833', 'icon': '🤖', 'status': 'building',
                'description': 'CI/CD Automation',
                'metrics': {'jobs': 0, 'builds': 0, 'failures': 0}
            },
            'Git': {
                'color': '#F05032', 'icon': '📚', 'status': 'committing',
                'description': 'Version Control System',
                'metrics': {'commits': 0, 'branches': 0, 'merges': 0}
            },
            'Ansible': {
                'color': '#EE0000', 'icon': '⚙️', 'status': 'configuring',
                'description': 'Configuration Management',
                'metrics': {'playbooks': 0, 'tasks': 0, 'hosts': 0}
            },
            'Terraform': {
                'color': '#7B42BC', 'icon': '🏗️', 'status': 'deploying',
                'description': 'Infrastructure as Code',
                'metrics': {'resources': 0, 'states': 0, 'modules': 0}
            },
            'Prometheus': {
                'color': '#E6522C', 'icon': '📊', 'status': 'monitoring',
                'description': 'Monitoring & Alerting',
                'metrics': {'targets': 0, 'alerts': 0, 'queries': 0}
            },
            'Grafana': {
                'color': '#F46800', 'icon': '📈', 'status': 'visualizing',
                'description': 'Data Visualization',
                'metrics': {'dashboards': 0, 'panels': 0, 'users': 0}
            }
        }
        
        # Initialize particle system
        self.init_particle_system()
        
        self.setup_ui()
        self.start_animations()
    
    def init_particle_system(self):
        """Initialize particle system for enhanced visual effects"""
        self.particle_system = []
        for _ in range(50):
            self.particle_system.append({
                'x': random.randint(0, 1400),
                'y': random.randint(0, 900),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': random.uniform(0, 1),
                'color': random.choice(['#00ff88', '#ff0088', '#0088ff', '#ffff00'])
            })
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with enhanced styling
        title_frame = tk.Frame(main_frame, bg='#0a0a0a')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🚀 Advanced DevOps Tools Animation Dashboard",
            font=('Arial', 28, 'bold'),
            fg='#00ff88',
            bg='#0a0a0a'
        )
        title_label.pack(side=tk.LEFT)
        
        # Version and info
        info_label = tk.Label(
            title_frame,
            text="v2.0 - Enhanced Edition",
            font=('Arial', 12),
            fg='#888888',
            bg='#0a0a0a'
        )
        info_label.pack(side=tk.RIGHT, pady=10)
        
        # Enhanced control panel
        control_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=3)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side controls
        left_controls = tk.Frame(control_frame, bg='#1a1a1a')
        left_controls.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Animation controls
        self.start_btn = tk.Button(
            left_controls,
            text="▶️ Start Animations",
            command=self.start_animations,
            bg='#00aa44',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            left_controls,
            text="⏹️ Stop Animations",
            command=self.stop_animations,
            bg='#aa4444',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Animation mode selector
        mode_label = tk.Label(left_controls, text="Mode:", bg='#1a1a1a', fg='white', font=('Arial', 10))
        mode_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.mode_var = tk.StringVar(value="circular")
        mode_combo = ttk.Combobox(
            left_controls,
            textvariable=self.mode_var,
            values=["circular", "matrix", "network", "spiral"],
            state="readonly",
            width=10
        )
        mode_combo.pack(side=tk.LEFT, padx=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
        
        # Center controls
        center_controls = tk.Frame(control_frame, bg='#1a1a1a')
        center_controls.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Animation speed control
        speed_label = tk.Label(center_controls, text="Speed:", bg='#1a1a1a', fg='white', font=('Arial', 10))
        speed_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(
            center_controls,
            from_=0.1,
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
        
        # Particle density control
        particle_label = tk.Label(center_controls, text="Particles:", bg='#1a1a1a', fg='white', font=('Arial', 10))
        particle_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.particle_var = tk.IntVar(value=50)
        particle_scale = tk.Scale(
            center_controls,
            from_=10,
            to=100,
            resolution=10,
            orient=tk.HORIZONTAL,
            variable=self.particle_var,
            bg='#1a1a1a',
            fg='white',
            highlightbackground='#1a1a1a',
            length=100
        )
        particle_scale.pack(side=tk.LEFT, padx=5)
        
        # Right side status
        right_controls = tk.Frame(control_frame, bg='#1a1a1a')
        right_controls.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Status display
        self.status_label = tk.Label(
            right_controls,
            text="Status: Animations Running",
            bg='#1a1a1a',
            fg='#00ff88',
            font=('Arial', 10, 'bold')
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # FPS counter
        self.fps_label = tk.Label(
            right_controls,
            text="FPS: 0",
            bg='#1a1a1a',
            fg='#888888',
            font=('Arial', 9)
        )
        self.fps_label.pack(side=tk.RIGHT, padx=(0, 20))
        
        # Animation canvas with enhanced styling
        self.canvas = tk.Canvas(
            main_frame,
            bg='#000000',
            highlightthickness=0,
            relief=tk.SUNKEN,
            bd=3
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced metrics panel
        metrics_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        metrics_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create enhanced metric displays
        self.metrics = {}
        tools_per_row = 4
        for i, (tool_name, tool_data) in enumerate(self.devops_tools.items()):
            row = i // tools_per_row
            col = i % tools_per_row
            
            metric_frame = tk.Frame(metrics_frame, bg='#1a1a1a', relief=tk.SUNKEN, bd=1)
            metric_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            # Tool header
            header_frame = tk.Frame(metric_frame, bg='#2a2a2a')
            header_frame.pack(fill=tk.X, padx=5, pady=2)
            
            tool_label = tk.Label(
                header_frame,
                text=f"{tool_data['icon']} {tool_name}",
                bg='#2a2a2a',
                fg=tool_data['color'],
                font=('Arial', 11, 'bold')
            )
            tool_label.pack(side=tk.LEFT)
            
            # Status indicator
            self.metrics[f"{tool_name}_status"] = tk.Label(
                header_frame,
                text="●",
                bg='#2a2a2a',
                fg='#00ff00',
                font=('Arial', 12)
            )
            self.metrics[f"{tool_name}_status"].pack(side=tk.RIGHT, padx=5)
            
            # Description
            desc_label = tk.Label(
                metric_frame,
                text=tool_data['description'],
                bg='#1a1a1a',
                fg='#888888',
                font=('Arial', 8)
            )
            desc_label.pack()
            
            # Metrics display
            self.metrics[tool_name] = tk.Label(
                metric_frame,
                text="Loading metrics...",
                bg='#1a1a1a',
                fg='#ffffff',
                font=('Arial', 8)
            )
            self.metrics[tool_name].pack()
        
        # Configure grid weights
        for i in range(tools_per_row):
            metrics_frame.columnconfigure(i, weight=1)
    
    def on_mode_change(self, event=None):
        """Handle animation mode changes"""
        self.animation_mode = self.mode_var.get()
        # Reset animation parameters for new mode
        self.init_particle_system()
    
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
        frame_count = 0
        start_time = time.time()
        
        while self.animation_running:
            try:
                frame_start = time.time()
                
                # Clear canvas
                self.canvas.delete("all")
                
                # Draw animated background based on mode
                if self.animation_mode == "circular":
                    self.draw_circular_background(angle, pulse_phase, wave_offset)
                elif self.animation_mode == "matrix":
                    self.draw_matrix_background(angle, pulse_phase)
                elif self.animation_mode == "network":
                    self.draw_network_background(angle, pulse_phase)
                elif self.animation_mode == "spiral":
                    self.draw_spiral_background(angle, pulse_phase)
                
                # Draw DevOps tools with animations
                self.draw_devops_tools(angle, pulse_phase)
                
                # Draw connection lines
                self.draw_connections(angle)
                
                # Draw particle system
                self.update_particle_system()
                self.draw_particles()
                
                # Draw metrics and status
                self.update_metrics()
                
                # Update animation parameters
                angle += 0.02 * self.speed_var.get()
                pulse_phase += 0.05 * self.speed_var.get()
                wave_offset += 0.03 * self.speed_var.get()
                
                # Calculate FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed
                    self.fps_label.config(text=f"FPS: {fps:.1f}")
                
                # Frame rate control
                frame_time = time.time() - frame_start
                sleep_time = max(0.01, 0.05 - frame_time)
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"Animation error: {e}")
                break
    
    def draw_circular_background(self, angle, pulse_phase, wave_offset):
        """Draw circular pattern background"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Concentric circles
        center_x, center_y = width // 2, height // 2
        max_radius = min(width, height) // 2
        
        for i in range(5):
            radius = max_radius * (i + 1) / 5
            alpha = abs(math.sin(angle + i * 0.5)) * 0.3
            color = f'#{int(50 + 30 * alpha):02x}{int(100 + 50 * alpha):02x}{int(150 + 50 * alpha):02x}'
            
            self.canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color, width=2
            )
    
    def draw_matrix_background(self, angle, pulse_phase):
        """Draw matrix-style background"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Matrix grid
        grid_size = 40
        for x in range(0, width, grid_size):
            for y in range(0, height, grid_size):
                alpha = abs(math.sin(angle + x * 0.01 + y * 0.01)) * 0.5
                color = f'#{int(100 * alpha):02x}{int(255 * alpha):02x}{int(100 * alpha):02x}'
                
                if random.random() < 0.1:
                    self.canvas.create_text(
                        x, y,
                        text="01",
                        fill=color,
                        font=('Courier', 8)
                    )
    
    def draw_network_background(self, angle, pulse_phase):
        """Draw network-style background"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Network nodes
        nodes = []
        for i in range(10):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            nodes.append((x, y))
            
            alpha = abs(math.sin(angle + i * 0.5)) * 0.7 + 0.3
            color = f'#{int(100 * alpha):02x}{int(150 * alpha):02x}{int(255 * alpha):02x}'
            
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color)
        
        # Connect nodes
        for i, (x1, y1) in enumerate(nodes):
            for j, (x2, y2) in enumerate(nodes[i+1:], i+1):
                if random.random() < 0.3:
                    alpha = abs(math.sin(angle + i * j * 0.1)) * 0.5
                    color = f'#{int(100 * alpha):02x}{int(150 * alpha):02x}{int(255 * alpha):02x}'
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
    
    def draw_spiral_background(self, angle, pulse_phase):
        """Draw spiral pattern background"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        
        # Spiral pattern
        for i in range(100):
            t = i * 0.1 + angle
            r = i * 2
            x = center_x + r * math.cos(t)
            y = center_y + r * math.sin(t)
            
            if 0 <= x <= width and 0 <= y <= height:
                alpha = abs(math.sin(t * 2)) * 0.5
                color = f'#{int(255 * alpha):02x}{int(100 * alpha):02x}{int(255 * alpha):02x}'
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color)
    
    def draw_devops_tools(self, angle, pulse_phase):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3
        
        for i, (tool_name, tool_data) in enumerate(self.devops_tools.items()):
            # Calculate position based on mode
            if self.animation_mode == "circular":
                tool_angle = angle + (i * 2 * math.pi / len(self.devops_tools))
                x = center_x + radius * math.cos(tool_angle)
                y = center_y + radius * math.sin(tool_angle)
            elif self.animation_mode == "matrix":
                x = 100 + (i % 4) * 300
                y = 100 + (i // 4) * 200
            elif self.animation_mode == "network":
                tool_angle = angle + (i * 2 * math.pi / len(self.devops_tools))
                x = center_x + radius * 0.7 * math.cos(tool_angle)
                y = center_y + radius * 0.7 * math.sin(tool_angle)
            else:  # spiral
                tool_angle = angle + (i * 2 * math.pi / len(self.devops_tools))
                spiral_radius = radius * (0.5 + 0.5 * math.sin(angle * 2))
                x = center_x + spiral_radius * math.cos(tool_angle)
                y = center_y + spiral_radius * math.sin(tool_angle)
            
            # Enhanced pulse effect
            pulse = 1 + 0.3 * math.sin(pulse_phase + i * 0.5)
            size = int(45 * pulse)
            
            # Draw tool circle with gradient effect
            color = tool_data['color']
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline='white', width=3
            )
            
            # Inner glow effect
            inner_size = int(size * 0.7)
            self.canvas.create_oval(
                x - inner_size, y - inner_size, x + inner_size, y + inner_size,
                fill='', outline='white', width=1
            )
            
            # Draw tool icon with enhanced styling
            self.canvas.create_text(
                x, y,
                text=tool_data['icon'],
                font=('Arial', int(24 * pulse), 'bold'),
                fill='white'
            )
            
            # Draw tool name
            self.canvas.create_text(
                x, y + size + 20,
                text=tool_name,
                font=('Arial', 11, 'bold'),
                fill=color
            )
            
            # Enhanced status indicator
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
            status_size = int(10 * pulse)
            self.canvas.create_oval(
                x + size - 15, y - size + 15,
                x + size - 15 + status_size, y - size + 15 + status_size,
                fill=status_color, outline='white', width=2
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
            if self.animation_mode == "circular":
                angle1 = angle + (i * 2 * math.pi / len(self.devops_tools))
                angle2 = angle + ((i + 1) * 2 * math.pi / len(self.devops_tools))
                
                x1 = center_x + radius * math.cos(angle1)
                y1 = center_y + radius * math.sin(angle1)
                x2 = center_x + radius * math.cos(angle2)
                y2 = center_y + radius * math.sin(angle2)
            else:
                # For other modes, connect to center
                tool_angle = angle + (i * 2 * math.pi / len(self.devops_tools))
                x1 = center_x + radius * 0.7 * math.cos(tool_angle)
                y1 = center_y + radius * 0.7 * math.sin(tool_angle)
                x2 = center_x
                y2 = center_y
            
            # Animated connection line with enhanced effects
            alpha = abs(math.sin(angle + i * 0.5)) * 0.8 + 0.2
            color = f'#{int(100 * alpha):02x}{int(150 * alpha):02x}{int(255 * alpha):02x}'
            
            # Draw multiple lines for glow effect
            for width_offset in [3, 2, 1]:
                alpha_offset = alpha * (1 - width_offset * 0.2)
                glow_color = f'#{int(100 * alpha_offset):02x}{int(150 * alpha_offset):02x}{int(255 * alpha_offset):02x}'
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=glow_color, width=width_offset, capstyle=tk.ROUND
                )
            
            # Enhanced data flow particles
            particle_pos = (angle + i * 0.5) % (2 * math.pi)
            if particle_pos < 0.4:
                particle_x = x1 + (x2 - x1) * particle_pos / 0.4
                particle_y = y1 + (y2 - y1) * particle_pos / 0.4
                
                # Particle glow effect
                for size in [6, 4, 2]:
                    alpha_particle = (0.4 - particle_pos) / 0.4 * (1 - size * 0.15)
                    particle_color = f'#{int(255 * alpha_particle):02x}{int(255 * alpha_particle):02x}{int(100 * alpha_particle):02x}'
                    self.canvas.create_oval(
                        particle_x - size, particle_y - size,
                        particle_x + size, particle_y + size,
                        fill=particle_color, outline='white'
                    )
    
    def update_particle_system(self):
        """Update particle system positions and properties"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Update existing particles
        for particle in self.particle_system:
            particle['x'] += particle['vx'] * self.speed_var.get()
            particle['y'] += particle['vy'] * self.speed_var.get()
            particle['life'] += 0.01
            
            # Wrap around edges
            if particle['x'] < 0:
                particle['x'] = width
            elif particle['x'] > width:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = height
            elif particle['y'] > height:
                particle['y'] = 0
            
            # Reset particle when life expires
            if particle['life'] > 1:
                particle['life'] = 0
                particle['x'] = random.randint(0, width)
                particle['y'] = random.randint(0, height)
                particle['vx'] = random.uniform(-2, 2)
                particle['vy'] = random.uniform(-2, 2)
                particle['color'] = random.choice(['#00ff88', '#ff0088', '#0088ff', '#ffff00'])
        
        # Adjust particle count
        target_count = self.particle_var.get()
        while len(self.particle_system) < target_count:
            self.particle_system.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': random.uniform(0, 1),
                'color': random.choice(['#00ff88', '#ff0088', '#0088ff', '#ffff00'])
            })
        
        while len(self.particle_system) > target_count:
            self.particle_system.pop()
    
    def draw_particles(self):
        """Draw particle system"""
        for particle in self.particle_system:
            alpha = particle['life'] * 0.7 + 0.3
            size = int(3 * alpha)
            
            # Parse color and apply alpha
            color = particle['color']
            if color.startswith('#'):
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                alpha_color = f'#{int(r * alpha):02x}{int(g * alpha):02x}{int(b * alpha):02x}'
                
                self.canvas.create_oval(
                    particle['x'] - size, particle['y'] - size,
                    particle['x'] + size, particle['y'] + size,
                    fill=alpha_color, outline='white', width=1
                )
    
    def update_metrics(self):
        """Update tool metrics with realistic values"""
        statuses = ['running', 'building', 'committing', 'configuring', 'deploying', 'monitoring', 'visualizing']
        
        for tool_name, tool_data in self.devops_tools.items():
            # Randomly change status
            if random.random() < 0.005:  # 0.5% chance to change status
                tool_data['status'] = random.choice(statuses)
            
            # Update metrics with realistic values
            for metric_name in tool_data['metrics']:
                if random.random() < 0.1:  # 10% chance to update metric
                    base_value = tool_data['metrics'][metric_name]
                    change = random.randint(-5, 10)
                    tool_data['metrics'][metric_name] = max(0, base_value + change)
            
            # Update status indicator
            status_color = '#00ff00' if tool_data['status'] == 'running' else '#ffff00'
            self.metrics[f"{tool_name}_status"].config(fg=status_color)
            
            # Update metric display
            metrics_text = f"Status: {tool_data['status']}\n"
            for metric_name, value in tool_data['metrics'].items():
                metrics_text += f"{metric_name.title()}: {value}\n"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            metrics_text += f"Updated: {timestamp}"
            
            self.metrics[tool_name].config(
                text=metrics_text,
                fg='#00ff88' if tool_data['status'] == 'running' else '#ffff00'
            )

def main():
    root = tk.Tk()
    app = AdvancedDevOpsAnimationApp(root)
    
    # Handle window close
    def on_closing():
        app.stop_animations()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 