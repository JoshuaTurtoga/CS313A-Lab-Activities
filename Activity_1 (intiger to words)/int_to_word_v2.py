import tkinter as tk
from tkinter import ttk


class NumberConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number to Words Converter")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('MainFrame.TFrame', background='#f0f0f0')
        self.style.configure('Title.TLabel',
                             font=('Helvetica', 16, 'bold'),
                             background='#f0f0f0',
                             foreground='#2c3e50')
        self.style.configure('Input.TLabel',
                             font=('Helvetica', 12),
                             background='#f0f0f0',
                             foreground='#34495e')
        self.style.configure('Convert.TButton',
                             font=('Helvetica', 11),
                             padding=10)
        self.style.configure('Result.TLabel',
                             font=('Helvetica', 12),
                             background='#f0f0f0',
                             foreground='#2c3e50')

        # Create main frame with padding
        self.main_frame = ttk.Frame(
            root, style='MainFrame.TFrame', padding="40")
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        self.title_label = ttk.Label(self.main_frame,
                                     text="Number to Words Converter",
                                     style='Title.TLabel')
        self.title_label.pack(pady=(0, 30))

        # Input section
        self.input_frame = ttk.Frame(self.main_frame, style='MainFrame.TFrame')
        self.input_frame.pack(fill='x', pady=(0, 20))

        self.label = ttk.Label(self.input_frame,
                               text="Enter a number:",
                               style='Input.TLabel')
        self.label.pack(pady=(0, 8))

        # Custom entry style
        self.entry = ttk.Entry(self.input_frame,
                               width=30,
                               justify='center',
                               font=('Helvetica', 12))
        self.entry.pack(pady=(0, 15))

        # Convert button with hover effect
        self.convert_button = ttk.Button(self.input_frame,
                                         text="Convert",
                                         style='Convert.TButton',
                                         command=self.convert_number)
        self.convert_button.pack(pady=(0, 20))

        # Result section with border
        self.result_frame = ttk.Frame(
            self.main_frame, style='MainFrame.TFrame')
        self.result_frame.pack(fill='x')

        self.result_label = ttk.Label(self.result_frame,
                                      text="Result will appear here",
                                      style='Result.TLabel',
                                      wraplength=500)
        self.result_label.pack(pady=(10, 0))

    def number_to_words(self, num):
        ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
                'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
                'seventeen', 'eighteen', 'nineteen']
        tens = ['', '', 'twenty', 'thirty', 'forty',
                'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        scales = ['', 'thousand', 'million',
                  'billion', 'trillion', 'quadrillion']

        if num == 0:
            return 'zero'

        def helper(n, scale):
            if n == 0:
                return ''

            elif n < 20:
                return ones[n] + ' ' + scales[scale] + ' '

            elif n < 100:
                return tens[n // 10] + ('-' + ones[n % 10] if n % 10 != 0 else '') + ' ' + scales[scale] + ' '

            else:
                return ones[n // 100] + ' hundred ' + (helper(n % 100, 0) if n % 100 != 0 else '') + scales[scale] + ' '

        num_str = str(num)
        groups = []
        while num_str:
            groups.append(num_str[-3:] if len(num_str) >= 3 else num_str)
            num_str = num_str[:-3]

        result = ''
        for i, group in enumerate(groups):
            if int(group) != 0:
                result = helper(int(group), i) + result

        return ' '.join(result.strip().split())

    def convert_number(self):
        try:
            number = int(self.entry.get())
            if number < 0:
                self.result_label.config(text="Please enter a positive number")
                return
            if number >= 1_000_000_000_000_000_000:  # Quadrillion limit
                self.result_label.config(
                    text="Number too large (limit is quadrillion)")
                return
            words = self.number_to_words(number)
            self.result_label.config(text=words.capitalize())
        except ValueError:
            self.result_label.config(text="Please enter a valid number")


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberConverterApp(root)
    root.mainloop()
