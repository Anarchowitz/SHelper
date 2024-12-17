import sys, os, json, webbrowser, requests
from PIL import Image

from openai import OpenAI

from collections import defaultdict
from datetime import datetime, timedelta

from PySide6.QtWidgets import QAbstractItemView,QScrollArea ,QSpacerItem ,QVBoxLayout ,QSizePolicy ,QLabel, QTableView,QTextEdit ,QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QListView, QPushButton, QWidget, QMessageBox
from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem

from info import Ui_InfoWindow
from ai import Ui_AiWindow
from memo import Ui_MemoWindow
from homework import Ui_HMWindow
# https://school.mos.ru/?backUrl=https%3A%2F%2Fschool.mos.ru%2Fv2%2Ftoken%2Frefresh

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SchoolHelper / Debug")
        self.stacked_widget = QStackedWidget()
        
        
        self.info_window = InfoWindow()
        self.ai_window = AiWindow()
        self.memo_window = MemoWindow()
        self.hm_window = HMWindow()

        self.stacked_widget.addWidget(self.info_window)
        self.stacked_widget.addWidget(self.ai_window)
        self.stacked_widget.addWidget(self.memo_window)
        self.stacked_widget.addWidget(self.hm_window)
        self.hm_window.update_visibility()

        self.setCentralWidget(self.stacked_widget)


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InfoWindow()
        self.hm_window = HMWindow()
        self.ui.setupUi(self)
        self.ui.aiButton.clicked.connect(self.show_ai_window)
        self.ui.memoButton.clicked.connect(self.show_memo_window)
        self.ui.homeworkButton.clicked.connect(self.show_hm_window)

    def show_memo_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.memo_window)

    def show_ai_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.ai_window)
    
    def show_hm_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.hm_window)


class AiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AiWindow()
        self.ui.setupUi(self)
        self.ui.infoButton.clicked.connect(self.show_info_window)
        self.ui.memoButton.clicked.connect(self.show_memo_window)
        self.ui.homeworkButton.clicked.connect(self.show_hm_window)

        # Создаем новый виджет для сообщений и устанавливаем его в scrollArea
        self.message_widget = QWidget()
        self.message_layout = QVBoxLayout(self.message_widget)
        self.ui.scrollArea.setWidget(self.message_widget)
        self.ui.scrollArea.setWidgetResizable(True)

        self.ui.sendButton.clicked.connect(self.send_message)

    def show_info_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.info_window)

    def show_memo_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.memo_window)

    def show_hm_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.hm_window)

    def send_message(self): 
        user_message = self.ui.textEdit.toPlainText() 
        if user_message: 
            self.display_message(user_message, is_user=True) 
            self.ui.textEdit.clear() 
            self.scroll_to_bottom()  # Прокручиваем вниз
            self.ai_message(user_message)

    def ai_message(self, user_message): 
        client = OpenAI( 
            api_key="sk-aitunnel-jJbl5JiPBgCygbIwCRpUFnK3PP0VHe8M", 
            base_url="https://api.aitunnel.ru/v1/", 
        ) 
        completion = client.chat.completions.create( 
            messages=[{"role": "user", "content": f"{user_message}"}], 
            max_tokens=1025, 
            model="gpt-4o-mini" 
        ) 
        end_message = completion.choices[0].message.content 
        print("[AI ANSWER] ->", end_message) 
        self.display_message(end_message, is_user=False) 
        self.scroll_to_bottom()  # Прокручиваем вниз

    def display_message(self, message, is_user): 
        # Добавляем префикс в зависимости от того, кто отправляет сообщение
        if is_user:
            message = "Пользователь: " + message
        else:
            message = "Нейросеть: " + message

        # Создаем метку для сообщения без стилей
        message_label = QLabel(message) 
        message_label.setWordWrap(True)  # Позволяем перенос текста 

        # Убираем стили и фон
        message_label.setStyleSheet("") 

        # Добавляем метку в layout
        self.message_layout.addWidget(message_label)  
        self.scroll_to_bottom()  # Прокручиваем вниз


    def scroll_to_bottom(self):
        self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())

class MemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MemoWindow()
        self.ui.setupUi(self)
        self.ui.listView.setStyleSheet("""
    QListView {
        color: #8593fe;          /* Цвет текста */  /* Цвет границы */
    }
    QListView::item {
        padding: 10px;               /* Отступы для элементов */
    }
    QListView::item:selected {
        background-color: #9785ff;   /* Цвет фона для выделенного элемента */
        color: white;                 /* Цвет текста для выделенного элемента */
        border:3px;
	    border-radius:10px;
    }
""")
        self.hm_window = HMWindow()
        self.ui.infoButton.clicked.connect(self.show_info_window)
        self.ui.aiButton.clicked.connect(self.show_ai_window)
        self.ui.homeworkButton.clicked.connect(self.show_hm_window)

        self.class_model = self.create_class_model()
        self.ui.listView.setModel(self.class_model)

        self.subject_model = QStringListModel()

        self.ui.listView.clicked.connect(self.on_class_selected)
        self.selected_class = None

    def create_class_model(self):
        classes = ["11 класс", "10 класс", "9 класс"]
        return QStringListModel(classes)

    def on_class_selected(self, index):
        self.selected_class = index.data()
        print(f"Выбранный класс: {self.selected_class}")

        subjects = []

        if self.selected_class == "11 класс":
            subjects = ["Назад", "", "Алгебра", "Геометрия", "Физика", "Вероятность и статистика"]
        elif self.selected_class == "10 класс":
            subjects = ["Назад", "", "Алгебра", "Геометрия", "Физика", "Вероятность и статистика"]
        elif self.selected_class == "9 класс":
            subjects = ["Назад", "", "Алгебра", "Геометрия", "Физика", "Теория Вероятности"]

        self.subject_model.setStringList(subjects)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.on_subject_selected)

    def on_subject_selected(self, index):
        selected_subject = index.data()

        print(f"Выбранный предмет: {selected_subject}, Класс: {self.selected_class}")

        if selected_subject == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        elif selected_subject == "Алгебра" and self.selected_class == "10 класс":
            print("Открытие тем по алгебре")
            self.algebra_list10()
        elif selected_subject == "Геометрия":
            self.geometry_list10()
        elif selected_subject == "Вероятность и статистика":
            self.statistica_list10()
        elif selected_subject == "Физика":
            self.physics_list10()
        else:
            if not selected_subject:
                return
            else:
                QMessageBox.warning(self, "Ошибка", "Выбранный предмет недоступен для данного класса.")

    def algebra_list10(self):
        topics = ["Назад","", "Показатель степени", "Показательные неравенства", "Логарифмы", "Тригонометрические выражения и уравнения", "Производная функция"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.algebra_theme10)

    def algebra_theme10(self, index):
        selected_topic = index.data()
        if not selected_topic:  
            return
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        elif selected_topic == "Показатель степени":
            self.algebra_stepeni10()
        elif selected_topic == "Показательные неравенства":
            self.algebra_neravenstva10()
        elif selected_topic == "Логарифмы":
            self.algebra_logarythm10()
        elif selected_topic == "Тригонометрические выражения и уравнения":
            self.algebra_trigonometry10()
        elif selected_topic == "Производная функция":
            self.algebra_prouzvodnaya10()
        else:
            QMessageBox.information(self, "Выбранная тема", f"Вы выбрали тему: {selected_topic}")

    def algebra_stepeni10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra10', 'stepeni.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_neravenstva10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra10', 'neravenstva.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_logarythm10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra10', 'logarythm.jpg')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_trigonometry10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra10', 'trigonometry.jpg')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_prouzvodnaya10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra10', 'prouzvodnaya.png')
        image_path2 = os.path.join(current_path, 'SHelper', 'memos', 'algebra10', 'prouzvodnaya2.png')
        try:
            img = Image.open(image_path)
            img2 = Image.open(image_path2)
            img.show()
            img2.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_list10(self):
        topics = ["Назад","", "Прямые и плоскости в пространстве. Параллельность прямых и плоскостей", "Перпендикулярность прямых и плоскостей", "Углы между прямыми и плоскостями", "Многогранники/Объемы многогранников"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.geometry_theme10)

    def geometry_theme10(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        elif selected_topic == "Прямые и плоскости в пространстве. Параллельность прямых и плоскостей":
            self.geometry_prostranstvo10()
        elif selected_topic == "Перпендикулярность прямых и плоскостей":
            self.geometry_perpedikularonst10()
        elif selected_topic == "Тригонометрические выражения и уравнения":
            self.algebra_trigonometry10()
        elif selected_topic == "Углы между прямыми и плоскостями":
            self.algebra_prouzvodnaya10()
        elif selected_topic == "Многогранники/Объемы многогранников":
            self.geometry_mnogogran10()
        else:
            QMessageBox.information(self, "Выбранная тема", f"Вы выбрали тему: {selected_topic}")
    def geometry_perpedikularonst10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry10', '1.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_prostranstvo10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry10', '2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_mnogogran10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry10', '3.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")

    def statistica_list10(self):
        topics = ["Назад","", "Случайные опыты и случайные события, опыты с равновозможными элементарными исходами", "Операции над событиями, сложение вероятностей", "Элементы комбинаторики", "Серии последовательных испытаний/Бернулли", "Случайные величины и распределения"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.statistica_theme10)

    def statistica_theme10(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        elif selected_topic == "Случайные опыты и случайные события, опыты с равновозможными элементарными исходами":
            self.statistica_opiti10(    )
        elif selected_topic == "Операции над событиями, сложение вероятностей":
            self.statistica_operations10()
        elif selected_topic == "Элементы комбинаторики":
            self.statistica_combinatorika10()
        elif selected_topic == "Серии последовательных испытаний/Бернулли":
            self.statistica_bernulli10()
        elif selected_topic == "Случайные величины и распределения":
            self.statistica_raspredelenie10()
        else:
            QMessageBox.information(self, "Выбранная тема", f"Вы выбрали тему: {selected_topic}")
    def statistica_opiti10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica10', '1.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def statistica_operations10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica10', '2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def statistica_combinatorika10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica10', '3.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def statistica_bernulli10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica10', '4.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def statistica_raspredelenie10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica10', '5.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_list10(self):
        topics = ["Назад","", "Кинематика", "Динамика", "Статика твёрдого тела", "Законы сохранения в механике", "Электрическое поле", "Постоянный электрический ток"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.physics_theme10)

    def physics_theme10(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        elif selected_topic == "Кинематика":
            self.physics_cinematic10()
        elif selected_topic == "Динамика":
            self.physics_dinamic10()
        elif selected_topic == "Статика твёрдого тела":
            self.physics_tverdoetelo10()
        elif selected_topic == "Законы сохранения в механике":
            self.physics_soxranenie10()
        elif selected_topic == "Электрическое поле":
            self.physics_electropole10()
        elif selected_topic == "Постоянный электрический ток":
            self.physics_tok10()
        else:
            QMessageBox.information(self, "Выбранная тема", f"Вы выбрали тему: {selected_topic}")

    def physics_cinematic10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics10', '1.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_dinamic10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics10', '2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_tverdoetelo10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics10', '3.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_soxranenie10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics10', '4.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_electropole10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics10', '5.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_tok10(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics10', '6.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")


    def show_info_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.info_window)
    def show_ai_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.ai_window)
    def show_hm_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.hm_window)



class HMWindow(QMainWindow, Ui_HMWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HMWindow()
        self.ui.setupUi(self)
        self.student_id = None
        
        self.homeworks_by_date = defaultdict(list)
        self.current_date = datetime.now()


        self.ui.nextweekButton.clicked.connect(self.next_week)
        self.ui.lastweekButton.clicked.connect(self.last_week)

        self.ui.saveButton.clicked.connect(self.save_token)
        self.ui.tokenButton.clicked.connect(self.token_button)
        self.ui.updateButton.clicked.connect(self.update_table)
        
        self.ui.memoButton.clicked.connect(self.show_memo_window)
        self.ui.infoButton.clicked.connect(self.show_info_window)
        self.ui.aiButton.clicked.connect(self.show_ai_window)


    def next_week(self):
        self.current_date += timedelta(days=7)
        self.homeworkcheck()
        self.populate_table()
    def last_week(self):
        self.current_date -= timedelta(days=7)
        self.homeworkcheck()
        self.populate_table()
    def token_button(self):
        webbrowser.open('https://school.mos.ru/?backUrl=https%3A%2F%2Fschool.mos.ru%2Fv2%2Ftoken%2Frefresh')
    def load_settings(self):
        print("Загрузка настроек...")
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w') as f:
                json.dump({}, f)

        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
                self.token_mesh = self.settings.get('token_mesh', '')
                self.ui.lineEdit.setText(self.token_mesh)
        except Exception as e:
            self.token_mesh = ''
            self.settings = {}

    def save_token(self):
        token = self.ui.lineEdit.text()
        settings = {'token_mesh': token}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        if token == '':
            QMessageBox.warning(self, "School Helper", "Значение не может быть пустым!")
        else:
            QMessageBox.information(self, "School Helper", "Токен успешно сохранен!")
        self.update_visibility()

    def update_visibility(self):
        print("Обновление видимости...")
        self.load_settings()
        if self.token_mesh.startswith("eyJhbG"):
            self.ui.label_2.setVisible(False)
            self.ui.lineEdit.setVisible(False)
            self.ui.tokenButton.setVisible(False)
            self.ui.saveButton.setVisible(False)
            self.ui.updateButton.setVisible(True)
            self.ui.tableView.setVisible(True)
            self.ui.lastweekButton.setVisible(True)
            self.ui.nextweekButton.setVisible(True)
            self.ui.label_3.setVisible(True)
            self.profilecheck()
            self.homeworkcheck()
            self.populate_table()
        else:
            self.ui.label_2.setVisible(True)
            self.ui.lineEdit.setVisible(True)
            self.ui.tokenButton.setVisible(True)
            self.ui.saveButton.setVisible(True)
            self.ui.updateButton.setVisible(False)
            self.ui.tableView.setVisible(False)
            self.ui.lastweekButton.setVisible(False)
            self.ui.nextweekButton.setVisible(False)
            self.ui.label_3.setVisible(False)

    def update_table(self):
        self.homeworks_by_date.clear()
        self.homeworkcheck()
        self.populate_table()
        
    def profilecheck(self):
        url = "https://school.mos.ru/api/family/mobile/v1/profile"
        headers = {
            "x-mes-subsystem": "familymp",
            "Authorization": f"Bearer {self.token_mesh}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data2 = response.json()
            #print(data2)
            if 'profile' in data2 and 'id' in data2['profile']:
                student_id = data2['profile']['id']
                print(f"Student-ID: {student_id}")
                self.student_id  = student_id
            else:
                print("Student-ID не найден.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    def homeworkcheck(self):
        today = self.current_date
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        start_date_str = start_of_week.strftime('%Y-%m-%d')
        end_date_str = end_of_week.strftime('%Y-%m-%d')
        self.ui.label_3.setText(f'<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">c {start_date_str} \u043f\u043e {end_date_str}</span></p></body></html>')

        url = f"https://school.mos.ru/api/family/web/v1/homeworks?from={start_date_str}&to={end_date_str}&student_id={self.student_id}"
        headers = {
            "x-mes-subsystem": "familyweb",
            "Authorization": f"Bearer {self.token_mesh}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            self.homeworks_by_date.clear()
            for homework in data['payload']:
                date_str = homework['date']
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                self.homeworks_by_date[date].append(homework)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def populate_table(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["День недели", "Предмет", "Задание"])
        days_of_week = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье"
        }
        sorted_dates = sorted(self.homeworks_by_date.keys())

        if not sorted_dates:
            model.appendRow([QStandardItem("Нет домашних заданий на эту неделю")])
        else:
            for date in sorted_dates:
                day_of_week_number = date.weekday()  # 0 = понедельник, 6 = воскресенье
                day_of_week = days_of_week[day_of_week_number]
                has_homework = False

                for homework in self.homeworks_by_date[date]:
                    if homework['homework'].strip() and homework['homework'] != ". ":
                        has_homework = True
                        homework_text = homework['homework']
                        row = [
                            QStandardItem(day_of_week),
                            QStandardItem(homework['subject_name']),
                            QStandardItem(homework_text),
                        ]
                        model.appendRow(row)

                if not has_homework and date == sorted_dates[-1]:
                    model.appendRow([QStandardItem("Нет домашних заданий на эту неделю")])

        self.ui.tableView.setModel(model)
        self.ui.tableView.setWordWrap(True)
        self.ui.tableView.resizeColumnsToContents()


    def show_info_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.info_window)
    def show_ai_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.ai_window)
    def show_memo_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.memo_window)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())