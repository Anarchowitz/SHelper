import sys, os, json, webbrowser, requests, datetime, threading
from PIL import Image
from openai import OpenAI
from collections import defaultdict
from datetime import datetime, timedelta
from PySide6.QtWidgets import QAbstractItemView,QScrollArea ,QSpacerItem ,QVBoxLayout ,QSizePolicy ,QLabel, QTableView,QTextEdit ,QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QListView, QPushButton, QWidget, QMessageBox, QHBoxLayout
from PySide6.QtCore import QStringListModel, Qt, QSize,Signal, Slot, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QShortcut, QKeySequence
from info import Ui_InfoWindow
from ai import Ui_AiWindow
from memo import Ui_MemoWindow
from homework import Ui_HMWindow
#shit imports

bug_button_active = False
first_name = 'Пользователь'
last_name = ''

def get_documents_path():
    if os.name == 'nt':  # Windows
        documents_path = os.path.join(os.environ['USERPROFILE'], 'Documents')
    return documents_path
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SchoolHelper")
        icon = QIcon()
        icon.addFile("C:/Users/user/Downloads/вариантиконки1-_1_.ico", QSize(), QIcon.Normal, QIcon.Off) # type: ignore
        self.setWindowIcon(icon)
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
        self.ui.label_2.setText(
            """<html><head/><body>
            <p align="center"><span style=" font-size:20pt; font-weight:700;">🌟 Добро пожаловать в School Helper! 🌟</span></p>
            <p><br/></p>
            <p><span style=" font-size:12pt;">Уважаемые ученики и преподаватели! Мы рады представить вам наше новое десктоп-приложение, созданное специально для школьников 9-11 классов. School Helper станет вашим незаменимым спутником в учёбе, предоставляя возможность удобно хранить памятки по всем предметам, быстро находить информацию о домашних заданиях и общаться с нейросетью, которая всегда готова прийти на помощь!</span></p>
            <p><span style=" font-size:12pt;">С School Helper вы сможете:</span></p>
            <p><span style=" font-size:12pt;">📚 Легко ориентироваться в учебном материале;</span></p>
            <p><span style=" font-size:12pt;">📝 Быстро находить информацию по домашним заданиям;</span></p>
            <p><span style=" font-size:12pt;">💬 Общаться с нейросетью для получения ответов на любые вопросы.</span></p>
            <p>Присоединяйтесь к нам и сделайте учёбу проще и увлекательнее! Вместе мы можем больше! 💪✨</p>
            </body></html>"""
        )
        self.ui.aiButton.clicked.connect(self.show_ai_window)
        self.ui.memoButton.clicked.connect(self.show_memo_window)
        self.ui.homeworkButton.clicked.connect(self.show_hm_window)
        self.ui.bugButton.clicked.connect(self.toggle_bug_button)

    def show_memo_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.memo_window)

    def show_ai_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.ai_window)
    
    def show_hm_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.hm_window)
    def toggle_bug_button(self):
        global bug_button_active
        bug_button_active = not bug_button_active
        if bug_button_active:
            self.ui.bugButton.setStyleSheet("background-color: green;")
            QMessageBox.information(self, "Режим разработчика", "Режим разработчика включен.")
        else:
            self.ui.bugButton.setStyleSheet("background-color: red;")
            QMessageBox.information(self, "Режим разработчика", "Режим разработчика выключен.")


class AiWindow(QMainWindow):
    ai_response_signal = Signal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_AiWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.setAcceptRichText(False)
        self.message_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(400) 
        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.message_layout)
        self.ui.textBrowser.setLayout(QVBoxLayout())
        self.ui.textBrowser.layout().addWidget(self.scroll_area)

        self.ui.infoButton.clicked.connect(self.show_info_window)
        self.ui.memoButton.clicked.connect(self.show_memo_window)
        self.ui.homeworkButton.clicked.connect(self.show_hm_window)
        self.ui.sendButton.clicked.connect(self.send_message)

        self.shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut.activated.connect(self.ui.sendButton.click)
        self.ai_response_signal.connect(self.display_ai_response)

    def show_info_window(self): 
        main_app.stacked_widget.setCurrentWidget(main_app.info_window)

    def show_memo_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.memo_window)

    def show_hm_window(self):
        main_app.stacked_widget.setCurrentWidget(main_app.hm_window)

    def send_message(self):
        user_message = self.ui.textEdit.toPlainText()
        self.display_message(user_message)
        self.ui.textEdit.clear()
        self.display_message("Думаю над ответом", is_ai=True)
        self.thinking_message_container = self.message_layout.itemAt(self.message_layout.count() - 1).widget()
        self.thinking_message = self.thinking_message_container.findChild(QTextEdit)
        self.thinking_message.setText("Думаю над ответом") # type: ignore
        self.thinking_dots = 0
        self.thinking_timer = QTimer()
        self.thinking_timer.timeout.connect(self.update_thinking_dots)
        self.thinking_timer.start(300)  # 500 миллисекунд = 0,5 секунды
        threading.Thread(target=self.get_ai_response_async, args=(user_message,)).start()

    def update_thinking_dots(self):
        self.thinking_dots += 1
        if self.thinking_dots == 1:
            self.thinking_message.setText("Думаю над ответом") # type: ignore
        elif self.thinking_dots > 1:
            dots = "." * (self.thinking_dots - 1)
            self.thinking_message.setText("Думаю над ответом" + dots) # type: ignore
        if self.thinking_dots > 3:
            self.thinking_dots = 0

    def get_ai_response_async(self, user_message):
        ai_response = self.get_ai_response(user_message)
        self.ai_response_signal.emit(ai_response)
        self.thinking_timer.stop()

    @Slot(str)
    def display_ai_response(self, ai_response):
        self.message_layout.removeWidget(self.thinking_message_container)
        self.thinking_message_container.deleteLater()
        self.display_message(ai_response, is_ai=True)

    def get_ai_response(self, user_message):
        api_key = "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"  # внутри скобок свой апи ключ отсюда https://openrouter.ai/settings/keys
        model = "deepseek/deepseek-r1"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": user_message}],
            "stream": True
        }

        with requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            stream=True
        ) as response:
            if response.status_code != 200:
                print("Ошибка API:", response.status_code)
                return ""

            full_response = []

            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode('utf-8').replace('data: ', '')
                    try:
                        chunk_json = json.loads(chunk_str)
                        if "choices" in chunk_json:
                            content = chunk_json["choices"][0]["delta"].get("content", "")
                            if content:
                                cleaned = content.replace('<think>', '').replace('</think>', '')
                                full_response.append(cleaned)
                    except:
                        pass

            return ''.join(full_response)
        

    def display_message(self, message, is_ai=False):
        message_container = QWidget()
        message_container.setMinimumHeight(100)
        message_layout = QVBoxLayout(message_container)
        message_layout.setContentsMargins(0, 0, 0, 0)
        sender_time_label = QLabel()
        if is_ai:
            sender_time_label.setText("Умный друг - " + datetime.now().strftime("%H:%M"))
        else:
            sender_time_label.setText(f"{first_name} {last_name} - " + datetime.now().strftime("%H:%M"))
        sender_time_label.setStyleSheet("font-size: 12px; color: #666666;")
        message_layout.addWidget(sender_time_label, alignment=Qt.AlignLeft if is_ai else Qt.AlignRight) # type: ignore
        message_text = QTextEdit()
        message_text.setReadOnly(True)
        message_text.setText(message)
        if is_ai:
            message_text.setStyleSheet("background-color: #212121; color: white; border-radius: 10px; padding: 5px;")
        else:
            message_text.setStyleSheet("background-color: #8593fe; color: white; border-radius: 10px; padding: 5px;")
        message_layout.addWidget(message_text)
        self.message_layout.addWidget(message_container, alignment=Qt.AlignTop | (Qt.AlignLeft if is_ai else Qt.AlignRight)) # type: ignore
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        QApplication.processEvents()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        message_text.setFixedWidth(400)
        message_text.setFixedHeight(message_text.document().size().height() + 20) # type: ignore
        message_container.setFixedWidth(420)
        message_container.setFixedHeight(message_text.height() + 20)


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
        #темы
        self.algebra_functions = {
            #11класс
            "Триногометрия": self.algebra_trigonometrya11,
            "Комплексные числа": self.algebra_chisla11,
            "Интегралы": self.algebra_integral11,
            "Бином Ньютона": self.algebra_binomnewton11,
            #10класс
            "Показатель степени": self.algebra_stepeni10,
            "Показательные неравенства": self.algebra_neravenstva10,
            "Логарифмы": self.algebra_logarythm10,
            "Тригонометрические выражения и уравнения": self.algebra_trigonometry10,
            "Производная функция": self.algebra_prouzvodnaya10,
            #9класс
            "Квадратные уравнения": self.algebra_kvadrat9,
            "Графики функций": self.algebra_grafiki9,
            "Разложение квадратного трехчлена на множители": self.algebra_trexchlen9,
            "Свойства корней": self.algebra_korni9,
            "Свойства степеней": self.algebra_stepeni9,
        }
        self.geometry_functions = {
            #11класс
            "Объёмы тел": self.geometry_obemtel11,
            "Метод координат в пространстве": self.geometry_coords11,
            "Тела вращения": self.geometry_tela11,
            #10класс
            "Прямые и плоскости в пространстве. Параллельность прямых и плоскостей": self.geometry_prostranstvo10,
            "Перпендикулярность прямых и плоскостей": self.geometry_perpedikularonst10,
            "Углы между прямыми и плоскостями": self.geometry_mnogogran10,
            "Многогранники/Объемы многогранников": self.geometry_mnogogran10,
            #9класс
            "Теорема Пифагора": self.geometry_pifagor9,
            "Площади фигур": self.geometry_ploshadi9,
            "Теорема синусов/косинусов/Герона": self.geometry_teoremi9,   
            "Свойства треугольников": self.geometry_svoystva9,
        }
        self.statistica_functions = {
            #11класс
            #повторяет 10 - нету ничего нового
            #10класс
            "Случайные опыты и случайные события, опыты с равновозможными элементарными исходами": self.statistica_opiti10,
            "Операции над событиями, сложение вероятностей": self.statistica_operations10,
            "Элементы комбинаторики": self.statistica_combinatorika10,
            "Серии последовательных испытаний/Бернулли": self.statistica_bernulli10,
            "Случайные величины и распределения": self.statistica_raspredelenie10,
            #9класс
            "Формула вероятности": self.statistica_formula9,
            "Игральная кость": self.statistica_kybik9,
            "Теория вероятностей": self.statistica_veroyatnost9,
        }
        topics = ["Назад", "", "Механические колебания и волны", "Молекулярная физика", "Законы постоянного тока", "Электромагнитная индукция"]
        self.physics_functions = {
            #11класс
            "Механические колебания и волны": self.physics_kolebanya11,
            "Молекулярная физика": self.physics_molekylar11,
            "Законы постоянного тока": self.physics_postoyanitok11,
            "Электромагнитная индукция": self.physics_induction11,
            #10класс
            "Кинематика": self.physics_cinematic10,
            "Динамика": self.physics_dinamic10,
            "Статика твёрдого тела": self.physics_tverdoetelo10,
            "Законы сохранения в механике": self.physics_soxranenie10,
            "Электрическое поле": self.physics_electropole10,
            "Постоянный электрический ток": self.physics_tok10,
            #9класс
            "Законы Ньютона": self.physics_newton9,
            "Движения тела": self.physics_telo9,
            "Механическая работа": self.physics_energy9,
            "Световые явления": self.physics_svet9,
            "Электромагнитное поле и электромагнитные волны": self.physics_elektro9,
        }

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
            return
        if self.selected_class == "11 класс":            
            if selected_subject == "Алгебра":
                self.algebra_list11()
            elif selected_subject == "Геометрия":
                self.geometry_list11()
            elif selected_subject == "Физика":
                self.physics_list11()
            elif selected_subject == "Вероятность и статистика":
                self.statistica_list11()
        elif self.selected_class == "10 класс":
            if selected_subject == "Алгебра":
                self.algebra_list10()
            elif selected_subject == "Геометрия":
                self.geometry_list10()
            elif selected_subject == "Физика":
                self.physics_list10()
            elif selected_subject == "Вероятность и статистика":
                self.statistica_list10()
        elif self.selected_class == "9 класс":            
            if selected_subject == "Алгебра":
                self.algebra_list9()
            elif selected_subject == "Геометрия":
                self.geometry_list9()
            elif selected_subject == "Физика":
                self.physics_list9()
            elif selected_subject == "Теория Вероятности":
                self.statistica_list9()
        else:
            if not selected_subject:
                return
            else:
                QMessageBox.warning(self, "Ошибка", "Выбранный предмет недоступен для данного класса.")
    #11класслагебра
    def algebra_list11(self):
        topics = ["Назад", "", "Триногометрия", "Комплексные числа", "Интегралы", "Бином Ньютона"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.algebra_theme11)

    def algebra_theme11(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.algebra_functions[selected_topic]()

    def algebra_trigonometrya11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra11', '1.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_chisla11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra11', '2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_integral11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra11', '3.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_binomnewton11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra11', '4.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    #10классалгебра
    def algebra_list10(self):
        topics = ["Назад", "", "Показатель степени", "Показательные неравенства", "Логарифмы", "Тригонометрические выражения и уравнения", "Производная функция"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.algebra_theme10)

    def algebra_theme10(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.algebra_functions[selected_topic]()

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
    #9классалгебра
    def algebra_list9(self):
        topics = ["Назад", "", "Квадратные уравнения", "Графики функций", "Разложение квадратного трехчлена на множители", "Свойства корней", "Свойства степеней"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.algebra_theme10)

    def algebra_theme9(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.algebra_functions[selected_topic]()

    def algebra_kvadrat9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra9', 'kvadrat.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_grafiki9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra9', 'grafiki.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_trexchlen9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra9', 'trexchlen.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_korni9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra9', 'korni.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def algebra_stepeni9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'algebra9', 'stepeni.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    
    #11классгеометрия
    def geometry_list11(self):
        topics = ["Назад", "", "Объёмы тел", "Метод координат в пространстве", "Тела вращения"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.geometry_theme11)

    def geometry_theme11(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.geometry_functions[selected_topic]()

    def geometry_obemtel11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry11', '1.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_coords11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry11', '2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_tela11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry11', '3.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    #10классгеометрия
    def geometry_list10(self):
        topics = ["Назад", "", "Прямые и плоскости в пространстве. Параллельность прямых и плоскостей", "Перпендикулярность прямых и плоскостей", "Углы между прямыми и плоскостями", "Многогранники/Объемы многогранников"]
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
        else:
            self.geometry_functions[selected_topic]()


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
    #9классгеометрия
    def geometry_list9(self):
        topics = ["Назад", "", "Теорема Пифагора", "Площади фигур", "Теорема синусов/косинусов/Герона", "Свойства треугольников"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.geometry_theme10)

    def geometry_theme9(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.geometry_functions[selected_topic]()

    def geometry_pifagor9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry9', 'pifagor.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_teoremi9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry9', 'teoremi.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_ploshadi9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry9', 'ploshadi.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def geometry_svoystva9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'geometry9', 'svoystva.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    
    #11класстервер
    def statistica_list11(self):
        topics = ["Назад", "", "Случайные опыты и случайные события, опыты с равновозможными элементарными исходами", "Операции над событиями, сложение вероятностей", "Элементы комбинаторики", "Серии последовательных испытаний/Бернулли", "Случайные величины и распределения"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.statistica_theme11)

    def statistica_theme11(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.statistica_functions[selected_topic]()

    #10класстервер
    def statistica_list10(self):
        topics = ["Назад", "", "Случайные опыты и случайные события, опыты с равновозможными элементарными исходами", "Операции над событиями, сложение вероятностей", "Элементы комбинаторики", "Серии последовательных испытаний/Бернулли", "Случайные величины и распределения"]
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
        else:
            self.statistica_functions[selected_topic]()
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
    #9класстервер
    def statistica_list9(self):
        topics = ["Назад", "", "Формула вероятности", "Игральная кость", "Теория вероятностей"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.statistica_theme10)

    def statistica_theme9(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.statistica_functions[selected_topic]()

    def statistica_formula9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica9', '123.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def statistica_kybik9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica9', 'kybik.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def statistica_veroyatnost9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'statistica9', 'veroyatnost2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    #11классфизика
    def physics_list11(self):
        topics = ["Назад", "", "Механические колебания и волны", "Молекулярная физика", "Законы постоянного тока", "Электромагнитная индукция"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.physics_theme11)

    def physics_theme11(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.physics_functions[selected_topic]()

    def physics_kolebanya11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics11', '1.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_molekylar11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics11', '2.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_postoyanitok11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics11', '3.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_induction11(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics11', '4.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    #10классфизика
    def physics_list10(self):
        topics = ["Назад", "", "Кинематика", "Динамика", "Статика твёрдого тела", "Законы сохранения в механике", "Электрическое поле", "Постоянный электрический ток"]
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
        else:
            self.physics_functions[selected_topic]()

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
    #9классфизика
    def physics_list9(self):
        topics = ["Назад", "", "Законы Ньютона", "Движения тела", "Механическая работа", "Световые явления", "Электромагнитное поле и электромагнитные волны"]
        self.subject_model.setStringList(topics)
        self.ui.listView.setModel(self.subject_model)
        self.ui.listView.clearSelection()

        self.ui.listView.clicked.disconnect()
        self.ui.listView.clicked.connect(self.physics_theme10)

    def physics_theme9(self, index):
        selected_topic = index.data()
        if selected_topic == "Назад":
            self.ui.listView.setModel(self.class_model)
            self.ui.listView.clearSelection()
            self.ui.listView.clicked.disconnect()
            self.ui.listView.clicked.connect(self.on_class_selected)
        else:
            self.physics_functions[selected_topic]()

    def physics_newton9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics9', 'newton.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_telo9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics9', 'telo.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_energy9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics9', 'energy.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_svet9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics9', 'svet.png')
        try:
            img = Image.open(image_path)
            img.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден: {image_path}")
            print(f"Файл не найден: {image_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")
            print(f"Произошла ошибка: {e}")
    def physics_elektro9(self):
        current_path = os.getcwd()
        image_path = os.path.join(current_path, 'SHelper', 'memos', 'physics9', 'elektro1.png')
        image_path2 = os.path.join(current_path, 'SHelper', 'memos', 'physics9', 'elektro2.png')
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
        documents_path = get_documents_path()
        settings_path = os.path.join(documents_path, 'SchoolHelper', 'SchoolHelper_settings.json')
        if not os.path.exists(settings_path):
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                json.dump({}, f)

        try:
            with open(settings_path, 'r') as f:
                self.settings = json.load(f)
                self.token_mesh = self.settings.get('token_mesh', '')
                self.ui.lineEdit.setText(self.token_mesh)
        except Exception as e:
            self.token_mesh = ''
            self.settings = {}

    def save_token(self):
        token = self.ui.lineEdit.text()
        settings = {'token_mesh': token}
        documents_path = get_documents_path()
        settings_path = os.path.join(documents_path, 'SchoolHelper', 'SchoolHelper_settings.json')
        settings_dir = os.path.dirname(settings_path)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        with open(settings_path, 'w') as f:
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
            if 'profile' in data2 and 'id' in data2['profile']:
                student_id = data2['profile']['id']
                print(f"Student-ID: {student_id}")
                global first_name, last_name
                first_name = data2['profile']['first_name']
                last_name = data2['profile']['last_name']
                print(first_name+' '+last_name)
                self.student_id  = student_id
            else:
                if bug_button_active:
                    QMessageBox.information(self, "Режим разработчика", "Student-ID не найден.")
        elif response.status_code == 401:
            self.reset_token()  # Сброс токена при ошибке 401
        else:
            if bug_button_active:
                QMessageBox.information(self, "Режим разработчика", f"Error: {response.status_code} - {response.text}")
    
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
        elif response.status_code == 401:
            self.reset_token()
        else:
            if bug_button_active:
                QMessageBox.information(self, "Режим разработчика", f"Error: {response.status_code} - {response.text}")
    def reset_token(self):
        self.token_mesh = ''
        self.settings['token_mesh'] = ''
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
        QMessageBox.warning(self, "School Helper", "Токен авторизации устарел. Пожалуйста, введите новый токен.")
        self.update_visibility()
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