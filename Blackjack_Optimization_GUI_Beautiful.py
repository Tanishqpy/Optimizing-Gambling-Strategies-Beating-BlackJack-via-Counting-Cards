import cvxpy as cp
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from matplotlib.figure import Figure
from tkinter.font import Font
import os
from PIL import Image, ImageTk

class ModernButton(tk.Button):
    """Custom button with modern styling"""
    def __init__(self, master=None, **kwargs):
        self.original_bg = kwargs.get('bg', '#4a6cd4')
        self.hover_bg = self._adjust_color(self.original_bg, 20)
        
        kwargs['bg'] = self.original_bg
        kwargs['fg'] = kwargs.get('fg', 'white')
        kwargs['relief'] = kwargs.get('relief', 'flat')
        kwargs['borderwidth'] = kwargs.get('borderwidth', 0)
        kwargs['padx'] = kwargs.get('padx', 15)
        kwargs['pady'] = kwargs.get('pady', 8)
        kwargs['font'] = kwargs.get('font', ('Segoe UI', 10))
        
        super().__init__(master, **kwargs)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _adjust_color(self, hex_color, amount):
        """Adjust color brightness"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _on_enter(self, e):
        """Mouse hover effect"""
        self.config(bg=self.hover_bg, cursor="hand2")
    
    def _on_leave(self, e):
        """Mouse leave effect"""
        self.config(bg=self.original_bg)

class ModernTooltip:
    """Custom tooltip for widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", 
                         borderwidth=1, padx=5, pady=2, font=("Segoe UI", 9))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class CustomFrame(ttk.LabelFrame):
    """Enhanced frame with better styling"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        style = ttk.Style()
        style.configure('TLabelframe', borderwidth=2)
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'))

class BlackjackOptimizationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Betting Optimization Suite")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f0f0f5")
        
        # Define color scheme
        self.colors = {
            'primary': '#4a6cd4',   # Blue
            'secondary': '#5e35b1', # Deep purple
            'accent': '#ec407a',    # Pink
            'background': '#f0f0f5',# Light gray-blue
            'text': '#333333',      # Dark gray
            'success': '#66bb6a',   # Green
            'warning': '#ffa726'    # Orange
        }
        
        # Configure ttk styles
        self.configure_styles()
        
        # Create header
        self.create_header()
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both", padx=15, pady=5)
        
        # Parameters tab
        self.params_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab_control.add(self.params_tab, text="Parameters")
        
        # Results tab
        self.results_tab = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab_control.add(self.results_tab, text="Results")
        
        # Setup parameter inputs
        self.setup_parameter_inputs()
        
        # Setup results display
        self.setup_results_display()
        
        # Add footer
        self.create_footer()
        
        # Initialize results storage
        self.optimal_bets = None
        self.expected_profit = None
        
    def configure_styles(self):
        """Configure custom ttk styles"""
        style = ttk.Style()
        
        # General styles
        style.configure('TFrame', background=self.colors['background'])
        style.configure('Tab.TFrame', background=self.colors['background'])
        style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text'])
        style.configure('TLabelframe', background=self.colors['background'])
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'), foreground=self.colors['primary'])
        
        # Tab style
        style.configure('TNotebook', background=self.colors['background'])
        style.configure('TNotebook.Tab', background=self.colors['background'], 
                        padding=[12, 6], font=('Segoe UI', 10))
        style.map('TNotebook.Tab', background=[('selected', self.colors['primary'])],
                  foreground=[('selected', 'white')])
        
        # Entry style
        style.configure('TEntry', padding=5)
    
    def create_header(self):
        """Create attractive header for the application"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        
        # App title
        title_font = Font(family="Segoe UI", size=16, weight="bold")
        title_label = tk.Label(header_frame, text="Blackjack Betting Optimization", 
                              bg=self.colors['primary'], fg="white", font=title_font)
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Subtitle
        subtitle_font = Font(family="Segoe UI", size=10, slant="italic")
        subtitle = tk.Label(header_frame, text="Advanced Strategy Simulation", 
                           bg=self.colors['primary'], fg="white", font=subtitle_font)
        subtitle.pack(side=tk.LEFT, padx=10, pady=15)
    
    def create_footer(self):
        """Create footer with status information"""
        footer_frame = tk.Frame(self.root, bg=self.colors['background'], height=30)
        footer_frame.pack(fill='x', side=tk.BOTTOM, padx=10, pady=5)
        
        status_label = tk.Label(footer_frame, text="Ready", bg=self.colors['background'],
                               fg=self.colors['text'], font=("Segoe UI", 9))
        status_label.pack(side=tk.LEFT)
        
        self.status_text = status_label
        
        # Version info
        version_label = tk.Label(footer_frame, text="v1.0.0", bg=self.colors['background'],
                                fg=self.colors['text'], font=("Segoe UI", 9))
        version_label.pack(side=tk.RIGHT)
    
    def setup_parameter_inputs(self):
        main_param_frame = ttk.Frame(self.params_tab)
        main_param_frame.pack(padx=20, pady=15, fill="both", expand=True)
        
        # Introduction text
        intro_frame = ttk.Frame(main_param_frame)
        intro_frame.pack(fill="x", padx=5, pady=10)
        
        intro_text = ("Configure the optimization parameters below to find the optimal betting strategy "
                      "based on count states and expected values.")
        intro_label = ttk.Label(intro_frame, text=intro_text, wraplength=800, 
                              font=("Segoe UI", 10), justify="left")
        intro_label.pack(anchor="w")
        
        # Create two-column layout
        columns_frame = ttk.Frame(main_param_frame)
        columns_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        left_column = ttk.Frame(columns_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=10)
        
        right_column = ttk.Frame(columns_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=10)
        
        # Basic parameters in left column
        param_frame = CustomFrame(left_column, text="Basic Parameters")
        param_frame.pack(padx=5, pady=10, fill="both", expand=True)
        
        # State count
        ttk.Label(param_frame, text="Number of count states (N):").grid(row=0, column=0, padx=8, pady=12, sticky="w")
        self.n_var = tk.StringVar(value="1000")
        n_entry = ttk.Entry(param_frame, textvariable=self.n_var, width=10)
        n_entry.grid(row=0, column=1, padx=8, pady=12)
        ModernTooltip(n_entry, "Total number of possible count states to optimize for")
        
        # Min bet
        ttk.Label(param_frame, text="Minimum bet (x_min):").grid(row=1, column=0, padx=8, pady=12, sticky="w")
        self.min_bet_var = tk.StringVar(value="1.0")
        min_entry = ttk.Entry(param_frame, textvariable=self.min_bet_var, width=10)
        min_entry.grid(row=1, column=1, padx=8, pady=12)
        ModernTooltip(min_entry, "Minimum allowable bet size")
        
        # Max bet
        ttk.Label(param_frame, text="Maximum bet (x_max):").grid(row=2, column=0, padx=8, pady=12, sticky="w")
        self.max_bet_var = tk.StringVar(value="100.0")
        max_entry = ttk.Entry(param_frame, textvariable=self.max_bet_var, width=10)
        max_entry.grid(row=2, column=1, padx=8, pady=12)
        ModernTooltip(max_entry, "Maximum allowable bet size")
        
        # EV parameters in right column
        ev_frame = CustomFrame(right_column, text="Expected Value Parameters")
        ev_frame.pack(padx=5, pady=10, fill="both", expand=True)
        
        # High count EV range
        ttk.Label(ev_frame, text="High count EV range:").grid(row=0, column=0, padx=8, pady=12, sticky="w")
        self.high_ev_min_var = tk.StringVar(value="0.01")
        high_ev_min_entry = ttk.Entry(ev_frame, textvariable=self.high_ev_min_var, width=6)
        high_ev_min_entry.grid(row=0, column=1, padx=5, pady=12)
        ModernTooltip(high_ev_min_entry, "Minimum expected value for high count states")
        
        ttk.Label(ev_frame, text="to").grid(row=0, column=2)
        self.high_ev_max_var = tk.StringVar(value="0.025")
        high_ev_max_entry = ttk.Entry(ev_frame, textvariable=self.high_ev_max_var, width=6)
        high_ev_max_entry.grid(row=0, column=3, padx=5, pady=12)
        ModernTooltip(high_ev_max_entry, "Maximum expected value for high count states")
        
        # Low count EV range
        ttk.Label(ev_frame, text="Low count EV range:").grid(row=1, column=0, padx=8, pady=12, sticky="w")
        self.low_ev_min_var = tk.StringVar(value="-0.01")
        low_ev_min_entry = ttk.Entry(ev_frame, textvariable=self.low_ev_min_var, width=6)
        low_ev_min_entry.grid(row=1, column=1, padx=5, pady=12)
        ModernTooltip(low_ev_min_entry, "Minimum expected value for low count states")
        
        ttk.Label(ev_frame, text="to").grid(row=1, column=2)
        self.low_ev_max_var = tk.StringVar(value="-0.005")
        low_ev_max_entry = ttk.Entry(ev_frame, textvariable=self.low_ev_max_var, width=6)
        low_ev_max_entry.grid(row=1, column=3, padx=5, pady=12)
        ModernTooltip(low_ev_max_entry, "Maximum expected value for low count states")
        
        # Number of states with special EVs
        ttk.Label(ev_frame, text="High/Low count states:").grid(row=2, column=0, padx=8, pady=12, sticky="w")
        self.ev_states_var = tk.StringVar(value="10")
        ev_states_entry = ttk.Entry(ev_frame, textvariable=self.ev_states_var, width=6)
        ev_states_entry.grid(row=2, column=1, padx=5, pady=12)
        ModernTooltip(ev_states_entry, "Number of states considered as high/low count")
        
        # Buttons with modern styling
        button_frame = ttk.Frame(main_param_frame)
        button_frame.pack(pady=20, fill="x")
        
        run_btn = ModernButton(button_frame, text="Run Optimization", command=self.run_optimization, 
                              bg=self.colors['primary'], font=("Segoe UI", 11))
        run_btn.pack(side=tk.LEFT, padx=15)
        
        reset_btn = ModernButton(button_frame, text="Reset Parameters", command=self.reset_parameters, 
                               bg=self.colors['secondary'], font=("Segoe UI", 11))
        reset_btn.pack(side=tk.LEFT, padx=15)
    
    def setup_results_display(self):
        # Main container for results
        main_results_container = ttk.Frame(self.results_tab)
        main_results_container.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Results text area with better styling
        result_text_frame = CustomFrame(main_results_container, text="Optimization Results")
        result_text_frame.pack(padx=5, pady=10, fill="x", expand=False)
        
        self.result_text = scrolledtext.ScrolledText(result_text_frame, width=80, height=10,
                                                  font=("Consolas", 10), bg="#fafafa", bd=1)
        self.result_text.pack(padx=8, pady=8, fill="both", expand=True)
        
        # Configure tags for styling text
        self.result_text.tag_configure("header", font=("Segoe UI", 11, "bold"), foreground=self.colors['primary'])
        self.result_text.tag_configure("success", foreground=self.colors['success'])
        self.result_text.tag_configure("emphasis", font=("Segoe UI", 10, "italic"))
        
        # Graph area with enhanced styling
        self.graph_frame = CustomFrame(main_results_container, text="Bet Size vs Count State")
        self.graph_frame.pack(padx=5, pady=10, fill="both", expand=True)
        
        # Create figure with a more professional style
        plt.style.use('ggplot')
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.figure.patch.set_facecolor('#fafafa')
        self.plot = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Add export button
        export_frame = ttk.Frame(main_results_container)
        export_frame.pack(fill="x", pady=10)
        
        export_btn = ModernButton(export_frame, text="Export Results", 
                                 bg=self.colors['accent'], font=("Segoe UI", 10))
        export_btn.pack(side=tk.RIGHT, padx=5)
    
    def reset_parameters(self):
        self.n_var.set("1000")
        self.min_bet_var.set("1.0")
        self.max_bet_var.set("100.0")
        self.high_ev_min_var.set("0.01")
        self.high_ev_max_var.set("0.025")
        self.low_ev_min_var.set("-0.01")
        self.low_ev_max_var.set("-0.005")
        self.ev_states_var.set("10")
        self.status_text.config(text="Parameters reset to default values")
    
    def run_optimization(self):
        try:
            # Parse input parameters
            N = int(self.n_var.get())
            x_min = float(self.min_bet_var.get())
            x_max = float(self.max_bet_var.get())
            high_ev_min = float(self.high_ev_min_var.get())
            high_ev_max = float(self.high_ev_max_var.get())
            low_ev_min = float(self.low_ev_min_var.get())
            low_ev_max = float(self.low_ev_max_var.get())
            ev_states = int(self.ev_states_var.get())
            
            # Update status
            self.status_text.config(text="Optimization in progress...")
            
            # Create thread to run optimization
            threading.Thread(target=self.run_optimization_thread, 
                             args=(N, x_min, x_max, high_ev_min, high_ev_max, 
                                   low_ev_min, low_ev_max, ev_states)).start()
            
            # Clear and update results text area
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Optimization in progress...\n", "emphasis")
            self.result_text.insert(tk.END, "Please wait while we calculate the optimal strategy...\n", "emphasis")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check your inputs: {str(e)}")
            self.status_text.config(text=f"Error: {str(e)}")
    
    def run_optimization_thread(self, N, x_min, x_max, high_ev_min, high_ev_max, low_ev_min, low_ev_max, ev_states):
        try:
            # Expected value per hand for each count state
            expected_ev = np.zeros(N)
            # Assign positive EVs for high counts
            expected_ev[-ev_states:] = np.linspace(high_ev_min, high_ev_max, ev_states)
            # Assign negative EVs for low counts
            expected_ev[:ev_states] = np.linspace(low_ev_min, low_ev_max, ev_states)

            # Probability of each count state (uniform for illustration)
            prob_state = np.ones(N) / N

            # Decision variables: bet size for each count state
            x = cp.Variable(N)

            # Objective: maximize expected profit across all count states
            objective = cp.Maximize(cp.sum(cp.multiply(prob_state, expected_ev * x)))

            # Constraints
            constraints = [
                x >= x_min,
                x <= x_max
                # Optionally: cp.sum(x) <= total_bankroll
            ]

            # Problem definition
            problem = cp.Problem(objective, constraints)

            # Solve
            problem.solve()
            
            # Store results
            self.optimal_bets = x.value
            self.expected_profit = problem.value
            
            # Update UI with results (must be done in main thread)
            self.root.after(0, self.update_results)
            
        except Exception as e:
            # Update UI with error (must be done in main thread)
            self.root.after(0, lambda: self.show_error(str(e)))
    
    def update_results(self):
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Display optimization results with styled text
        self.result_text.insert(tk.END, "OPTIMIZATION COMPLETE\n", "header")
        self.result_text.insert(tk.END, "═══════════════════════\n\n")
        self.result_text.insert(tk.END, f"Maximum expected profit per hand: ", "emphasis")
        self.result_text.insert(tk.END, f"{self.expected_profit:.6f}\n\n", "success")
        
        # Sample of optimal bet sizes
        self.result_text.insert(tk.END, "SAMPLE OF OPTIMAL BET SIZES:\n", "header")
        self.result_text.insert(tk.END, "─────────────────────────────\n")
        
        N = len(self.optimal_bets)
        samples = [0, N//4, N//2, 3*N//4, N-1] 
        for idx in samples:
            self.result_text.insert(tk.END, f"• Count state {idx}: ")
            self.result_text.insert(tk.END, f"{self.optimal_bets[idx]:.2f}\n")
        
        # Update status
        self.status_text.config(text="Optimization completed successfully")
        
        # Plot the results
        self.plot_results()
        
        # Switch to the results tab
        self.tab_control.select(1)
    
    def plot_results(self):
        self.plot.clear()
        
        x_vals = list(range(len(self.optimal_bets)))
        
        # Create color gradient based on bet sizes for visual appeal
        cmap = plt.cm.viridis
        norm = plt.Normalize(min(self.optimal_bets), max(self.optimal_bets))
        colors = cmap(norm(self.optimal_bets))
        
        # Plot with gradient coloring and improved styling
        sc = self.plot.scatter(x_vals, self.optimal_bets, c=self.optimal_bets, 
                              cmap=cmap, alpha=0.8, edgecolors='none', s=25)
        
        # Add line plot with custom styling
        self.plot.plot(x_vals, self.optimal_bets, color='#3366FF', linestyle='-', 
                       linewidth=1.2, alpha=0.7)
        
        # Add a color bar with better styling
        cbar = self.figure.colorbar(sc, ax=self.plot)
        cbar.set_label('Optimal Bet Size', fontsize=10, fontweight='bold')
        
        # Highlight extreme points
        max_idx = np.argmax(self.optimal_bets)
        min_idx = np.argmin(self.optimal_bets)
        
        # Add annotations for max and min points
        self.plot.plot(max_idx, self.optimal_bets[max_idx], 'ro', markersize=10, 
                      label=f'Max Bet: {self.optimal_bets[max_idx]:.2f}')
        self.plot.annotate(f'{self.optimal_bets[max_idx]:.2f}', 
                          (max_idx, self.optimal_bets[max_idx]),
                          textcoords="offset points", xytext=(0,10), 
                          ha='center', fontsize=9, fontweight='bold')
        
        self.plot.plot(min_idx, self.optimal_bets[min_idx], 'go', markersize=10, 
                      label=f'Min Bet: {self.optimal_bets[min_idx]:.2f}')
        self.plot.annotate(f'{self.optimal_bets[min_idx]:.2f}', 
                          (min_idx, self.optimal_bets[min_idx]),
                          textcoords="offset points", xytext=(0,10), 
                          ha='center', fontsize=9, fontweight='bold')
        
        # Add plot styling and annotations
        self.plot.set_xlabel('Count State', fontsize=12, fontweight='bold')
        self.plot.set_ylabel('Optimal Bet Size', fontsize=12, fontweight='bold')
        self.plot.set_title('Optimal Betting Strategy by Count State', fontsize=14, fontweight='bold',
                          color='#333333')
        
        # Customize grid
        self.plot.grid(True, linestyle='--', alpha=0.4, color='gray')
        
        # Set background color
        self.plot.set_facecolor('#fafafa')
        
        # Add legend with better styling
        self.plot.legend(loc='best', framealpha=0.8, fontsize=10)
        
        # Adjust axis limits for better visualization
        y_min = min(self.optimal_bets) * 0.95
        y_max = max(self.optimal_bets) * 1.05
        self.plot.set_ylim([y_min, y_max])
        
        # Prettify axis numbers
        self.plot.tick_params(axis='both', which='major', labelsize=10)
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Draw plot
        self.canvas.draw()
    
    def show_error(self, error_msg):
        messagebox.showerror("Optimization Error", f"An error occurred: {error_msg}")
        self.result_text.delete(1.0, tk.END)
        
        # Format error message for better visibility
        self.result_text.tag_configure("error_header", foreground="red", font=("Segoe UI", 12, "bold"))
        self.result_text.tag_configure("error_detail", foreground="#CC0000", font=("Segoe UI", 10))
        
        self.result_text.insert(tk.END, "ERROR OCCURRED\n", "error_header")
        self.result_text.insert(tk.END, "═══════════════\n\n")
        self.result_text.insert(tk.END, f"{error_msg}\n\n", "error_detail")
        self.result_text.insert(tk.END, "Please check your inputs and try again.", "error_detail")
        
        # Update status
        self.status_text.config(text=f"Error: {error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackOptimizationGUI(root)
    root.mainloop()
