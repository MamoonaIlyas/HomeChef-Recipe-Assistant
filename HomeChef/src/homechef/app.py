import sys
from PySide6.QtWidgets import QApplication
import os # We need this to handle file paths reliably
from .ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # --- Load and apply the global stylesheet ---
    # Construct the path to the stylesheet file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # This is the corrected line.
    # It goes up two directories from 'homechef' to 'src' and then to 'HomeChef'.
    stylesheet_path = os.path.join(current_dir, "..", "..", "style.css")
    
    try:
        with open(stylesheet_path, "r") as f:
            app.setStyleSheet(f.read())
        print("Stylesheet loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Stylesheet file not found at '{stylesheet_path}'.")
        print("Please ensure 'style.css' is in the main 'HOMECHEF' directory.")
    except Exception as e:
        print(f"An error occurred while loading the stylesheet: {e}")
    # --- End stylesheet loading ---

    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()