import tkinter as tk
from tkinter import ttk, scrolledtext, font
import requests
from typing import Optional, List
import json
import threading
from tkinter import messagebox

class PromptDirectorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MetaPrompt Forge v1.0")
        self.root.geometry("1000x600")
        
        # Configure default font size
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        
        text_font = font.nametofont("TkTextFont")
        text_font.configure(size=14)
        
        fixed_font = font.nametofont("TkFixedFont")
        fixed_font.configure(size=14)
        
        # Set base URL and model
        self.base_url = "http://localhost:11434"
        self.model = "gemma2:9b"
        self.available_models: List[str] = []
        
        # Configure root grid - equal weights for columns
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)  # Main content row
        self.root.grid_rowconfigure(1, weight=0)  # Buttons row
        self.root.grid_rowconfigure(2, weight=0)  # Status bar row
        
        self.setup_ui()
        self.setup_styles()
        
        # Bind Enter key to generate_prompt
        self.root.bind('<Return>', lambda event: self.generate_prompt())
        
        # Fetch available models on startup
        threading.Thread(target=self.fetch_models, daemon=True).start()
        
    def setup_styles(self):
        """Configure custom styles for the UI elements"""
        style = ttk.Style()
        style.configure('Generate.TButton', 
                       padding=5,
                       font=('Helvetica', 14, 'bold'))
        style.configure('Copy.TButton',
                       padding=5,
                       font=('Helvetica', 14))
        style.configure('Status.TLabel',
                       padding=2,
                       font=('Helvetica', 12))
        style.configure('TLabel',
                       font=('Helvetica', 14))
        style.configure('TLabelframe.Label',
                       font=('Helvetica', 14))
        style.configure('TEntry',
                       font=('Helvetica', 14))
        style.configure('TCombobox',
                       font=('Helvetica', 14))
                       
    def fetch_models(self):
        """Fetch available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                self.available_models = [model['name'] for model in response.json()['models']]
                # Update combobox values
                self.model_combo['values'] = self.available_models
                if self.model in self.available_models:
                    self.model_combo.set(self.model)
                elif self.available_models:
                    self.model_combo.set(self.available_models[0])
                self.set_status("Models loaded successfully")
            else:
                self.set_status("Failed to fetch models")
        except Exception as e:
            self.set_status(f"Error fetching models: {str(e)}")
        
    def setup_ui(self):
        """Create all UI elements"""
        # Create main frames
        self.create_input_frame()
        self.create_output_frame()
        self.create_button_row()
        self.create_status_bar()
        
    def create_input_frame(self):
        """Create the left input frame"""
        input_frame = ttk.LabelFrame(self.root, text="Input", padding="3 3 3 3")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        # Settings frame at the top
        settings_frame = ttk.Frame(input_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 2))
        
        # Model selection (combobox)
        ttk.Label(settings_frame, text="Model:").pack(side=tk.LEFT, padx=(0, 2))
        self.model_combo = ttk.Combobox(settings_frame, width=20, font=('Helvetica', 14))
        self.model_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Base URL
        ttk.Label(settings_frame, text="URL:").pack(side=tk.LEFT, padx=(0, 2))
        self.url_var = tk.StringVar(value=self.base_url)
        url_entry = ttk.Entry(settings_frame, textvariable=self.url_var, width=25, font=('Helvetica', 14))
        url_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Refresh models button
        refresh_btn = ttk.Button(settings_frame, 
                               text="↻", 
                               width=3,
                               command=lambda: threading.Thread(target=self.fetch_models, daemon=True).start())
        refresh_btn.pack(side=tk.LEFT)
        
        # Query input
        ttk.Label(input_frame, text="Enter your query:").pack(anchor="w")
        self.query_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, font=('Helvetica', 14))
        self.query_input.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
    def create_output_frame(self):
        """Create the right output frame"""
        output_frame = ttk.LabelFrame(self.root, text="Structured Prompt Output", padding="3 3 3 3")
        output_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=('Helvetica', 14))
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def create_button_row(self):
        """Create row with buttons under the main frames"""
        # Left side - Generate button (aligned with input frame)
        generate_btn = ttk.Button(self.root, 
                                text="Generate Structured Prompt", 
                                style='Generate.TButton',
                                command=self.generate_prompt)
        generate_btn.grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        
        # Right side - Copy button (aligned with output frame)
        copy_btn = ttk.Button(self.root,
                            text="Copy to Clipboard",
                            style='Copy.TButton',
                            command=self.copy_to_clipboard)
        copy_btn.grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.root, 
                                    textvariable=self.status_var,
                                    style='Status.TLabel')
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=2)
        self.set_status("Ready")
        
    def set_status(self, message: str):
        """Update status bar message"""
        self.status_var.set(f"Status: {message}")
        
    def copy_to_clipboard(self):
        """Copy output text to clipboard"""
        output_text = self.output_text.get("1.0", tk.END).strip()
        if output_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_text)
            self.set_status("Prompt copied to clipboard")
        else:
            self.set_status("No prompt to copy")
            
    def call_ollama(self, prompt: str) -> Optional[str]:
        """Send request to Ollama API"""
        try:
            response = requests.post(
                f"{self.url_var.get()}/api/generate",
                json={
                    "model": self.model_combo.get(),
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json().get('response', '')
        except Exception as e:
            return f"API Error: {str(e)}"
            
    def generate_prompt(self):
        """Generate the structured prompt"""
        def generate():
            self.set_status("Generating prompt...")
            query = self.query_input.get("1.0", tk.END).strip()
            
            if not query:
                self.set_status("Error: Query cannot be empty!")
                return
                
            # Clear output
            self.output_text.delete("1.0", tk.END)
            
            meta_prompt = f"""Analyze the user query and create a comprehensive structured prompt that emphasizes source verification and citation requirements.

OUTPUT FORMAT MUST BE EXACTLY AS FOLLOWS:

SYSTEM MESSAGE:
[Define the specific expert role needed for the response]
[Specify professional background and expertise level]

CONTEXT:
[Specify main context and knowledge domain]
[Define scope and relevance]

SOURCE AND CITATION REQUIREMENTS:
1. Primary Sources:
   - Academic journals required
   - Peer-reviewed publications
   - Official institutional data
   - Time period of acceptable sources

2. Citation Format:
   - How to reference sources in the response
   - Required citation elements
   - Handling of direct quotes
   - Treatment of statistical data

3. Fact Verification:
   - Multiple source verification requirement
   - Cross-reference guidelines
   - Data recency requirements
   - Confidence level indicators

4. Source Authorities:
   - Acceptable institutional sources
   - Required database checks
   - Expert verification needs
   - Industry standard references

RESPONSE CHARACTERISTICS:
1. Evidence-Based Components:
   - Every claim must be sourced
   - Statistical data requirements
   - Expert opinion integration
   - Research basis for recommendations

2. Structure and Format:
   - Response type (list/text/analysis/steps)
   - Number of points/examples
   - Length guidelines
   - Format specifications

3. Quality Standards:
   - Peer-review level requirements
   - Data verification standards
   - Source credibility metrics
   - Update frequency requirements

CONSTRAINTS:
- Only use verifiable sources
- No speculative content
- No unsourced claims
- Time-bound relevance
- Geographic relevance
- Industry-specific limitations

NEGATIVE INSTRUCTIONS:
- No unverified claims
- No obsolete sources
- No single-source facts
- No anecdotal evidence
- No promotional content
- No opinion-based statements

VERIFICATION PROTOCOL:
1. Source Check Requirements:
   - Minimum number of sources
   - Source diversity requirements
   - Currency of information
   - Authority verification

2. Data Validation:
   - Statistical significance needed
   - Sample size requirements
   - Methodology verification
   - Replication standards

USER QUERY:
{query}

REFORMULATED QUERY:
[Clear and specific reformulation with emphasis on verified information]

Remember:
1. Every factual claim must be sourceable
2. Prefer recent sources (within last 5 years where applicable)
3. Use multiple sources for verification
4. Include confidence levels for claims
5. Specify any gaps in available verified information
6. Note when sources conflict on specific points
7. Maintain academic rigor in source selection"""

            result = self.call_ollama(meta_prompt)
            
            # Update output
            self.output_text.insert("1.0", result)
            self.set_status("Ready")
            
        # Run in separate thread to prevent UI freezing
        threading.Thread(target=generate, daemon=True).start()

def main():
    root = tk.Tk()
    app = PromptDirectorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()