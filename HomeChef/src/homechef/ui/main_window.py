from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QTextEdit, QLabel, QTabWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
import pathlib
import markdown
from ..services import db
from ..services.openai_client import chat_reply
from ..logic.recommender import match_score
from .custom_dialog import CustomDialog

PROJECT_ROOT = pathlib.Path.cwd()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HomeChef – AI Recipe Assistant")
        self.resize(1000, 650)
        self._load_styles()
        db.init_db()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self._init_recipes_tab()
        self._init_pantry_tab()
        self._init_grocery_tab()
        self._init_assistant_tab()

    def _load_styles(self):
        style_path = PROJECT_ROOT / "style.css"
        if style_path.exists():
            with open(style_path, "r") as f:
                QApplication.instance().setStyleSheet(f.read())
            print("Stylesheet loaded successfully.")
        else:
            print(f"ERROR: Could not find style.css at: {str(style_path)}")

    def _init_recipes_tab(self):
        page = QWidget(); layout = QVBoxLayout(page); top_layout = QHBoxLayout(); self.search_box = QLineEdit(); self.search_box.setPlaceholderText("Search recipes by title..."); self.search_btn = QPushButton("Search"); self.search_btn.clicked.connect(self._load_recipes); search_icon = QIcon(str(PROJECT_ROOT / "icons/search.svg")); self.search_btn.setIcon(search_icon); self.search_btn.setIconSize(QSize(18, 18)); top_layout.addWidget(self.search_box); top_layout.addWidget(self.search_btn); layout.addLayout(top_layout)
        main_layout = QHBoxLayout(); self.recipe_list = QListWidget(); self.recipe_list.currentRowChanged.connect(self._show_recipe_details); main_layout.addWidget(self.recipe_list, 30)
        right_panel = QVBoxLayout(); top_right_layout = QHBoxLayout(); self.recipe_image = QLabel("Select a recipe to see details"); self.recipe_image.setFixedSize(300, 200); self.recipe_image.setAlignment(Qt.AlignCenter); self.recipe_image.setObjectName("recipe_image"); top_right_layout.addWidget(self.recipe_image)
        title_meta_layout = QVBoxLayout(); title_meta_layout.setContentsMargins(10, 0, 0, 0); self.recipe_title = QLabel("Welcome to HomeChef!"); self.recipe_title.setObjectName("recipe_title"); self.recipe_meta = QLabel("Your personal cooking assistant."); self.recipe_meta.setObjectName("recipe_meta"); self.recipe_meta.setWordWrap(True); title_meta_layout.addWidget(self.recipe_title); title_meta_layout.addWidget(self.recipe_meta); title_meta_layout.addStretch(); top_right_layout.addLayout(title_meta_layout)
        right_panel.addLayout(top_right_layout)
        self.recipe_details = QTextEdit(); self.recipe_details.setReadOnly(True); self.recipe_details.setObjectName("recipe_details"); self.add_to_grocery_btn = QPushButton("Add Missing Ingredients to Grocery List"); self.add_to_grocery_btn.clicked.connect(self._add_missing_to_grocery); right_panel.addWidget(self.recipe_details, 1); right_panel.addWidget(self.add_to_grocery_btn); main_layout.addLayout(right_panel, 70); layout.addLayout(main_layout, 1)
        bottom_layout = QHBoxLayout(); self.have_box = QLineEdit(); self.have_box.setPlaceholderText("I have: e.g., tomato, pasta, cheese"); self.suggest_btn = QPushButton("Suggest by Ingredients (AI)"); self.suggest_btn.clicked.connect(self._ai_suggest_from_have); bottom_layout.addWidget(self.have_box, 1); bottom_layout.addWidget(self.suggest_btn); layout.addLayout(bottom_layout)
        self.tabs.addTab(page, "Recipes"); self._load_recipes()

    def _init_pantry_tab(self):
        page = QWidget(); main_layout = QHBoxLayout(page); main_layout.setSpacing(15); left_layout = QVBoxLayout(); left_layout.addWidget(QLabel("Your Pantry Items")); self.pantry_edit = QTextEdit(); self.pantry_edit.setPlaceholderText("One ingredient per line, e.g.\nFlour\nEggs\nSugar"); left_layout.addWidget(self.pantry_edit); pantry_btns_layout = QHBoxLayout(); self.pantry_load_btn = QPushButton("Load Pantry"); self.pantry_save_btn = QPushButton("Save Pantry"); self.pantry_load_btn.clicked.connect(self._load_pantry); self.pantry_save_btn.clicked.connect(self._save_pantry); pantry_btns_layout.addWidget(self.pantry_load_btn); pantry_btns_layout.addWidget(self.pantry_save_btn); left_layout.addLayout(pantry_btns_layout)
        right_panel = QWidget(); right_panel.setObjectName("pantry_info_panel"); right_layout = QVBoxLayout(right_panel); right_layout.setAlignment(Qt.AlignCenter); icon_label = QLabel(); pantry_icon = QPixmap(str(PROJECT_ROOT / "icons/archive.svg")); icon_label.setPixmap(pantry_icon.scaled(QSize(64, 64), Qt.KeepAspectRatio, Qt.SmoothTransformation)); icon_label.setObjectName("pantry_icon_label"); icon_label.setAlignment(Qt.AlignCenter); title_label = QLabel("Manage Your Pantry"); title_label.setObjectName("pantry_info_title"); title_label.setAlignment(Qt.AlignCenter)
        text_label = QLabel("Add the ingredients you have at home here, one per line. This list helps the app suggest recipes and identify what you need to buy for a meal."); text_label.setObjectName("pantry_info_text"); text_label.setWordWrap(True); text_label.setAlignment(Qt.AlignCenter); right_layout.addWidget(icon_label); right_layout.addWidget(title_label); right_layout.addWidget(text_label); right_layout.addStretch()
        main_layout.addLayout(left_layout, 60); main_layout.addWidget(right_panel, 40); self.tabs.addTab(page, "Pantry"); self._load_pantry()
    
    # --- NEW: HELPER FUNCTION TO RESET THE RECIPE VIEW ---
    def _clear_recipe_details(self):
        """Resets the recipe details panel to its default state."""
        self.recipe_image.setPixmap(QPixmap()) # Clear the image
        self.recipe_image.setText("Select a recipe to see details")
        self.recipe_title.setText("Welcome to HomeChef!")
        self.recipe_meta.setText("Your personal cooking assistant.")
        self.recipe_details.clear()

    # --- UPDATED: SEARCH LOGIC NOW HANDLES NO RESULTS ---
    def _load_recipes(self):
        self.recipe_list.clear()
        self._clear_recipe_details() # Reset the view every time a search starts

        query = self.search_box.text().strip()
        self._recipes = db.get_recipes(query)

        # If the search returned no results, show a message
        if not self._recipes and query:
            dialog = CustomDialog(
                "No Results",
                f"Sorry, no recipes were found matching '{query}'.\nPlease try a different search term.",
                "info",
                parent=self
            )
            dialog.exec()
            # After showing the message, load all recipes again so the list isn't empty
            self._recipes = db.get_recipes()

        # Populate the list with the final results (either search or all)
        for r in self._recipes:
            self.recipe_list.addItem(f"{r['title']}")
            
    def _show_recipe_details(self, idx):
        if idx < 0 or idx >= len(self._recipes):
            self._clear_recipe_details() # Use the helper function here too
            return
            
        r = self._recipes[idx]
        self.recipe_title.setText(r['title'])
        meta = f"Time: {r.get('time_minutes') or '?'} min | Difficulty: {r.get('difficulty') or '?'}\nIngredients: " + ", ".join(r.get('ingredients', []))
        self.recipe_meta.setText(meta)
        steps_text = "\n".join([f"Step {i+1}. {s}" for i, s in enumerate(r.get('steps', []))])
        self.recipe_details.setPlainText(steps_text)
        self.recipe_image.setPixmap(QPixmap())
        
        image_path = r.get('image_path')
        if image_path:
            full_path = PROJECT_ROOT / image_path
            if full_path.exists():
                pixmap = QPixmap(str(full_path))
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(self.recipe_image.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                    self.recipe_image.setPixmap(scaled_pixmap); self.recipe_image.setText("")
                else: self.recipe_image.setText("Failed to load image.")
            else: self.recipe_image.setText("Image Not Found.")
        else: self.recipe_image.setText("No Image Available.")

    def _add_missing_to_grocery(self):
        idx = self.recipe_list.currentRow()
        if idx < 0: return
        r = self._recipes[idx]
        pantry = db.get_pantry()
        _, missing = match_score(pantry, r['ingredients'])
        if not missing:
            dialog = CustomDialog("All Set!", "You already have all the ingredients.", "success", parent=self); dialog.exec()
            return
        capitalized_missing = [item.title() for item in missing]
        grocery = list(dict.fromkeys(db.get_grocery() + capitalized_missing))
        db.set_grocery(grocery)
        dialog = CustomDialog("Added", f"Added missing items: {', '.join(capitalized_missing)}", "success", parent=self); dialog.exec()
        self._load_grocery()

    def _ai_suggest_from_have(self):
        have = self.have_box.text().strip()
        if not have:
            dialog = CustomDialog("Input Needed", "Please enter some ingredients you have.", "warning", parent=self); dialog.exec()
            return
        titles = ", ".join([r['title'] for r in self._recipes[:30]]); prompt = (f"User has: {have}.\nRecipes available: {titles}.\nSuggest 3 matches or 2 new creative ideas. Be concise."); system = "You are a helpful cooking assistant."; reply = chat_reply(system, prompt)
        dialog = CustomDialog("AI Suggestions", reply, "info", parent=self); dialog.exec()

    def _load_pantry(self):
        self.pantry_edit.setPlainText("\n".join(db.get_pantry()))

    def _save_pantry(self):
        raw = [line.strip().title() for line in self.pantry_edit.toPlainText().splitlines() if line.strip()]
        db.set_pantry(raw)
        dialog = CustomDialog("Saved", f"Saved {len(raw)} pantry items.", "success", parent=self); dialog.exec()
        self._load_pantry()

    def _init_grocery_tab(self):
        page = QWidget(); layout = QVBoxLayout(page); input_layout = QHBoxLayout(); self.grocery_input = QLineEdit(); self.grocery_input.setPlaceholderText("Enter a grocery item"); self.add_grocery_btn = QPushButton("Add to List"); self.add_grocery_btn.clicked.connect(self._add_grocery_item); add_icon = QIcon(str(PROJECT_ROOT / "icons/plus-circle.svg")); self.add_grocery_btn.setIcon(add_icon); self.add_grocery_btn.setIconSize(QSize(18, 18)); input_layout.addWidget(self.grocery_input); input_layout.addWidget(self.add_grocery_btn)
        self.grocery_list_widget = QListWidget(); self.grocery_list_widget.setSelectionMode(QListWidget.ExtendedSelection); btns = QHBoxLayout(); self.remove_grocery_btn = QPushButton("Remove Selected"); self.clear_grocery_btn = QPushButton("Clear All"); self.copy_grocery_btn = QPushButton("Copy to Clipboard"); remove_icon = QIcon(str(PROJECT_ROOT / "icons/trash-2.svg")); self.remove_grocery_btn.setIcon(remove_icon); self.remove_grocery_btn.setIconSize(QSize(18, 18)); clear_icon = QIcon(str(PROJECT_ROOT / "icons/x-circle.svg")); self.clear_grocery_btn.setIcon(clear_icon); self.clear_grocery_btn.setIconSize(QSize(18, 18)); copy_icon = QIcon(str(PROJECT_ROOT / "icons/copy.svg")); self.copy_grocery_btn.setIcon(copy_icon); self.copy_grocery_btn.setIconSize(QSize(18, 18)); self.remove_grocery_btn.clicked.connect(self._remove_grocery_item); self.clear_grocery_btn.clicked.connect(self._clear_grocery); self.copy_grocery_btn.clicked.connect(self._copy_grocery); btns.addWidget(self.remove_grocery_btn); btns.addWidget(self.clear_grocery_btn); btns.addWidget(self.copy_grocery_btn)
        layout.addLayout(input_layout); layout.addWidget(QLabel("Grocery List")); layout.addWidget(self.grocery_list_widget, 1); layout.addLayout(btns); self.tabs.addTab(page, "Grocery"); self._load_grocery()
    
    def _load_grocery(self):
        self.grocery_list_widget.clear(); self.grocery_list_widget.addItems(db.get_grocery())

    def _clear_grocery(self):
        db.set_grocery([]); self._load_grocery()

    def _copy_grocery(self):
        items = [self.grocery_list_widget.item(i).text() for i in range(self.grocery_list_widget.count())]
        QApplication.clipboard().setText("\n".join(items))
        dialog = CustomDialog("Copied", "Grocery list copied to clipboard.", "success", parent=self); dialog.exec()

    def _add_grocery_item(self):
        item_name = self.grocery_input.text().strip().title()
        if item_name:
            db.add_grocery_item(item_name)
            self._load_grocery()
            self.grocery_input.clear()

    def _remove_grocery_item(self):
        selected_items = self.grocery_list_widget.selectedItems()
        if not selected_items: return
        for item in selected_items: db.remove_grocery_item(item.text())
        self._load_grocery()
    
    def _init_assistant_tab(self):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(15, 15, 15, 15); self.assistant_reply = QTextEdit(); self.assistant_reply.setReadOnly(True); self.assistant_reply.setObjectName("assistant_reply_box"); self.assistant_reply.setPlaceholderText("Ask the AI for a recipe, technique, or substitution...\n\nThe response will appear here."); input_layout = QHBoxLayout(); self.assistant_input = QLineEdit(); self.assistant_input.setPlaceholderText("Ask a question..."); self.assistant_input.setObjectName("assistant_input_bar"); self.assistant_input.returnPressed.connect(self._ask_ai); self.assistant_send_btn = QPushButton(""); self.assistant_send_btn.setObjectName("assistant_send_btn"); send_icon = QIcon(str(PROJECT_ROOT / "icons/send.svg")); self.assistant_send_btn.setIcon(send_icon); self.assistant_send_btn.setIconSize(QSize(24, 24)); self.assistant_send_btn.clicked.connect(self._ask_ai); input_layout.addWidget(self.assistant_input); input_layout.addWidget(self.assistant_send_btn); layout.addWidget(self.assistant_reply, 1); layout.addLayout(input_layout); self.tabs.addTab(page, "Assistant")

    def _ask_ai(self):
        question = self.assistant_input.text().strip()
        if not question: return
        self.assistant_reply.setHtml("<i>Asking AI, please wait...</i>"); QApplication.processEvents()
        system = "You are a friendly, expert home-cooking assistant. Use markdown for formatting, like **bold text** for titles, and lists."
        try:
            ans_markdown = chat_reply(system, question)
            ans_html = markdown.markdown(ans_markdown, extensions=['fenced_code', 'tables'])
            self.assistant_reply.setHtml(ans_html)
        except Exception as e:
            self.assistant_reply.setHtml(f"<b>Error:</b><br>{e}")
        self.assistant_input.clear()