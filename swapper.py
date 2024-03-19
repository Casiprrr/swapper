import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QGroupBox, QHBoxLayout, QTextEdit, QScrollArea, QCheckBox, QMainWindow, QDesktopWidget, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5 import QtWidgets
import fitz  # PyMuPDF

def insert_text(page, elements, font_size=12, color=(0, 0, 0)):  # Setze Farbe auf Schwarz
    font_size = font_size * 0.75  # Convert from points to pixels
    for (x, y, text) in elements:
        page.insert_text((x, y), text, fontsize=font_size, color=color)  # Setze die Schriftfarbe explizit

def insert_text_into_pdf(pdf_file, output_file, data):
    input_dir = "input"
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_file_path = os.path.join(input_dir, pdf_file)
    output_file = os.path.join(output_dir, output_file)
    
    doc = fitz.open(input_file_path)
    for key in data:
        if isinstance(data[key], list):  # Check if the value is a list
            for entry in data[key]:
                page_num = entry['page_num']
                if page_num <= len(doc):
                    page = doc[page_num - 1]
                    insert_text(page, [(entry['x'], entry['y'], entry['value'])])
        else:
            page_num = data[key]['page_num']
            if page_num <= len(doc):
                page = doc[page_num - 1]
                insert_text(page, [(data[key]['x'], data[key]['y'], data[key]['value'])])
    doc.save(output_file)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weaning-Anträge generieren")
        self.setGeometry(100, 100, 600, 400)

        self.application_form = ApplicationForm()
        self.setCentralWidget(self.application_form)

    def fillFormWithTestData(self):
        self.application_form.fillWithTestData()

    def submitForm(self):
        self.application_form.submitForm()

    def showEvent(self, event):
        super().showEvent(event)

        # Bestimme die verfügbare Größe des Bildschirms
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Setze die Fenstergröße als Prozentsatz der Bildschirmgröße
        window_width = int(screen_width * 1.0)  
        window_height = int(screen_height * 1.0) 
        self.resize(window_width, window_height)

        
class ApplicationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('self')
        # Scrollbereich erstellen
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area.setWidget(scroll_area_widget)
        
        # Layout für den Scrollbereich erstellen
        layout = QVBoxLayout()

        checkboxes_layout = QHBoxLayout()

        # Erste Reihe
        row1_layout = QVBoxLayout()
        self.checkbox_clemens = QCheckBox('Münster Clemenshospital')
        row1_layout.addWidget(self.checkbox_clemens)
        self.checkbox_ibbenbueren = QCheckBox('Ibbenbüren Klinikum Ibbenbüren')
        row1_layout.addWidget(self.checkbox_ibbenbueren)
        self.checkbox_dortmund_luenen = QCheckBox('Dortmund-Lünen Weaning Zentrum Klinikum Westfalen')
        row1_layout.addWidget(self.checkbox_dortmund_luenen)
        self.checkbox_dortmund = QCheckBox('Dortmund Klinikum Dortmund')
        row1_layout.addWidget(self.checkbox_dortmund)
        checkboxes_layout.addLayout(row1_layout)

        # Zweite Reihe
        row2_layout = QVBoxLayout()
        self.checkbox_vest = QCheckBox('Marl Weaning Zentrum Vest')
        row2_layout.addWidget(self.checkbox_vest)
        self.checkbox_haltern = QCheckBox('Haltern St. Sixtus Hospital')
        row2_layout.addWidget(self.checkbox_haltern)
        self.checkbox_soest = QCheckBox('Soest Marienkrankenhaus')
        row2_layout.addWidget(self.checkbox_soest)
        self.checkbox_bielefeld = QCheckBox('Bielefeld Ev. Krankenhaus Bethel')
        row2_layout.addWidget(self.checkbox_bielefeld)
        checkboxes_layout.addLayout(row2_layout)

        # Dritte Reihe
        row3_layout = QVBoxLayout()
        self.checkbox_schmallenberg = QCheckBox('Schmallenberg Fachkrankenhaus Kloster Grafschaft')
        row3_layout.addWidget(self.checkbox_schmallenberg)
        self.checkbox_hemer = QCheckBox('Hemer Weaningzentrum an der Lungenklinik')
        row3_layout.addWidget(self.checkbox_hemer)
        self.checkbox_essen = QCheckBox('Essen Weaning Zentrum Ev. Kliniken Mitte')
        row3_layout.addWidget(self.checkbox_essen)
        checkboxes_layout.addLayout(row3_layout)


        # Vierte Reihe
        row4_layout = QVBoxLayout()
        self.checkbox_koeln = QCheckBox('Köln Lungenklinik Nord St. Marien')
        row4_layout.addWidget(self.checkbox_koeln)
        self.checkbox_bad_lippspringe = QCheckBox('Bad Lippspringe Karl-Hansen-Klinik')
        row4_layout.addWidget(self.checkbox_bad_lippspringe)
        self.checkbox_oldenburg = QCheckBox('Oldenburg Pius-Hospital')
        row4_layout.addWidget(self.checkbox_oldenburg)
        checkboxes_layout.addLayout(row4_layout)

        layout.addLayout(checkboxes_layout)


        for checkbox in [self.checkbox_clemens, self.checkbox_ibbenbueren,
                          self.checkbox_dortmund_luenen, self.checkbox_dortmund, 
                          self.checkbox_vest, self.checkbox_haltern, self.checkbox_soest, 
                          self.checkbox_bielefeld, self.checkbox_schmallenberg, self.checkbox_hemer, 
                          self.checkbox_essen, self.checkbox_koeln, self.checkbox_bad_lippspringe, self.checkbox_oldenburg]:
            checkbox.stateChanged.connect(self.updateBoxVisibility)
            checkbox.stateChanged.connect(self.updateLaborValuesVisibility)
            checkbox.stateChanged.connect(self.toggle_ct_wert)
            checkbox.stateChanged.connect(self.toggle_c19_verdacht)



        # Button für Testdaten
        testdaten_layout = QHBoxLayout()

        self.test_button = QPushButton('Testdaten')
        self.test_button.setStyleSheet("background-color: orange")  # Hintergrundfarbe auf rot setzen
        self.test_button.clicked.connect(self.fillWithTestData)  # Verknüpfen Sie den Klick mit der Methode fillWithTestData
        self.test_button.clicked.connect(self.submitForm)  # Verknüpfen Sie den Klick mit der Methode submitForm

        self.test_button2 = QPushButton('Testdaten basic')
        self.test_button2.setStyleSheet("color: white; background-color: blue")  # Hintergrundfarbe auf blau setzen
        self.test_button2.clicked.connect(self.fillWithTestDataBasic)
        self.test_button2.clicked.connect(self.submitForm)
        
        self.clearall_button = QPushButton('Alles zurücksezten')
        self.clearall_button.setStyleSheet("color: white; background-color: red")  # Hintergrundfarbe auf rot setzen
        self.clearall_button.clicked.connect(self.clearAll)

        self.makeAllVisible_button = QPushButton('Alle sichtbar')
        self.makeAllVisible_button.setStyleSheet("color: white; background-color: green")  # Hintergrundfarbe auf grün setzen
        self.makeAllVisible_button.setFixedWidth(100)
        self.makeAllVisible_button.clicked.connect(self.makeAllVisible)

        testdaten_layout.addWidget(self.test_button)
        testdaten_layout.addWidget(self.test_button2)
        testdaten_layout.addWidget(self.clearall_button)
        testdaten_layout.addWidget(self.makeAllVisible_button)
        layout.addLayout(testdaten_layout)
        
        self.statdoc_layout = QHBoxLayout()
        self.station_label =QLabel('Station:')
        self.station_combo = QComboBox()
        self.station_combo.addItems(['Station 22', 'Station 19'])
        self.statdoc_layout.addWidget(self.station_label)
        self.statdoc_layout.addWidget(self.station_combo)
        
        self.doctor_label = QLabel('Stationsärztin / -arzt:')
        self.doctor_input = QLineEdit()
        self.statdoc_layout.addWidget(self.doctor_label)
        self.statdoc_layout.addWidget(self.doctor_input)

        self.stat_time_gruppe = QGroupBox('')
        self.stat_time_gruppe.setVisible(False)
        self.stat_time_layout = QHBoxLayout()
        self.stat_time_label = QLabel('Auf der Station seit')
        self.stat_time_input = QLineEdit()
        self.stat_time_input.setPlaceholderText('TT.MM.JJJJ')
        self.stat_time_input.setFixedWidth(100)
        self.kh_time_label = QLabel('Im Krankenhaus seit')
        self.kh_time_input = QLineEdit()
        self.kh_time_input.setPlaceholderText('TT.MM.JJJJ')
        self.kh_time_input.setFixedWidth(100)
        self_kh_dg_label = QLabel('Aufnahmediagnose Krankenhaus:')
        self.kh_dg_input = QLineEdit()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.stat_time_gruppe.setLayout(self.stat_time_layout)
        self.stat_time_layout.addWidget(self.stat_time_label)
        self.stat_time_layout.addWidget(self.stat_time_input)
        self.stat_time_layout.addWidget(self.kh_time_label)
        self.stat_time_layout.addWidget(self.kh_time_input)
        self.stat_time_layout.addWidget(self_kh_dg_label)
        self.stat_time_layout.addWidget(self.kh_dg_input)
        self.stat_time_layout.addItem(spacer)
        

        
        layout.addLayout(self.statdoc_layout)
        layout.addWidget(self.stat_time_gruppe)

        #Dicke Überschriften
        font = QFont()
        font.setBold(True)
        


        # Kasten für Patientendaten
        patient_data_box = QGroupBox('Patientendaten')
        patient_data_box.setFont(font)
        patient_data_layout = QVBoxLayout()
        patient_data_box.setStyleSheet("QGroupBox { background-color: rgb(255, 255, 220); }")

        # Name
        name_layout = QHBoxLayout()
        self.lastname_label = QLabel('Nachname:')
        self.lastname_input = QLineEdit()
        name_layout.addWidget(self.lastname_label)
        name_layout.addWidget(self.lastname_input)
        self.firstname_label = QLabel('Vorname:')
        self.firstname_input = QLineEdit()
        name_layout.addWidget(self.firstname_label)
        name_layout.addWidget(self.firstname_input)
        patient_data_layout.addLayout(name_layout)

        # Geb.-Datum und Geschlecht
        birth_gender_layout = QHBoxLayout()

        self.gender_label = QLabel('Geschlecht:')
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(['männlich', 'weiblich'])
        self.gender_combo.setCurrentIndex(-1)
        birth_gender_layout.addWidget(self.gender_label)
        birth_gender_layout.addWidget(self.gender_combo)
        patient_data_layout.addLayout(birth_gender_layout)
        self.gender_label.setVisible(False)
        self.gender_combo.setVisible(False)

        self.birthdate_label = QLabel('Geburtsdatum:')
        self.birthdate_input = QLineEdit()
        birthdate_validator = QIntValidator(10000000, 99999999)
        self.birthdate_input.setValidator(birthdate_validator)
        self.birthdate_input.setPlaceholderText('TT.MM.JJJJ')
        birth_gender_layout.addWidget(self.birthdate_label)
        birth_gender_layout.addWidget(self.birthdate_input)

        self.age_label = QLabel('Alter:')
        self.age_input = QLineEdit()
        self.age_input.setReadOnly(True)  # Das Alter wird automatisch berechnet und das Feld ist schreibgeschützt
        self.age_input.setVisible(False)
        self.age_label.setVisible(False)
        birth_gender_layout.addWidget(self.age_label)
        birth_gender_layout.addWidget(self.age_input)


        # Verbindung des Textänderungs-Signals des Geburtsdatum-Eingabefelds mit der Funktion zur Berechnung des Alters
        self.birthdate_input.textChanged.connect(self.update_age_and_gfr)
        self.gender_combo.currentIndexChanged.connect(self.update_gfr)

        # Größe und Gewicht
        height_weight_layout = QHBoxLayout()
        self.height_label = QLabel('Größe (cm):')
        self.height_input = QLineEdit()
        height_weight_layout.addWidget(self.height_label)
        height_weight_layout.addWidget(self.height_input)
        self.weight_label = QLabel('Gewicht (kg):')
        self.weight_input = QLineEdit()
        height_weight_layout.addWidget(self.weight_label)
        height_weight_layout.addWidget(self.weight_input)
        patient_data_layout.addLayout(height_weight_layout)

        self.height_input.textChanged.connect(self.updateAdipositasText)
        self.weight_input.textChanged.connect(self.updateAdipositasText)

        # Adresse
        address_layout = QHBoxLayout()
        self.street_label = QLabel('Straße + Hausnummer:')
        self.street_input = QLineEdit()
        address_layout.addWidget(self.street_label)
        address_layout.addWidget(self.street_input)
        self.plz_label = QLabel('PLZ:')
        self.plz_input = QLineEdit()
        address_layout.addWidget(self.plz_label)
        address_layout.addWidget(self.plz_input)
        self.city_label = QLabel('Wohnort:')
        self.city_input = QLineEdit()
        address_layout.addWidget(self.city_label)
        address_layout.addWidget(self.city_input)
        patient_data_layout.addLayout(address_layout)
        self.street_label.setVisible(False)
        self.street_input.setVisible(False)
        self.plz_label.setVisible(False)
        self.plz_input.setVisible(False)
        self.city_label.setVisible(False)
        self.city_input.setVisible(False)

        # Hausarzt und Angehöriger
        gp_kin_layout = QHBoxLayout()
        self.next_of_kin_label = QLabel('Nächster Angehöriger:')
        self.next_of_kin_input = QLineEdit()
        gp_kin_layout.addWidget(self.next_of_kin_label)
        gp_kin_layout.addWidget(self.next_of_kin_input)
        self.next_of_kin_tel_label = QLabel('Telefonnummer:')
        self.next_of_kin_tel_input = QLineEdit()
        gp_kin_layout.addWidget(self.next_of_kin_tel_label)
        gp_kin_layout.addWidget(self.next_of_kin_tel_input)
        self.general_practitioner_label = QLabel('Hausarzt:')
        self.general_practitioner_input = QLineEdit()
        gp_kin_layout.addWidget(self.general_practitioner_label)
        gp_kin_layout.addWidget(self.general_practitioner_input)
        self.general_practitioner_label.setVisible(False)
        self.general_practitioner_input.setVisible(False)
        self.next_of_kin_tel_label.setVisible(False)
        self.next_of_kin_tel_input.setVisible(False)
        self.next_of_kin_label.setVisible(False)
        self.next_of_kin_input.setVisible(False)
        patient_data_layout.addLayout(gp_kin_layout)
        self.next_of_kin_input.textChanged.connect(self.update_betreuung_name_label)

        # Beruf und Versicherung
        job_insurance_layout = QHBoxLayout()
        self.insurance_label = QLabel('Krankenkasse:')
        self.insurance_input = QLineEdit()
        job_insurance_layout.addWidget(self.insurance_label)
        job_insurance_layout.addWidget(self.insurance_input)
        self.job_label = QLabel('Beruf:')
        self.job_input = QLineEdit()
        job_insurance_layout.addWidget(self.job_label)
        job_insurance_layout.addWidget(self.job_input)
        patient_data_layout.addLayout(job_insurance_layout)
        self.job_input.setVisible(False)
        self.job_label.setVisible(False)
        self.insurance_input.setVisible(False)
        self.insurance_label.setVisible(False)

        # Vollmacht
        self.vollmacht_gruppe = QGroupBox('Vollmacht / Verfügung')
        vollmacht_layout = QVBoxLayout()

        vollmacht_layout_line1 = QHBoxLayout()
        self.betreuung_label = QLabel('Betreuung eingerichtet?')
        self.betreuung_label.setFixedWidth(220)
        self.betreuung_combo = QComboBox()
        self.betreuung_combo.addItems(['ja', 'nein'])
        self.betreuung_combo.setCurrentIndex(-1)
            
        vollmacht_layout_line11 = QHBoxLayout()
        vollmacht_layout_line11.setContentsMargins(20, 0, 0, 0)
        self.betreuung_name_label = QLabel('')  # Wird später dynamisch gesetzt
        self.betreuung_name_label.setFixedWidth(300)
        self.betreuung_name_combo = QComboBox()
        self.betreuung_name_combo.addItems(['ja', 'nein'])
        self.betreuung_name_combo.setCurrentIndex(0)

        vollmacht_layout_line12 = QHBoxLayout()
        vollmacht_layout_line12.setContentsMargins(60, 0, 0, 0)
        self.betreuung_name2_label = QLabel('Name des Betreuers:')
        self.betreuung_name2_input = QLineEdit()
        self.betreuung_name2_input.setPlaceholderText('Name')
        self.betreuung_name2_tel_label = QLabel('Telefonnummer des Betreuers:')
        self.betreuung_name2_tel_input = QLineEdit()
        self.betreuung_name2_tel_input.setPlaceholderText('Nummer')

        self.betreuung_name_label.setVisible(False)
        self.betreuung_name_combo.setVisible(False)
        self.betreuung_name2_label.setVisible(False)
        self.betreuung_name2_input.setVisible(False)
        self.betreuung_name2_tel_label.setVisible(False)
        self.betreuung_name2_tel_input.setVisible(False)

        vollmacht_layout_line2 = QHBoxLayout()
        self.vorsorgevollmacht_label = QLabel('Vorsorgevollmacht vorhanden?')
        self.vorsorgevollmacht_label.setFixedWidth(220)
        self.vorsorgevollmacht_combo = QComboBox()
        self.vorsorgevollmacht_combo.addItems(['ja', 'nein'])
        self.vorsorgevollmacht_combo.setCurrentIndex(-1)
        vollmacht_layout_line3 = QHBoxLayout()
        self.verfuegung_label = QLabel('Patientenverfügung vorhanden?')
        self.verfuegung_label.setFixedWidth(220)
        self.verfuegung_combo = QComboBox()
        self.verfuegung_combo.addItems(['ja', 'nein'])
        self.verfuegung_combo.setCurrentIndex(-1)
        vollmacht_layout_line4 = QHBoxLayout()
        self.versorgungzuhause_label = QLabel('Versorgung zu Hause:')
        self.versorgungzuhause_label.setFixedWidth(220)
        self.versorgungzuhause_combo = QComboBox()
        self.versorgungzuhause_combo.addItems(['selbständig', 'durch Angehörige' , 'durch Pflegedienst' , 'nicht möglich'])
        self.versorgungzuhause_combo.setCurrentIndex(-1)

        vollmacht_layout.addLayout(vollmacht_layout_line1)
        vollmacht_layout_line1.addWidget(self.betreuung_label)
        vollmacht_layout_line1.addWidget(self.betreuung_combo)
        vollmacht_layout.addLayout(vollmacht_layout_line11)
        vollmacht_layout_line11.addWidget(self.betreuung_name_label)
        vollmacht_layout_line11.addWidget(self.betreuung_name_combo)
        vollmacht_layout.addLayout(vollmacht_layout_line12)
        vollmacht_layout_line12.addWidget(self.betreuung_name2_label)
        vollmacht_layout_line12.addWidget(self.betreuung_name2_input)
        vollmacht_layout_line12.addWidget(self.betreuung_name2_tel_label)
        vollmacht_layout_line12.addWidget(self.betreuung_name2_tel_input)
        vollmacht_layout.addLayout(vollmacht_layout_line2)
        vollmacht_layout_line2.addWidget(self.vorsorgevollmacht_label)
        vollmacht_layout_line2.addWidget(self.vorsorgevollmacht_combo)
        vollmacht_layout.addLayout(vollmacht_layout_line3)
        vollmacht_layout_line3.addWidget(self.verfuegung_label)
        vollmacht_layout_line3.addWidget(self.verfuegung_combo)
        vollmacht_layout.addLayout(vollmacht_layout_line4)
        vollmacht_layout_line4.addWidget(self.versorgungzuhause_label)
        vollmacht_layout_line4.addWidget(self.versorgungzuhause_combo)
        
        self.vollmacht_gruppe.setLayout(vollmacht_layout)
        patient_data_layout.addWidget(self.vollmacht_gruppe)

        self.vollmacht_gruppe.setVisible(False)
        self.betreuung_combo.currentTextChanged.connect(self.toggle_betreuung)
        self.betreuung_name_combo.currentTextChanged.connect(self.toggle_betreuung)


        #Allgemeinzustand vor Akuterkrankung
        self.az_gruppe = QGroupBox('Allgemeinzustand vor Akuterkrankung')
        az_layout = QHBoxLayout()
        self.az_label = QLabel('Selbständigkeitsgrad:')
        self.az_label.setFixedWidth(220)
        self.az_combo = QComboBox()
        self.az_combo.addItems(['selbständig', 'geringe Einschränkung ohne Hilfebedürftigkeit', 'geringe Einschränkung mit Hilfebedürftigkeit', 'Hilfe notwendig beim Ankleiden und Essen' , 'komplett hilfebedürftig'])
        self.az_combo.setCurrentIndex(-1)

        az_layout.addWidget(self.az_label)
        az_layout.addWidget(self.az_combo)

        self.az_gruppe.setLayout(az_layout)
        patient_data_layout.addWidget(self.az_gruppe)

        self.az_gruppe.setVisible(False)

        patient_data_box.setLayout(patient_data_layout)
        layout.addWidget(patient_data_box)

        # Kasten für Atemweg
        atemwegbox_box = QGroupBox('Atemweg')
        atemwegbox_box.setFont(font)
        atemwegbox_layout = QVBoxLayout()
        atemwegbox_box.setStyleSheet("QGroupBox { background-color: rgb(255, 220, 220); }")

        airway_dg_layout = QHBoxLayout()
        self.airway_dg_label = QLabel('Diagnose, die zur Beatmung führte:')
        self.airway_dg_input = QLineEdit()
        self.atemweg_label = QLabel('Atemweg:')
        self.atemweg_combo = QComboBox()
        self.atemweg_combo.addItems(['Tubus', 'Trachealkanüle'])
        self.atemweg_combo.setCurrentIndex(1)
        airway_dg_layout.addWidget(self.atemweg_label)
        airway_dg_layout.addWidget(self.atemweg_combo)
        airway_dg_layout.addWidget(self.airway_dg_label)
        airway_dg_layout.addWidget(self.airway_dg_input)
        atemwegbox_layout.addLayout(airway_dg_layout)
        self.atemweg_combo.currentTextChanged.connect(self.toggle_trachealkanule)

        itn_layout = QHBoxLayout()
        self.airway_date_label = QLabel('Datum der Intubation:')
        self.airway_date_input = QLineEdit()
        self.airway_date_input.setPlaceholderText('TT.MM.JJJJ')
        self.airway_days_label = QLabel('Tage seit Intubation:')
        self.airway_days_label.setVisible(False)
        self.airway_days_text = QLabel()
        self.airway_days_input = QLineEdit()
        self.airway_days_input.setReadOnly(True)
        self.airway_days_input.setVisible(False)
        itn_layout.addWidget(self.airway_date_label)
        itn_layout.addWidget(self.airway_date_input)
        itn_layout.addWidget(self.airway_days_label)
        itn_layout.addWidget(self.airway_days_text)
        itn_layout.addWidget(self.airway_days_input)

        atemwegbox_layout.addLayout(itn_layout)
        
        tk_layout = QHBoxLayout()
        self.tk_date_label = QLabel('Datum der Tracheotomie:')
        self.tk_date_input = QLineEdit()
        self.tk_date_input.setPlaceholderText('TT.MM.JJJJ')
        self.tk_days_label = QLabel('Tage seit Trachealkanüle:')
        self.tk_days_label.setVisible(False)
        self.tk_days_text = QLabel()
        self.tk_days_input = QLineEdit()
        self.tk_days_input.setReadOnly(True)
        self.tk_days_input.setVisible(False)
        tk_layout.addWidget(self.tk_date_label)
        tk_layout.addWidget(self.tk_date_input)
        tk_layout.addWidget(self.tk_days_label)
        tk_layout.addWidget(self.tk_days_text)
        tk_layout.addWidget(self.tk_days_input)

        atemwegbox_layout.addLayout(tk_layout)

        self.airway_date_input.textChanged.connect(lambda: self.updateDays(self.airway_date_input, self.airway_days_input))
        self.tk_date_input.textChanged.connect(lambda: self.updateDays(self.tk_date_input, self.tk_days_input))
        self.airway_days_input.textChanged.connect(self.update_airway_days_text)
        self.tk_days_input.textChanged.connect(self.update_tk_days_text)

        # Setzen Sie das Atemweg-Layout im Kasten
        atemwegbox_box.setLayout(atemwegbox_layout)
        layout.addWidget(atemwegbox_box)

        # Kasten für Weaning
        self.weaning_box = QGroupBox('Weaning')
        self.weaning_box.setFont(font)
        self.weaning_box.setVisible(False)
        weaning_layout = QVBoxLayout()
        self.weaning_box.setStyleSheet("QGroupBox { background-color: rgb(220, 255, 220); }")

        ext_versuche_layout = QHBoxLayout()
        self.ext_versuche_label = QLabel('Anzahl der Extubationsversuche:')
        self.ext_versuche_input = QLineEdit()
        self.ext_versuche_wann_label = QLabel('Wann durchgeführt?')
        self.ext_versuche_wann_input = QLineEdit()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ext_versuche_label.setVisible(False)
        self.ext_versuche_input.setVisible(False)
        self.ext_versuche_wann_label.setVisible(False)
        self.ext_versuche_wann_input.setVisible(False)
        self.ext_versuche_input.textChanged.connect(self.update_Reintub)

        re_intubationen_layout = QHBoxLayout()
        self.re_intub_label = QLabel('Anzahl Re-Intubationen')
        self.re_intub_input = QLineEdit()
        self.re_intub_input.setFixedWidth(50)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.re_intub_label.setVisible(False)
        self.re_intub_input.setVisible(False)

        weaning_method_layout = QHBoxLayout()
        self.weaning_method_label = QLabel('Angewandte Weaning-Methode:')
        self.weaning_method_input = QLineEdit()
        self.scheitern_label = QLabel('Vermuteter Grund des Scheiterns:')
        self.scheitern_input = QLineEdit()
        self.weaning_method_label.setVisible(False)
        self.weaning_method_input.setVisible(False)

        beatmungs_dauer_layout = QHBoxLayout()
        self.beatmung_maschinell_label = QLabel('maschinell')
        self.beatmung_maschinell_input = QLineEdit()
        self.beatmung_maschinell_einheit_label = QLabel('h/Tag')
        self.beatmung_spontan_label = QLabel('spontan')
        self.beatmung_spontan_input = QLineEdit()
        self.beatmung_spontan_einheit_label = QLabel('h/Tag')
        self.beatmung_maschinell_label.setVisible(False)
        self.beatmung_maschinell_input.setVisible(False)

        motivation_stimmung_layout = QHBoxLayout()
        motivation_stimmung_layout.setAlignment(Qt.AlignLeft)
        self.motivation_label = QLabel('Motivation des Patienten:')
        self.motivation_combo = QComboBox()
        self.motivation_combo.addItems(['sehr gut' , 'gut' , 'weniger gut' , 'gar nicht'])
        self.motivation_combo.setCurrentIndex(-1)
        self.stimmung_label = QLabel('Stimmung des Patienten')
        self.stimmung_combo = QComboBox()
        self.stimmung_combo.addItems(['euphorisch' , 'adäquat' , 'weinerlich' , 'depressiv'])
        self.stimmung_combo.setCurrentIndex(-1)
        self.motivation_label.setVisible(False)
        self.motivation_combo.setVisible(False)
        self.stimmung_label.setVisible(False)
        self.stimmung_combo.setVisible(False)

        ext_versuche_layout.addWidget(self.ext_versuche_label)
        ext_versuche_layout.addWidget(self.ext_versuche_input)
        ext_versuche_layout.addWidget(self.ext_versuche_wann_label)
        ext_versuche_layout.addWidget(self.ext_versuche_wann_input)
        ext_versuche_layout.addItem(spacer)

        re_intubationen_layout.addWidget(self.re_intub_label)
        re_intubationen_layout.addWidget(self.re_intub_input)
        re_intubationen_layout.addItem(spacer)

        weaning_method_layout.addWidget(self.weaning_method_label)
        weaning_method_layout.addWidget(self.weaning_method_input)
        weaning_method_layout.addWidget(self.scheitern_label)
        weaning_method_layout.addWidget(self.scheitern_input)

        beatmungs_dauer_layout.addWidget(self.beatmung_maschinell_label)
        beatmungs_dauer_layout.addWidget(self.beatmung_maschinell_input)
        beatmungs_dauer_layout.addWidget(self.beatmung_maschinell_einheit_label)
        beatmungs_dauer_layout.addWidget(self.beatmung_spontan_label)
        beatmungs_dauer_layout.addWidget(self.beatmung_spontan_input)
        beatmungs_dauer_layout.addWidget(self.beatmung_spontan_einheit_label)

        motivation_stimmung_layout.addWidget(self.motivation_label)
        motivation_stimmung_layout.addWidget(self.motivation_combo)
        motivation_stimmung_layout.addWidget(self.stimmung_label)
        motivation_stimmung_layout.addWidget(self.stimmung_combo)
        
        weaning_layout.addLayout(ext_versuche_layout)
        weaning_layout.addLayout(re_intubationen_layout)
        weaning_layout.addLayout(weaning_method_layout)
        weaning_layout.addLayout(beatmungs_dauer_layout)
        weaning_layout.addLayout(motivation_stimmung_layout)

        self.weaning_box.setLayout(weaning_layout)
        layout.addWidget(self.weaning_box)

        #Aktueller Zustand des Patienten
        self.current_state_box = QGroupBox('Aktueller Zustand des Patienten')
        self.current_state_box.setFont(font)
        self.current_state_box.setVisible(False)
        current_state_layout = QVBoxLayout()
        self.current_state_box.setStyleSheet("QGroupBox { background-color: rgb(220, 220, 255); }")

        consciousness_pflegebeduerftigkeit_layout = QHBoxLayout()
        consciousness_pflegebeduerftigkeit_layout.setAlignment(Qt.AlignLeft)

        self.consciousness_label = QLabel('Bewusstseinszustand:')
        self.consciousness_combo = QComboBox()
        self.consciousness_combo.addItems(['wach + voll orientiert', 'kooperativ, orientiert, ruhig' , 'schläft, leicht erweckbar' , 'Reaktion auf lautes Ansprechen' , 'komatöser Pat. ohne Reaktionen' , 'Delir'])
        self.consciousness_combo.setCurrentIndex(-1)
        self.consciousness_label.setVisible(False)
        self.consciousness_combo.setVisible(False)

        self.pflegebeduerftigkeit_label = QLabel('Pflegebedürftigkeit:')
        self.pflegebeduerftigkeit_combo = QComboBox()
        self.pflegebeduerftigkeit_combo.addItems(['voll' , 'teils' , 'gering'])
        self.pflegebeduerftigkeit_combo.setCurrentIndex(-1)
        self.pflegebeduerftigkeit_label.setVisible(False)
        self.pflegebeduerftigkeit_combo.setVisible(False)

        self.mobilisation_label = QLabel('Mobilisation:')
        self.mobilisation_combo = QComboBox()
        self.mobilisation_combo.addItems(['keine Mobilisation' , 'Bettkante' , 'Stand/Gehen'])
        self.mobilisation_combo.setCurrentIndex(-1)
        self.mobilisation_label.setVisible(False)

        darminkontinenz_layout = QHBoxLayout()
        darminkontinenz_layout.setAlignment(Qt.AlignLeft)
        self.darminkontinenz_label = QLabel('Darminkontinenz:')
        self.darminkontinenz_combo = QComboBox()
        self.darminkontinenz_combo.addItems(['ja' , 'nein'])
        self.darminkontinenz_combo.setCurrentIndex(0)
        self.darminkontinenz_label.setVisible(False)
        self.darminkontinenz_combo.setVisible(False)

        dekubitus_gruppe = QWidget()
        dekubitus_layout = QHBoxLayout()
        dekubitus_layout.setAlignment(Qt.AlignLeft)
        self.dekubitus_label = QLabel('Dekubitus:')
        self.dekubitus_combo = QComboBox()
        self.dekubitus_combo.addItems(['ja' , 'nein'])
        self.dekubitus_combo.setCurrentIndex(-1)
        self.dekubitus_lokalisation_label = QLabel('Lokalisation:')
        self.dekubitus_lokalisation_combo = QComboBox()
        self.dekubitus_lokalisation_combo.addItems(['Sakral' , 'Ferse' , 'Sakral + Ferse' , 'Sonstige'])
        self.dekubitus_lokalisation_combo.setCurrentIndex(-1)
        self.dekubitus_lokalisation_sonstige_input = QLineEdit()
        self.dekubitus_lokalisation_sonstige_input.setPlaceholderText('Sonstige')
        self.dekubitus_lokalisation_sonstige_input.setFixedWidth(200)
        self.dekubitus_grad_label = QLabel('Grad:')
        self.dekubitus_grad_combo = QComboBox()
        self.dekubitus_grad_combo.addItems(['1' , '2' , '3' , '4'])
        self.dekubitus_grad_combo.setCurrentIndex(-1)  

        self.dekubitus_lokalisation_label.setVisible(False)
        self.dekubitus_lokalisation_combo.setVisible(False)
        self.dekubitus_lokalisation_sonstige_input.setVisible(False)
        self.dekubitus_grad_label.setVisible(False)
        self.dekubitus_grad_combo.setVisible(False)

        self.dekubitus_combo.currentTextChanged.connect(self.toggle_dekubitus1)
        self.dekubitus_lokalisation_combo.currentTextChanged.connect(self.toggle_dekubitus2)


        self.vp_gruppe = QGroupBox('Vitalparameter')
        self.vp_gruppe.setVisible(False)
        vp_layout = QHBoxLayout()
        rr_label = QLabel('Blutdruck:')
        self.rr_syst_input = QLineEdit()
        self.rr_syst_input.setFixedWidth(50)
        rr_trennstrich_label = QLabel('/')
        self.rr_diast_input = QLineEdit()
        self.rr_diast_input.setFixedWidth(50)
        rr_einheit_label = QLabel('mmHg')
        hf_label = QLabel('Puls:')
        self.hf_input = QLineEdit()
        self.hf_input.setFixedWidth(50)
        hf_einheit_label = QLabel('Schläge/min')
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        

        consciousness_pflegebeduerftigkeit_layout.addWidget(self.consciousness_label)
        consciousness_pflegebeduerftigkeit_layout.addWidget(self.consciousness_combo)
        consciousness_pflegebeduerftigkeit_layout.addWidget(self.pflegebeduerftigkeit_label)
        consciousness_pflegebeduerftigkeit_layout.addWidget(self.pflegebeduerftigkeit_combo)
        consciousness_pflegebeduerftigkeit_layout.addWidget(self.mobilisation_label)
        consciousness_pflegebeduerftigkeit_layout.addWidget(self.mobilisation_combo)

        darminkontinenz_layout.addWidget(self.darminkontinenz_label)
        darminkontinenz_layout.addWidget(self.darminkontinenz_combo)

        dekubitus_layout.addWidget(self.dekubitus_label)
        dekubitus_layout.addWidget(self.dekubitus_combo)
        dekubitus_layout.addWidget(self.dekubitus_lokalisation_label)
        dekubitus_layout.addWidget(self.dekubitus_lokalisation_combo)
        dekubitus_layout.addWidget(self.dekubitus_lokalisation_sonstige_input)
        dekubitus_layout.addWidget(self.dekubitus_grad_label)
        dekubitus_layout.addWidget(self.dekubitus_grad_combo)
        dekubitus_layout.addItem(spacer)

        self.vp_gruppe.setLayout(vp_layout)
        vp_layout.addWidget(rr_label)
        vp_layout.addWidget(self.rr_syst_input)
        vp_layout.addWidget(rr_trennstrich_label)
        vp_layout.addWidget(self.rr_diast_input)
        vp_layout.addWidget(rr_einheit_label)
        vp_layout.addWidget(hf_label)
        vp_layout.addWidget(self.hf_input)
        vp_layout.addWidget(hf_einheit_label)
        vp_layout.addItem(spacer)

        current_state_layout.addLayout(consciousness_pflegebeduerftigkeit_layout)
        current_state_layout.addLayout(darminkontinenz_layout)
        current_state_layout.addWidget(dekubitus_gruppe)
        dekubitus_gruppe.setLayout(dekubitus_layout)
        current_state_layout.addWidget(self.vp_gruppe)

        self.current_state_box.setLayout(current_state_layout)
        layout.addWidget(self.current_state_box)


        #Katheter-Box
        self.catheter_box = QGroupBox('Zugänge')
        self.catheter_box.setFont(font)
        catheter_layout = QVBoxLayout()
        self.catheter_box.setStyleSheet("QGroupBox { background-color: rgb(220, 255, 255); }")
        self.catheter_box.setVisible(False)


        # Arterie
        artery_layout = QHBoxLayout()
        self.artery_label = QLabel('Arterie:')
        self.artery_combo = QComboBox()
        self.artery_combo.addItems(['Radialis re.', 'Radialis li.', 'Brachialis re.', 'Brachialis li.', 'A. Femoralis re.', 'A. Femoralis li.'])
        self.artery_combo.setCurrentIndex(-1)
        artery_layout.addWidget(self.artery_label)
        artery_layout.addWidget(self.artery_combo)
        artery_layout.addWidget(QLabel('gelegt am:'))
        self.artery_date_input = QLineEdit()    
        self.artery_date_input.setPlaceholderText('TT.MM.JJJJ')
        artery_layout.addWidget(self.artery_date_input)
        self.artery_time_label = QLabel('Tage:')
        self.artery_time_label.setVisible(False)
        self.artery_time_text = QLabel()
        self.artery_time_input = QLineEdit()
        self.artery_time_input.setReadOnly(True)
        self.artery_time_input.setVisible(False)
        artery_layout.addWidget(self.artery_time_label)
        artery_layout.addWidget(self.artery_time_text)
        artery_layout.addWidget(self.artery_time_input)
        catheter_layout.addLayout(artery_layout)

        self.artery_date_input.textChanged.connect(lambda: self.updateDays(self.artery_date_input, self.artery_time_input))
        self.artery_time_input.textChanged.connect(self.update_artery_time_text)

        # ZVK
        cvc_layout = QHBoxLayout()
        self.cvc_label = QLabel('ZVK:')
        self.cvc_combo = QComboBox()
        self.cvc_combo.addItems(['V. jugularis int. re.', 'V. jugularis int. li.', 'V. subclavia re.', 'V. subclavia li.', 'V. femoralis re.', 'V. femoralis li.',])
        self.cvc_combo.setCurrentIndex(-1)
        cvc_layout.addWidget(self.cvc_label)
        cvc_layout.addWidget(self.cvc_combo)
        self.lumen_label = QLabel('Lumen:')
        self.lumen_combo = QComboBox()
        self.lumen_combo.addItems(['1-lumig', '2-lumig', '3-lumig', '4-lumig', '5-lumig'])
        self.lumen_combo.setCurrentIndex(-1)
        cvc_layout.addWidget(self.lumen_label)
        cvc_layout.addWidget(self.lumen_combo)
        cvc_layout.addWidget(QLabel('gelegt am:'))
        self.cvc_date_input = QLineEdit()
        self.cvc_date_input.setPlaceholderText('TT.MM.JJJJ')
        cvc_layout.addWidget(self.cvc_date_input)
        self.cvc_time_label = QLabel('Tage:')
        self.cvc_time_label.setVisible(False)
        self.cvc_time_text = QLabel()
        self.cvc_time_input = QLineEdit()
        self.cvc_time_input.setReadOnly(True)
        self.cvc_time_input.setVisible(False)
        cvc_layout.addWidget(self.cvc_time_label)
        cvc_layout.addWidget(self.cvc_time_text)
        cvc_layout.addWidget(self.cvc_time_input)
        catheter_layout.addLayout(cvc_layout)

        self.cvc_date_input.textChanged.connect(lambda: self.updateDays(self.cvc_date_input, self.cvc_time_input))
        self.cvc_time_input.textChanged.connect(self.update_cvc_time_text)


        # Blasenkatheter
        bladder_layout = QHBoxLayout()
        self.bladder_label = QLabel('Blasenkatheter:')
        self.bladder_combo = QComboBox()
        self.bladder_combo.addItems(['Transurethraler DK', 'Suprapubischer DK'])
        self.bladder_combo.setCurrentIndex(-1)
        bladder_layout.addWidget(self.bladder_label)
        bladder_layout.addWidget(self.bladder_combo)
        bladder_layout.addWidget(QLabel('gelegt am:'))
        self.bladder_date_input = QLineEdit()
        self.bladder_date_input.setPlaceholderText('TT.MM.JJJJ')
        bladder_layout.addWidget(self.bladder_date_input)
        self.bladder_time_label = QLabel('Tage:')
        self.bladder_time_label.setVisible(False)
        self.bladder_time_text = QLabel()
        self.bladder_time_input = QLineEdit()
        self.bladder_time_input.setReadOnly(True)
        self.bladder_time_input.setVisible(False)
        bladder_layout.addWidget(self.bladder_time_label)
        bladder_layout.addWidget(self.bladder_time_text)
        bladder_layout.addWidget(self.bladder_time_input)
        catheter_layout.addLayout(bladder_layout)

        self.bladder_date_input.textChanged.connect(lambda: self.updateDays(self.bladder_date_input, self.bladder_time_input))
        self.bladder_time_input.textChanged.connect(self.update_bladder_time_text)

        #Magensonde
        magensonde_layout = QHBoxLayout()
        self.magensonde_label = QLabel('Magensonde:')
        self.magensonde_combo = QComboBox()
        self.magensonde_combo.addItems(['Nasogastral', 'Nasoduodenal', 'Nasojejunale', 'PEG', 'PEJ'])
        self.magensonde_combo.setCurrentIndex(-1)
        magensonde_layout.addWidget(self.magensonde_label)
        magensonde_layout.addWidget(self.magensonde_combo)
        magensonde_layout.addWidget(QLabel('gelegt am:'))
        self.magensonde_date_input = QLineEdit()
        self.magensonde_date_input.setPlaceholderText('TT.MM.JJJJ')
        magensonde_layout.addWidget(self.magensonde_date_input)
        self.magensonde_time_label = QLabel('Tage:')
        self.magensonde_time_label.setVisible(False)
        self.magensonde_time_text = QLabel()
        self.magensonde_time_input = QLineEdit()
        self.magensonde_time_input.setReadOnly(True)
        self.magensonde_time_input.setVisible(False)
        magensonde_layout.addWidget(self.magensonde_time_label)
        magensonde_layout.addWidget(self.magensonde_time_text)
        magensonde_layout.addWidget(self.magensonde_time_input)
        catheter_layout.addLayout(magensonde_layout)

        self.magensonde_date_input.textChanged.connect(lambda: self.updateDays(self.magensonde_date_input, self.magensonde_time_input))
        self.magensonde_time_input.textChanged.connect(self.update_magensonde_time_text)

        self.catheter_box.setLayout(catheter_layout)
        layout.addWidget(self.catheter_box)    

        # Mibi Box
        self.mibi_box = QGroupBox('Mibi')
        self.mibi_box.setFont(font)
        mibi_layout = QVBoxLayout()
        self.mibi_box.setStyleSheet("QGroupBox { background-color: rgb(255, 220, 255); }")
        self.mibi_box.setVisible(False)
        
        # Aktuelle Antibiose
        self.mibi_label_current = QLabel('Aktuelle Antibiose:')
        self.mibi_input_current = QTextEdit()
        self.mibi_input_current.setAcceptRichText(False)
        mibi_layout.addWidget(self.mibi_label_current)
        mibi_layout.addWidget(self.mibi_input_current)

        # Frühere Antibiose
        self.mibi_label_previous = QLabel('Frühere Antibiose:')
        self.mibi_input_previous = QTextEdit()
        self.mibi_input_previous.setAcceptRichText(False)
        mibi_layout.addWidget(self.mibi_label_previous)
        mibi_layout.addWidget(self.mibi_input_previous)

        # Erreger-Nachweise
        self.erregernachweis_label = QLabel('Erreger-Nachweise:')
        self.erregernachweis_input = QTextEdit()
        self.erregernachweis_input.setAcceptRichText(False)
        mibi_layout.addWidget(self.erregernachweis_label)
        mibi_layout.addWidget(self.erregernachweis_input)

        # (Resistent) Erreger
        self.resistente_erreger_label = QLabel('Resistente Erreger:')
        self.checkbox_vre1 = QCheckBox('VRE rektal')
        self.checkbox_vre2 = QCheckBox('VRE Wunde')
        self.checkbox_mrsa1 = QCheckBox('MRSA Nase')
        self.checkbox_mrsa2 = QCheckBox('MRSA Wunde')
        self.checkbox_3mrgn = QCheckBox('3-MRGN Wunde')
        self.checkbox_4mrgn = QCheckBox('4-MRGN Wunde')
        self.resistente_erreger_textinput = QLineEdit()
        self.resistente_erreger_textinput.setPlaceholderText("Sonstige resistente Erreger")

        self.c19_cdiff_label = QLabel('Typische Erreger')
        self.c19_cdiff_label.setVisible(False)
        self.checkbox_cdiff = QCheckBox('C. difficile / Clostridien')
        self.cdiff_date_input = QLineEdit()
        self.cdiff_date_input.setPlaceholderText('Nachweis am (TT.MM.JJJJ)')
        self.cdiff_date_input.setVisible(False)
        self.c19_status_label = QLabel('Aktueller Status Covid-19')
        self.c19_status_label.setFixedWidth(180)
        self.c19_combo = QComboBox()
        self.c19_combo.addItems(['aktuell negativ', 'aktuell positiv'])
        self.c19_combo.setCurrentIndex(-1)
        self.c19_combo.setPlaceholderText('Bitte auswählen')
        self.c19_verdacht_label = QLabel('Aktuell V.a. Covid-19?')
        self.c19_verdacht_label.setVisible(False)
        self.c19_verdacht_combo = QComboBox()
        self.c19_verdacht_combo.addItems(['nein', 'ja'])
        self.c19_verdacht_combo.setCurrentIndex(-1)
        self.c19_verdacht_combo.setPlaceholderText('Bitte auswählen')
        self.c19_verdacht_combo.setVisible(False)
        self.c19_negtest_date_input = QLineEdit('')
        self.c19_negtest_date_input.setPlaceholderText('Datum des letzten negativen Tests, TT.MM.JJJJ')
        self.c19_negtest_date_input.setVisible(False)
        self.checkbox_znc19 = QCheckBox('Z.n. COVID-19 mit 2 neg. Abstrichen')
        self.checkbox_znc19.setVisible(False)
        self.ctwert_label = QLabel('Ct-Wert:')
        self.ctwert_input = QLineEdit()
        self.ctwert_label.setVisible(False)
        self.ctwert_input.setVisible(False)

        self.checkbox_cdiff.stateChanged.connect(self.toggle_cdiff)



        mibi_layout.addWidget(self.c19_cdiff_label)

        cdiff_layout = QHBoxLayout()
        cdiff_layout.addWidget(self.checkbox_cdiff)
        cdiff_layout.addWidget(self.cdiff_date_input)
        mibi_layout.addLayout(cdiff_layout)

        c19_layout = QVBoxLayout()
        self.c19_untergruppe_widget = QWidget()
        c19_untergruppe_layout = QHBoxLayout()  
        c19_untergruppe_layout.addWidget(self.c19_status_label)
        c19_untergruppe_layout.addWidget(self.c19_combo)
        c19_untergruppe_layout.addWidget(self.c19_verdacht_label)
        c19_untergruppe_layout.addWidget(self.c19_verdacht_combo)
        c19_untergruppe_layout.addWidget(self.c19_negtest_date_input)
        c19_untergruppe_layout.addWidget(self.checkbox_znc19)
        c19_untergruppe_layout.addWidget(self.ctwert_label)
        c19_untergruppe_layout.addWidget(self.ctwert_input)
        self.c19_untergruppe_widget.setLayout(c19_untergruppe_layout) 

        self.c19_combo.currentTextChanged.connect(self.toggle_c19_negtest_date)
        self.c19_combo.currentTextChanged.connect(self.toggle_ct_wert)
        self.c19_combo.currentTextChanged.connect(self.toggle_c19_verdacht)

 
        c19_layout.addWidget(self.c19_untergruppe_widget)
        mibi_layout.addLayout(c19_layout)



        mibi_layout.addWidget(self.resistente_erreger_label)
        mibi_layout.addWidget(self.checkbox_vre1)
        mibi_layout.addWidget(self.checkbox_vre2)
        mibi_layout.addWidget(self.checkbox_mrsa1)
        mibi_layout.addWidget(self.checkbox_mrsa2)
        mibi_layout.addWidget(self.checkbox_3mrgn)
        mibi_layout.addWidget(self.checkbox_4mrgn)
        mibi_layout.addWidget(self.resistente_erreger_textinput)

        # für Update der Labels
        self.vre1_label = QLabel()
        self.vre2_label = QLabel()
        self.mrsa1_label = QLabel()
        self.mrsa2_label = QLabel()
        self.mrgn3_label = QLabel()
        self.mrgn4_label = QLabel()
        mibi_layout.addWidget(self.vre1_label)
        mibi_layout.addWidget(self.vre2_label)
        mibi_layout.addWidget(self.mrsa1_label)
        mibi_layout.addWidget(self.mrsa2_label)
        mibi_layout.addWidget(self.mrgn3_label)
        mibi_layout.addWidget(self.mrgn4_label)
        self.vre1_label.setVisible(False)
        self.vre2_label.setVisible(False)
        self.mrsa1_label.setVisible(False)
        self.mrsa2_label.setVisible(False)
        self.mrgn3_label.setVisible(False)
        self.mrgn4_label.setVisible(False)
        self.checkbox_vre1.stateChanged.connect(self.update_label)
        self.checkbox_vre2.stateChanged.connect(self.update_label)
        self.checkbox_mrsa1.stateChanged.connect(self.update_label)
        self.checkbox_mrsa2.stateChanged.connect(self.update_label)
        self.checkbox_3mrgn.stateChanged.connect(self.update_label)
        self.checkbox_4mrgn.stateChanged.connect(self.update_label)

        self.mibi_box.setLayout(mibi_layout)
        layout.addWidget(self.mibi_box)

        self.labor_box = QGroupBox('Labor')
        self.labor_box.setFont(font)
        labor_layout = QVBoxLayout()
        self.labor_box.setStyleSheet("QGroupBox { background-color: rgb(220, 255, 220); }")
        self.labor_box.setVisible(False)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Hb, Leukozyten, CRP, PCT, Quick, PTT, Thrombozyten in einer Zeile
        line1_layout = QHBoxLayout()
        

        hb_layout = QVBoxLayout()
        self.hb_label = QLabel('Hämoglobin (g/dl):')
        self.hb_input = QLineEdit()
        hb_layout.addWidget(self.hb_label)
        hb_layout.addWidget(self.hb_input)
        line1_layout.addLayout(hb_layout)

        hkt_layout = QVBoxLayout()
        self.hkt_label = QLabel('Hämatokrit (%):')
        self.hkt_input = QLineEdit()
        hkt_layout.addWidget(self.hkt_label)
        hkt_layout.addWidget(self.hkt_input)
        line1_layout.addLayout(hkt_layout)

        leuko_layout = QVBoxLayout()
        self.leuko_label = QLabel('Leukozyten (/µL):')
        self.leuko_input = QLineEdit()
        leuko_layout.addWidget(self.leuko_label)
        leuko_layout.addWidget(self.leuko_input)
        line1_layout.addLayout(leuko_layout)

        crp_layout = QVBoxLayout()
        self.crp_label = QLabel('CRP (mg/L):')
        self.crp_input = QLineEdit()
        crp_layout.addWidget(self.crp_label)
        crp_layout.addWidget(self.crp_input)
        line1_layout.addLayout(crp_layout)

        pct_layout = QVBoxLayout()
        self.pct_label = QLabel('PCT (%):')
        self.pct_input = QLineEdit()
        pct_layout.addWidget(self.pct_label)
        pct_layout.addWidget(self.pct_input)
        line1_layout.addLayout(pct_layout)

        quick_layout = QVBoxLayout()
        self.quick_label = QLabel('Quick (%):')
        self.quick_input = QLineEdit()
        quick_layout.addWidget(self.quick_label)
        quick_layout.addWidget(self.quick_input)
        line1_layout.addLayout(quick_layout)

        inr_layout = QVBoxLayout()
        self.inr_label = QLabel('INR:')
        self.inr_input = QLineEdit()
        inr_layout.addWidget(self.inr_label)
        inr_layout.addWidget(self.inr_input)
        line1_layout.addLayout(inr_layout)

        ptt_layout = QVBoxLayout()
        self.ptt_label = QLabel('PTT (s):')
        self.ptt_input = QLineEdit()
        ptt_layout.addWidget(self.ptt_label)
        ptt_layout.addWidget(self.ptt_input)
        line1_layout.addLayout(ptt_layout)

        thrombo_layout = QVBoxLayout()
        self.thrombo_label = QLabel('Thrombozyten (x10^3/µL):')
        self.thrombo_input = QLineEdit()
        thrombo_layout.addWidget(self.thrombo_label)
        thrombo_layout.addWidget(self.thrombo_input)
        line1_layout.addLayout(thrombo_layout)

        labor_layout.addLayout(line1_layout)
        line1_layout.addItem(spacer)


        # Harnstoff, Kreatinin, Bili, GOT, GPT, AP, GGT in einer Zeile
        line2_layout = QHBoxLayout()

        harnstoff_layout = QVBoxLayout()
        self.harnstoff_label = QLabel('Harnstoff (mg/dl):')
        self.harnstoff_input = QLineEdit()
        harnstoff_layout.addWidget(self.harnstoff_label)
        harnstoff_layout.addWidget(self.harnstoff_input)
        line2_layout.addLayout(harnstoff_layout)

        krea_layout = QVBoxLayout()
        self.krea_label = QLabel('Kreatinin (mg/dl):')
        self.krea_input = QLineEdit()
        krea_layout.addWidget(self.krea_label)
        krea_layout.addWidget(self.krea_input)
        line2_layout.addLayout(krea_layout)
        self.krea_input.textChanged.connect(self.update_gfr)

        gfr_layout = QVBoxLayout()
        self.gfr_label = QLabel('GFR (ml/min):')
        self.gfr_input = QLineEdit()
        gfr_layout.addWidget(self.gfr_label)
        gfr_layout.addWidget(self.gfr_input)
        self.gfr_input.setReadOnly(True)
        line2_layout.addLayout(gfr_layout)
        self.gfr_label.setVisible(False)
        self.gfr_input.setVisible(False)


        bili_layout = QVBoxLayout()
        self.bili_label = QLabel('Bilirubin (mg/dl):')
        self.bili_input = QLineEdit()
        bili_layout.addWidget(self.bili_label)
        bili_layout.addWidget(self.bili_input)
        line2_layout.addLayout(bili_layout)

        got_layout = QVBoxLayout()
        self.got_label = QLabel('GOT (U/L):')
        self.got_input = QLineEdit()
        got_layout.addWidget(self.got_label)
        got_layout.addWidget(self.got_input)
        line2_layout.addLayout(got_layout)

        gpt_layout = QVBoxLayout()
        self.gpt_label = QLabel('GPT (U/L):')
        self.gpt_input = QLineEdit()
        gpt_layout.addWidget(self.gpt_label)
        gpt_layout.addWidget(self.gpt_input)
        line2_layout.addLayout(gpt_layout)

        ap_layout = QVBoxLayout()
        self.ap_label = QLabel('Alkal. Phosph. (U/L):')
        self.ap_input = QLineEdit()
        ap_layout.addWidget(self.ap_label)
        ap_layout.addWidget(self.ap_input)
        line2_layout.addLayout(ap_layout)

        ggt_layout = QVBoxLayout()
        self.ggt_label = QLabel('GGT (U/L):')
        self.ggt_input = QLineEdit()
        ggt_layout.addWidget(self.ggt_label)
        ggt_layout.addWidget(self.ggt_input)
        line2_layout.addLayout(ggt_layout)

        labor_layout.addLayout(line2_layout)
        line2_layout.addItem(spacer)

        # Na+, Kalium, BNP in einer Zeile
        line3_layout = QHBoxLayout()

        na_layout = QVBoxLayout()
        self.na_label = QLabel('Natrium (mmol/L):')
        self.na_input = QLineEdit()
        na_layout.addWidget(self.na_label)
        na_layout.addWidget(self.na_input)
        line3_layout.addLayout(na_layout)

        k_layout = QVBoxLayout()
        self.k_label = QLabel('Kalium (mmol/L):')
        self.k_input = QLineEdit()
        k_layout.addWidget(self.k_label)
        k_layout.addWidget(self.k_input)
        line3_layout.addLayout(k_layout)

        bnp_layout = QVBoxLayout()
        self.bnp_label = QLabel('BNP (pg/ml):')
        self.bnp_input = QLineEdit()
        bnp_layout.addWidget(self.bnp_label)
        bnp_layout.addWidget(self.bnp_input)
        line3_layout.addLayout(bnp_layout)

        labor_layout.addLayout(line3_layout)
        line3_layout.addItem(spacer)

        # HIT-Schnelltest
        self.labor_line4_gruppe = QWidget()
        line4_layout = QHBoxLayout()
        self.labor_line4_gruppe.setLayout(line4_layout)
        self.hit_label = QLabel('HIT-Schnelltest positiv?')
        self.hit_combo = QComboBox()
        self.hit_combo.addItems(['nein', 'ja'])
        self.hit_combo.setCurrentIndex(0)
        line4_layout.addWidget(self.hit_label)
        line4_layout.addWidget(self.hit_combo)
        self.labor_line4_gruppe.setVisible(False)

        labor_layout.addWidget(self.labor_line4_gruppe)
        line4_layout.addItem(spacer)

        self.labor_box.setLayout(labor_layout)
        layout.addWidget(self.labor_box)


        # Beatmungsparameter
        self.ventilation_box = QGroupBox('Beatmungsparameter')
        self.ventilation_box.setFont(font)
        ventilation_layout = QVBoxLayout()
        self.ventilation_box.setStyleSheet("QGroupBox { background-color: rgb(220, 220, 255); }")
        self.ventilation_box.setVisible(False)

        # Modus (input, label + combo in einer Zeile)
        line1_layout = QHBoxLayout()

        self.modus_input = QLineEdit()
        self.modus_label = QLabel('Beatmungsmodus:')
        self.modus_input.setPlaceholderText("Beatmungsmodus, z.B. Bilevel, BiLevel ST, WOBOV, PSV")

        line1_layout.addWidget(self.modus_label)
        line1_layout.addWidget(self.modus_input)

        # Erstelle line2_layout für die restlichen Parameter
        line2_layout = QHBoxLayout()

        spitzendruck_layout = QVBoxLayout()
        self.spitzendruck_label = QLabel('Spitzendruck / IPAP (cmH2O):')
        self.spitzendruck_input = QLineEdit()
        spitzendruck_layout.addWidget(self.spitzendruck_label)
        spitzendruck_layout.addWidget(self.spitzendruck_input)
        line2_layout.addLayout(spitzendruck_layout)

        atemfrequenz_layout = QVBoxLayout()
        self.atemfrequenz_label = QLabel('Atemfrequenz (/min):')
        self.atemfrequenz_input = QLineEdit()
        atemfrequenz_layout.addWidget(self.atemfrequenz_label)
        atemfrequenz_layout.addWidget(self.atemfrequenz_input)
        line2_layout.addLayout(atemfrequenz_layout)

        izue_layout = QVBoxLayout()
        self.izue_label = QLabel('I:E-Verhältnis:')
        self.izue_input = QLineEdit()
        izue_layout.addWidget(self.izue_label)
        izue_layout.addWidget(self.izue_input)
        line2_layout.addLayout(izue_layout)

        tinsp_layout = QVBoxLayout()
        self.tinsp_label = QLabel('Tinsp (s):')
        self.tinsp_input = QLineEdit()
        tinsp_layout.addWidget(self.tinsp_label)
        tinsp_layout.addWidget(self.tinsp_input)
        line2_layout.addLayout(tinsp_layout)


        peep_layout = QVBoxLayout()
        self.peep_label = QLabel('PEEP (cmH2O):')
        self.peep_input = QLineEdit()
        peep_layout.addWidget(self.peep_label)
        peep_layout.addWidget(self.peep_input)
        line2_layout.addLayout(peep_layout)

        fio2_layout = QVBoxLayout()
        self.fio2_label = QLabel('FiO2 (%):')
        self.fio2_input = QLineEdit()
        fio2_layout.addWidget(self.fio2_label)
        fio2_layout.addWidget(self.fio2_input)
        line2_layout.addLayout(fio2_layout)

        ventilation_layout.addLayout(line1_layout)
        ventilation_layout.addLayout(line2_layout)

        self.ventilation_box.setLayout(ventilation_layout)  
        layout.addWidget(self.ventilation_box)




        #BGA

        self.bga_box = QGroupBox('BGA')
        self.bga_box.setFont(font)
        bga_layout = QVBoxLayout()
        self.bga_box.setStyleSheet("QGroupBox { background-color: rgb(255, 255, 220); }")
        self.bga_box.setVisible(False)

        # pH, pO2, SaO2, pCO2, HCO3, BE in einer Zeile
        line4_layout = QHBoxLayout()
        
        ph_layout = QVBoxLayout()
        self.ph_label = QLabel('pH:')
        self.ph_input = QLineEdit()
        ph_layout.addWidget(self.ph_label)

        ph_layout.addWidget(self.ph_input)
        line4_layout.addLayout(ph_layout)

        po2_layout = QVBoxLayout()
        self.po2_label = QLabel('pO2 (mmHg):')
        self.po2_input = QLineEdit()
        po2_layout.addWidget(self.po2_label)
        po2_layout.addWidget(self.po2_input)
        line4_layout.addLayout(po2_layout)

        pco2_layout = QVBoxLayout()
        self.pco2_label = QLabel('pCO2 (mmHg):')
        self.pco2_input = QLineEdit()
        pco2_layout.addWidget(self.pco2_label)
        pco2_layout.addWidget(self.pco2_input)
        line4_layout.addLayout(pco2_layout)

        sao2_layout = QVBoxLayout()
        self.sao2_label = QLabel('SaO2 (%):')
        self.sao2_input = QLineEdit()
        sao2_layout.addWidget(self.sao2_label)
        sao2_layout.addWidget(self.sao2_input)
        line4_layout.addLayout(sao2_layout)

        hco3_layout = QVBoxLayout()
        self.hco3_label = QLabel('HCO3 (mmol/L):')
        self.hco3_input = QLineEdit()
        hco3_layout.addWidget(self.hco3_label)
        hco3_layout.addWidget(self.hco3_input)
        line4_layout.addLayout(hco3_layout)

        be_layout = QVBoxLayout()
        self.be_label = QLabel('BE:')
        self.be_input = QLineEdit()
        be_layout.addWidget(self.be_label)
        be_layout.addWidget(self.be_input)
        line4_layout.addLayout(be_layout)

        bga_layout.addLayout(line4_layout)

        self.bga_box.setLayout(bga_layout)
        layout.addWidget(self.bga_box)

        # Hauptlayout für Vorerkrankungen
        self.vorerkrankungen_box = QGroupBox('Vorerkrankungen')
        self.vorerkrankungen_box.setFont(font)
        vorerkrankungen_layout = QVBoxLayout()
        self.vorerkrankungen_box.setStyleSheet("QGroupBox { background-color: rgb(255, 220, 255); }")
        self.vorerkrankungen_box.setVisible(False)

        # Adipositas
        self.adipositas_text = QLabel()
        vorerkrankungen_layout.addWidget(self.adipositas_text)
        self.adipositas_input = QLineEdit()
        vorerkrankungen_layout.addWidget(self.adipositas_input)
        self.adipositas_combo = QComboBox()
        self.adipositas_combo.addItems(['ja', 'nein'])
        self.adipositas_combo.setVisible(False)
        self.adipositas_input.setVisible(False)
        vorerkrankungen_layout.addWidget(self.adipositas_combo)

        line1_layout = QHBoxLayout()
        line2_layout = QHBoxLayout()
        # Kardiovaskuläre Erkrankungen
        self.kardiovaskulaere_gruppe = QGroupBox('Kardiovaskuläre Erkrankungen')
        self.kardiovaskulaere_gruppe.setVisible(False)
        kardiovaskulaere_layout = QVBoxLayout()
        self.checkbox_aht = QCheckBox('Arterielle Hypertonie')
        self.checkbox_khk = QCheckBox('Koronare Herzkrankheit')
        self.checkbox_herzinsuff = QCheckBox('Herzinsuffizienz')
        self.checkbox_pulmht = QCheckBox('Pulmonale Hypertonie')
        self.checkbox_pavk = QCheckBox('Periphere arterielle Verschlusskrankheit')
        kardiovaskulaere_layout.addWidget(self.checkbox_aht)
        kardiovaskulaere_layout.addWidget(self.checkbox_khk)
        kardiovaskulaere_layout.addWidget(self.checkbox_herzinsuff)
        kardiovaskulaere_layout.addWidget(self.checkbox_pulmht)
        kardiovaskulaere_layout.addWidget(self.checkbox_pavk)
        # für Update der Labels
        self.aht_label = QLabel()
        self.khk_label = QLabel()
        self.herzinsuff_label = QLabel()
        self.pulmht_label = QLabel()
        self.pavk_label = QLabel()
        kardiovaskulaere_layout.addWidget(self.aht_label)
        kardiovaskulaere_layout.addWidget(self.khk_label)
        kardiovaskulaere_layout.addWidget(self.herzinsuff_label)
        kardiovaskulaere_layout.addWidget(self.pulmht_label)
        kardiovaskulaere_layout.addWidget(self.pavk_label)
        self.aht_label.setVisible(False)
        self.khk_label.setVisible(False)
        self.herzinsuff_label.setVisible(False)
        self.pulmht_label.setVisible(False)
        self.pavk_label.setVisible(False)
        self.checkbox_aht.stateChanged.connect(self.update_label)
        self.checkbox_khk.stateChanged.connect(self.update_label)
        self.checkbox_herzinsuff.stateChanged.connect(self.update_label)
        self.checkbox_pulmht.stateChanged.connect(self.update_label)
        self.checkbox_pavk.stateChanged.connect(self.update_label)

        self.kardiovaskulaere_gruppe.setLayout(kardiovaskulaere_layout)

        # Metabolische und endokrine Erkrankungen
        self.metabolisch_endokrine_gruppe = QGroupBox('Metabolische und endokrine Erkrankungen')
        self.metabolisch_endokrine_gruppe.setVisible(False)
        metabolisch_endokrine_layout = QVBoxLayout()
        self.checkbox_dm = QCheckBox('Diabetes mellitus')
        self.checkbox_hypothyreose = QCheckBox('Hypothyreose')
        self.checkbox_hyperthyreose = QCheckBox('Hyperthyreose')
        metabolisch_endokrine_layout.addWidget(self.checkbox_dm)
        metabolisch_endokrine_layout.addWidget(self.checkbox_hypothyreose)
        metabolisch_endokrine_layout.addWidget(self.checkbox_hyperthyreose)
        # für Update der Labels
        self.dm_label = QLabel()
        self.hypothyreose_label = QLabel()
        self.hyperthyreose_label = QLabel()
        metabolisch_endokrine_layout.addWidget(self.dm_label)
        metabolisch_endokrine_layout.addWidget(self.hypothyreose_label)
        metabolisch_endokrine_layout.addWidget(self.hyperthyreose_label)
        self.dm_label.setVisible(False)
        self.hypothyreose_label.setVisible(False)
        self.hyperthyreose_label.setVisible(False)
        self.checkbox_dm.stateChanged.connect(self.update_label)
        self.checkbox_hypothyreose.stateChanged.connect(self.update_label)
        self.checkbox_hyperthyreose.stateChanged.connect(self.update_label)

        self.metabolisch_endokrine_gruppe.setLayout(metabolisch_endokrine_layout)

        # Neurologische und vaskuläre Erkrankungen
        self.neuro_vaskulaere_gruppe = QGroupBox('Neurologische / vaskuläre Erkrankungen')
        self.neuro_vaskulaere_gruppe.setVisible(False)
        neuro_vaskulaere_layout = QVBoxLayout()
        self.checkbox_apoplex = QCheckBox('(Z.n.) Apoplex')
        self.checkbox_delir = QCheckBox('(Z.n.) Delir')
        self.checkbox_cip = QCheckBox('Critical Illness Polyneuropathie')
        self.checkbox_cim = QCheckBox('Critical Illness Myopathie')
        neuro_vaskulaere_layout.addWidget(self.checkbox_apoplex)
        neuro_vaskulaere_layout.addWidget(self.checkbox_delir)
        neuro_vaskulaere_layout.addWidget(self.checkbox_cip)
        neuro_vaskulaere_layout.addWidget(self.checkbox_cim)
        # für Update der Labels
        self.apoplex_label = QLabel()
        self.delir_label = QLabel()
        self.cip_label = QLabel()
        self.cim_label = QLabel()
        neuro_vaskulaere_layout.addWidget(self.apoplex_label)
        neuro_vaskulaere_layout.addWidget(self.delir_label)
        neuro_vaskulaere_layout.addWidget(self.cip_label)
        neuro_vaskulaere_layout.addWidget(self.cim_label)
        self.apoplex_label.setVisible(False)
        self.delir_label.setVisible(False)
        self.cip_label.setVisible(False)
        self.cim_label.setVisible(False)
        self.checkbox_apoplex.stateChanged.connect(self.update_label)
        self.checkbox_delir.stateChanged.connect(self.update_label)
        self.checkbox_cip.stateChanged.connect(self.update_label)
        self.checkbox_cim.stateChanged.connect(self.update_label)

        self.neuro_vaskulaere_gruppe.setLayout(neuro_vaskulaere_layout)

        # Nierenerkrankungen
        nierenerkrankungen_gruppe = QGroupBox('Nierenerkrankungen')
        nierenerkrankungen_layout = QVBoxLayout()
        self.checkbox_cni = QCheckBox('Chronische Niereninsuffizienz')
        self.checkbox_ani = QCheckBox('Akute Niereninsuffizienz')
        self.checkbox_dialyse = QCheckBox('Dialysepflicht')
        self.dialyse_combo = QComboBox()
        self.dialyse_combo.addItems(['intermittierend' , 'kontinuierlich'])
        self.dialyse_combo.setCurrentIndex(-1)
        self.dialyse_combo.setPlaceholderText('Dialyseart')
        self.dialyse_combo.setVisible(False)
        nierenerkrankungen_layout.addWidget(self.checkbox_cni)
        nierenerkrankungen_layout.addWidget(self.checkbox_ani)
        nierenerkrankungen_layout.addWidget(self.checkbox_dialyse)
        nierenerkrankungen_layout.addWidget(self.dialyse_combo)
        # für Update der Labels
        self.cni_label = QLabel()
        self.ani_label = QLabel()
        self.dialyse_label = QLabel()
        nierenerkrankungen_layout.addWidget(self.cni_label)
        nierenerkrankungen_layout.addWidget(self.ani_label)
        nierenerkrankungen_layout.addWidget(self.dialyse_label)
        self.cni_label.setVisible(False)
        self.ani_label.setVisible(False)
        self.dialyse_label.setVisible(False)
        self.checkbox_cni.stateChanged.connect(self.update_label)
        self.checkbox_ani.stateChanged.connect(self.update_label)
        self.checkbox_dialyse.stateChanged.connect(self.update_label)
        nierenerkrankungen_gruppe.setLayout(nierenerkrankungen_layout)

        # Pulmonale Erkrankungen
        self.pulmonale_gruppe = QGroupBox('Pulmonale Erkrankungen')
        self.pulmonale_gruppe.setVisible(False)
        pulmonale_layout = QVBoxLayout()
        self.checkbox_asthma = QCheckBox('Asthma bronchiale')
        self.checkbox_copd = QCheckBox('COPD')
        self.checkbox_pneumonie = QCheckBox('(Z.n.) Pneumonie')
        self.checkbox_thorakorestr = QCheckBox('Thorakorestriktive Erkrankung (z.B. Skoliose, Fibrose)')
        self.checkbox_interstit = QCheckBox('Interstitielle Lungenerkrankung')
        self.checkbox_osas = QCheckBox('Obstruktives Schlafapnoesyndrom')
        self.checkbox_osas.setVisible(False)
        pulmonale_layout.addWidget(self.checkbox_asthma)
        pulmonale_layout.addWidget(self.checkbox_copd)
        pulmonale_layout.addWidget(self.checkbox_pneumonie)
        pulmonale_layout.addWidget(self.checkbox_interstit)
        pulmonale_layout.addWidget(self.checkbox_osas)
        pulmonale_layout.addWidget(self.checkbox_thorakorestr)
        # für Update der Labels
        self.asthma_label = QLabel()
        self.copd_label = QLabel()
        self.pneumonie_label = QLabel()
        self.interstit_label = QLabel()
        self.osas_label = QLabel()
        self.thorakorestr_label = QLabel()
        pulmonale_layout.addWidget(self.asthma_label)
        pulmonale_layout.addWidget(self.copd_label)
        pulmonale_layout.addWidget(self.pneumonie_label)
        pulmonale_layout.addWidget(self.interstit_label)
        pulmonale_layout.addWidget(self.osas_label)
        pulmonale_layout.addWidget(self.thorakorestr_label)
        self.asthma_label.setVisible(False)
        self.copd_label.setVisible(False)
        self.pneumonie_label.setVisible(False)
        self.interstit_label.setVisible(False)
        self.osas_label.setVisible(False)
        self.thorakorestr_label.setVisible(False)
        self.checkbox_asthma.stateChanged.connect(self.update_label)
        self.checkbox_copd.stateChanged.connect(self.update_label)
        self.checkbox_pneumonie.stateChanged.connect(self.update_label)
        self.checkbox_interstit.stateChanged.connect(self.update_label)
        self.checkbox_osas.stateChanged.connect(self.update_label)
        self.checkbox_thorakorestr.stateChanged.connect(self.update_label)

        self.pulmonale_gruppe.setLayout(pulmonale_layout)

        # Abusus und Lebensstil
        self.abusus_lebensstil_gruppe = QGroupBox('Abusus und Lebensstil')
        self.abusus_lebensstil_gruppe.setFixedWidth(200)
        abusus_lebensstil_layout = QVBoxLayout()
        self.checkbox_nikotin = QCheckBox('Nikotinabusus')
        self.nikotin_py_textinput = QLineEdit()
        self.nikotin_py_textinput.setFixedWidth(120)
        self.nikotin_py_textinput.setStyleSheet("margin-left: 20px;")

        self.nikotin_py_textinput.setPlaceholderText('Packyears')
        self.checkbox_alkohol = QCheckBox('Alkoholabusus')
        abusus_lebensstil_layout.addWidget(self.checkbox_nikotin)
        abusus_lebensstil_layout.addWidget(self.nikotin_py_textinput)
        abusus_lebensstil_layout.addWidget(self.checkbox_alkohol)
        # für Update der Labels
        self.nikotin_label = QLabel()
        self.alkohol_label = QLabel()
        abusus_lebensstil_layout.addWidget(self.nikotin_label)
        abusus_lebensstil_layout.addWidget(self.alkohol_label)
        self.nikotin_label.setVisible(False)
        self.alkohol_label.setVisible(False)
        self.checkbox_nikotin.stateChanged.connect(self.update_label)
        self.checkbox_alkohol.stateChanged.connect(self.update_label)

        self.abusus_lebensstil_gruppe.setLayout(abusus_lebensstil_layout)

        # Neuromuskuläre Erkrankungen
        self.neuromuskulaere_gruppe = QGroupBox('Neuromuskuläre Erkrankungen')
        neuromuskulaere_layout = QVBoxLayout()
        self.checkbox_neuromusk = QCheckBox('Neuromuskuläre Erkrankung')
        neuromuskulaere_layout.addWidget(self.checkbox_neuromusk)
        # für Update der Labels
        self.neuromusk_label = QLabel()
        neuromuskulaere_layout.addWidget(self.neuromusk_label)
        self.neuromusk_label.setVisible(False)
        self.checkbox_neuromusk.stateChanged.connect(self.update_label)
        
        self.neuromuskulaere_gruppe.setLayout(neuromuskulaere_layout)

        #Infektionsserologie
        self.infektionsserologie_gruppe = QGroupBox('Infektionsserologie')
        self.infektionsserologie_gruppe.setFixedWidth(500)
        self.infektionsserologie_gruppe.setVisible(False)
        infektionsserologie_layout = QVBoxLayout()
        infektionsserologie_line1_layout = QHBoxLayout()
        self.checkbox_hivpos = QCheckBox('HIV positiv')
        self.checkbox_hivneg = QCheckBox('HIV negativ')
        infektionsserologie_line2_layout = QHBoxLayout()
        self.checkbox_hbsagpos = QCheckBox('HbsAg positiv')
        self.checkbox_hbsagneg = QCheckBox('HbsAg negativ')
        infektionsserologie_line3_layout = QHBoxLayout()
        self.checkbox_hcvpos = QCheckBox('HCV AK positiv')
        self.checkbox_hcvneg = QCheckBox('HCV AK negativ')

        # Verbinden Sie die CheckBoxes mit der Funktion
        self.checkbox_hivpos.stateChanged.connect(lambda: self.on_checkbox_state_changed(self.checkbox_hivpos))
        self.checkbox_hivneg.stateChanged.connect(lambda: self.on_checkbox_state_changed(self.checkbox_hivneg))
        self.checkbox_hbsagpos.stateChanged.connect(lambda: self.on_checkbox_state_changed(self.checkbox_hbsagpos))
        self.checkbox_hbsagneg.stateChanged.connect(lambda: self.on_checkbox_state_changed(self.checkbox_hbsagneg))
        self.checkbox_hcvpos.stateChanged.connect(lambda: self.on_checkbox_state_changed(self.checkbox_hcvpos))
        self.checkbox_hcvneg.stateChanged.connect(lambda: self.on_checkbox_state_changed(self.checkbox_hcvneg))


        infektionsserologie_line1_layout.addWidget(self.checkbox_hivpos)
        infektionsserologie_line1_layout.addWidget(self.checkbox_hivneg)
        infektionsserologie_line2_layout.addWidget(self.checkbox_hbsagpos)
        infektionsserologie_line2_layout.addWidget(self.checkbox_hbsagneg)
        infektionsserologie_line3_layout.addWidget(self.checkbox_hcvpos)
        infektionsserologie_line3_layout.addWidget(self.checkbox_hcvneg)


        infektionsserologie_layout.addLayout(infektionsserologie_line1_layout)
        infektionsserologie_layout.addLayout(infektionsserologie_line2_layout)
        infektionsserologie_layout.addLayout(infektionsserologie_line3_layout)

        self.infektionsserologie_gruppe.setLayout(infektionsserologie_layout)

        # Zusammenfügen aller Gruppen

        line1_layout.addWidget(self.kardiovaskulaere_gruppe)
        line1_layout.addWidget(self.pulmonale_gruppe)
        line1_layout.addWidget(nierenerkrankungen_gruppe)
        line1_layout.addWidget(self.metabolisch_endokrine_gruppe)
        line1_layout.addItem(spacer)
        line2_layout.addWidget(self.neuro_vaskulaere_gruppe)
        line2_layout.addWidget(self.abusus_lebensstil_gruppe)
        line2_layout.addWidget(self.neuromuskulaere_gruppe)
        line2_layout.addWidget(self.infektionsserologie_gruppe)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        line2_layout.addItem(spacer)
        
        vorerkrankungen_layout.addLayout(line1_layout)
        vorerkrankungen_layout.addLayout(line2_layout)


        self.vorerkrankungen_box.setLayout(vorerkrankungen_layout)

        layout.addWidget(self.vorerkrankungen_box)

        #Medikamente-Box
        self.medikamente_box = QGroupBox('Medikamente')
        self.medikamente_box.setFont(font)
        self.medikamente_box.setVisible(False)
        medikamente_layout = QHBoxLayout()
        self.medikamente_box.setStyleSheet("QGroupBox { background-color: rgb(255, 220, 220); }")

        #Katecholamine
        self.katecholamine_gruppe = QGroupBox('Katecholamine')
        katecholamine_layout = QVBoxLayout()
        self.katecholamine_subgruppe = QWidget()
        self.katecholamine_subgruppe_layout = QVBoxLayout()
        self.katecholamine_subgruppe.setVisible(False)
        self.katecholamine_combo = QComboBox()
        self.katecholamine_combo.addItems(['nein', 'ja'])


        noradrenalin_layout = QHBoxLayout()
        self.katecholamine_checkbox1 = QCheckBox('Noradrenalin (0,1mg/ml)')
        self.katecholamine_checkbox1.setFixedSize(170, 38)
        self.noradrenalin_text = QLabel()
        self.noradrenalin_laufrate = QLineEdit()
        self.noradrenalin_laufrate_einheit = QLabel('ml/h')
        self.noradrenalin_laufrate.setVisible(False)
        self.noradrenalin_laufrate_einheit.setVisible(False)
        noradrenalin_layout.addWidget(self.katecholamine_checkbox1)
        noradrenalin_layout.addWidget(self.noradrenalin_laufrate)
        noradrenalin_layout.addWidget(self.noradrenalin_laufrate_einheit)
        noradrenalin_layout.setAlignment(Qt.AlignLeft)

        adrenalin_layout = QHBoxLayout()
        self.katecholamine_checkbox2 = QCheckBox('Adrenalin')
        self.katecholamine_checkbox2.setFixedSize(170, 38)
        self.adrenalin_text = QLabel()
        self.adrenalin_laufrate = QLineEdit()
        self.adrenalin_laufrate_einheit = QLabel('ml/h')
        self.adrenalin_laufrate.setVisible(False)
        self.adrenalin_laufrate_einheit.setVisible(False)
        adrenalin_layout.addWidget(self.katecholamine_checkbox2)
        adrenalin_layout.addWidget(self.adrenalin_laufrate)
        adrenalin_layout.addWidget(self.adrenalin_laufrate_einheit)
        adrenalin_layout.setAlignment(Qt.AlignLeft)

        dobutamin_layout = QHBoxLayout()
        self.katecholamine_checkbox3 = QCheckBox('Dobutamin')
        self.katecholamine_checkbox3.setFixedSize(170, 38)
        self.dobutamin_text = QLabel()
        self.dobutamin_laufrate = QLineEdit()
        self.dobutamin_laufrate_einheit = QLabel('ml/h')
        self.dobutamin_laufrate.setVisible(False)
        self.dobutamin_laufrate_einheit.setVisible(False)
        dobutamin_layout.addWidget(self.katecholamine_checkbox3)
        dobutamin_layout.addWidget(self.dobutamin_laufrate)
        dobutamin_layout.addWidget(self.dobutamin_laufrate_einheit)
        dobutamin_layout.setAlignment(Qt.AlignLeft)

        katecholamine_sonstige_layout = QHBoxLayout()
        self.katecholamine_sonstige_input = QLineEdit()
        self.katecholamine_sonstige_input.setPlaceholderText('Sonstige')
        self.katecholamine_sonstige_input.setFixedWidth(160)
        self.katecholamine_sonstige_laufrate_input = QLineEdit()
        self.katecholamine_sonstige_laufrate_input.setFixedWidth(100)
        self.katecholamine_sonstige_laufrate_einheit = QLabel('ml/h')
        katecholamine_sonstige_layout.addWidget(self.katecholamine_sonstige_input)
        katecholamine_sonstige_layout.addWidget(self.katecholamine_sonstige_laufrate_input)
        katecholamine_sonstige_layout.addWidget(self.katecholamine_sonstige_laufrate_einheit)


        self.katecholamine_subgruppe_layout.addLayout(noradrenalin_layout)
        self.katecholamine_subgruppe_layout.addLayout(adrenalin_layout)
        self.katecholamine_subgruppe_layout.addLayout(dobutamin_layout)
        self.katecholamine_subgruppe_layout.addLayout(katecholamine_sonstige_layout)


        katecholamine_layout.addWidget(self.katecholamine_combo)
        katecholamine_layout.addWidget(self.katecholamine_subgruppe)
    

        self.katecholamine_combo.currentIndexChanged.connect(self.update_katecholamine_widgets)
        self.katecholamine_checkbox1.stateChanged.connect(self.update_medikationcheckboxes)
        self.katecholamine_checkbox2.stateChanged.connect(self.update_medikationcheckboxes)
        self.katecholamine_checkbox3.stateChanged.connect(self.update_medikationcheckboxes)
        
        #Sedierung
        self.sedierung_gruppe = QGroupBox('Sedierung')
        self.sedierung_gruppe.setFixedWidth(400)
        sedierung_layout = QVBoxLayout()

        propofol_layout = QHBoxLayout()
        self.sedierung_checkbox1 = QCheckBox('Propofol 2%')
        self.sedierung_checkbox1.setFixedSize(150, 38)
        self.propofol_text = QLabel()
        self.propofol_text.setVisible(False)
        self.propofol_laufrate_input = QLineEdit()
        self.propofol_laufrate_input.setFixedWidth(100)
        self.propofol_laufrate_einheit = QLabel('ml/h')
        self.propofol_laufrate_input.setVisible(False)
        self.propofol_laufrate_einheit.setVisible(False)
        propofol_layout.addWidget(self.sedierung_checkbox1)
        propofol_layout.addWidget(self.propofol_text)
        propofol_layout.addWidget(self.propofol_laufrate_input)
        propofol_layout.addWidget(self.propofol_laufrate_einheit)
        propofol_layout.setAlignment(Qt.AlignLeft)

        sufenta_layout = QHBoxLayout()
        self.sedierung_checkbox2 = QCheckBox('Sufentanil 5 µg/ml')
        self.sedierung_checkbox2.setFixedSize(150, 38)
        self.sufenta_text = QLabel()
        self.sufenta_laufrate_input = QLineEdit()
        self.sufenta_laufrate_input.setFixedWidth(100)
        self.sufenta_laufrate_einheit = QLabel('ml/h')
        self.sufenta_laufrate_input.setVisible(False)
        self.sufenta_laufrate_einheit.setVisible(False)
        sufenta_layout.addWidget(self.sedierung_checkbox2)
        sufenta_layout.addWidget(self.sufenta_laufrate_input)
        sufenta_layout.addWidget(self.sufenta_laufrate_einheit)
        sufenta_layout.setAlignment(Qt.AlignLeft)

        fenta_layout = QHBoxLayout()
        self.sedierung_checkbox3 = QCheckBox('Fentanyl s.c.')
        self.sedierung_checkbox3.setFixedSize(150, 38)
        self.fenta_text = QLabel()
        self.fenta_laufrate_input = QLineEdit()
        self.fenta_laufrate_input.setFixedWidth(100)
        self.fenta_laufrate_einheit = QLabel('µg/h')
        self.fenta_laufrate_input.setVisible(False)
        self.fenta_laufrate_einheit.setVisible(False)
        fenta_layout.addWidget(self.sedierung_checkbox3)
        fenta_layout.addWidget(self.fenta_laufrate_input)
        fenta_layout.addWidget(self.fenta_laufrate_einheit)
        fenta_layout.setAlignment(Qt.AlignLeft)

        midazolam_layout = QHBoxLayout()
        self.sedierung_checkbox4 = QCheckBox('Midazolam (2 mg/ml)')
        self.sedierung_checkbox4.setFixedSize(150, 38)
        self.midazolam_text = QLabel()
        self.midazolam_text.setVisible(False)
        self.midazolam_laufrate_input = QLineEdit()
        self.midazolam_laufrate_input.setFixedWidth(100)
        self.midazolam_laufrate_einheit = QLabel('ml/h')
        self.midazolam_laufrate_input.setVisible(False)
        self.midazolam_laufrate_einheit.setVisible(False)
        midazolam_layout.addWidget(self.sedierung_checkbox4)
        midazolam_layout.addWidget(self.midazolam_laufrate_input)
        midazolam_layout.addWidget(self.midazolam_laufrate_einheit)
        midazolam_layout.setAlignment(Qt.AlignLeft)

        dexdor_layout = QHBoxLayout()
        self.sedierung_checkbox5 = QCheckBox('Dexdometedomidin')
        self.sedierung_checkbox5.setFixedSize(150, 38)
        self.dexdor_text = QLabel()
        self.dexdor_laufrate_input = QLineEdit()
        self.dexdor_laufrate_input.setFixedWidth(100)
        self.dexdor_laufrate_einheit = QLabel('ml/h')
        self.dexdor_laufrate_input.setVisible(False)
        self.dexdor_laufrate_einheit.setVisible(False)
        dexdor_layout.addWidget(self.sedierung_checkbox5)
        dexdor_layout.addWidget(self.dexdor_laufrate_input)
        dexdor_layout.addWidget(self.dexdor_laufrate_einheit)
        dexdor_layout.setAlignment(Qt.AlignLeft)

        ketamin_layout = QHBoxLayout()
        self.sedierung_checkbox6 = QCheckBox('Ketamin')
        self.sedierung_checkbox6.setFixedSize(150, 38)
        self.ketamin_text = QLabel()
        self.ketamin_laufrate_input = QLineEdit()
        self.ketamin_laufrate_input.setFixedWidth(100)
        self.ketamin_laufrate_einheit = QLabel('ml/h')
        self.ketamin_laufrate_input.setVisible(False)
        self.ketamin_laufrate_einheit.setVisible(False)
        ketamin_layout.addWidget(self.sedierung_checkbox6)
        ketamin_layout.addWidget(self.ketamin_laufrate_input)
        ketamin_layout.addWidget(self.ketamin_laufrate_einheit)
        ketamin_layout.setAlignment(Qt.AlignLeft)

        sedierung_sonstige_layout = QHBoxLayout()
        self.sedierung_sonstige_input = QLineEdit()
        self.sedierung_sonstige_input.setPlaceholderText('Sonstige')
        self.sedierung_sonstige_input.setFixedWidth(140)
        self.sedierung_sonstige_laufrate_input = QLineEdit()
        self.sedierung_sonstige_laufrate_input.setFixedWidth(100)
        self.sedierung_sonstige_laufrate_einheit = QLabel('ml/h')
        sedierung_sonstige_layout.addWidget(self.sedierung_sonstige_input)
        sedierung_sonstige_layout.addWidget(self.sedierung_sonstige_laufrate_input)
        sedierung_sonstige_layout.addWidget(self.sedierung_sonstige_laufrate_einheit)

        sedierung_layout.addLayout(propofol_layout) 
        sedierung_layout.addLayout(sufenta_layout)
        sedierung_layout.addLayout(fenta_layout)
        sedierung_layout.addLayout(midazolam_layout)
        sedierung_layout.addLayout(dexdor_layout)
        sedierung_layout.addLayout(ketamin_layout)
        sedierung_layout.addLayout(sedierung_sonstige_layout)

        self.sedierung_checkbox1.stateChanged.connect(self.update_medikationcheckboxes)
        self.sedierung_checkbox2.stateChanged.connect(self.update_medikationcheckboxes)
        self.sedierung_checkbox3.stateChanged.connect(self.update_medikationcheckboxes)
        self.sedierung_checkbox4.stateChanged.connect(self.update_medikationcheckboxes)
        self.sedierung_checkbox5.stateChanged.connect(self.update_medikationcheckboxes)
        self.sedierung_checkbox6.stateChanged.connect(self.update_medikationcheckboxes)

        #Ernährung
        self.ernaehrung_gruppe = QGroupBox('Ernährung')
        ernaehrung_layout = QVBoxLayout()

        parenteral_layout = QVBoxLayout()
        parenteral_layout.setAlignment(Qt.AlignLeft)
        parenteral_layout_line1 = QHBoxLayout()
        parenteral_layout_line1.setAlignment(Qt.AlignLeft)
        self.ernaehrung_checkbox1 = QCheckBox('Parenterale Ernährung')
        self.ernaehrung_checkbox1.setFixedSize(200, 38)
        self.ernaehrung_parenteral_combo = QComboBox()
        self.ernaehrung_parenteral_combo.addItems(['Nutriflex Lipid Plus' , 'Nutriflex + AS' , 'Drei-Komponenten'])
        self.ernaehrung_parenteral_combo.setCurrentIndex(-1)
        self.ernaehrung_parenteral_combo.setVisible(False)
        parenteral_layout_line2 = QHBoxLayout()
        nutriLP_layout = QVBoxLayout()
        self.ernaehrung_parenteral_nutriLP_label = QLabel('Nutriflex Lipid Plus')
        self.ernaehrung_parenteral_nutriLP_label.setVisible(False)
        nutriLP_layout2 = QHBoxLayout()
        self.ernaehrung_parenteral_nutriLP_laufrate_input = QLineEdit()
        self.ernaehrung_parenteral_nutriLP_laufrate_input.setText('0')
        self.ernaehrung_parenteral_nutriLP_laufrate_einheit = QLabel('ml/h')
        self.ernaehrung_parenteral_nutriLP_laufrate_input.setVisible(False)
        self.ernaehrung_parenteral_nutriLP_laufrate_einheit.setVisible(False)
        glc40_layout = QVBoxLayout()
        self.ernaehrung_parenteral_glc40_label = QLabel('Glucose 40% B. Braun')
        self.ernaehrung_parenteral_glc40_label.setVisible(False)
        glc40_layout2 = QHBoxLayout()
        self.ernaehrung_parenteral_glc40_laufrate_input = QLineEdit()
        self.ernaehrung_parenteral_glc40_laufrate_input.setText('0')
        self.ernaehrung_parenteral_glc40_laufrate_einheit = QLabel('ml/h')
        self.ernaehrung_parenteral_glc40_laufrate_input.setVisible(False)
        self.ernaehrung_parenteral_glc40_laufrate_einheit.setVisible(False)
        as_layout = QVBoxLayout()
        self.ernaehrung_parenteral_as_label = QLabel('Aminoplasmal® B. Braun 10%')
        self.ernaehrung_parenteral_as_label.setVisible(False)
        as_layout2 = QHBoxLayout()
        self.ernaehrung_parenteral_as_laufrate_input = QLineEdit()
        self.ernaehrung_parenteral_as_laufrate_input.setText('0')
        self.ernaehrung_parenteral_as_laufrate_einheit = QLabel('ml/h')
        self.ernaehrung_parenteral_as_laufrate_input.setVisible(False)
        self.ernaehrung_parenteral_as_laufrate_einheit.setVisible(False)
        lipid_plus_layout = QVBoxLayout()
        self.ernaehrung_parenteral_lipid_plus_label = QLabel('Lipide')
        self.ernaehrung_parenteral_lipid_plus_label.setVisible(False)
        lipid_plus_layout2 = QHBoxLayout()
        self.ernaehrung_parenteral_lipid_plus_laufrate_input = QLineEdit()
        self.ernaehrung_parenteral_lipid_plus_laufrate_input.setText('0')
        self.ernaehrung_parenteral_lipid_plus_laufrate_einheit = QLabel('ml/h')
        self.ernaehrung_parenteral_lipid_plus_laufrate_input.setVisible(False)
        self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.setVisible(False)

        parenteral_layout_line1.addWidget(self.ernaehrung_checkbox1)
        parenteral_layout_line1.addWidget(self.ernaehrung_parenteral_combo)
        parenteral_layout_line2.addLayout(nutriLP_layout)
        nutriLP_layout.addWidget(self.ernaehrung_parenteral_nutriLP_label)
        nutriLP_layout.addLayout(nutriLP_layout2)
        nutriLP_layout2.addWidget(self.ernaehrung_parenteral_nutriLP_laufrate_input)
        nutriLP_layout2.addWidget(self.ernaehrung_parenteral_nutriLP_laufrate_einheit)
        parenteral_layout_line2.addLayout(glc40_layout)
        glc40_layout.addWidget(self.ernaehrung_parenteral_glc40_label)
        glc40_layout.addLayout(glc40_layout2)
        glc40_layout2.addWidget(self.ernaehrung_parenteral_glc40_laufrate_input)
        glc40_layout2.addWidget(self.ernaehrung_parenteral_glc40_laufrate_einheit)
        parenteral_layout_line2.addLayout(as_layout)
        as_layout.addWidget(self.ernaehrung_parenteral_as_label)
        as_layout.addLayout(as_layout2)
        as_layout2.addWidget(self.ernaehrung_parenteral_as_laufrate_input)
        as_layout2.addWidget(self.ernaehrung_parenteral_as_laufrate_einheit)
        parenteral_layout_line2.addLayout(lipid_plus_layout)
        lipid_plus_layout.addWidget(self.ernaehrung_parenteral_lipid_plus_label)
        lipid_plus_layout.addLayout(lipid_plus_layout2)
        lipid_plus_layout2.addWidget(self.ernaehrung_parenteral_lipid_plus_laufrate_input)
        lipid_plus_layout2.addWidget(self.ernaehrung_parenteral_lipid_plus_laufrate_einheit)

        self.ernaehrung_parenteral_combo.currentIndexChanged.connect(self.update_medikationcombos)
        self.ernaehrung_parenteral_combo.currentIndexChanged.connect(self.parenteral_kcal)
        self.ernaehrung_parenteral_nutriLP_laufrate_input.textChanged.connect(self.parenteral_kcal)
        self.ernaehrung_parenteral_glc40_laufrate_input.textChanged.connect(self.parenteral_kcal)
        self.ernaehrung_parenteral_as_laufrate_input.textChanged.connect(self.parenteral_kcal)
        self.ernaehrung_parenteral_lipid_plus_laufrate_input.textChanged.connect(self.parenteral_kcal)


        enteral_layout = QHBoxLayout()
        enteral_layout.setAlignment(Qt.AlignLeft)
        self.ernaehrung_checkbox2 = QCheckBox('Enterale Ernährung')
        self.ernaehrung_checkbox2.setFixedSize(200, 38)
        self.ernaehrung_enteral_combo = QComboBox()
        self.ernaehrung_enteral_combo.addItems(['1 kcal/ml' , '1.5 kcal/ml' , '2 kcal/ml'])
        self.ernaehrung_enteral_combo.setCurrentIndex(-1)
        self.ernaehrung_enteral_combo.setVisible(False)
        self.ernaehrung_enteral_laufrate_input = QLineEdit()
        self.ernaehrung_enteral_laufrate_input.setFixedWidth(100)
        self.ernaehrung_enteral_laufrate_einheit = QLabel('ml/h')
        self.ernaehrung_enteral_laufrate_input.setVisible(False)
        self.ernaehrung_enteral_laufrate_einheit.setVisible(False)
        enteral_layout.addWidget(self.ernaehrung_checkbox2)
        enteral_layout.addWidget(self.ernaehrung_enteral_combo)
        enteral_layout.addWidget(self.ernaehrung_enteral_laufrate_input)
        enteral_layout.addWidget(self.ernaehrung_enteral_laufrate_einheit)

        self.ernaehrung_checkbox2.stateChanged.connect(self.update_medikationcheckboxes)
        self.ernaehrung_enteral_combo.currentIndexChanged.connect(self.enteral_kcal)
        self.ernaehrung_enteral_laufrate_input.textChanged.connect(self.enteral_kcal)


        self.ernaehrung_checkbox3 = QCheckBox('Oraler Kostaufbau')
        self.ernaehrung_checkbox4 = QCheckBox('keine Ernährung')

        kalorien_parenteral_layout = QHBoxLayout()
        self.kalorien_parenteral_label = QLabel('Kalorien parenteral: ')
        self.kalorien_parenteral = QLabel('0')

        kalorien_enteral_layout = QHBoxLayout()
        self.kalorien_enteral_label = QLabel('Kalorien enteral: ')
        self.kalorien_enteral = QLabel('0')

        kalorien_gesamt_layout = QHBoxLayout()
        self.kalorien_gesamt_label = QLabel('Kalorien gesamt: ')
        self.kalorien_gesamt = QLabel('0')

        ernaehrung_layout.addLayout(parenteral_layout)
        parenteral_layout.addLayout(parenteral_layout_line1)
        parenteral_layout.addLayout(parenteral_layout_line2)

        ernaehrung_layout.addLayout(enteral_layout)
        ernaehrung_layout.addWidget(self.ernaehrung_checkbox3)
        ernaehrung_layout.addWidget(self.ernaehrung_checkbox4)

        ernaehrung_layout.addLayout(kalorien_parenteral_layout)
        kalorien_parenteral_layout.addWidget(self.kalorien_parenteral_label)
        kalorien_parenteral_layout.addWidget(self.kalorien_parenteral)

        ernaehrung_layout.addLayout(kalorien_enteral_layout)
        kalorien_enteral_layout.addWidget(self.kalorien_enteral_label)
        kalorien_enteral_layout.addWidget(self.kalorien_enteral)

        ernaehrung_layout.addLayout(kalorien_gesamt_layout)
        kalorien_gesamt_layout.addWidget(self.kalorien_gesamt_label)
        kalorien_gesamt_layout.addWidget(self.kalorien_gesamt)

        # Med.-Plan
        self.medplan_gruppe = QGroupBox('Medikamentenplan')
        medplan_layout = QVBoxLayout()
        self.medplan = QTextEdit()
        self.medplan.setAcceptRichText(False)
        self.medplan.setPlaceholderText('Medikamentenplan hier einfügen')

        medplan_layout.addWidget(self.medplan)

        self.ernaehrung_checkbox1.stateChanged.connect(self.update_medikationcheckboxes)
        self.ernaehrung_checkbox2.stateChanged.connect(self.update_medikationcheckboxes)



        medikamente_layout.addWidget(self.katecholamine_gruppe, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.katecholamine_gruppe.setLayout(katecholamine_layout)
        katecholamine_layout.addWidget(self.katecholamine_subgruppe)
        self.katecholamine_subgruppe.setLayout(self.katecholamine_subgruppe_layout)

        medikamente_layout.addWidget(self.sedierung_gruppe)
        self.sedierung_gruppe.setLayout(sedierung_layout)

        medikamente_layout.addWidget(self.ernaehrung_gruppe)
        self.ernaehrung_gruppe.setLayout(ernaehrung_layout)

        medikamente_layout.addWidget(self.medplan_gruppe)
        self.medplan_gruppe.setLayout(medplan_layout)

        self.medikamente_box.setLayout(medikamente_layout)
        layout.addWidget(self.medikamente_box)






        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submitForm)
        layout.addWidget(self.submit_button)

        # Fügen Sie das Layout dem Scrollbereich hinzu
        scroll_area_widget.setLayout(layout)

        # Das Layout des Hauptfensters erstellen und das Scrollbereichs-Widget einfügen
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # Das Hauptfenster zeigt das Hauptlayout an und wird größer gemacht
        self.setLayout(main_layout)
        self.resize(1400, 900) 
        self.show()

    def updateBoxVisibility(self): 
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_haltern.isChecked()):
            self.street_label.setVisible(True)
            self.street_input.setVisible(True)
            self.plz_input.setVisible(True)
            self.plz_label.setVisible(True)
            self.city_input.setVisible(True)
            self.city_label.setVisible(True)
        else:
            self.street_label.setVisible(False)
            self.street_input.setVisible(False)
            self.plz_input.setVisible(False)
            self.plz_label.setVisible(False)
            self.city_input.setVisible(False)
            self.city_label.setVisible(False)
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or 
            self.checkbox_bielefeld.isChecked()):
            self.gender_label.setVisible(True)
            self.gender_combo.setVisible(True)
        else:
            self.gender_label.setVisible(False)
            self.gender_combo.setVisible(False)        
        if (self.checkbox_dortmund_luenen.isChecked() or 
            self.checkbox_dortmund.isChecked() or 
            self.checkbox_ibbenbueren.isChecked() or 
            self.checkbox_vest.isChecked() or 
            self.checkbox_soest.isChecked() or 
            self.checkbox_hemer.isChecked() or 
            self.checkbox_bad_lippspringe.isChecked() or 
            self.checkbox_schmallenberg.isChecked() or 
            self.checkbox_bielefeld.isChecked()):
            self.catheter_box.setVisible(True)
        else:
            self.catheter_box.setVisible(False)
        if (self.checkbox_dortmund_luenen.isChecked() or 
            self.checkbox_dortmund.isChecked() or 
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked() or 
            self.checkbox_bielefeld.isChecked()):
            self.labor_box.setVisible(True)
        else:
            self.labor_box.setVisible(False)
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.bga_box.setVisible(True)
        else:
            self.bga_box.setVisible(False)
            #Beruf
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked()):
            self.job_input.setVisible(True)
            self.job_label.setVisible(True)
        else:
            self.job_input.setVisible(False)
            self.job_label.setVisible(False)
            #Hausarzt
        if (self.checkbox_dortmund.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.general_practitioner_input.setVisible(True)
            self.general_practitioner_label.setVisible(True)
        else:
            self.general_practitioner_input.setVisible(False)
            self.general_practitioner_label.setVisible(False)

        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_soest.isChecked() or 
            self.checkbox_hemer.isChecked()):
            self.vollmacht_gruppe.setVisible(True)
        else:
            self.vollmacht_gruppe.setVisible(False)

        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked()):
            self.az_gruppe.setVisible(True)
            self.versorgungzuhause_label.setVisible(True)
            self.versorgungzuhause_combo.setVisible(True)
            self.vorsorgevollmacht_label.setVisible(True)
            self.vorsorgevollmacht_combo.setVisible(True)
        else:
            self.versorgungzuhause_label.setVisible(False)
            self.versorgungzuhause_combo.setVisible(False)
            self.vorsorgevollmacht_label.setVisible(False)
            self.vorsorgevollmacht_combo.setVisible(False)
            self.az_gruppe.setVisible(False)

        if self.checkbox_soest.isChecked():
            self.verfuegung_label.setVisible(True)
            self.verfuegung_combo.setVisible(True)
        else:
            self.verfuegung_label.setVisible(False)
            self.verfuegung_combo.setVisible(False)

            #Beatmungsmodi
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.ventilation_box.setVisible(True)
        else:
            self.ventilation_box.setVisible(False)
            #Versicherung
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_oldenburg.isChecked()):
            self.insurance_input.setVisible(True)
            self.insurance_label.setVisible(True)
        else:
            self.insurance_input.setVisible(False)
            self.insurance_label.setVisible(False)
            #Angehörige
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked()):
            self.next_of_kin_input.setVisible(True)
            self.next_of_kin_label.setVisible(True)
        else:
            self.next_of_kin_input.setVisible(False)
            self.next_of_kin_label.setVisible(False)
            #Angehörige Tel
        if (self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked()):
            self.next_of_kin_tel_input.setVisible(True)
            self.next_of_kin_tel_label.setVisible(True)
        else:
            self.next_of_kin_tel_input.setVisible(False)
            self.next_of_kin_tel_label.setVisible(False)
            #Vorerkrankungen
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.vorerkrankungen_box.setVisible(True)
        else:
            self.vorerkrankungen_box.setVisible(False)
            #Vorerkrankungen / kardiovask. Gruppe
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.kardiovaskulaere_gruppe.setVisible(True)
        else:
            self.kardiovaskulaere_gruppe.setVisible(False)
            #Vorerkrankungen / pulmonale Gruppe
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.pulmonale_gruppe.setVisible(True)
        else:
            self.pulmonale_gruppe.setVisible(False)
            #Vorerkrankungen / metabolisch-endokrine Gruppe
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.metabolisch_endokrine_gruppe.setVisible(True)
        else:
            self.metabolisch_endokrine_gruppe.setVisible(False)
            #Vorerkrankungen / neuro-vaskuläre Gruppe
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.neuro_vaskulaere_gruppe.setVisible(True)
        else:
            self.neuro_vaskulaere_gruppe.setVisible(False)
            #Neuromukuläre Erkrankungen
        if (self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_soest.isChecked()):
            self.neuromuskulaere_gruppe.setVisible(True)
        else:
            self.neuromuskulaere_gruppe.setVisible(False)
            #Dialyse
        if self.checkbox_haltern.isChecked():
            self.dialyse_combo.setVisible(True)
        else:
            self.dialyse_combo.setVisible(False)
            #Vorerkrankungen / sonstige Gruppe
        if (self.checkbox_bad_lippspringe.isChecked()):
            self.checkbox_osas.setVisible(True)
        else:
            self.checkbox_osas.setVisible(False)
            #Mibi-Box
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.mibi_box.setVisible(True)
        else:
            self.mibi_box.setVisible(False)
            #current + previous antibiose
        if (self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.mibi_label_previous.setVisible(True)
            self.mibi_input_previous.setVisible(True)
            self.mibi_label_current.setVisible(True)
            self.mibi_input_current.setVisible(True)
        else:
            self.mibi_label_previous.setVisible(False)
            self.mibi_input_previous.setVisible(False)
            self.mibi_label_current.setVisible(False)
            self.mibi_input_current.setVisible(False)
            #nur current antibiose
        if self.checkbox_bad_lippspringe.isChecked():
            self.mibi_label_current.setVisible(True)
            self.mibi_input_current.setVisible(True)
        else:
            self.mibi_label_current.setVisible(False)
            self.mibi_input_current.setVisible(False)
            #Erreger-Nachweise
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.erregernachweis_input.setVisible(True)
            self.erregernachweis_label.setVisible(True)
        else:
            self.erregernachweis_input.setVisible(False)
            self.erregernachweis_label.setVisible(False)
            #C.difficile
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_koeln.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.c19_cdiff_label.setVisible(True)
            self.cdiff_date_input.setVisible(True)
            self.checkbox_cdiff.setVisible(True)
        else:
            self.cdiff_date_input.setVisible(False)
            self.checkbox_cdiff.setVisible(False)
            #c19
        if (self.checkbox_koeln.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_schmallenberg.isChecked()):
            self.c19_untergruppe_widget.setVisible(True)
        else:
            self.c19_untergruppe_widget.setVisible(False)
            #py
        if (self.checkbox_schmallenberg.isChecked()):
            self.nikotin_py_textinput.setVisible(True)
        else:
            self.nikotin_py_textinput.setVisible(False)
            #abusus-box
        if (self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_schmallenberg.isChecked()):
            self.abusus_lebensstil_gruppe.setVisible(True)
        else:
            self.abusus_lebensstil_gruppe.setVisible(False)
            #Medikamente-Box
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.medikamente_box.setVisible(True)
        else:
            self.medikamente_box.setVisible(False)
            #Katecholamin-Box
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_essen.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.katecholamine_gruppe.setVisible(True)
        else:
            self.katecholamine_gruppe.setVisible(False)
            #Sedierung-Box
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.sedierung_gruppe.setVisible(True)
        else:
            self.sedierung_gruppe.setVisible(False)
            #Ernährung-Box
        if (self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_haltern.isChecked() or
            self.checkbox_bad_lippspringe.isChecked() or
            self.checkbox_schmallenberg.isChecked()):
            self.ernaehrung_gruppe.setVisible(True)
        else:
            self.ernaehrung_gruppe.setVisible(False)
            #Med.-Plan-Box
        if (self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_vest.isChecked() or
            self.checkbox_soest.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_schmallenberg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.medplan_gruppe.setVisible(True)
        else:
            self.medplan_gruppe.setVisible(False)
            #auf der Station seit
        if self.checkbox_ibbenbueren.isChecked():
            self.stat_time_gruppe.setVisible(True)
        else:
            self.stat_time_gruppe.setVisible(False)
            #Weaning Box
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_ibbenbueren.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.weaning_box.setVisible(True)
        else:
            self.weaning_box.setVisible(False)
            #Anzahl der Extubationsversuche
        if (self.checkbox_clemens.isChecked() or
            self.checkbox_ibbenbueren.isChecked()):
            self.ext_versuche_label.setVisible(True)
            self.ext_versuche_input.setVisible(True)
        else:
            self.ext_versuche_label.setVisible(False)
            self.ext_versuche_input.setVisible(False)
            #Extubationsversuche wann
        if self.checkbox_clemens.isChecked():
            self.ext_versuche_wann_label.setVisible(True)
            self.ext_versuche_wann_input.setVisible(True)
        else:
            self.ext_versuche_wann_label.setVisible(False)
            self.ext_versuche_wann_input.setVisible(False)
            #Anzahl Re-Intubationen
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked()):
            self.re_intub_label.setVisible(True)
            self.re_intub_input.setVisible(True)
        else:
            self.re_intub_label.setVisible(False)
            self.re_intub_input.setVisible(False)
            #Weaning-Methode
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked()):
            self.weaning_method_label.setVisible(True)
            self.weaning_method_input.setVisible(True)
        else:
            self.weaning_method_label.setVisible(False)
            self.weaning_method_input.setVisible(False)
            #Scheitern
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked()):
            self.scheitern_label.setVisible(True)
            self.scheitern_input.setVisible(True)
        else:
            self.scheitern_label.setVisible(False)
            self.scheitern_input.setVisible(False)
            #Maschinell
        if self.checkbox_dortmund.isChecked():
            self.beatmung_maschinell_label.setVisible(True)
            self.beatmung_maschinell_input.setVisible(True)
            self.beatmung_maschinell_einheit_label.setVisible(True)
        else:
            self.beatmung_maschinell_label.setVisible(False)
            self.beatmung_maschinell_input.setVisible(False)
            self.beatmung_maschinell_einheit_label.setVisible(False)
            #Spontan
        if (self.checkbox_dortmund.isChecked() or 
            self.checkbox_oldenburg.isChecked() or
            self.checkbox_bielefeld.isChecked()):
            self.beatmung_spontan_label.setVisible(True)
            self.beatmung_spontan_input.setVisible(True)
            self.beatmung_spontan_einheit_label.setVisible(True)
        else:
            self.beatmung_spontan_label.setVisible(False)
            self.beatmung_spontan_input.setVisible(False)
            self.beatmung_spontan_einheit_label.setVisible(False)

            #Motivation + Stimmung
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_hemer.isChecked()):
            self.motivation_label.setVisible(True)
            self.motivation_combo.setVisible(True)
            self.stimmung_label.setVisible(True)
            self.stimmung_combo.setVisible(True)
        else:
            self.motivation_label.setVisible(False)
            self.motivation_combo.setVisible(False)
            self.stimmung_label.setVisible(False)
            self.stimmung_combo.setVisible(False)
            #Aktueller Zustand Patient
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_dortmund.isChecked() or
            self.checkbox_hemer.isChecked() or
            self.checkbox_oldenburg.isChecked()):
            self.current_state_box.setVisible(True)
        else:
            self.current_state_box.setVisible(False)
            #Bewusstsein
        if self.checkbox_dortmund_luenen.isChecked():
            self.consciousness_label.setVisible(True)
            self.consciousness_combo.setVisible(True)
        else:
            self.consciousness_label.setVisible(False)
            self.consciousness_combo.setVisible(False)
            #Pflegebedürftigkeit
        if self.checkbox_dortmund_luenen.isChecked():
            self.pflegebeduerftigkeit_label.setVisible(True)
            self.pflegebeduerftigkeit_combo.setVisible(True)
        else:
            self.pflegebeduerftigkeit_label.setVisible(False)
            self.pflegebeduerftigkeit_combo.setVisible(False)
            #Mobilisation
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_oldenburg.isChecked()):
            self.mobilisation_label.setVisible(True)
            self.mobilisation_combo.setVisible(True)
        else:
            self.mobilisation_label.setVisible(False)
            self.mobilisation_combo.setVisible(False)
            #VP
        if self.checkbox_dortmund_luenen.isChecked():
            self.vp_gruppe.setVisible(True)
        else:
            self.vp_gruppe.setVisible(False)
            #Stuhlinkontinenz
        if self.checkbox_dortmund_luenen.isChecked():
            self.darminkontinenz_label.setVisible(True)
            self.darminkontinenz_combo.setVisible(True)
        else:
            self.darminkontinenz_label.setVisible(False)
            self.darminkontinenz_combo.setVisible(False)
            #HIT ST
        if self.checkbox_dortmund_luenen.isChecked():
            self.labor_line4_gruppe.setVisible(True)
        else:
            self.labor_line4_gruppe.setVisible(False)
            #Infektionsserologie
        if (self.checkbox_dortmund_luenen.isChecked() or
            self.checkbox_soest.isChecked()):
            self.infektionsserologie_gruppe.setVisible(True)
        else:
            self.infektionsserologie_gruppe.setVisible(False)
            

#boxvis
    def updateLaborValuesVisibility(self):
    # Liste der gemeinsamen Laborwerte
        common_lab_values = {
            "krea": [
                self.checkbox_dortmund_luenen,
                self.checkbox_hemer,
                self.checkbox_bad_lippspringe,
                self.checkbox_schmallenberg,
                self.checkbox_bielefeld,
                self.checkbox_haltern,
                self.checkbox_ibbenbueren,
                self.checkbox_dortmund
            ],
            "crp": [
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_vest,
                self.checkbox_hemer,
                self.checkbox_haltern,
                self.checkbox_bad_lippspringe,
                self.checkbox_schmallenberg,
                self.checkbox_bielefeld
            ],
            "gpt": [
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren, 
                self.checkbox_hemer
            ],
            "got": [
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren
            ],
            "na": [
                self.checkbox_dortmund_luenen,
                self.checkbox_ibbenbueren,
                self.checkbox_hemer
            ],
            "harnstoff": [
                self.checkbox_dortmund_luenen,
                self.checkbox_ibbenbueren,
                self.checkbox_hemer,
                self.checkbox_bad_lippspringe,
                self.checkbox_schmallenberg
            ],
            "leuko": [
                self.checkbox_ibbenbueren,
                self.checkbox_hemer,
                self.checkbox_bad_lippspringe,
                self.checkbox_bielefeld
            ],
            "pct": [
                self.checkbox_ibbenbueren,
                self.checkbox_bielefeld
            ],
            "bnp": [
                self.checkbox_ibbenbueren,
                self.checkbox_bad_lippspringe
            ],
            "gfr": [
                self.checkbox_bielefeld
            ],
            "hkt": [
                self.checkbox_schmallenberg
            ],
            "bili": [
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_hemer
            ],
            "k": [
                self.checkbox_vest,
                self.checkbox_bielefeld,
                self.checkbox_hemer, 
                self.checkbox_ibbenbueren,
                self.checkbox_dortmund_luenen
            ],
            "thrombo": [
                self.checkbox_hemer,
                self.checkbox_ibbenbueren
            ],
            
            "quick": [self.checkbox_ibbenbueren],
            "ptt": [self.checkbox_ibbenbueren],
            "inr": [self.checkbox_ibbenbueren],
            "ggt": [self.checkbox_ibbenbueren],
            "ap": [self.checkbox_ibbenbueren],

            "hco3": [
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_soest,
                self.checkbox_oldenburg,
                self.checkbox_schmallenberg
            ],
            "be": [
                self.checkbox_soest,
                self.checkbox_hemer,
                self.checkbox_oldenburg,
                self.checkbox_bielefeld
            ],
            "sao2": [
                self.checkbox_dortmund_luenen,
                self.checkbox_hemer
            ],
            "spitzendruck": [
                self.checkbox_clemens,
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_soest,
                self.checkbox_hemer,
                self.checkbox_bielefeld
            ],
            "peep": [
                self.checkbox_clemens,
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_soest,
                self.checkbox_hemer,
                self.checkbox_bielefeld
            ],
            "atemfrequenz": [
                self.checkbox_clemens,
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_hemer,
                self.checkbox_bielefeld
            ],
            "fio2": [
                self.checkbox_clemens,
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_vest,
                self.checkbox_soest,
                self.checkbox_hemer,
                self.checkbox_oldenburg,
                self.checkbox_haltern,
                self.checkbox_bad_lippspringe,
                self.checkbox_bielefeld
            ],
            "tinsp": [
                self.checkbox_ibbenbueren,
                self.checkbox_hemer,
                self.checkbox_bielefeld
            ],
            "izue": [
                self.checkbox_ibbenbueren,
                self.checkbox_hemer
            ],
            "modus": [
                self.checkbox_clemens,
                self.checkbox_dortmund_luenen,
                self.checkbox_dortmund,
                self.checkbox_ibbenbueren,
                self.checkbox_vest,
                self.checkbox_koeln,
                self.checkbox_essen,
                self.checkbox_soest,
                self.checkbox_hemer,
                self.checkbox_bad_lippspringe,
                self.checkbox_schmallenberg,
                self.checkbox_bielefeld
            ],
        }

        # Aktualisierung der Sichtbarkeit für jeden Laborwert
        for lab_value, checkboxes in common_lab_values.items():
            visible = any(checkbox.isChecked() for checkbox in checkboxes)
            getattr(self, f"{lab_value}_input").setVisible(visible)
            getattr(self, f"{lab_value}_label").setVisible(visible)

    def update_age_and_gfr(self):
        self.calculateAge()
        self.update_gfr()
        
    def calculateAge(self):
        current_date = QDate.currentDate()
        birthdate_str = self.birthdate_input.text()
        birthdate = QDate.fromString(birthdate_str, 'dd.MM.yyyy')
        if birthdate.isValid():
            age = birthdate.daysTo(current_date) // 365
            self.age_input.setText(str(age))
            return age
        else:
            self.age_input.setText("")
            return 0
        
    def enteral_kcal(self):
        kcal_werte = {
            0: 1.0,
            1: 1.5,
            2: 2.0,
        }
        ausgewaehlter_index = self.ernaehrung_enteral_combo.currentIndex()
        if ausgewaehlter_index >= 0:
            ausgewaehltes_kcal = kcal_werte[ausgewaehlter_index]
        else:
            ausgewaehltes_kcal = 0

        laufrate_text = self.ernaehrung_enteral_laufrate_input.text()
        laufrate_text = laufrate_text.replace(",", ".")
        if laufrate_text:
            try:
                laufrate = float(laufrate_text)
            except ValueError:
                laufrate = 0
        else:
            laufrate = 0
        kalorien_enteral_24h = ausgewaehltes_kcal * laufrate * 24
        kalorien_enteral_24h = round(kalorien_enteral_24h)
        self.kalorien_enteral.setText(str(kalorien_enteral_24h))

        self.gesamt_kcal()

    def parenteral_kcal(self):

        # Variablen zur Speicherung der Kalorien pro Komponente
        kcal_nutriLP = 0
        kcal_glc40 = 0
        kcal_as = 0
        kcal_lipid_plus = 0

        # Berechne Kalorien für Nutriflex Lipid Plus
        if self.ernaehrung_parenteral_combo.currentText() == 'Nutriflex Lipid Plus':
            try:
                nutriLP_laufrate = float(self.ernaehrung_parenteral_nutriLP_laufrate_input.text())
                kcal_nutriLP = nutriLP_laufrate * 1.01
            except ValueError:
                nutriLP_laufrate = 0
                kcal_nutriLP = 0

        # Berechne Kalorien für Nutriflex + AS
        elif self.ernaehrung_parenteral_combo.currentText() == 'Nutriflex + AS':
            try:
                nutriLP_laufrate = float(self.ernaehrung_parenteral_nutriLP_laufrate_input.text())
                as_laufrate = float(self.ernaehrung_parenteral_as_laufrate_input.text())
                kcal_nutriLP = nutriLP_laufrate * 1.01
                kcal_as = as_laufrate * 0.4
            except ValueError:
                nutriLP_laufrate = 0
                as_laufrate = 0
                kcal_glc40 = 0
                kcal_as = 0

        # Berechne Kalorien für Drei-Komponenten
        elif self.ernaehrung_parenteral_combo.currentText() == 'Drei-Komponenten':
            try:
                glc40_laufrate = float(self.ernaehrung_parenteral_glc40_laufrate_input.text())
                as_laufrate = float(self.ernaehrung_parenteral_as_laufrate_input.text())
                lipid_plus_laufrate = float(self.ernaehrung_parenteral_lipid_plus_laufrate_input.text())
                kcal_glc40 = glc40_laufrate * 1.6
                kcal_as = as_laufrate * 0.4
                kcal_lipid_plus = lipid_plus_laufrate * 1
            except ValueError:
                lipid_plus_laufrate = 0
                glc40_laufrate = 0
                as_laufrate = 0
                kcal_glc40 = 0
                kcal_as = 0
                kcal_lipid_plus = 0

        # Berechne Gesamtkcalorien
        kalorien_parenteral_24h = (kcal_nutriLP + kcal_glc40 + kcal_as + kcal_lipid_plus)*24
        kalorien_parenteral_24h = round(kalorien_parenteral_24h)


        # Trage Kalorien ins Feld ein
        self.kalorien_parenteral.setText(str(kalorien_parenteral_24h))

        self.gesamt_kcal()

    def gesamt_kcal(self):

        # Berechne Gesamtkcalorien
        kalorien_gesamt = float(self.kalorien_parenteral.text()) + float(self.kalorien_enteral.text())
        kalorien_gesamt = round(kalorien_gesamt)

        # Trage Kalorien ins Feld ein
        self.kalorien_gesamt.setText(str(kalorien_gesamt))

    
    def update_gfr(self):
        try:
            creatinine_str = self.krea_input.text().replace(',', '.')  # Ersetze das Komma durch einen Punkt
            creatinine = float(creatinine_str)
            
            if creatinine <= 0:
                raise ValueError("Kreatinin muss größer als 0 sein")
            
            age = self.calculateAge()  # Alter basierend auf dem Geburtsdatum neu berechnen
            sex = self.gender_combo.currentText()
            is_afro_american = False  # Immer "weiß", daher False
            
            k = 0.7 if sex == 'weiblich' else 0.9
            a = -0.329 if sex == 'weiblich' else -0.411
            min_creatinine_k_ratio = min(creatinine / k, 1)
            max_creatinine_k_ratio = max(creatinine / k, 1)
            
            gfr = 141 * min_creatinine_k_ratio ** a * max_creatinine_k_ratio ** (-1.209) * 0.993 ** age
            
            if is_afro_american:
                gfr *= 1.159
            
            self.gfr_input.setText(f"{gfr:.2f}")
        except ValueError as e:
            self.gfr_input.setText("")
            

    def updateDays(self, date_input, time_input):
        # Erhalten des aktuellen Datums
        current_date = QDate.currentDate()
        
        # Abrufen des Datums aus dem QLineEdit-Feld und Konvertieren in ein QDate-Objekt
        date_str = date_input.text()
        date = QDate.fromString(date_str, 'dd.MM.yyyy')

        # Berechnen der Differenz zwischen dem aktuellen Datum und dem Datum des Einfügens des Katheters
        if date.isValid():
            days_difference = date.daysTo(current_date)
            time_input.setText(str(days_difference))
        else:
            time_input.setText("")

    def update_airway_days_text(self):
        self.airway_days_text.setText(self.airway_days_input.text())
        self.airway_days_label.setVisible(True)

    def update_tk_days_text(self):
        self.tk_days_text.setText(self.tk_days_input.text())
        self.tk_days_label.setVisible(True)
    
    def update_artery_time_text(self):
        self.artery_time_text.setText(self.artery_time_input.text())
        self.artery_time_label.setVisible(True)

    def update_cvc_time_text(self):
        self.cvc_time_text.setText(self.cvc_time_input.text())
        self.cvc_time_label.setVisible(True)

    def update_bladder_time_text(self):
        self.bladder_time_text.setText(self.bladder_time_input.text())
        self.bladder_time_label.setVisible(True)

    def update_magensonde_time_text(self):
        self.magensonde_time_text.setText(self.magensonde_time_input.text())
        self.magensonde_time_label.setVisible(True)


    def toggle_trachealkanule(self, text):
        if text == 'Trachealkanüle':
            self.tk_date_label.setVisible(True)
            self.tk_date_input.setVisible(True)
            self.tk_days_text.setVisible(True)
        else:
            self.tk_date_label.setVisible(False)
            self.tk_date_input.setVisible(False)
            self.tk_days_label.setVisible(False)
            self.tk_days_text.setVisible(False)

    def toggle_c19_negtest_date(self, text):
        if text == 'aktuell negativ':
            self.c19_negtest_date_input.setVisible(True)
            self.c19_verdacht_combo.setVisible(True)
            self.c19_verdacht_label.setVisible(True)
            self.checkbox_znc19.setVisible(True)
        else:
            self.c19_negtest_date_input.setVisible(False)
            self.c19_verdacht_combo.setVisible(False)
            self.c19_verdacht_label.setVisible(False)
            self.checkbox_znc19.setVisible(False)
            


    def toggle_ct_wert(self, text):
        text = self.c19_combo.currentText()
        if text == 'aktuell positiv' and self.checkbox_schmallenberg.isChecked():
            self.ctwert_label.setVisible(True)
            self.ctwert_input.setVisible(True)
        else:
            self.ctwert_label.setVisible(False)
            self.ctwert_input.setVisible(False)

    def toggle_c19_verdacht(self, text):
        text = self.c19_combo.currentText()
        if text == 'aktuell negativ' and self.checkbox_hemer.isChecked():
            self.c19_verdacht_combo.setVisible(True)
            self.c19_verdacht_label.setVisible(True)
        else:
            self.c19_verdacht_combo.setVisible(False)
            self.c19_verdacht_label.setVisible(False)

    def toggle_cdiff(self, state):
        if state == Qt.Checked:
            self.cdiff_date_input.setVisible(True)
        else:
            self.cdiff_date_input.setVisible(False)
            self.cdiff_date_input.clear()

    def update_betreuung_name_label(self):
        text = self.next_of_kin_input.text()
        self.betreuung_name_label.setText('Ist der/die Betreuer(in) ' + text + '?')

    def toggle_betreuung(self):
        index1 = self.betreuung_combo.currentIndex()
        index2 = self.betreuung_name_combo.currentIndex()
        if index1 == 0:
            self.betreuung_name_label.setVisible(True)
            self.betreuung_name_combo.setVisible(True)
        else:
            self.betreuung_name_label.setVisible(False)
            self.betreuung_name_combo.setVisible(False)
            self.betreuung_name2_label.setVisible(False)
            self.betreuung_name2_input.setVisible(False)
            self.betreuung_name2_tel_label.setVisible(False)
            self.betreuung_name2_tel_input.setVisible(False)
            self.betreuung_name2_input.clear()
            self.betreuung_name2_tel_input.clear()
        if index2 == 1:
            self.betreuung_name2_label.setVisible(True)
            self.betreuung_name2_input.setVisible(True)
            self.betreuung_name2_tel_label.setVisible(True)
            self.betreuung_name2_tel_input.setVisible(True)
        else:
            self.betreuung_name2_label.setVisible(False)
            self.betreuung_name2_input.setVisible(False)
            self.betreuung_name2_tel_label.setVisible(False)
            self.betreuung_name2_tel_input.setVisible(False)
            self.betreuung_name2_input.clear()
            self.betreuung_name2_tel_input.clear()
    


    def clearAll(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            if isinstance(widget, QtWidgets.QComboBox):
                widget.setCurrentIndex(-1)
            elif isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QTextEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QCheckBox): 
                widget.setChecked(False)  

    def makeAllVisible(self):
        checkboxes = [
            self.checkbox_clemens, 
            self.checkbox_dortmund_luenen, 
            self.checkbox_dortmund, 
            self.checkbox_ibbenbueren,
            self.checkbox_vest, 
            self.checkbox_koeln, 
            self.checkbox_essen, 
            self.checkbox_soest,
            self.checkbox_hemer, 
            self.checkbox_bad_lippspringe, 
            self.checkbox_schmallenberg, 
            self.checkbox_bielefeld,
            self.checkbox_haltern, 
            self.checkbox_oldenburg
        ]
        
        for checkbox in checkboxes:
            checkbox.setChecked(not checkbox.isChecked())

    def on_checkbox_state_changed(self, checkbox):
        # Überprüfen, welcher CheckBox aktiviert wurde und deaktivieren Sie die entsprechende gegensätzliche CheckBox
        if checkbox.isChecked():
            if checkbox == self.checkbox_hivpos:
                self.checkbox_hivneg.setChecked(False)
            elif checkbox == self.checkbox_hivneg:
                self.checkbox_hivpos.setChecked(False)
            elif checkbox == self.checkbox_hbsagpos:
                self.checkbox_hbsagneg.setChecked(False)
            elif checkbox == self.checkbox_hbsagneg:
                self.checkbox_hbsagpos.setChecked(False)
            elif checkbox == self.checkbox_hcvpos:
                self.checkbox_hcvneg.setChecked(False)
            elif checkbox == self.checkbox_hcvneg:
                self.checkbox_hcvpos.setChecked(False)


    def fillWithTestData(self):

        #Statdoc
        self.station_combo.setCurrentText("Station 22")
        self.doctor_input.setText("Dr. Maxi Mustermann")
        # Persönliche Informationen
        self.lastname_input.setText("Mustermann")
        self.firstname_input.setText("Max")
        self.birthdate_input.setText("01.01.1980")
        self.gender_combo.setCurrentText("männlich")

        # Körperliche Daten
        self.height_input.setText("180")
        self.weight_input.setText("120")

        # Adresse
        self.street_input.setText("Musterstraße 123")
        self.plz_input.setText("12345")
        self.city_input.setText("Musterstadt")

        # Medizinische Informationen
        self.general_practitioner_input.setText("Dr. Maria Musterfrau")
        self.next_of_kin_input.setText("Maria Mustermann")
        self.next_of_kin_tel_input.setText("0123456789")
        self.job_input.setText("Softwareentwickler")
        self.insurance_input.setText("Techniker")

        # Medizinische Historie
        self.atemweg_combo.setCurrentText("Trachealkanüle")
        self.airway_date_input.setText("01.01.2024")
        self.airway_dg_input.setText("COVID-19")
        self.tk_date_input.setText("15.01.2024")
        self.artery_combo.setCurrentText("Radialis re.")
        self.artery_date_input.setText("01.02.2024")
        self.cvc_combo.setCurrentText("V. jugularis int. re.")
        self.lumen_combo.setCurrentText("2-lumig")
        self.cvc_date_input.setText("10.02.2024")
        self.bladder_combo.setCurrentText("Suprapubischer DK")
        self.bladder_date_input.setText("05.01.2024")
        self.magensonde_combo.setCurrentText("PEG")
        self.magensonde_date_input.setText("01.02.2024")

        # Mibi
        self.mibi_input_current.setText("Ceftriaxon 2g i.v. alle 24h")
        self.mibi_input_previous.setText("Flucloxacillin 2g i.v. alle 6h")

        #Resistente Erreger
        self.checkbox_vre1.setChecked(True)
        self.checkbox_3mrgn.setChecked(True)
        self.checkbox_mrsa1.setChecked(True)
        self.checkbox_cdiff.setChecked(True)

        # Medizinischer Erregernachweis
        self.erregernachweis_input.setText("S. aureus im Blutkulturflasche vom 01.01.2024 <br> E. coli im Urin vom 01.01.2024")
        self.cdiff_date_input.setText("01.02.2024")

        # Laborwerte
        self.hb_input.setText("12.5")
        self.hkt_input.setText("40")
        self.leuko_input.setText("8.5")
        self.crp_input.setText("5.0")
        self.pct_input.setText("0.5")
        self.quick_input.setText("100")
        self.inr_input.setText("1.0")
        self.ptt_input.setText("30")
        self.thrombo_input.setText("200")
        self.harnstoff_input.setText("20")
        self.krea_input.setText("1.0")
        self.bili_input.setText("1.0")
        self.got_input.setText("20")
        self.gpt_input.setText("25")
        self.ap_input.setText("100")
        self.ggt_input.setText("30")
        self.na_input.setText("140")
        self.k_input.setText("4.0")
        self.bnp_input.setText("100")

        # BGA
        self.ph_input.setText("7.4")
        self.po2_input.setText("100")
        self.sao2_input.setText("98")
        self.pco2_input.setText("40")
        self.hco3_input.setText("24")
        self.be_input.setText("0")

        #Ventilation
        self.modus_input.setText("BIPAP")
        self.spitzendruck_input.setText("20")
        self.atemfrequenz_input.setText("14")
        self.izue_input.setText("1:2")
        self.tinsp_input.setText("1.5")
        self.peep_input.setText("10")
        self.fio2_input.setText("30")

        #Vorerkrankungen
        self.checkbox_aht.setChecked(True)
        self.checkbox_dm.setChecked(True)
        self.checkbox_khk.setChecked(True)
        self.checkbox_herzinsuff.setChecked(True)
        self.checkbox_pulmht.setChecked(True)
        self.checkbox_cni.setChecked(True)
        self.checkbox_ani.setChecked(True)
        self.checkbox_dialyse.setChecked(True)
        self.dialyse_combo.setCurrentIndex(1)
        self.checkbox_pavk.setChecked(True)
        self.checkbox_copd.setChecked(True)
        self.checkbox_asthma.setChecked(True)
        self.checkbox_nikotin.setChecked(True)
        self.checkbox_alkohol.setChecked(True)
        self.checkbox_apoplex.setChecked(True)
        self.checkbox_neuromusk.setChecked(True)
        self.checkbox_cip.setChecked(True)
        self.checkbox_cim.setChecked(True)
        self.checkbox_interstit.setChecked(True)
        self.checkbox_thorakorestr.setChecked(True)
        self.checkbox_pneumonie.setChecked(True)
        self.checkbox_osas.setChecked(True)
        self.nikotin_py_textinput.setText("20")

        #Medikamente

        self.katecholamine_combo.setCurrentText("ja")
        self.katecholamine_checkbox1.setChecked(True)
        self.noradrenalin_laufrate.setText("2")
        self.sedierung_checkbox3.setChecked(True)
        self.fenta_laufrate_input.setText("12,5")
        self.ernaehrung_checkbox1.setChecked(True)
        self.ernaehrung_parenteral_combo.setCurrentIndex(0)
        self.ernaehrung_parenteral_nutriLP_laufrate_input.setText("42")
        self.ernaehrung_checkbox2.setChecked(True)
        self.ernaehrung_enteral_combo.setCurrentIndex(0)
        self.ernaehrung_enteral_laufrate_input.setText("20")
        self.medplan.setText("ASS 100 mg p.o. 1-0-0<br>Atorvastatin 40 mg p.o. 0-0-1<br>Metoprolol 50 mg p.o. 1-0-1<br>Ramipril 5 mg p.o. 1-0-0<br>Pantoprazol 20 mg p.o. 1-0-0<br>Metformin 500 mg p.o. 1-0-1<br>Simvastatin 20 mg p.o. 0-0-1<br>Amlodipin 5 mg p.o. 1-0-0")

        #Betreuung

        self.betreuung_combo.setCurrentText("nein")
        self.vorsorgevollmacht_combo.setCurrentText("nein")
        self.versorgungzuhause_combo.setCurrentIndex(1)
        self.az_combo.setCurrentIndex(2)
        self.verfuegung_combo.setCurrentText("ja") 

        #Station seit
        self.stat_time_input.setText("15.02.2024")
        self.kh_time_input.setText("05.02.2024")
        self.kh_dg_input.setText("Akute Cholezystitis")

        #Weaning
        self.ext_versuche_input.setText("3")
        self.ext_versuche_wann_input.setText("immer mal wieder")
        self.weaning_method_input.setText("diskontinuierlich")
        self.scheitern_input.setText("Delir")
        self.motivation_combo.setCurrentIndex(0)
        self.stimmung_combo.setCurrentIndex(0)
        self.beatmung_maschinell_input.setText("20")
        self.beatmung_spontan_input.setText("4")

        #Aktueller Zustand des Patienten
        self.pflegebeduerftigkeit_combo.setCurrentIndex(2)
        self.mobilisation_combo.setCurrentIndex(0)
        self.consciousness_combo.setCurrentIndex(0)
        
        #VP
        self.rr_syst_input.setText("120")
        self.rr_diast_input.setText("80")
        self.hf_input.setText("73")

        #Infektionsserologie

        self.checkbox_hbsagpos.setChecked(True)
        self.checkbox_hcvpos.setChecked(True)
        self.checkbox_hivneg.setChecked(True)

        #Dekubitus


        self.dekubitus_combo.setCurrentText("ja")
        self.dekubitus_lokalisation_combo.setCurrentText("Sakral")
        self.dekubitus_grad_combo.setCurrentText("1")
        
#tdtd

    def fillWithTestDataBasic(self):

        #Statdoc
        self.station_combo.setCurrentText("Station 22")
        self.doctor_input.setText("Dr. Stefan Braune")
        # Persönliche Informationen
        self.lastname_input.setText("Mustermann")
        self.firstname_input.setText("Max")
        self.birthdate_input.setText("01.01.1980")
        self.gender_combo.setCurrentText("männlich")

        # Körperliche Daten
        self.height_input.setText("180")
        self.weight_input.setText("80")

        #Atemweg
        self.atemweg_combo.setCurrentText("Trachealkanüle")
        self.airway_dg_input.setText("COVID-19")
        self.airway_date_input.setText("01.02.2024")
        self.tk_date_input.setText("15.02.2024")

    
    def calculateBMI(self):
        # Extrahieren der Eingabewerte
        height = self.height_input.text().strip()
        weight = self.weight_input.text().strip()
        try:
            height_m = float(height) / 100  # Umwandlung in Meter
            weight_kg = float(weight)
            bmi = weight_kg / (height_m ** 2)
            if bmi >= 30:
                self.adipositas_combo.setCurrentIndex(self.adipositas_combo.findText('ja'))
            else:
                self.adipositas_combo.setCurrentIndex(self.adipositas_combo.findText('nein'))
            return bmi
        except ValueError:
            return None

    def updateAdipositasText(self):
        bmi = self.calculateBMI()
        if bmi is not None:
            bmi_text = f" (BMI {bmi:.2f})"
            self.adipositas_input.setText(f"{bmi:.2f}")
            if bmi < 18.5:
                self.adipositas_text.setText(f"Untergewicht{bmi_text}")
            elif 18.5 <= bmi < 25:
                self.adipositas_text.setText(f"Normalgewicht{bmi_text}")
            elif 25 <= bmi < 30:
                self.adipositas_text.setText(f"Übergewicht{bmi_text}")
            elif 30 <= bmi < 35:
                self.adipositas_text.setText(f"Adipositas Grad I{bmi_text}")
            elif 35 <= bmi < 40:
                self.adipositas_text.setText(f"Adipositas Grad II{bmi_text}")
            else:  # BMI >= 40
                self.adipositas_text.setText(f"Adipositas Grad III{bmi_text}")
        else:
            self.adipositas_text.setText("")


    def update_label(self):
        checkbox = self.sender()
        if checkbox.isChecked():
            if checkbox == self.checkbox_aht:
                self.aht_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_khk:
                self.khk_label.setText("KHK, ")
            elif checkbox == self.checkbox_herzinsuff:
                self.herzinsuff_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_pulmht:
                self.pulmht_label.setText("pulm. HT, ")
            elif checkbox == self.checkbox_pavk:
                self.pavk_label.setText("pAVK, ")
            elif checkbox == self.checkbox_dm:
                self.dm_label.setText("DM, ")
            elif checkbox == self.checkbox_hypothyreose:
                self.hypothyreose_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_hyperthyreose:
                self.hyperthyreose_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_apoplex:
                self.apoplex_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_delir:
                self.delir_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_cip:
                self.cip_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_cim:
                self.cim_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_cni:
                self.cni_label.setText("chron. NI, ")
            elif checkbox == self.checkbox_ani:
                self.ani_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_dialyse:
                self.dialyse_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_asthma:
                self.asthma_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_copd:
                self.copd_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_pneumonie:
                self.pneumonie_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_interstit:
                self.interstit_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_osas:
                self.osas_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_thorakorestr:
                self.thorakorestr_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_nikotin:
                self.nikotin_label.setText(checkbox.text())
            elif checkbox == self.checkbox_alkohol:
                self.alkohol_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_neuromusk:
                self.neuromusk_label.setText(checkbox.text())
            elif checkbox == self.checkbox_vre1:
                self.vre1_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_vre2:
                self.vre2_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_mrsa1:
                self.mrsa1_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_mrsa2:
                self.mrsa2_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_3mrgn:
                self.mrgn3_label.setText(checkbox.text() + ", ")
            elif checkbox == self.checkbox_4mrgn:
                self.mrgn4_label.setText(checkbox.text() + ", ")
        else:
            if checkbox == self.checkbox_aht:
                self.aht_label.setText('')
            elif checkbox == self.checkbox_khk:
                self.khk_label.setText('')
            elif checkbox == self.checkbox_herzinsuff:
                self.herzinsuff_label.setText('')
            elif checkbox == self.checkbox_pulmht:
                self.pulmht_label.setText('')
            elif checkbox == self.checkbox_pavk:
                self.pavk_label.setText('')
            elif checkbox == self.checkbox_dm:
                self.dm_label.setText('')
            elif checkbox == self.checkbox_hypothyreose:
                self.hypothyreose_label.setText('')
            elif checkbox == self.checkbox_hyperthyreose:
                self.hyperthyreose_label.setText('')
            elif checkbox == self.checkbox_apoplex:
                self.apoplex_label.setText('')
            elif checkbox == self.checkbox_delir:
                self.delir_label.setText('')
            elif checkbox == self.checkbox_cip:
                self.cip_label.setText('')
            elif checkbox == self.checkbox_cim:
                self.cim_label.setText('')
            elif checkbox == self.checkbox_cni:
                self.cni_label.setText('')
            elif checkbox == self.checkbox_ani:
                self.ani_label.setText('')
            elif checkbox == self.checkbox_dialyse:
                self.dialyse_label.setText('')
            elif checkbox == self.checkbox_asthma:
                self.asthma_label.setText('')
            elif checkbox == self.checkbox_copd:
                self.copd_label.setText('')
            elif checkbox == self.checkbox_pneumonie:
                self.pneumonie_label.setText('')
            elif checkbox == self.checkbox_interstit:
                self.interstit_label.setText('')
            elif checkbox == self.checkbox_osas:
                self.osas_label.setText('')
            elif checkbox == self.checkbox_thorakorestr:
                self.thorakorestr_label.setText('')
            elif checkbox == self.checkbox_nikotin:
                self.nikotin_label.setText('')
            elif checkbox == self.checkbox_alkohol:
                self.alkohol_label.setText('')
            elif checkbox == self.checkbox_neuromusk:
                self.neuromusk_label.setText('')
            elif checkbox == self.checkbox_vre1:
                self.vre1_label.setText('')
            elif checkbox == self.checkbox_vre2:
                self.vre2_label.setText('')
            elif checkbox == self.checkbox_mrsa1:
                self.mrsa1_label.setText('')
            elif checkbox == self.checkbox_mrsa2:
                self.mrsa2_label.setText('')
            elif checkbox == self.checkbox_3mrgn:
                self.mrgn3_label.setText('')
            elif checkbox == self.checkbox_4mrgn:
                self.mrgn4_label.setText('')

    def update_medikationcheckboxes(self):
        checkbox = self.sender()
        if checkbox.isChecked():
            if checkbox == self.sedierung_checkbox1:
                self.propofol_laufrate_input.setVisible(True) 
                self.propofol_laufrate_einheit.setVisible(True)
                self.propofol_text.setText('Propofol 2%')
            elif checkbox == self.sedierung_checkbox2:
                self.sufenta_laufrate_input.setVisible(True) 
                self.sufenta_laufrate_einheit.setVisible(True)
                self.sufenta_text.setText('Sufentanil 5µg/ml')
            elif checkbox == self.sedierung_checkbox3:
                self.fenta_laufrate_input.setVisible(True) 
                self.fenta_laufrate_einheit.setVisible(True)
                self.fenta_text.setText('Fentanyl Pfaster')
            elif checkbox == self.sedierung_checkbox4:
                self.midazolam_laufrate_input.setVisible(True) 
                self.midazolam_laufrate_einheit.setVisible(True)
                self.midazolam_text.setText('Midazolam 2mg/ml')
            elif checkbox == self.sedierung_checkbox5:
                self.dexdor_laufrate_input.setVisible(True) 
                self.dexdor_laufrate_einheit.setVisible(True)
                self.dexdor_text.setText('Dexdometomidin XXX?')
            elif checkbox == self.sedierung_checkbox6:
                self.ketamin_laufrate_input.setVisible(True) 
                self.ketamin_laufrate_einheit.setVisible(True)
                self.ketamin_text.setText('Ketamin XXX?')
            elif checkbox == self.katecholamine_checkbox1:
                self.noradrenalin_laufrate.setVisible(True)
                self.noradrenalin_laufrate_einheit.setVisible(True)
                self.noradrenalin_text.setText('Noradrenalin 0,1 mg/ml')
            elif checkbox == self.katecholamine_checkbox2:
                self.adrenalin_laufrate.setVisible(True)
                self.adrenalin_laufrate_einheit.setVisible(True)
                self.adrenalin_text.setText('Adrenalin 0,1 mg/ml')
            elif checkbox == self.katecholamine_checkbox3:
                self.dobutamin_laufrate.setVisible(True)
                self.dobutamin_laufrate_einheit.setVisible(True)
                self.dobutamin_text.setText('Dobutamin XXX?')
            elif checkbox == self.ernaehrung_checkbox1:
                self.ernaehrung_parenteral_combo.setVisible(True)
            elif checkbox == self.ernaehrung_checkbox2:
                self.ernaehrung_enteral_combo.setVisible(True)
                self.ernaehrung_enteral_laufrate_input.setVisible(True)
                self.ernaehrung_enteral_laufrate_einheit.setVisible(True)
        else:
            if checkbox == self.sedierung_checkbox1:
                self.propofol_laufrate_input.setVisible(False)  
                self.propofol_laufrate_einheit.setVisible(False)
                self.propofol_text.setText('')
            elif checkbox == self.sedierung_checkbox2:
                self.sufenta_laufrate_input.setVisible(False)  
                self.sufenta_laufrate_einheit.setVisible(False)
                self.sufenta_text.setText('')
            elif checkbox == self.sedierung_checkbox3:
                self.fenta_laufrate_input.setVisible(False)  
                self.fenta_laufrate_einheit.setVisible(False)
                self.fenta_text.setText('')
            elif checkbox == self.sedierung_checkbox4:
                self.midazolam_laufrate_input.setVisible(False)  
                self.midazolam_laufrate_einheit.setVisible(False)
                self.midazolam_text.setText('')
            elif checkbox == self.sedierung_checkbox5:
                self.dexdor_laufrate_input.setVisible(False)  
                self.dexdor_laufrate_einheit.setVisible(False)
                self.dexdor_text.setText('')
            elif checkbox == self.sedierung_checkbox6:
                self.ketamin_laufrate_input.setVisible(False)  
                self.ketamin_laufrate_einheit.setVisible(False) 
                self.ketamin_text.setText('') 
            elif checkbox == self.katecholamine_checkbox1:
                self.noradrenalin_laufrate.setVisible(False)
                self.noradrenalin_laufrate_einheit.setVisible(False)
                self.noradrenalin_text.setText('')
            elif checkbox == self.katecholamine_checkbox2:
                self.adrenalin_laufrate.setVisible(False)
                self.adrenalin_laufrate_einheit.setVisible(False)
                self.adrenalin_text.setText('')
            elif checkbox == self.katecholamine_checkbox3:
                self.dobutamin_laufrate.setVisible(False)
                self.dobutamin_laufrate_einheit.setVisible(False)
                self.dobutamin_text.setText('')
            elif checkbox == self.ernaehrung_checkbox1:
                self.ernaehrung_parenteral_combo.setVisible(False)
                self.ernaehrung_parenteral_combo.setCurrentIndex(-1)
                self.ernaehrung_parenteral_nutriLP_label.setVisible(False)
                self.ernaehrung_parenteral_nutriLP_laufrate_input.setVisible(False)
                self.ernaehrung_parenteral_nutriLP_laufrate_input.setText('0')
                self.ernaehrung_parenteral_nutriLP_laufrate_einheit.setVisible(False)
                self.ernaehrung_parenteral_as_label.setVisible(False)
                self.ernaehrung_parenteral_as_laufrate_input.setVisible(False)
                self.ernaehrung_parenteral_as_laufrate_input.setText('0')
                self.ernaehrung_parenteral_as_laufrate_einheit.setVisible(False)
                self.ernaehrung_parenteral_lipid_plus_label.setVisible(False)
                self.ernaehrung_parenteral_lipid_plus_laufrate_input.setVisible(False)
                self.ernaehrung_parenteral_lipid_plus_laufrate_input.setText('0')
                self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.setVisible(False)
                self.ernaehrung_parenteral_glc40_label.setVisible(False)
                self.ernaehrung_parenteral_glc40_laufrate_input.setVisible(False)
                self.ernaehrung_parenteral_glc40_laufrate_input.setText('0')
                self.ernaehrung_parenteral_glc40_laufrate_einheit.setVisible(False)
            elif checkbox == self.ernaehrung_checkbox2:
                self.ernaehrung_enteral_combo.setVisible(False)
                self.ernaehrung_enteral_combo.setCurrentIndex(-1)
                self.ernaehrung_enteral_laufrate_input.setVisible(False)
                self.ernaehrung_enteral_laufrate_input.setText('')
                self.ernaehrung_enteral_laufrate_einheit.setVisible(False)

    def update_medikationcombos(self, index):
        index = self.ernaehrung_parenteral_combo.currentIndex()
        if index == 0: # nur NutriFlex
            self.ernaehrung_parenteral_nutriLP_label.setVisible(True)
            self.ernaehrung_parenteral_nutriLP_laufrate_input.setVisible(True)
            self.ernaehrung_parenteral_nutriLP_laufrate_einheit.setVisible(True)
            self.ernaehrung_parenteral_as_label.setVisible(False)
            self.ernaehrung_parenteral_as_laufrate_input.setVisible(False)
            self.ernaehrung_parenteral_as_laufrate_einheit.setVisible(False)
            self.ernaehrung_parenteral_lipid_plus_label.setVisible(False)
            self.ernaehrung_parenteral_lipid_plus_laufrate_input.setVisible(False)
            self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.setVisible(False)
            self.ernaehrung_parenteral_glc40_label.setVisible(False)
            self.ernaehrung_parenteral_glc40_laufrate_input.setVisible(False)
            self.ernaehrung_parenteral_glc40_laufrate_einheit.setVisible(False)
            self.ernaehrung_parenteral_as_laufrate_input.setText('0')
            self.ernaehrung_parenteral_lipid_plus_laufrate_input.setText('0')
            self.ernaehrung_parenteral_glc40_laufrate_input.setText('0')
        elif index == 1: # Nutri + AS
            self.ernaehrung_parenteral_nutriLP_label.setVisible(True)
            self.ernaehrung_parenteral_nutriLP_laufrate_input.setVisible(True)
            self.ernaehrung_parenteral_nutriLP_laufrate_einheit.setVisible(True)
            self.ernaehrung_parenteral_as_label.setVisible(True)
            self.ernaehrung_parenteral_as_laufrate_input.setVisible(True)
            self.ernaehrung_parenteral_as_laufrate_einheit.setVisible(True)
            self.ernaehrung_parenteral_lipid_plus_label.setVisible(False)
            self.ernaehrung_parenteral_lipid_plus_laufrate_input.setVisible(False)
            self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.setVisible(False)
            self.ernaehrung_parenteral_glc40_label.setVisible(False)
            self.ernaehrung_parenteral_glc40_laufrate_input.setVisible(False)
            self.ernaehrung_parenteral_glc40_laufrate_einheit.setVisible(False)
            self.ernaehrung_parenteral_lipid_plus_laufrate_input.setText('0')
            self.ernaehrung_parenteral_glc40_laufrate_input.setText('0')
        elif index == 2: #3 Komponenten
            self.ernaehrung_parenteral_as_label.setVisible(True)
            self.ernaehrung_parenteral_as_laufrate_einheit.setVisible(True)
            self.ernaehrung_parenteral_as_laufrate_input.setVisible(True)
            self.ernaehrung_parenteral_lipid_plus_label.setVisible(True)
            self.ernaehrung_parenteral_lipid_plus_laufrate_input.setVisible(True)
            self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.setVisible(True)
            self.ernaehrung_parenteral_glc40_label.setVisible(True)
            self.ernaehrung_parenteral_glc40_laufrate_input.setVisible(True)
            self.ernaehrung_parenteral_glc40_laufrate_einheit.setVisible(True)
            self.ernaehrung_parenteral_nutriLP_label.setVisible(False)
            self.ernaehrung_parenteral_nutriLP_laufrate_input.setVisible(False)
            self.ernaehrung_parenteral_nutriLP_laufrate_einheit.setVisible(False)
            self.ernaehrung_parenteral_nutriLP_laufrate_input.setText('0')
        

    
    def update_katecholamine_widgets(self, index):
        if index == 1:
            self.katecholamine_subgruppe.setVisible(True)
        else:
            self.katecholamine_subgruppe.setVisible(False)

    def update_Reintub(self):
        self.re_intub_input.setText(self.ext_versuche_input.text())

    def toggle_dekubitus1(self):
        if self.dekubitus_combo.currentText() == 'ja':
            self.dekubitus_lokalisation_label.setVisible(True)
            self.dekubitus_lokalisation_combo.setVisible(True)
            self.dekubitus_lokalisation_combo.setFocus()
#            self.dekubitus_lokalisation_combo.showPopup()
            self.dekubitus_grad_label.setVisible(True)
            self.dekubitus_grad_combo.setVisible(True)
        else:
            self.dekubitus_lokalisation_label.setVisible(False)
            self.dekubitus_lokalisation_combo.setVisible(False)
            self.dekubitus_lokalisation_combo.setCurrentIndex(-1)
            self.dekubitus_grad_label.setVisible(False)
            self.dekubitus_grad_combo.setVisible(False)
            self.dekubitus_grad_combo.setCurrentIndex(-1)
            self.dekubitus_lokalisation_sonstige_input.setVisible(False)

    def toggle_dekubitus2(self):
        if self.dekubitus_lokalisation_combo.currentText() == 'Sonstige':
            self.dekubitus_lokalisation_sonstige_input.setVisible(True)
            self.dekubitus_lokalisation_sonstige_input.setFocus()
        else:
            self.dekubitus_lokalisation_sonstige_input.setVisible(False)
       
    
    def submitForm(self):
        X = 'X'
        first_name = self.firstname_input.text()
        last_name = self.lastname_input.text()
        birthdate = self.birthdate_input.text()
        try:
            if not birthdate:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein Geburtsdatum ein.")
                return
            else:
                bd_first_digit = birthdate[0]
                bd_second_digit = birthdate[1]
                bd_third_digit = birthdate[3]
                bd_fourth_digit = birthdate[4]
                bd_fifth_digit = birthdate[6]
                bd_sixth_digit = birthdate[7]
                bd_seventh_digit = birthdate[8]
                bd_eighth_digit = birthdate[9]
        except ValueError:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Geburtsdatum ein.")

        atemweg = self.atemweg_combo.currentText()
        insurance = self.insurance_input.text()
        airway_dg = self.airway_dg_input.text()
        airway_date = self.airway_date_input.text()
        height = self.height_input.text()
        try:
            if not height:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Körpergröße ein.")
                return
            else:
                for h in height:
                    if not h.isdigit():
                        QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine korrekte Körpergröße ein (ganze Zahlen).")
                        return
                    elif len(height) < 3:
                        QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine korrekte Körpergröße ein (ganze Zahlen).")
                        return
                height1 = height[0]
                height2 = height[1]
                height3 = height[2]
        except ValueError:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine korrekte Körpergröße ein.")
        weight = self.weight_input.text()
        try:
            if not weight:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein Körpergewicht ein.")
                return
            else:
                for w in weight:
                    if not w.isdigit():
                        QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Körpergewicht ein (ganze Zahlen).")
                        return
                    elif len(weight) < 2:
                        QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Körpergewicht ein (ganze Zahlen).")
                        return
                weight1 = weight[0]
                weight2 = weight[1]
                if len(weight) == 3:
                    weight3 = weight[2]
                else:
                    weight3 = None
        except ValueError:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Körpergewicht ein.")
        current_date = datetime.now().strftime("%d.%m.%Y")
        cd_first_digit = current_date[0]
        cd_second_digit = current_date[1]
        cd_third_digit = current_date[3]
        cd_fourth_digit = current_date[4]
        cd_fifth_digit = current_date[6]
        cd_sixth_digit = current_date[7]
        cd_seventh_digit = current_date[8]
        cd_eighth_digit = current_date[9]
        age = self.age_input.text()
        sfh ='St. Franziskus-Hospital Münster, Intensivstation'
        sfhklein ='St. Franziskus-Hospital Münster'
        sfhsehrklein ='SFH Münster'
        if self.station_combo.currentText() == 'Station 22':
            its = 'Intensivstation 22'
            tel = '0251 935 1060'
            pflege ='Pflegekräfte Station 22'
            pflegetel ='0251 935 1722'
            fax ='0251 935 3622'
            email ='stephanie.haves@sfh-muenster.de'
            fach = 'chirurgisch/anästhesiologische'
        if self.station_combo.currentText() == 'Station 19':
            its = 'Intensivstation 19'
            tel = '0251 935 1057'
            pflege ='Pflegekräfte Station 19'
            pflegetel ='0251 935 1719'
            fax ='0251 935 3619'                                        ##### hier fehlt noch die richtige Faxnummer
            email = 'innere.med4@sfh-muenster.de'
            fach = 'internistische'
        itsaddr1 ='Hohenzollernring 70'
        itsaddr2 ='48145 Münster'
        itsplz ='48145'
        itsstadt ='Münster'
        sofort ='Sofort'
        doctor = self.doctor_input.text()
        airway_date = self.airway_date_input.text()
        try:
            if not airway_date:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Intubationsdatum ein.")
                return
            else:
                aw_1 = airway_date[0:2]
                aw_2 = airway_date[3:5]
                aw_3 = airway_date[6:10]
        except ValueError:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Intubationsdatum ein.")
        tk_date = self.tk_date_input.text()
        try:
            if not tk_date and atemweg == 'Trachealkanüle':
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Datum der Tracheotomie ein.")
                return
            else:
                tk_1 = tk_date[0:2]
                tk_2 = tk_date[3:5]
                tk_3 = tk_date[6:10]
        except ValueError:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie ein korrektes Datum der Tracheotomie ein.")

        bmi = self.calculateBMI()

        # Einheiten
        weight_value = weight
        weight_unit = 'kg'
        height_value = height
        height_unit = 'cm'
        hb_value = self.hb_input.text()  
        hkt_value = self.hkt_input.text()  
        hb_unit = 'g/dl'  # Einheit für Hämoglobin
        leuko_value = self.leuko_input.text()
        leuko_unit = '/µL'
        crp_value = self.crp_input.text()
        crp_unit = 'mg/L'
        pct_value = self.pct_input.text()
        pct_unit = '%'
        quick_value = self.quick_input.text()
        quick_unit = '%'
        ptt_value = self.ptt_input.text()
        ptt_unit = 's'
        inr_value = self.inr_input.text()
        inr_unit = ''
        thrombo_value = self.thrombo_input.text()
        thrombo_unit = 'Tsd/µL'
        harnstoff_value = self.harnstoff_input.text()
        harnstoff_unit = 'mg/dl'
        krea_value = self.krea_input.text()
        krea_unit = 'mg/dl'
        gfr_value = self.gfr_input.text()
        gfr_unit = 'ml/min'
        bili_value = self.bili_input.text()
        bili_unit = 'mg/dl'
        got_value = self.got_input.text()
        got_unit = 'U/L'
        gpt_value = self.gpt_input.text()
        gpt_unit = 'U/L'
        ap_value = self.ap_input.text()
        ap_unit = 'U/L'
        ggt_value = self.ggt_input.text()
        ggt_unit = 'U/L'
        na_value = self.na_input.text()
        na_unit = 'mmol/L'
        k_value = self.k_input.text()
        k_unit = 'mmol/L'
        bnp_value = self.bnp_input.text()
        bnp_unit = 'pg/ml'


        reserreger0 = self.vre1_label.text() + self.vre2_label.text() + self.mrsa1_label.text() + self.mrsa2_label.text() + self.mrgn3_label.text() + self.mrgn4_label.text() + self.resistente_erreger_textinput.text()

        if len(reserreger0) > 1 and reserreger0[-2:] == ", ":
            reserreger = reserreger0[:-2]
        else:
            reserreger = reserreger0
        mrsavalue0 = self.mrsa1_label.text() + self.mrsa2_label.text()
        mrsavalue = mrsavalue0[:-2]
        mrgnvalue0 = self.mrgn3_label.text() + self.mrgn4_label.text()
        mrgnvalue = mrgnvalue0[:-2]
        preconditionsrel =self.khk_label.text() + self.pavk_label.text() + self.herzinsuff_label.text() + self.pulmht_label.text() + self.dm_label.text() + self.apoplex_label.text() + self.cni_label.text() + self.copd_label.text()
        dialyse0 = self.dialyse_label.text()
        if len(dialyse0) > 1:
            dialyse = dialyse0[:-2]
        else:
            dialyse = ''

        if len(preconditionsrel) > 1:
            preconditionsrel1 = preconditionsrel[:-2]  # Entfernen des letzten Zeichens
        else:
            preconditionsrel1 = preconditionsrel

        if self.katecholamine_sonstige_input.text():
            katecholamin_sonstige = self.katecholamine_sonstige_input.text() + ' ' + self.katecholamine_sonstige_laufrate_input.text() + ' ' + self.katecholamine_sonstige_laufrate_einheit.text() + ', '
        else:
            katecholamin_sonstige = ''

        if self.katecholamine_checkbox1.isChecked():
            arterenol = self.katecholamine_checkbox1.text() + ' ' + self.noradrenalin_laufrate.text() + ' ' + self.noradrenalin_laufrate_einheit.text() + ', '
        else:
            arterenol = ''
        if self.katecholamine_checkbox2.isChecked():
            adrenalin = self.katecholamine_checkbox2.text() + ' ' + self.adrenalin_laufrate.text() + ' ' + self.adrenalin_laufrate_einheit.text() + ', '
        else:
            adrenalin = ''
        if self.katecholamine_checkbox3.isChecked():
            dobutamin = self.katecholamine_checkbox3.text() + ' ' + self.dobutamin_laufrate.text() + ' ' + self.dobutamin_laufrate_einheit.text() + ', '
        else:
            dobutamin = ''
        if self.katecholamine_combo.currentIndex() == 1:
            katecholamine0 = arterenol + adrenalin + dobutamin + katecholamin_sonstige
        else:
            katecholamine0 = ' , '
        if len(katecholamine0) > 1:
            katecholamine = katecholamine0[:-2]
        
        if self.sedierung_sonstige_input.text():
            sedierung_sonstige = self.sedierung_sonstige_input.text() + ' ' + self.sedierung_sonstige_laufrate_input.text() + ' ' + self.sedierung_sonstige_laufrate_einheit.text() + ', '
        else:
            sedierung_sonstige = ''
        
        if self.sedierung_checkbox1.isChecked():
            propofol = self.sedierung_checkbox1.text() + ' ' + self.propofol_laufrate_input.text() + ' ' + self.propofol_laufrate_einheit.text() + ', '
        else:
            propofol = ''
        if self.sedierung_checkbox2.isChecked():
            sufenta = self.sedierung_checkbox2.text() + ' ' + self.sufenta_laufrate_input.text() + ' ' + self.sufenta_laufrate_einheit.text() + ', '
        else:
            sufenta = ''
        if self.sedierung_checkbox3.isChecked():
            fenta = self.sedierung_checkbox3.text() + ' ' + self.fenta_laufrate_input.text() + ' ' + self.fenta_laufrate_einheit.text() + ', '
        else:
            fenta = ''
        if self.sedierung_checkbox4.isChecked():
            midazolam = self.sedierung_checkbox4.text() + ' ' + self.midazolam_laufrate_input.text() + ' ' + self.midazolam_laufrate_einheit.text() + ', '
        else:
            midazolam = ''
        if self.sedierung_checkbox5.isChecked():
            dexdor = self.sedierung_checkbox5.text() + ' ' + self.dexdor_laufrate_input.text() + ' ' + self.dexdor_laufrate_einheit.text() + ', '
        else:
            dexdor = ''
        if self.sedierung_checkbox6.isChecked():
            ketamin = self.sedierung_checkbox6.text() + ' ' + self.ketamin_laufrate_input.text() + ' ' + self.ketamin_laufrate_einheit.text() + ', '
        else:
            ketamin = ''

        if self.sedierung_checkbox1.isChecked() or self.sedierung_checkbox2.isChecked() or self.sedierung_checkbox3.isChecked() or self.sedierung_checkbox4.isChecked() or self.sedierung_checkbox5.isChecked() or self.sedierung_checkbox6.isChecked():
            sedierung0 = propofol + sufenta + fenta + midazolam + dexdor + ketamin + sedierung_sonstige
        else:
            sedierung0 = ' , '
        if len(sedierung0) > 1:
            sedierung = sedierung0[:-2]

        if self.ernaehrung_parenteral_combo.currentIndex() == 0:
            nutrimono = self.ernaehrung_parenteral_combo.currentText() + ' ' + self.ernaehrung_parenteral_nutriLP_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_nutriLP_laufrate_einheit.text() + ', '
            parenterale = nutrimono
        elif self.ernaehrung_parenteral_combo.currentIndex() == 1:
            nutrias = 'Nutriflex Lipid Plus + AS' + ' ' + self.ernaehrung_parenteral_nutriLP_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_nutriLP_laufrate_einheit.text() + ' / ' + self.ernaehrung_parenteral_as_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_as_laufrate_einheit.text() + ', '
            parenterale = nutrias
        elif self.ernaehrung_parenteral_combo.currentIndex() == 2:
            dreikompo = 'Glc40%/AS/Lipide' + ' ' + self.ernaehrung_parenteral_glc40_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_glc40_laufrate_einheit.text() + ' / ' + self.ernaehrung_parenteral_as_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_as_laufrate_einheit.text() + ' / ' + self.ernaehrung_parenteral_lipid_plus_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.text() + ', '
            parenterale = dreikompo
    
        if self.kalorien_parenteral.text():
            kcalparenterale = self.kalorien_parenteral.text()
        else:
            kcalparenterale = ''

        if self.kalorien_enteral.text():
            kcalenterale = self.kalorien_enteral.text()
        else:
            kcalenterale = ''

        if self.ernaehrung_parenteral_combo.currentIndex() == 0:
            ernaehrung_parenteral = 'parenteral: Nutriflex Lipid Plus ' + self.ernaehrung_parenteral_nutriLP_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_nutriLP_laufrate_einheit.text()
        elif self.ernaehrung_parenteral_combo.currentIndex() == 1:
            ernaehrung_parenteral = 'parenteral: Nutriflex Lipid Plus / AS ' + self.ernaehrung_parenteral_nutriLP_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_nutriLP_laufrate_einheit.text() + ' / ' + self.ernaehrung_parenteral_as_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_as_laufrate_einheit.text()
        elif self.ernaehrung_parenteral_combo.currentIndex() == 2:
            ernaehrung_parenteral = 'parenteral: Glc40%/AS/Lipide ' + self.ernaehrung_parenteral_glc40_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_glc40_laufrate_einheit.text() + ' / ' + self.ernaehrung_parenteral_as_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_as_laufrate_einheit.text() + ' / ' + self.ernaehrung_parenteral_lipid_plus_laufrate_input.text() + ' ' + self.ernaehrung_parenteral_lipid_plus_laufrate_einheit.text()
        else:
            ernaehrung_parenteral = ''

        ernaehrung_enteral = 'enteral über ' + self.magensonde_combo.currentText() + ': Fresubin SK ' + self.ernaehrung_enteral_combo.currentText() + ' ' + self.ernaehrung_enteral_laufrate_input.text() + ' ml/h'

        if self.ernaehrung_checkbox1.isChecked() and self.ernaehrung_checkbox2.isChecked():
            ernaehrung = ernaehrung_parenteral + ' ' + ernaehrung_enteral
        elif self.ernaehrung_checkbox1.isChecked():
            ernaehrung = ernaehrung_parenteral
        elif self.ernaehrung_checkbox2.isChecked():
            ernaehrung = ernaehrung_enteral
        else:
            ernaehrung = ''


        medikation = self.medplan.toPlainText()
        medikation_lines = medikation.split('\n')
        medikation_line1 = medikation_lines[0] if len(medikation_lines) >= 1 else ""
        medikation_line2 = medikation_lines[1] if len(medikation_lines) >= 2 else ""
        medikation_line3 = medikation_lines[2] if len(medikation_lines) >= 3 else ""
        medikation_line4 = medikation_lines[3] if len(medikation_lines) >= 4 else ""
        medikation_line5 = medikation_lines[4] if len(medikation_lines) >= 5 else ""
        medikation_line6 = medikation_lines[5] if len(medikation_lines) >= 6 else ""
        medikation_line7 = medikation_lines[6] if len(medikation_lines) >= 7 else ""
        medikation_line8 = medikation_lines[7] if len(medikation_lines) >= 8 else ""
        medikation_line9 = medikation_lines[8] if len(medikation_lines) >= 9 else ""
        medikation_line10 = medikation_lines[9] if len(medikation_lines) >= 10 else ""
        medikation_line11 = medikation_lines[10] if len(medikation_lines) >= 11 else ""
        medikation_line12 = medikation_lines[11] if len(medikation_lines) >= 12 else ""
        

        current_ab0 = self.mibi_input_current.toPlainText()
        current_ab_lines = current_ab0.split('\n')
        current_ab = ', '.join(current_ab_lines[:4])

        erregernachweis0 = self.erregernachweis_input.toPlainText()
        erregernachweis_lines = erregernachweis0.split('\n')
        erregernachweis = ', '.join(erregernachweis_lines[:4])

        if self.betreuung_combo.currentIndex() == 0 and self.betreuung_name_combo.currentIndex() == 0:
            betreuung_name = self.next_of_kin_input.text()
            betreuung_tel = self.next_of_kin_tel_input.text()
        elif self.betreuung_combo.currentIndex() == 0 and self.betreuung_name_combo.currentIndex() == 1:
            betreuung_name = self.betreuung_name2_input.text()
            betreuung_tel = self.betreuung_name2_tel_input.text()
        else:
            betreuung_name = ''
            betreuung_tel = ''

        if self.dekubitus_combo.currentText() == 'ja':
            dekubitus = self.dekubitus_lokalisation_combo.currentText() + ' Grad ' + self.dekubitus_grad_combo.currentText()
        else:
            dekubitus = ''

        serologie_hiv = self.checkbox_hivpos.text() if self.checkbox_hivpos.isChecked() else self.checkbox_hivneg.text()
        serologie_hbsag = 'HepB: ' + self.checkbox_hbsagpos.text() if self.checkbox_hbsagpos.isChecked() else 'HepB: ' + self.checkbox_hbsagneg.text()
        serologie_hcv = 'HepC: ' + self.checkbox_hcvpos.text() if self.checkbox_hcvpos.isChecked() else 'HepC: ' + self.checkbox_hcvneg.text()

        serologie = serologie_hiv + ', ' + serologie_hbsag + ', ' + serologie_hcv

        if self.dekubitus_lokalisation_combo.currentText() == 'Sonstige':
            dekubituslokalisation = self.dekubitus_lokalisation_sonstige_input.text()
        else:
            dekubituslokalisation = self.dekubitus_lokalisation_combo.currentText()
    

        # Daten für Antrag 1 aktualisieren 
        data_antrag1 = {
            'birthdate': {'x': 400, 'y': 205, 'value': birthdate, 'page_num': 1},
            'sfh_station': {'x': 75, 'y': 250, 'value': f"{sfhklein}, {fach} {its}, Ansprechpartner: {doctor}", 'page_num': 1},
            'itsaddr1': {'x': 75, 'y': 275, 'value': itsaddr1, 'page_num': 1},
            'itsaddr2': {'x': 75, 'y': 300, 'value': itsaddr2, 'page_num': 1},
            'tel': {'x': 400, 'y': 300, 'value': tel, 'page_num': 1},
            'name': {'x': 75, 'y': 205, 'value': f"{first_name} {last_name}", 'page_num': 1},  
            'current_date': {'x': 420, 'y': 118, 'value': current_date, 'page_num': 1},
            'atemweg': {'x': 350, 'y': 553, 'value': atemweg, 'page_num': 1},
            'extversuche': {'x': 80, 'y': 600, 'value': self.ext_versuche_input.text(), 'page_num': 1},
            'extversuchewann': {'x': 400, 'y': 600, 'value': self.ext_versuche_wann_input.text(), 'page_num': 1},
            'height': {'x': 80, 'y': 753, 'value': f"{height_value} {height_unit}", 'page_num': 1},
            'weight': {'x': 120, 'y': 753, 'value': f"{weight_value} {weight_unit}", 'page_num': 1},
            'airway-date': {'x': 80, 'y': 553, 'value': airway_date, 'page_num': 1},
            'airway-dg': {'x': 80, 'y': 345, 'value': airway_dg, 'page_num': 1},
            'insurance': {'x': 350, 'y': 752, 'value': insurance, 'page_num': 1},
            'reserreger': {'x': 80, 'y': 705, 'value': reserreger, 'page_num': 1},
            'modus': {'x': 80, 'y': 655, 'value': self.modus_input.text(), 'page_num': 1},
            'druecke': {'x': 120, 'y': 655, 'value': f"{self.spitzendruck_input.text()}/{self.peep_input.text()} cmH2O", 'page_num': 1},
            'frequenz': {'x': 200, 'y': 655, 'value': f"AF: {self.atemfrequenz_input.text()}/min", 'page_num': 1},
            'fio2': {'x': 280, 'y': 655, 'value': f"FiO2: {self.fio2_input.text()}%", 'page_num': 1},
            'preconditionsrel1': {'x': 75, 'y': 415, 'value': preconditionsrel1, 'page_num': 1},
            'dialyse': {'x': 75, 'y': 440, 'value': dialyse, 'page_num': 1},
            'katecholamine': {'x': 75, 'y': 485, 'value': katecholamine, 'page_num': 1},
            'sedierung': {'x': 75, 'y': 510, 'value': sedierung, 'page_num': 1},

    }
        

        data_antrag2 = {
            'sfh_station': {'x': 200, 'y': 348, 'value': f"{sfhklein}, {fach} {its}", 'page_num': 1},
            'doctor': {'x': 200, 'y': 365, 'value': self.doctor_input.text(), 'page_num': 1}, 
            'tel': {'x': 200, 'y': 418, 'value': tel, 'page_num': 1},
            'fax': {'x': 360, 'y': 418, 'value': fax, 'page_num': 1},
            'birthdate': {'x': 200, 'y': 495, 'value': birthdate, 'page_num': 1},
            'name': {'x': 200, 'y': 470, 'value': f"{first_name} {last_name}", 'page_num': 1},
            'Insurance': {'x': 380, 'y': 562, 'value': insurance, 'page_num': 1},
            'Street': {'x': 235, 'y': 538, 'value': self.street_input.text(), 'page_num': 1},
            'PLZ': {'x': 230, 'y': 517, 'value': self.plz_input.text(), 'page_num': 1},
            'City': {'x': 330, 'y': 517, 'value': self.city_input.text(), 'page_num': 1},
            'job': {'x': 205, 'y': 562, 'value': self.job_input.text(), 'page_num': 1},
            'next_of_kin': {'x': 205, 'y': 583, 'value': self.next_of_kin_input.text(), 'page_num': 1},
            'height': {'x': 360, 'y': 285, 'value': height, 'page_num': 2},
            'weight': {'x': 208, 'y': 285, 'value': weight, 'page_num': 2},
            'airway_dg': {'x': 222, 'y': 145, 'value': airway_dg, 'page_num': 2},
            'airway_date': {'x': 222, 'y': 159, 'value': airway_date, 'page_num': 2},
            'tk_date': {'x': 492, 'y': 174, 'value': self.tk_date_input.text(), 'page_num': 2},
            'artery': {'x': 190, 'y': 508, 'value': self.artery_combo.currentText(), 'page_num': 2},
            'artery_date': {'x': 403, 'y': 508, 'value': self.artery_date_input.text(), 'page_num': 2},
            'cvc_and_lumen': {'x': 190, 'y': 522, 'value': f"{self.cvc_combo.currentText()} ({self.lumen_combo.currentText()})", 'page_num': 2},
            'cvc_date': {'x': 403, 'y': 522, 'value': self.cvc_date_input.text(), 'page_num': 2},
            'hb': {'x': 204, 'y': 300, 'value': self.hb_input.text(), 'page_num': 2},
            'na': {'x': 315, 'y': 300, 'value': self.na_input.text(), 'page_num': 2},
            'k': {'x': 465, 'y': 300, 'value': self.k_input.text(), 'page_num': 2},
            'krea': {'x': 204, 'y': 313, 'value': f"{krea_value} {krea_unit}", 'page_num': 2},
            'harnstoff': {'x': 315, 'y': 313, 'value': f"{harnstoff_value} {harnstoff_unit}", 'page_num': 2},
            'got': {'x': 465, 'y': 313, 'value': f"{got_value} {got_unit}", 'page_num': 2},
            'gpt': {'x': 204, 'y': 327, 'value': f"{gpt_value} {gpt_unit}", 'page_num': 2},
            'crp': {'x': 315, 'y': 327, 'value': f"{crp_value} {crp_unit}", 'page_num': 2},
            'modus': {'x': 320, 'y': 185, 'value': self.modus_input.text(), 'page_num': 2},
            'fiO2': {'x': 320, 'y': 200, 'value': f"{self.fio2_input.text()}%", 'page_num': 2},
            'peep': {'x': 320, 'y': 213, 'value': f"{self.peep_input.text()} cmH2O", 'page_num': 2},
            'af': {'x': 420, 'y': 200, 'value': f"{self.atemfrequenz_input.text()}/min", 'page_num': 2},
            'spitzendruck': {'x': 420, 'y': 213, 'value': f"{self.spitzendruck_input.text()} cmH2O", 'page_num': 2},
            'po2': {'x': 100, 'y': 242, 'value': f"{self.po2_input.text()} mmHg", 'page_num': 2},
            'pco2': {'x': 250, 'y': 242, 'value': f"{self.pco2_input.text()} mmHg", 'page_num': 2},
            'ph': {'x': 400, 'y': 242, 'value': self.ph_input.text(), 'page_num': 2},
            'hc03': {'x': 100, 'y': 255, 'value': f"{self.hco3_input.text()} mmol/L", 'page_num': 2},
            'saO2': {'x': 250, 'y': 255, 'value': f"{self.sao2_input.text()}%", 'page_num': 2},
            'cdiff': {'x': 235, 'y': 396, 'value': f"{self.cdiff_date_input.text()}", 'page_num': 2},
            'katecholamine': {'x': 295, 'y': 537, 'value': katecholamine, 'page_num': 2},
            'anzahlreintub': {'x': 355, 'y': 635, 'value': self.re_intub_input.text(), 'page_num': 2},
            'weaningmethod': {'x': 220, 'y': 648, 'value': self.weaning_method_input.text(), 'page_num': 2},
            'scheiternweaning': {'x': 220, 'y': 662, 'value': self.scheitern_input.text(), 'page_num': 2},
            'rr': {'x': 150, 'y': 494, 'value': f"{self.rr_syst_input.text()}/{self.rr_diast_input.text()}", 'page_num': 2},
            'pulse': {'x': 365, 'y': 494, 'value': self.hf_input.text(), 'page_num': 2},
            'dekubitus': {'x': 120, 'y': 606, 'value': dekubitus, 'page_num': 2},
        }
        data_antrag3 = {
            'sfh': {'x': 214, 'y': 272, 'value': sfh, 'page_num': 1},
            'doctor': {'x': 214, 'y': 286, 'value': self.doctor_input.text(), 'page_num': 1}, 
            'itsplz': {'x': 245, 'y': 300, 'value': itsplz, 'page_num': 1},
            'itsstadt': {'x': 320, 'y': 300, 'value': itsstadt, 'page_num': 1},
            'itsaddr1': {'x': 250, 'y': 313, 'value': itsaddr1, 'page_num': 1},
            'tel': {'x': 220, 'y': 326, 'value': tel, 'page_num': 1},
            'fax': {'x': 390, 'y': 326, 'value': fax, 'page_num': 1},
            'birthdate1': {'x': 224, 'y': 392, 'value': f"{bd_first_digit}{bd_second_digit}", 'page_num': 1},
            'birthdate2': {'x': 260, 'y': 392, 'value': f"{bd_third_digit}{bd_fourth_digit}", 'page_num': 1},
            'birthdate3': {'x': 296, 'y': 392, 'value': f"{bd_fifth_digit}{bd_sixth_digit}{bd_seventh_digit}{bd_eighth_digit}", 'page_num': 1},
            'name': {'x': 220, 'y': 378, 'value': f"{first_name} {last_name}", 'page_num': 1},
            'Street': {'x': 250, 'y': 417, 'value': self.street_input.text(), 'page_num': 1},
            'PLZ': {'x': 240, 'y': 406, 'value': self.plz_input.text(), 'page_num': 1},
            'City': {'x': 330, 'y': 406, 'value': self.city_input.text(), 'page_num': 1},
            'job': {'x': 220, 'y': 430, 'value': self.job_input.text(), 'page_num': 1},
            'insurance': {'x': 395, 'y': 430, 'value': insurance, 'page_num': 1},
            'next_of_kin': {'x': 220, 'y': 445, 'value': self.next_of_kin_input.text(), 'page_num': 1},
            'general_practitioner': {'x': 220, 'y': 458, 'value': self.general_practitioner_input.text(), 'page_num': 1},
            'weight': {'x': 170, 'y': 120, 'value': weight, 'page_num': 2},
            'height': {'x': 350, 'y': 120, 'value': height, 'page_num': 2},
            'airway_dg': {'x': 250, 'y': 667, 'value': airway_dg, 'page_num': 1},
            'aw_1': {'x': 260, 'y': 693, 'value': aw_1, 'page_num': 1},
            'aw_2': {'x': 305, 'y': 693, 'value': aw_2, 'page_num': 1},
            'aw_3': {'x': 340, 'y': 693, 'value': aw_3, 'page_num': 1},
            'tk_1': {'x': 432, 'y': 748, 'value': tk_1, 'page_num': 1},
            'tk_2': {'x': 462, 'y': 748, 'value': tk_2, 'page_num': 1},
            'tk_3': {'x': 485, 'y': 748, 'value': tk_3, 'page_num': 1},
            'artery': {'x': 215, 'y': 185, 'value': self.artery_combo.currentText(), 'page_num': 2},
            'artery_date': {'x': 415, 'y': 185, 'value': self.artery_date_input.text(), 'page_num': 2},
            'cvc_and_lumen': {'x': 215, 'y': 200, 'value': f"{self.cvc_combo.currentText()} ({self.lumen_combo.currentText()})", 'page_num': 2},
            'cvc_date': {'x': 415, 'y': 200, 'value': self.cvc_date_input.text(), 'page_num': 2},
            'bladder': {'x': 215, 'y': 213, 'value': self.bladder_combo.currentText(), 'page_num': 2},
            'bladder_date': {'x': 415, 'y': 213, 'value': self.bladder_date_input.text(), 'page_num': 2},
            'magensonde': {'x': 215, 'y': 226, 'value': self.magensonde_combo.currentText(), 'page_num': 2},
            'magensonde_date': {'x': 415, 'y': 226, 'value': self.magensonde_date_input.text(), 'page_num': 2},
            'reserreger': {'x': 335, 'y': 532, 'value': reserreger, 'page_num': 2},
            'crp': {'x': 112, 'y': 478, 'value': self.crp_input.text(), 'page_num': 2},
            'hb': {'x': 253, 'y': 478, 'value': self.hb_input.text(), 'page_num': 2},
            'krea': {'x': 380, 'y': 478, 'value': self.krea_input.text(), 'page_num': 2},
            'bili': {'x': 112, 'y': 492, 'value': self.bili_input.text(), 'page_num': 2},
            'got': {'x': 253, 'y': 492, 'value': self.got_input.text(), 'page_num': 2},
            'gpt': {'x': 380, 'y': 492, 'value': self.gpt_input.text(), 'page_num': 2},
            'modus': {'x': 155, 'y': 720, 'value': self.modus_input.text(), 'page_num': 1},
            'fio2': [
            {'x': 310, 'y': 720, 'value': self.fio2_input.text(), 'page_num': 1},
            {'x': 450, 'y': 715, 'value': self.fio2_input.text(), 'page_num': 2},],   
            'atemfrequenz': {'x': 420, 'y': 720, 'value': f"{self.atemfrequenz_input.text()}/min", 'page_num': 1},
            'peep': {'x': 310, 'y': 735, 'value': f"{self.peep_input.text()} cmH2O", 'page_num': 1},
            'spitzendruck': {'x': 420, 'y': 735, 'value': f"{self.spitzendruck_input.text()} cmH2O", 'page_num': 1},
            'ph': {'x': 90, 'y': 715, 'value': self.ph_input.text(), 'page_num': 2},
            'po2' : {'x': 150, 'y': 715, 'value': self.po2_input.text(), 'page_num': 2},
            'pco2' : {'x': 250, 'y': 715, 'value': self.pco2_input.text(), 'page_num': 2},
            'hco3' : {'x': 347, 'y': 715, 'value': self.hco3_input.text(), 'page_num': 2},
            'fiO2' : {'x': 450, 'y': 715, 'value': self.fio2_input.text(), 'page_num': 2},
            'katecholamine': {'x': 375, 'y': 147, 'value': katecholamine, 'page_num': 2},
            'sedierung': {'x': 380, 'y': 397, 'value': sedierung, 'page_num': 2},
            'anzahlreintub': {'x': 250, 'y': 595, 'value': self.re_intub_input.text(), 'page_num': 2},
            'weaningmethod': {'x': 250, 'y': 610, 'value': self.weaning_method_input.text(), 'page_num': 2},
            'scheiternweaning': {'x': 250, 'y': 636, 'value': self.scheitern_input.text(), 'page_num': 2},
            'beatmungmaschinell': {'x': 265, 'y': 650, 'value': self.beatmung_maschinell_input.text(), 'page_num': 2},
            'beatmungspontan': {'x': 400, 'y': 650, 'value': self.beatmung_spontan_input.text(), 'page_num': 2},
            'rr_syst': {'x': 148, 'y': 133, 'value': self.rr_syst_input.text(), 'page_num': 2},
            'rr_diast': {'x': 190, 'y': 133, 'value': self.rr_diast_input.text(), 'page_num': 2},
            'pulse': {'x': 350, 'y': 133, 'value': self.hf_input.text(), 'page_num': 2},
            'dekubitus_grad': {'x': 260, 'y': 373, 'value': self.dekubitus_grad_combo.currentText(), 'page_num': 2},
            'dekubitus_lokalisation': {'x': 340, 'y': 372, 'value': self.dekubitus_lokalisation_combo.currentText(), 'page_num': 2},

        }

        data_antrag4 = {
            'current_date': {'x': 380, 'y': 115, 'value': current_date, 'page_num': 1},
            'last_name': {'x': 70, 'y': 155, 'value': last_name, 'page_num': 1},
            'first_name': {'x': 240, 'y': 155, 'value': first_name, 'page_num': 1},
            'birthdate': {'x': 398, 'y': 155, 'value': birthdate, 'page_num': 1},
            'adress': {'x': 70, 'y': 182, 'value': f"{self.street_input.text()}, {self.plz_input.text()} {self.city_input.text()}", 'page_num': 1},
            'insurance': {'x': 140, 'y': 209, 'value': insurance, 'page_num': 1},
            'height': {'x': 90, 'y': 236, 'value': height, 'page_num': 1},
            'weight': {'x': 270, 'y': 236, 'value': weight, 'page_num': 1},
            'bmi': {'x': 380, 'y': 236, 'value': f"{bmi:.2f}", 'page_num': 1},
            'next_of_kin': {'x': 140, 'y': 263, 'value': self.next_of_kin_input.text(), 'page_num': 1},
            'next_of_kin_tel': {'x': 370, 'y': 263, 'value': self.next_of_kin_tel_input.text(), 'page_num': 1},
            'doctor': {'x': 140, 'y': 410, 'value': self.doctor_input.text(), 'page_num': 1},
            'sfhklein': {'x': 140, 'y': 336, 'value': sfhklein, 'page_num': 1},
            'telsfh': {'x': 370, 'y': 336, 'value': '0251 935 0', 'page_num': 1},
            'its': {'x': 140, 'y': 362, 'value': its, 'page_num': 1},
            'tel': [
                {'x': 370, 'y': 362, 'value': tel, 'page_num': 1},
                {'x': 370, 'y': 410, 'value': tel, 'page_num': 1},],
            'X': {'x': 136, 'y': 385, 'value': X, 'page_num': 1},
            'pflege': {'x': 140, 'y': 435, 'value': pflege, 'page_num': 1},
            'stationseit': {'x': 140, 'y': 461, 'value': self.stat_time_input.text(), 'page_num': 1},
            'khseite': {'x': 370, 'y': 461, 'value': self.kh_time_input.text(), 'page_num': 1},
            'pflegetel': {'x': 370, 'y': 435, 'value': pflegetel, 'page_num': 1},
            'khdg': {'x': 140, 'y': 505, 'value': self.kh_dg_input.text(), 'page_num': 1},
            'airway_dg': {'x': 140, 'y': 558, 'value': airway_dg, 'page_num': 1},
            'airway_date': {'x': 90, 'y': 57, 'value': airway_date, 'page_num': 2},
            'cvc_and_date': {'x': 80, 'y': 262, 'value': f"{self.cvc_combo.currentText()} ({self.cvc_date_input.text()})", 'page_num': 2},
            'artery_and_date': {'x': 130, 'y': 288, 'value': f"{self.artery_combo.currentText()} ({self.artery_date_input.text()})", 'page_num': 2},
            'bladder_date': {'x': 283, 'y': 311, 'value': self.bladder_date_input.text(), 'page_num': 2} if self.bladder_combo.currentIndex() == 0 else {'x': 283, 'y': 330, 'value': self.bladder_date_input.text(), 'page_num': 2},
            'modus': {'x': 190, 'y': 403, 'value': self.modus_input.text(), 'page_num': 2},
            'beatmungsparameter': {'x': 120, 'y': 430, 'value': f"IPAP {self.spitzendruck_input.text()} / PEEP {self.peep_input.text()} / AF {self.atemfrequenz_input.text()} / Tinsp {self.tinsp_input.text()} / I:E {self.izue_input.text()} / FiO2 {self.fio2_input.text()}%", 'page_num': 2},
            'po2': {'x': 194, 'y': 455, 'value': self.po2_input.text(), 'page_num': 2},
            'pco2': {'x': 340, 'y': 455, 'value': self.pco2_input.text(), 'page_num': 2},
            'ph': {'x': 490, 'y': 455, 'value': self.ph_input.text(), 'page_num': 2},
            'be': {'x': 194, 'y': 480, 'value': self.hco3_input.text(), 'page_num': 2},
            'hco3': {'x': 490, 'y': 480, 'value': self.hco3_input.text(), 'page_num': 2},
            'tk_date': {'x': 438, 'y': 180, 'value': self.tk_date_input.text(), 'page_num': 2},
            'mibi_current': {'x':140, 'y': 287, 'value': self.mibi_input_current.toPlainText(), 'page_num': 3},
            'mibi_previous': {'x':140, 'y': 340, 'value': self.mibi_input_previous.toPlainText(), 'page_num': 3},
            'reserreger': {'x': 150, 'y': 660, 'value': reserreger, 'page_num': 3},
            'hb': {'x': 145, 'y': 518, 'value': f"{hb_value} {hb_unit}", 'page_num': 3},
            'leuko': {'x': 262, 'y': 518, 'value': f"{leuko_value} {leuko_unit}", 'page_num': 3},
            'thrombo': {'x': 385, 'y': 518, 'value': f"{thrombo_value} {thrombo_unit}", 'page_num': 3},
            'Na': {'x': 145, 'y': 491, 'value': f"{na_value} {na_unit}", 'page_num': 3},
            'K': {'x': 262, 'y': 491, 'value': f"{k_value} {k_unit}", 'page_num': 3},
            'Harnstoff': {'x': 385, 'y': 491, 'value': f"{harnstoff_value} {harnstoff_unit}", 'page_num': 3},
            'Krea': {'x': 478, 'y': 491, 'value': f"{krea_value} {krea_unit}", 'page_num': 3},
            'Quick': {'x': 145, 'y': 545, 'value': f"{quick_value} {quick_unit}", 'page_num': 3},
            'PTT': {'x': 262, 'y': 545, 'value': f"{ptt_value} {ptt_unit}", 'page_num': 3},
            'INR': {'x': 385, 'y': 545, 'value': f"{inr_value} {inr_unit}", 'page_num': 3},
            'Bili': {'x': 145, 'y': 572, 'value': f"{bili_value} {bili_unit}", 'page_num': 3},
            'GOT': {'x': 222, 'y': 572, 'value': f"{got_value} {got_unit}", 'page_num': 3},
            'GPT': {'x': 300, 'y': 572, 'value': f"{gpt_value} {gpt_unit}", 'page_num': 3},
            'GGT': {'x': 373, 'y': 572, 'value': f"{ggt_value} {ggt_unit}", 'page_num': 3},
            'AP': {'x': 480, 'y': 572, 'value': f"{ap_value} {ap_unit}", 'page_num': 3},
            'CRP': {'x': 146, 'y': 598, 'value': f"{crp_value} {crp_unit}", 'page_num': 3},
            'PCT': {'x': 262, 'y': 598, 'value': f"{pct_value} {pct_unit}", 'page_num': 3},
            'BNP': {'x': 372, 'y': 598, 'value': f"{bnp_value} {bnp_unit}", 'page_num': 3},
            'anzahlextub': {'x': 145, 'y': 154, 'value': self.ext_versuche_input.text(), 'page_num': 2},
        }

        data_antrag5 = {
            'name': {'x': 75, 'y': 150, 'value': f"{first_name} {last_name}", 'page_num': 1},  # Fügen Sie den Wert des Vor- und Nachnamens ein
            'birthdate': {'x': 75, 'y': 165, 'value': birthdate, 'page_num': 1},
            'street': {'x': 75, 'y': 180, 'value': self.street_input.text(), 'page_num': 1},
            'plz_and_city': {'x': 75, 'y': 195, 'value': f"{self.plz_input.text()} {self.city_input.text()}", 'page_num': 1},
            'insurance': {'x': 75, 'y': 210, 'value': insurance, 'page_num': 1},
            'airway_dg': {'x': 75, 'y': 350, 'value': airway_dg, 'page_num': 1},
            'preconditionsrel1': {'x': 75, 'y': 413, 'value': preconditionsrel1, 'page_num': 1},
            'age': {'x':110, 'y': 438, 'value': age, 'page_num': 1},
            'height': {'x': 220, 'y': 438, 'value': height, 'page_num': 1},
            'weight': {'x': 336, 'y': 438, 'value': weight, 'page_num': 1},
            'CRP': {'x': 173, 'y': 203, 'value': crp_value, 'page_num': 2},
            'hb': {'x': 313, 'y': 203, 'value': hb_value, 'page_num': 2},
            'krea': {'x': 441, 'y': 203, 'value': krea_value, 'page_num': 2},
            'doc': {'x': 179, 'y': 570, 'value': self.doctor_input.text(), 'page_num': 2},
            'artery-time': {'x': 465, 'y': 651, 'value': f"{self.artery_time_input.text()} ({self.artery_date_input.text()})", 'page_num': 1},
            'cvc-time': {'x': 465, 'y': 666, 'value': f"{self.cvc_time_input.text()} ({self.cvc_date_input.text()})", 'page_num': 1},
            'pco2': {'x': 205, 'y': 580, 'value': f"{self.pco2_input.text()} mmHg", 'page_num': 1},
            'po2': {'x': 205, 'y': 595, 'value': f"{self.po2_input.text()} mmHg", 'page_num': 1},
            'fiO2': {'x': 300, 'y': 595, 'value': f"{self.fio2_input.text()}", 'page_num': 1},
            'ph': {'x': 215, 'y': 610, 'value': self.ph_input.text(), 'page_num': 1},
            'modus': {'x': 445, 'y': 580, 'value': self.modus_input.text(), 'page_num': 1},
            'sedierung': {'x': 235, 'y': 115, 'value': sedierung, 'page_num': 2},
            'katecholamine': {'x': 225, 'y': 142, 'value': katecholamine, 'page_num': 2},
            'dekubitus_lokalisation': {'x': 170, 'y': 445, 'value': self.dekubitus_lokalisation_combo.currentText(), 'page_num': 2},
            'dekubitus_grad': {'x': 470, 'y': 445, 'value': self.dekubitus_grad_combo.currentText(), 'page_num': 2},
        }

        data_antrag6 = {
            'cd1': {'x': 405, 'y': 82, 'value': f"{cd_first_digit}{cd_second_digit}", 'page_num': 1},
            'cd2': {'x': 440, 'y': 82, 'value': f"{cd_third_digit}{cd_fourth_digit}", 'page_num': 1},
            'cd3': {'x': 475, 'y': 82, 'value': f"{cd_fifth_digit}{cd_sixth_digit}{cd_seventh_digit}{cd_eighth_digit}", 'page_num': 1},
            'sfh ': {'x': 108, 'y': 108, 'value': sfh, 'page_num': 1},
            'doctor': {'x': 175, 'y': 131, 'value': self.doctor_input.text(), 'page_num': 1},
            'tel': {'x': 417, 'y': 131, 'value': tel, 'page_num': 1},
            'name': {'x': 130, 'y': 155, 'value': f"{first_name} {last_name}", 'page_num': 1},  # Fügen Sie den Wert des Vor- und Nachnamens ein
            'bd_12': {'x': 120, 'y': 180, 'value': f"{bd_first_digit}{bd_second_digit}", 'page_num': 1},
            'bd_34': {'x': 154, 'y': 180, 'value': f"{bd_third_digit}{bd_fourth_digit}", 'page_num': 1},
            'bd_5678': {'x': 188, 'y': 180, 'value': f"{bd_fifth_digit}{bd_sixth_digit}{bd_seventh_digit}{bd_eighth_digit}", 'page_num': 1},
            'age': {'x': 284, 'y': 180, 'value': age, 'page_num': 1},
            'insurance': {'x': 460, 'y': 180, 'value': insurance, 'page_num': 1},
            'airway_dg': {'x': 270, 'y': 230, 'value': airway_dg, 'page_num': 1},
            'modus': {'x': 180, 'y': 307, 'value': self.modus_input.text(), 'page_num': 1},
            'aw_1': {'x': 116, 'y': 334, 'value': aw_1, 'page_num': 1},
            'aw_2': {'x': 142, 'y': 334, 'value': aw_2, 'page_num': 1},
            'aw_3': {'x': 173, 'y': 334, 'value': aw_3, 'page_num': 1},
            'tk_1': {'x': 322, 'y': 334, 'value': tk_1, 'page_num': 1},
            'tk_2': {'x': 350, 'y': 334, 'value': tk_2, 'page_num': 1},
            'tk_3': {'x': 380, 'y': 334, 'value': tk_3, 'page_num': 1},
            'airway_days': {'x': 125, 'y': 347, 'value': self.airway_days_input.text(), 'page_num': 1},
            'weight': {'x': 225, 'y': 643, 'value': weight, 'page_num': 1},
            'c19_negtest_date': {'x': 513, 'y': 467, 'value': self.c19_negtest_date_input.text(), 'page_num': 1},
        }

        data_antrag7 = {
            'name': {'x': 75, 'y': 124, 'value': f"{first_name} {last_name}", 'page_num': 1}, 
            'birthdate': {'x': 75, 'y': 136, 'value': birthdate, 'page_num': 1},
            'street': {'x': 75, 'y': 148, 'value': self.street_input.text(), 'page_num': 1},
            'plz_and_city': {'x': 75, 'y': 160, 'value': f"{self.plz_input.text()} {self.city_input.text()}", 'page_num': 1},
            'airway_dg': {'x': 75, 'y': 210, 'value': airway_dg, 'page_num': 1},
            'airway_date': {'x': 180, 'y': 263, 'value': f"{airway_date} ({self.airway_days_input.text()} Tage)", 'page_num': 1},
            'height': {'x': 160, 'y': 397, 'value': height, 'page_num': 1},
            'weight': {'x': 320, 'y': 397, 'value': weight, 'page_num': 1},
            'reserreger': {'x': 360, 'y': 597, 'value': reserreger, 'page_num': 1},
            'sfhklein': {'x': 75, 'y': 647, 'value': sfhklein, 'page_num': 1},
            'its': {'x': 75, 'y': 657, 'value': its, 'page_num': 1},
            'itsaddr1': {'x': 75, 'y': 669, 'value': itsaddr1, 'page_num': 1},
            'itsaddr2': {'x': 75, 'y': 681, 'value': itsaddr2, 'page_num': 1},
            'tel': {'x': 75, 'y': 691, 'value': tel, 'page_num': 1},
            'sofort': {'x': 380, 'y': 630, 'value': sofort, 'page_num': 1},
            'po2': {'x': 170, 'y': 535, 'value': f"{self.po2_input.text()} mmHg", 'page_num': 1},
            'pc02': {'x': 360, 'y': 535, 'value': f"{self.pco2_input.text()} mmHg", 'page_num': 1},
            'modus': {'x': 380, 'y': 455, 'value': self.modus_input.text(), 'page_num': 1},
            'dekubitus_lokalisation': {'x': 200, 'y': 427, 'value': self.dekubitus_lokalisation_combo.currentText(), 'page_num': 1},
            'dekubitus_grad': {'x': 500, 'y': 427, 'value': self.dekubitus_grad_combo.currentText(), 'page_num': 1},
        }

        data_antrag8 = {
            'current_date': {'x': 445, 'y': 286, 'value': current_date, 'page_num': 1},
            'namerv': [
            {'x': 215, 'y': 316, 'value': f"{last_name}, {first_name}", 'page_num': 1},
            {'x': 215, 'y': 108, 'value': f"{last_name}, {first_name}", 'page_num': 4},
            {'x': 215, 'y': 108, 'value': f"{last_name}, {first_name}", 'page_num': 5},],            
            'birthdate': [
            {'x': 215, 'y': 340, 'value': birthdate, 'page_num': 1},
            {'x': 470, 'y': 108, 'value': birthdate, 'page_num': 4},
            {'x': 470, 'y': 108, 'value': birthdate, 'page_num': 5},],
            'next_of_kin': {'x': 100, 'y': 470, 'value': self.next_of_kin_input.text(), 'page_num': 1},
            'next of kin tel': {'x': 270, 'y': 470, 'value': self.next_of_kin_tel_input.text(), 'page_num': 1},
            'sfh': {'x': 225, 'y': 700, 'value': sfh, 'page_num': 1},
            'sfhadress': {'x': 225, 'y': 725, 'value': f"{itsaddr1}, {itsplz} {itsstadt}", 'page_num': 1}, 
            'doctor': {'x': 225, 'y': 750, 'value': self.doctor_input.text(), 'page_num': 1},
            'tel': {'x': 225, 'y': 773, 'value': tel, 'page_num': 1},
            'pflege': {'x': 225, 'y': 106, 'value': pflege, 'page_num': 2},
            'pflegetel': {'x': 225, 'y': 127, 'value': pflegetel, 'page_num': 2},
            'fax': {'x': 225, 'y': 150, 'value': fax, 'page_num': 2},
            'weight': {'x': 168, 'y': 655, 'value': weight, 'page_num': 2},
            'height': {'x': 305, 'y': 655, 'value': height, 'page_num': 2},
            'airway_date': {'x': 190, 'y': 710, 'value': airway_date, 'page_num': 2},
            'tk_date': {'x': 410, 'y': 710, 'value': self.tk_date_input.text(), 'page_num': 2},
            'hb': {'x': 205, 'y': 353, 'value': hb_value, 'page_num': 3},
            'reserreger': {'x': 320, 'y': 590, 'value': reserreger, 'page_num': 3},
            'atemweg': {'x': 280, 'y': 158, 'value': atemweg, 'page_num': 5},
            'artery': {'x': 230, 'y': 195, 'value': self.artery_combo.currentText(), 'page_num': 5},
            'artery_date': {'x': 440, 'y': 195, 'value': self.artery_date_input.text(), 'page_num': 5},
            'cvc_and_lumen': {'x': 230, 'y': 210, 'value': f"{self.cvc_combo.currentText()} ({self.lumen_combo.currentText()})", 'page_num': 5},
            'cvc_date': {'x': 440, 'y': 210, 'value': self.cvc_date_input.text(), 'page_num': 5},
            'bladder': {'x': 230, 'y': 228, 'value': self.bladder_combo.currentText(), 'page_num': 5},
            'bladder_date': {'x': 460, 'y': 228, 'value': self.bladder_date_input.text(), 'page_num': 5},
            'magensonde': {'x': 230, 'y': 245, 'value': self.magensonde_combo.currentText(), 'page_num': 5},
            'magensonde_date': {'x': 440, 'y': 245, 'value': self.magensonde_date_input.text(), 'page_num': 5},
            'mibi_current': {'x': 100, 'y': 645, 'value': self.mibi_input_current.toPlainText(), 'page_num': 4},
            'mibi_previous': {'x': 100, 'y': 695, 'value': self.mibi_input_previous.toPlainText(), 'page_num': 4},
            'modus': {'x': 210, 'y': 105, 'value': self.modus_input.text(), 'page_num': 3},
            'spitzendruck': {'x': 410, 'y': 105, 'value': f"{self.spitzendruck_input.text()} cmH2O", 'page_num': 3},
            'peep': {'x': 495, 'y': 105, 'value': f"{self.peep_input.text()} cmH2O", 'page_num': 3},
            'fio2': {'x': 210, 'y': 125, 'value': self.fio2_input.text(), 'page_num': 3},
            'po2': {'x': 305, 'y': 125, 'value': self.po2_input.text(), 'page_num': 3},
            'pco2': {'x': 460, 'y': 125, 'value': self.pco2_input.text(), 'page_num': 3},
            'ph': {'x': 210, 'y': 145, 'value': self.ph_input.text(), 'page_num': 3},
            'be': {'x': 305, 'y': 145, 'value': self.be_input.text(), 'page_num': 3},
            'hco3': {'x': 460, 'y': 145, 'value': self.hco3_input.text(), 'page_num': 3},
            'medikation_line1': {'x': 100, 'y': 405, 'value': medikation_line1, 'page_num': 4},
            'medikation_line2': {'x': 100, 'y': 423, 'value': medikation_line2, 'page_num': 4},
            'medikation_line3': {'x': 100, 'y': 441, 'value': medikation_line3, 'page_num': 4},
            'medikation_line4': {'x': 100, 'y': 459, 'value': medikation_line4, 'page_num': 4},
            'medikation_line5': {'x': 100, 'y': 477, 'value': medikation_line5, 'page_num': 4},
            'medikation_line6': {'x': 100, 'y': 494, 'value': medikation_line6, 'page_num': 4},
            'medikation_line7': {'x': 100, 'y': 512, 'value': medikation_line7, 'page_num': 4},
            'medikation_line8': {'x': 100, 'y': 529, 'value': medikation_line8, 'page_num': 4},
            'medikation_line9': {'x': 100, 'y': 547, 'value': medikation_line9, 'page_num': 4},
            'medikation_line10': {'x': 100, 'y': 564, 'value': medikation_line10, 'page_num': 4},
            'medikation_line11': {'x': 100, 'y': 582, 'value': medikation_line11, 'page_num': 4},
            'medikation_line12': {'x': 100, 'y': 600, 'value': medikation_line12, 'page_num': 4},
            'ernaehrung': {'x': 190, 'y': 263, 'value': ernaehrung, 'page_num': 5},
            'serologie': {'x': 100, 'y': 555, 'value': serologie, 'page_num': 3},

        }

        data_antrag9 = {
            'sfhklein': {'x': 140, 'y': 228, 'value': sfhklein, 'page_num': 1},
            'itsaddr1': {'x': 140, 'y': 244, 'value': itsaddr1, 'page_num': 1},
            'itsaddr2': {'x': 140, 'y': 260, 'value': itsaddr2, 'page_num': 1},
            'doctor': {'x': 140, 'y': 276, 'value': self.doctor_input.text(), 'page_num': 1},
            'tel': {'x': 140, 'y': 292, 'value': tel, 'page_num': 1},
            'fax': {'x': 140, 'y': 308, 'value': fax, 'page_num': 1},
            'email': {'x': 140, 'y': 324, 'value': email, 'page_num': 1},
            'last_name': {'x': 415, 'y': 228, 'value': last_name, 'page_num': 1},
            'first_name': {'x': 415, 'y': 244, 'value': first_name, 'page_num': 1},
            'birthdate': {'x': 415, 'y': 260, 'value': birthdate, 'page_num': 1},
            'street': {'x': 415, 'y': 276, 'value': self.street_input.text(), 'page_num': 1},
            'plz_and_city': {'x': 415, 'y': 292, 'value': f"{self.plz_input.text()} {self.city_input.text()}", 'page_num': 1},
            'next_of_kin': {'x': 415, 'y': 308, 'value': self.next_of_kin_input.text(), 'page_num': 1},
            'next_of_kin_tel': {'x': 415, 'y': 324, 'value': self.next_of_kin_tel_input.text(), 'page_num': 1},
            'height': {'x': 140, 'y': 440, 'value': height, 'page_num': 1},
            'weight': {'x': 140, 'y': 456, 'value': weight, 'page_num': 1},
            'bmi': {'x': 140, 'y': 472, 'value': f"{bmi:.2f}", 'page_num': 1},
            'airway_date': {'x': 170, 'y': 680, 'value': airway_date[:-5], 'page_num': 1},
            'tk_date': {'x': 210, 'y': 696, 'value': self.tk_date_input.text(), 'page_num': 1},
            'crp': {'x': 380, 'y': 383, 'value': f"{crp_value} {crp_unit}", 'page_num': 2},
            'hb': {'x': 380, 'y': 400, 'value': f"{hb_value} {hb_unit}", 'page_num': 2},
            'krea': {'x': 380, 'y': 417, 'value': f"{krea_value} {krea_unit}", 'page_num': 2},
            'harnstoff': {'x': 380, 'y': 434, 'value': f"{harnstoff_value} {harnstoff_unit}", 'page_num': 2},
            'kalium': {'x': 380, 'y': 451, 'value': f"{k_value} {k_unit}", 'page_num': 2},
            'na': {'x': 510, 'y': 383, 'value': f"{na_value} {na_unit}", 'page_num': 2},
            'leuko': {'x': 510, 'y': 400, 'value': f"{leuko_value} {leuko_unit}", 'page_num': 2},
            'thrombo': {'x': 510, 'y': 417, 'value': f"{thrombo_value} {thrombo_unit}", 'page_num': 2},
            'bili': {'x': 510, 'y': 434, 'value': f"{bili_value} {bili_unit}", 'page_num': 2},
            'gpt': {'x': 510, 'y': 451, 'value': f"{gpt_value} {gpt_unit}", 'page_num': 2},
            'po2': {'x': 219, 'y': 504, 'value': f"{self.po2_input.text()} mmHg", 'page_num': 2},
            'pco2': {'x': 219, 'y': 521, 'value': f"{self.pco2_input.text()} mmHg", 'page_num': 2},
            'ph': {'x': 219, 'y': 538, 'value': self.ph_input.text(), 'page_num': 2},
            'be': {'x': 219, 'y': 555, 'value': self.be_input.text(), 'page_num': 2},
            'sao2': {'x': 219, 'y': 572, 'value': f"{self.sao2_input.text()} %", 'page_num': 2},
            'modus': {'x': 406, 'y': 489, 'value': self.modus_input.text(), 'page_num': 2},
            'spitzendruck': {'x': 406, 'y': 506, 'value': f"{self.spitzendruck_input.text()} cmH2O", 'page_num': 2},
            'peep': {'x': 406, 'y': 523, 'value': f"{self.peep_input.text()} cmH2O", 'page_num': 2},
            'atemfrequenz': {'x': 406, 'y': 557, 'value': f"{self.atemfrequenz_input.text()} /min", 'page_num': 2},
            'izue': {'x': 406, 'y': 574, 'value': self.izue_input.text(), 'page_num': 2},
            'tinsp': {'x': 406, 'y': 591, 'value': f"{self.tinsp_input.text()} s", 'page_num': 2},
            'fio2': [
            {'x': 219, 'y': 487, 'value': self.fio2_input.text(), 'page_num': 2},
            {'x': 406, 'y': 540, 'value': self.fio2_input.text(), 'page_num': 2},],
            'betreuung_name': {'x': 415, 'y': 375, 'value': betreuung_name, 'page_num': 1},
            'betreuung_tel': {'x': 415, 'y': 392, 'value': betreuung_tel, 'page_num': 1},
            'dekubitus_lokalisation': {'x': 415, 'y': 645, 'value': f"{dekubituslokalisation} Grad {self.dekubitus_grad_combo.currentText()}", 'page_num': 2},
        }

        data_antrag10 = {
            'last_name': {'x': 115, 'y': 117, 'value': last_name, 'page_num': 1},
            'first_name': {'x': 320, 'y': 117, 'value': first_name, 'page_num': 1},
            'birthdate': {'x': 115, 'y': 145, 'value': birthdate, 'page_num': 1},
            'insurance': {'x': 292, 'y': 145, 'value': insurance, 'page_num': 1},
            'height': {'x': 115, 'y': 188, 'value': height, 'page_num': 1},
            'weight': {'x': 227, 'y': 188, 'value': weight, 'page_num': 1},
            'bmi': {'x': 320, 'y': 188, 'value': f"{bmi:.2f}", 'page_num': 1},
            'sfhsehrklein': {'x': 115, 'y': 237, 'value': sfhsehrklein, 'page_num': 1},
            'doctor': {'x': 115, 'y': 263, 'value': self.doctor_input.text(), 'page_num': 1},
            'pflege': {'x': 115, 'y': 290, 'value': pflege, 'page_num': 1},
            'station': {'x': 320, 'y': 237, 'value': 'Station 22', 'page_num': 1},
            'tel': {'x': 320, 'y': 263, 'value': tel, 'page_num': 1},
            'pflegetel': {'x': 320, 'y': 290, 'value': pflegetel, 'page_num': 1},
            'sofort': {'x': 220, 'y': 317, 'value': sofort, 'page_num': 1},
            'atemweg_date': {'x': 140, 'y': 426, 'value': airway_date, 'page_num': 1},
            'tk_date': {'x': 320, 'y': 445, 'value': self.tk_date_input.text(), 'page_num': 1},
            'next_of_kin_and_tel': {'x': 223, 'y': 739, 'value': f"{self.next_of_kin_input.text()} / {self.next_of_kin_tel_input.text()}", 'page_num': 1},
            'fio2': {'x': 80, 'y': 508, 'value': self.fio2_input.text(), 'page_num': 1},
            'po2': {'x': 175, 'y': 508, 'value': f"{self.po2_input.text()} mmHg", 'page_num': 1},
            'pco2': {'x': 280, 'y': 508, 'value': f"{self.pco2_input.text()} mmHg", 'page_num': 1},
            'ph': {'x': 80, 'y': 530, 'value': self.ph_input.text(), 'page_num': 1},
            'be': {'x': 175, 'y': 530, 'value': self.be_input.text(), 'page_num': 1},
            'hco3': {'x': 280, 'y': 530, 'value': f"{self.hco3_input.text()} mmol/l", 'page_num': 1},
            'preconditionsrel1': {'x': 140, 'y': 365, 'value': f"HD: {airway_dg}, ND: {preconditionsrel1}", 'page_num': 1},
            'mobilisation': {'x': 40, 'y': 638, 'value': self.mobilisation_combo.currentText(), 'page_num': 1},
            'dekubitus': {'x': 40, 'y': 675, 'value': dekubitus, 'page_num': 1},
        }

        data_antrag11 = {
            'name': {'x': 50, 'y': 270, 'value': f"{first_name} {last_name}", 'page_num': 1},
            'namerv': {'x': 45, 'y': 62, 'value': f"{last_name}, {first_name}", 'page_num': 2},
            'birthdate': {'x': 50, 'y': 285, 'value': birthdate, 'page_num': 1},
            'street': {'x': 50, 'y': 300, 'value': self.street_input.text(), 'page_num': 1},
            'plz_and_city': {'x': 50, 'y': 315, 'value': f"{self.plz_input.text()} {self.city_input.text()}", 'page_num': 1},
            'cd_first_digit': {'x': 422, 'y': 244, 'value': cd_first_digit, 'page_num': 1},
            'cd_second_digit': {'x': 439, 'y': 244, 'value': cd_second_digit, 'page_num': 1},
            'cd_third_digit': {'x': 458, 'y': 244, 'value': cd_third_digit, 'page_num': 1},
            'cd_fourth_digit': {'x': 475, 'y': 244, 'value': cd_fourth_digit, 'page_num': 1},
            'cd_eight_digit': {'x': 543, 'y': 244, 'value': cd_eighth_digit, 'page_num': 1},
            'bd_first_digit': {'x': 402, 'y': 367, 'value': bd_first_digit, 'page_num': 1},
            'bd_second_digit': {'x': 419, 'y': 367, 'value': bd_second_digit, 'page_num': 1},
            'bd_third_digit': {'x': 438, 'y': 367, 'value': bd_third_digit, 'page_num': 1},
            'bd_fourth_digit': {'x': 455, 'y': 367, 'value': bd_fourth_digit, 'page_num': 1},
            'bd_fifth_digit': {'x': 473, 'y': 367, 'value': bd_fifth_digit, 'page_num': 1},
            'bd_sixth_digit': {'x': 490, 'y': 367, 'value': bd_sixth_digit, 'page_num': 1},
            'bd_seventh_digit': {'x': 508, 'y': 367, 'value': bd_seventh_digit, 'page_num': 1},
            'bd_eight_digit': {'x': 523, 'y': 367, 'value': bd_eighth_digit, 'page_num': 1},
            'sfh': {'x': 50, 'y': 446, 'value': sfh, 'page_num': 1},
            'doctor_and_tel': {'x': 50, 'y': 496, 'value': f"{self.doctor_input.text()} / {tel}", 'page_num': 1},
            'pflege_and_tel': {'x': 50, 'y': 546, 'value': f"{pflege} / {pflegetel}", 'page_num': 1},
            'preconditionsrel1': {'x': 50, 'y': 680, 'value': preconditionsrel1, 'page_num': 1},
            'aw_11': {'x': 48, 'y': 123, 'value': aw_1[:-1], 'page_num': 2},
            'aw_12': {'x': 65, 'y': 123, 'value': aw_1[-1], 'page_num': 2},
            'aw_21': {'x': 84, 'y': 123, 'value': aw_2[:-1], 'page_num': 2},
            'aw_22': {'x': 101, 'y': 123, 'value': aw_2[-1], 'page_num': 2},
            'aw_33': {'x': 150, 'y': 123, 'value': '2', 'page_num': 2},
            'aw_34': {'x': 169, 'y': 123, 'value': aw_3[3], 'page_num': 2},
            'pco2': {'x': 309, 'y': 193, 'value': self.pco2_input.text(), 'page_num': 2},
            'po2': {'x': 375, 'y': 193, 'value': self.po2_input.text(), 'page_num': 2},
            'fio2': {'x': 452, 'y': 193, 'value': self.fio2_input.text(), 'page_num': 2},
            'mmHg': [ 
                {'x': 302, 'y': 208, 'value': 'mmHg', 'page_num': 2},
                {'x': 368, 'y': 208, 'value': 'mmHg', 'page_num': 2},],
            'crp': {'x': 215, 'y': 272, 'value': crp_value, 'page_num': 2},
            'crp_unit': {'x': 212, 'y': 288, 'value': crp_unit, 'page_num': 2},
            'hb': {'x': 277, 'y': 272, 'value': hb_value, 'page_num': 2},
            'hb_unit': {'x': 274, 'y': 288, 'value': hb_unit, 'page_num': 2},
            'krea': {'x': 394, 'y': 272, 'value': krea_value, 'page_num': 2},
            'krea_unit': {'x': 391, 'y': 288, 'value': krea_unit, 'page_num': 2},
            'weight1': {'x': 108, 'y': 660, 'value': weight1, 'page_num': 2},
            'weight2': {'x': 124, 'y': 660, 'value': weight2, 'page_num': 2},
            'weight3': {'x': 140, 'y': 660, 'value': weight3, 'page_num': 2},
            'height1': {'x': 244, 'y': 660, 'value': height1, 'page_num': 2},
            'height2': {'x': 260, 'y': 660, 'value': height2, 'page_num': 2},
            'height3': {'x': 276, 'y': 660, 'value': height3, 'page_num': 2},
            'dialyseart': {'x': 190, 'y': 380, 'value': self.dialyse_combo.currentText(), 'page_num': 2},
        }

        data_antrag12 = {
            'sfhklein': {'x': 70, 'y': 210, 'value': sfhklein, 'page_num': 1},
            'itsaddr1': {'x': 70, 'y': 220, 'value': itsaddr1, 'page_num': 1},
            'itsaddr2': {'x': 70, 'y': 230, 'value': itsaddr2, 'page_num': 1},
            'doctor': {'x': 70, 'y': 265, 'value': self.doctor_input.text(), 'page_num': 1},
            '22': {'x': 90, 'y': 305, 'value': '22', 'page_num': 1},
            'tel': {'x': 160, 'y': 305, 'value': tel, 'page_num': 1},
            'fax': {'x': 290, 'y': 305, 'value': fax, 'page_num': 1},
            'sofort': {'x': 290, 'y': 327, 'value': sofort, 'page_num': 1},
            'last_name': {'x': 330, 'y': 210, 'value': last_name, 'page_num': 1},
            'first_name': {'x': 330, 'y': 235, 'value': first_name, 'page_num': 1},
            'birthdate': {'x': 370, 'y': 260, 'value': birthdate, 'page_num': 1},
            'city': {'x': 370, 'y': 274, 'value': self.city_input.text(), 'page_num': 1},  
            'next_of_kin_and_tel': {'x': 290, 'y': 352, 'value': f"{self.next_of_kin_input.text()} / {self.next_of_kin_tel_input.text()}", 'page_num': 1},
            'tk_date': {'x': 320, 'y': 578, 'value': self.tk_date_input.text(), 'page_num': 1},
            'modus': {'x': 230, 'y': 617, 'value': self.modus_input.text(), 'page_num': 1},
            'resistente_erreger': {'x': 325, 'y': 731, 'value': reserreger, 'page_num': 1},
            'crp': {'x': 215, 'y': 109, 'value': crp_value, 'page_num': 2},
            'krea': {'x': 215, 'y': 122, 'value': krea_value, 'page_num': 2},
            'bnp': {'x': 215, 'y': 135, 'value': bnp_value, 'page_num': 2},
            'po2': {'x': 270, 'y': 199, 'value': f"{self.po2_input.text()} mmHg", 'page_num': 2},
            'pco2': {'x': 349, 'y': 199, 'value': f"{self.pco2_input.text()} mmHg", 'page_num': 2},
            'ph': {'x': 420, 'y': 199, 'value': self.ph_input.text(), 'page_num': 2},
            'fio2': {'x': 490, 'y': 199, 'value': self.fio2_input.text(), 'page_num': 2},
            'hb': {'x': 298, 'y': 110, 'value': hb_value, 'page_num': 2},
            'harnstoff': {'x': 335, 'y': 123, 'value': harnstoff_value, 'page_num': 2},
            'leuko': {'x': 385, 'y': 109, 'value': leuko_value, 'page_num': 2},
            'height,weight': {'x': 240, 'y': 537, 'value': f"{height} kg, {weight} cm", 'page_num': 2},
            'current_date': {'x': 100, 'y': 695, 'value': current_date, 'page_num': 2},
            'airway_date': {'x': 146, 'y': 539, 'value': airway_date, 'page_num': 1},
            'current_ab': {'x': 240, 'y': 782, 'value': current_ab, 'page_num': 1},
        }

        data_antrag13 = {
            'sfh': {'x': 160, 'y': 515, 'value': f"{sfh} 22", 'page_num': 1},
            'X': [
                {'x': 59, 'y': 455, 'value': 'X', 'page_num': 1}, # wenn Weaning
                {'x': 165, 'y': 558, 'value': 'X', 'page_num': 1},],
            'doctor': {'x': 165, 'y': 620, 'value': self.doctor_input.text(), 'page_num': 1},
            'tel': [
                {'x': 320, 'y': 620, 'value': tel, 'page_num': 1},
                {'x': 270, 'y': 740, 'value': tel, 'page_num': 1},],
            'pflege': {'x': 165, 'y': 660, 'value': pflege, 'page_num': 1},
            'pflegetel': {'x': 370, 'y': 660, 'value': pflegetel, 'page_num': 1},
            'fax': {'x': 150, 'y': 700, 'value': fax, 'page_num': 1},
            'height': {'x': 100, 'y': 192, 'value': height, 'page_num': 2},
            'weight': {'x': 215, 'y': 192, 'value': weight, 'page_num': 2},
            'next_of_kin_and_tel': {'x': 60, 'y': 299, 'value': f"{self.next_of_kin_input.text()} / {self.next_of_kin_tel_input.text()}", 'page_num': 2},
            'airway_date': {'x': 130, 'y': 47, 'value': airway_date, 'page_num': 3},
            'tk_date': {'x': 275, 'y': 47, 'value': self.tk_date_input.text(), 'page_num': 3},
            'modus': {'x': 435, 'y': 80, 'value': self.modus_input.text(), 'page_num': 3},
            'po2': {'x': 190, 'y': 503, 'value': self.po2_input.text(), 'page_num': 3},
            'pco2': {'x': 295, 'y': 503, 'value': self.pco2_input.text(), 'page_num': 3},
            'ph': {'x': 380, 'y': 503, 'value': self.ph_input.text(), 'page_num': 3},
            'hco3': {'x': 450, 'y': 503, 'value': self.hco3_input.text(), 'page_num': 3},
            'crp': {'x': 150, 'y': 520, 'value': f"{crp_value} {crp_unit}", 'page_num': 3},
            'normcrp': {'x': 260, 'y': 520, 'value': '<5 mg/L', 'page_num': 3},
            'hb_hkt': {'x': 220, 'y': 550, 'value': f"{hb_value} {hb_unit} / {hkt_value}", 'page_num': 3},
            'krea_harnstoff': {'x': 150, 'y': 237, 'value': f"{krea_value} {krea_unit} / {harnstoff_value} {harnstoff_unit}", 'page_num': 3},
            'name': {'x': 160, 'y': 82, 'value': f"{first_name} {last_name}", 'page_num': 4},
            'cvc': {'x': 200, 'y': 241, 'value': self.cvc_combo.currentText(), 'page_num': 4},
            'cvc_date': {'x': 335, 'y': 241, 'value': self.cvc_date_input.text(), 'page_num': 4},  
            'nikotin_py': {'x': 464, 'y': 637, 'value': f"{self.nikotin_py_textinput.text()}py", 'page_num': 2},
            'medikation': {'x': 60, 'y': 500, 'value': medikation, 'page_num': 2},
            'katecholamine': {'x': 230, 'y': 450, 'value': katecholamine, 'page_num': 3},
            'ernaehrung': {'x': 130, 'y': 660, 'value': ernaehrung, 'page_num': 3},
            'sofort': {'x': 370, 'y': 790, 'value': sofort, 'page_num': 3},
        }

        data_antrag14 = {
            'sfh': {'x': 140, 'y': 152, 'value': sfh, 'page_num': 1},
            'doctor': {'x': 170, 'y': 179, 'value': self.doctor_input.text(), 'page_num': 1},
            'tel': {'x': 85, 'y': 200, 'value': tel, 'page_num': 1},
            'fax': {'x': 230, 'y': 200, 'value': fax, 'page_num': 1},
            'email': {'x': 395, 'y': 200, 'value': email, 'page_num': 1},
            'height': {'x': 290, 'y': 245, 'value': f"{height} cm", 'page_num': 1},
            'weight': {'x': 300, 'y': 266, 'value': f"{weight} kg", 'page_num': 1},
            'airway_date': {'x': 320, 'y': 287, 'value': airway_date, 'page_num': 1},
            'tk_date': {'x': 340, 'y': 330, 'value': self.tk_date_input.text(), 'page_num': 1},
            'modus': {'x': 400, 'y': 374, 'value': self.modus_input.text(), 'page_num': 1},
            'spitzendruck': {'x': 313, 'y': 402, 'value': self.spitzendruck_input.text(), 'page_num': 1},
            'peep': {'x': 401, 'y': 402, 'value': self.peep_input.text(), 'page_num': 1},
            'fio2': {'x': 450, 'y': 402, 'value': self.fio2_input.text(), 'page_num': 1},
            'af': {'x': 497, 'y': 402, 'value': self.atemfrequenz_input.text(), 'page_num': 1},
            'tinsp': {'x': 540, 'y': 402, 'value': self.tinsp_input.text(), 'page_num': 1},
            'po2': {'x': 272, 'y': 537, 'value': self.po2_input.text(), 'page_num': 1},
            'pco2': {'x': 332, 'y': 537, 'value': self.pco2_input.text(), 'page_num': 1},
            'ph': {'x': 375, 'y': 537, 'value': self.ph_input.text(), 'page_num': 1},
            'be': {'x': 420, 'y': 537, 'value': self.be_input.text(), 'page_num': 1},
            'airway_dg': {'x': 100, 'y': 558, 'value': airway_dg, 'page_num': 1},
            'leukos': {'x': 105, 'y': 441, 'value': f"{leuko_value} {leuko_unit}", 'page_num': 2},
            'crp': {'x': 170, 'y': 441, 'value': f"{crp_value} {crp_unit}", 'page_num': 2},
            'pct': {'x': 238, 'y': 441, 'value': f"{pct_value} {pct_unit}", 'page_num': 2},
            'hb': {'x': 295, 'y': 441, 'value': f"{hb_value} {hb_unit}", 'page_num': 2},
            'krea': {'x': 367, 'y': 441, 'value': f"{krea_value} {krea_unit}", 'page_num': 2},
            'kalium': {'x': 515, 'y': 441, 'value': f"{k_value} {k_unit}", 'page_num': 2},
            'gfr': {'x': 442, 'y': 441, 'value': f"{gfr_value} {gfr_unit}", 'page_num': 2},
            'general_practitioner': {'x': 90, 'y': 528, 'value': self.general_practitioner_input.text(), 'page_num': 2},
            'current_date': {'x': 40, 'y': 680, 'value': current_date, 'page_num': 2},
            'preconditionsrel1': {'x': 140, 'y': 580, 'value': preconditionsrel1, 'page_num': 1},
            'erregernachweis': {'x': 150, 'y': 650, 'value': erregernachweis, 'page_num': 1},
            'current_ab': {'x': 140, 'y': 695, 'value': current_ab, 'page_num': 1},
            'katecholamine': {'x': 140, 'y': 715, 'value': katecholamine, 'page_num': 1},
            'rr': {'x': 435, 'y': 715, 'value': f"{self.rr_syst_input.text()}/{self.rr_diast_input.text()}mmHg", 'page_num': 1},
            'hf': {'x': 520, 'y': 715, 'value': f"{self.hf_input.text()} /min", 'page_num': 1},
        }

        if self.gender_combo.currentText() == 'männlich':     
            data_antrag2['gender_checkbox1'] = {'x': 453, 'y': 495, 'value': 'X', 'page_num': 1}
            data_antrag3['gender_checkbox2'] = {'x': 448, 'y': 392, 'value': 'X', 'page_num': 1}

        if self.gender_combo.currentText() == 'weiblich':     
            data_antrag2['gender_checkbox1'] = {'x': 530, 'y': 495, 'value': 'X', 'page_num': 1}
            data_antrag3['gender_checkbox2'] = {'x': 495, 'y': 394, 'value': 'X', 'page_num': 1}

        if self.atemweg_combo.currentText() == 'Tubus' or self.atemweg_combo.currentText() == 'Trachealkanüle':
            data_antrag4['invasiv_checkbox1'] = {'x': 215, 'y': 54, 'value': 'X', 'page_num': 2}  

        if self.atemweg_combo.currentText() == 'Tubus':     
            data_antrag2['atemweg_checkbox1'] = {'x': 252, 'y': 174, 'value': 'X', 'page_num': 2}
            data_antrag3['atemweg_checkbox2'] = {'x': 205, 'y': 748, 'value': 'X', 'page_num': 1}
            data_antrag5['atemweg_checkbox3'] = {'x': 359, 'y': 511, 'value': 'X', 'page_num': 1}
            data_antrag5['atemweg_checkbox4'] = {'x': 267, 'y': 495, 'value': 'X', 'page_num': 1}
            data_antrag6['atemweg_checkbox5'] = {'x': 37, 'y': 336, 'value': 'X', 'page_num': 1}
            data_antrag10['atemweg_checkbox6'] = {'x': 312, 'y': 426, 'value': 'X', 'page_num': 1}
            data_antrag4['atemweg_checkbox7'] = {'x': 207, 'y': 155, 'value': 'X', 'page_num': 2}
            data_antrag12['atemweg_checkbox8'] = {'x': 149, 'y': 578, 'value': 'X', 'page_num': 1}
            data_antrag14['atemweg_checkbox9'] = {'x': 390, 'y': 311, 'value': 'X', 'page_num': 1}


        if self.atemweg_combo.currentText() == 'Trachealkanüle':     
            data_antrag2['atemweg_checkbox1'] = {'x': 335, 'y': 174, 'value': 'X', 'page_num': 2}
            data_antrag3['atemweg_checkbox2'] = {'x': 290, 'y': 748, 'value': 'X', 'page_num': 1}
            data_antrag5['atemweg_checkbox3'] = {'x': 359, 'y': 541, 'value': 'X', 'page_num': 1}
            data_antrag6['atemweg_checkbox4'] = {'x': 37, 'y': 336, 'value': 'X', 'page_num': 1}
            data_antrag6['atemweg_checkbox5'] = {'x': 214, 'y': 336, 'value': 'X', 'page_num': 1}
            data_antrag6['atemweg_checkbox6'] = {'x': 426, 'y': 336, 'value': 'X', 'page_num': 1}
            data_antrag7['atemweg_checkbox7'] = {'x': 171, 'y': 561, 'value': 'X', 'page_num': 1}
            data_antrag7['atemweg_checkbox8'] = {'x': 376, 'y': 561, 'value': 'X', 'page_num': 1}
            data_antrag8['atemweg_checkbox9'] = {'x': 358, 'y': 728, 'value': 'X', 'page_num': 2}
            data_antrag10['atemweg_checkbox10'] = {'x': 432, 'y': 426, 'value': 'X', 'page_num': 1}
            data_antrag10['atemweg_checkbox11'] = {'x': 495, 'y': 445, 'value': 'X', 'page_num': 1}
            data_antrag4['atemweg_checkbox12'] = {'x': 207, 'y': 181, 'value': 'X', 'page_num': 2}
            data_antrag11['atemweg_checkbox13'] = {'x': 186, 'y': 238, 'value': 'X', 'page_num': 2}
            data_antrag11['atemweg_checkbox14'] = {'x': 408, 'y': 238, 'value': 'X', 'page_num': 2}
            data_antrag12['atemweg_checkbox15'] = {'x': 264, 'y': 578, 'value': 'X', 'page_num': 1}
            data_antrag13['atemweg_checkbox16'] = {'x': 413, 'y': 47, 'value': 'X', 'page_num': 3}
            data_antrag13['atemweg_checkbox17'] = {'x': 98, 'y': 135, 'value': 'X', 'page_num': 4}
            data_antrag14['atemweg_checkbox18'] = {'x': 505, 'y': 311, 'value': 'X', 'page_num': 1}
            data_antrag14['atemweg_checkbox19'] = {'x': 511, 'y': 332, 'value': 'X', 'page_num': 1}


        if reserreger: #(wenn nicht leer)
            data_antrag10['resistente_erreger1'] = {'x': 280, 'y': 601, 'value': reserreger, 'page_num': 1}
            data_antrag10['resistente_erreger2'] = {'x': 127, 'y': 602, 'value': 'X', 'page_num': 1}

        if self.checkbox_mrsa1.isChecked() or self.checkbox_mrsa2.isChecked():
            data_antrag3['resistente_erreger_checkbox1'] = {'x': 320, 'y': 530, 'value': 'X', 'page_num': 2}
            data_antrag5['resistente_erreger_checkbox2a'] = {'x': 231, 'y': 271, 'value': 'X', 'page_num': 2}
            data_antrag5['resistente_erreger'] = {'x': 120, 'y': 271, 'value': mrsavalue, 'page_num': 2}
            data_antrag6['resistente_erreger_checkbox3'] = {'x': 214, 'y': 482, 'value': 'X', 'page_num': 1}
            data_antrag7['resistente_erreger_checkbox4'] = {'x': 202, 'y': 600, 'value': 'X', 'page_num': 1}
            data_antrag8['resistente_erreger_checkbox5'] = {'x': 200, 'y': 590, 'value': 'X', 'page_num': 3}
            data_antrag8['resistente_erreger_checkbox6'] = {'x': 240, 'y': 610, 'value': 'X', 'page_num': 3}
            data_antrag9['resistente_erreger_checkbox7'] = {'x': 144, 'y': 218, 'value': 'X', 'page_num': 2}
            data_antrag11['resistente_erreger_checkbox8'] = {'x': 186, 'y': 732, 'value': 'X', 'page_num': 1}
            data_antrag12['resistente_erreger_checkbox9'] = {'x': 427, 'y': 705, 'value': 'X', 'page_num': 1}
            data_antrag13['resistente_erreger_checkbox10'] = {'x': 379, 'y': 276, 'value': 'X', 'page_num': 3}
            data_antrag14['resistente_erreger_checkbox11'] = {'x': 38, 'y': 673, 'value': 'X', 'page_num': 1}

        if self.checkbox_3mrgn.isChecked() or self.checkbox_4mrgn.isChecked():
            data_antrag3['resistente_erreger_checkbox1a'] = {'x': 320, 'y': 543, 'value': 'X', 'page_num': 2}
            data_antrag5['resistente_erreger_checkbox2b'] = {'x': 231, 'y': 308, 'value': 'X', 'page_num': 2}
            data_antrag5['resistente_erreger1'] = {'x': 80, 'y': 322, 'value': mrgnvalue, 'page_num': 2}
            data_antrag7['resistente_erreger_checkbox3'] = {'x': 202, 'y': 600, 'value': 'X', 'page_num': 1}
            data_antrag9['resistente_erreger_checkbox4'] = {'x': 144, 'y': 235, 'value': 'X', 'page_num': 2}
            data_antrag11['resistente_erreger_checkbox5'] = {'x': 252, 'y': 753, 'value': 'X', 'page_num': 1}
            data_antrag11['resistente_erreger2'] = {'x': 350, 'y': 754, 'value': mrgnvalue, 'page_num': 1}

        if self.checkbox_3mrgn.isChecked():
            data_antrag8['resistente_erreger_checkbox1'] = {'x': 320, 'y': 610, 'value': 'X', 'page_num': 3}
            data_antrag8['resistente_erreger_checkbox2'] = {'x': 200, 'y': 590, 'value': 'X', 'page_num': 3}
            data_antrag9['resistente_erreger_checkbox3'] = {'x': 79, 'y': 236, 'value': 'X', 'page_num': 2}
            data_antrag13['resistente_erreger_checkbox4'] = {'x': 200, 'y': 276, 'value': 'X', 'page_num': 3}
            data_antrag14['resistente_erreger_checkbox5.1'] = {'x': 195, 'y': 673, 'value': 'X', 'page_num': 1}



        if self.checkbox_4mrgn.isChecked():
            data_antrag8['resistente_erreger_checkbox1'] = {'x': 398, 'y': 610, 'value': 'X', 'page_num': 3}
            data_antrag8['resistente_erreger_checkbox2'] = {'x': 200, 'y': 590, 'value': 'X', 'page_num': 3}
            data_antrag9['resistente_erreger_checkbox3'] = {'x': 104, 'y': 236, 'value': 'X', 'page_num': 2}
            data_antrag13['resistente_erreger_checkbox4'] = {'x': 108, 'y': 276, 'value': 'X', 'page_num': 3}
            data_antrag14['resistente_erreger_checkbox5.2'] = {'x': 101, 'y': 673, 'value': 'X', 'page_num': 1}



        if self.checkbox_vre1.isChecked() or self.checkbox_vre2.isChecked():
            data_antrag6['resistente_erreger_checkbox1'] = {'x': 320, 'y': 469, 'value': 'X', 'page_num': 1}
            data_antrag7['resistente_erreger_checkbox2'] = {'x': 202, 'y': 600, 'value': 'X', 'page_num': 1}
            data_antrag8['resistente_erreger_checkbox3'] = {'x': 200, 'y': 590, 'value': 'X', 'page_num': 3}
            data_antrag8['resistente_erreger_checkbox4'] = {'x': 478, 'y': 610, 'value': 'X', 'page_num': 3}
            data_antrag9['resistente_erreger_checkbox5'] = {'x': 144, 'y': 252, 'value': 'X', 'page_num': 2}
            data_antrag11['resistente_erreger_checkbox6'] = {'x': 184, 'y': 754, 'value': 'X', 'page_num': 1}
            data_antrag13['resistente_erreger_checkbox7'] = {'x': 448, 'y': 276, 'value': 'X', 'page_num': 3}
            data_antrag14['resistente_erreger_checkbox8'] = {'x': 323, 'y': 673, 'value': 'X', 'page_num': 1}

        if self.checkbox_cdiff.isChecked():
            data_antrag2['cdiff_checkbox0'] = {'x': 340, 'y': 396, 'value': 'positiv', 'page_num': 2}
            data_antrag3['cdiff_checkbox1'] = {'x': 320, 'y': 557, 'value': 'X', 'page_num': 2}
            data_antrag6['cdiff_checkbox2'] = {'x': 214, 'y': 494, 'value': 'X', 'page_num': 1}
            data_antrag8['cdiff_checkbox3'] = {'x': 320, 'y': 630, 'value': 'X', 'page_num': 3}
            data_antrag8['cdiff_checkbox4'] = {'x': 200, 'y': 590, 'value': 'X', 'page_num': 3}
            data_antrag13['cdiff_checkbox5'] = {'x': 271, 'y': 276, 'value': 'X', 'page_num': 3}
            data_antrag14['cdiff_checkbox6'] = {'x': 263, 'y': 673, 'value': 'X', 'page_num': 1}
        else:
            data_antrag3['cdiff_checkbox1'] = {'x': 214, 'y': 557, 'value': 'X', 'page_num': 2}


        if self.c19_combo.currentText() == 'aktuell positiv':
            data_antrag9['c19p_checkbox1'] = {'x': 144, 'y': 305, 'value': 'X', 'page_num': 2}
            data_antrag13['c19p_checkbox2'] = {'x': 59, 'y': 292, 'value': 'X', 'page_num': 3}
            data_antrag13['c19p_checkbox3'] = {'x': 165, 'y': 292, 'value': 'X', 'page_num': 3}
            data_antrag13['ct_wert1'] = {'x': 300, 'y': 292, 'value': self.ctwert_input.text(), 'page_num': 3}

        if self.c19_combo.currentText() == 'aktuell negativ':
            data_antrag13['c19n_checkbox1'] = {'x': 165, 'y': 308, 'value': 'X', 'page_num': 3}

        if self.c19_verdacht_combo.currentText() == 'ja':
            data_antrag9['c19__verdacht_checkbox1'] = {'x': 144, 'y': 270, 'value': 'X', 'page_num': 2}

        if self.c19_negtest_date_input.text():
            data_antrag9['c19_negtest_date'] = {'x': 144, 'y': 289, 'value': 'X', 'page_num': 2}

        if self.checkbox_znc19.isChecked():
            data_antrag9['znc19_checkbox1'] = {'x': 144, 'y': 323, 'value': 'X', 'page_num': 2}
            data_antrag13['znc19_checkbox2'] = {'x': 377, 'y': 308, 'value': 'X', 'page_num': 3}
        
            
        if self.artery_combo.currentText(): #(wenn nicht leer)
            data_antrag9['artery_checkbox1'] = {'x': 144, 'y': 629, 'value': 'X', 'page_num': 2}
            data_antrag12['artery_checkbox2'] = {'x': 356, 'y': 275, 'value': 'X', 'page_num': 2}
            data_antrag14['artery_checkbox4'] = {'x': 110, 'y': 398, 'value': 'X', 'page_num': 2}
            data_antrag4['artery_checkbox5'] = {'x': 24, 'y': 289, 'value': 'X', 'page_num': 2}

        else: #für Antrag 12
            data_antrag12['artery_checkbox1'] = {'x': 285, 'y': 275, 'value': 'X', 'page_num': 2}

        if self.artery_combo.currentText() == 'Radialis re.':
            data_antrag5['artery_checkbox1'] = {'x': 285, 'y': 652, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox2'] = {'x': 223, 'y': 654, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox3'] = {'x': 360, 'y': 652, 'value': 'X', 'page_num': 1}

        if self.artery_combo.currentText() == 'Radialis li.':
            data_antrag5['artery_checkbox1'] = {'x': 318, 'y': 652, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox2'] = {'x': 223, 'y': 654, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox3'] = {'x': 360, 'y': 652, 'value': 'X', 'page_num': 1}

        if self.artery_combo.currentText() == 'A. Femoralis re.':     
            data_antrag5['artery_checkbox1'] = {'x': 285, 'y': 652, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox2'] = {'x': 223, 'y': 654, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox3'] = {'x': 395, 'y': 652, 'value': 'X', 'page_num': 1}

        if self.artery_combo.currentText() == 'A. Femoralis li.':     
            data_antrag5['artery_checkbox1'] = {'x': 318, 'y': 652, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox2'] = {'x': 223, 'y': 654, 'value': 'X', 'page_num': 1}
            data_antrag5['artery_checkbox3'] = {'x': 395, 'y': 652, 'value': 'X', 'page_num': 1}

        if self.cvc_combo.currentText(): #(wenn nicht leer)
            data_antrag9['cvc_checkbox1'] = {'x': 219, 'y': 645, 'value': 'X', 'page_num': 2}
            data_antrag12['cvc_checkbox2'] = {'x': 356, 'y': 263, 'value': 'X', 'page_num': 2}
            data_antrag13['cvc_checkbox3'] = {'x': 110, 'y': 241, 'value': 'ZVK', 'page_num': 4}
            data_antrag14['cvc_checkbox4'] = {'x': 110, 'y': 377, 'value': 'X', 'page_num': 2}
            data_antrag4['cvc_checkbox5'] = {'x': 24, 'y': 263, 'value': 'X', 'page_num': 2}
        else: #für Antrag 12
            data_antrag12['cvc_checkbox1'] = {'x': 285, 'y': 263, 'value': 'X', 'page_num': 2}

        if self.cvc_combo.currentText() == 'V. jugularis int. re.':     
            data_antrag5['cvc_checkbox1'] = {'x': 285, 'y': 666, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox2'] = {'x': 223, 'y': 668, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox3'] = {'x': 360, 'y': 666, 'value': 'X', 'page_num': 1}
        
        if self.cvc_combo.currentText() == 'V. jugularis int. li.':     
            data_antrag5['cvc_checkbox1'] = {'x': 318, 'y': 666, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox2'] = {'x': 223, 'y': 668, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox3'] = {'x': 360, 'y': 666, 'value': 'X', 'page_num': 1}

        if self.cvc_combo.currentText() == 'V. subclavia re.':     
            data_antrag5['cvc_checkbox1'] = {'x': 285, 'y': 666, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox2'] = {'x': 223, 'y': 668, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox3'] = {'x': 405, 'y': 666, 'value': 'X', 'page_num': 1}

        if self.cvc_combo.currentText() == 'V. subclavia li.':     
            data_antrag5['cvc_checkbox1'] = {'x': 318, 'y': 666, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox2'] = {'x': 223, 'y': 668, 'value': 'X', 'page_num': 1}
            data_antrag5['cvc_checkbox3'] = {'x': 405, 'y': 666, 'value': 'X', 'page_num': 1}

        if 'jugularis' in self.cvc_combo.currentText():
            data_antrag12['cvc_checkbox1'] = {'x': 435, 'y': 260, 'value': '________', 'page_num': 2}

        if 'subclavia' in self.cvc_combo.currentText():
            data_antrag12['cvc_checkbox1'] = {'x': 390, 'y': 260, 'value': '________', 'page_num': 2}

        if self.bladder_combo.currentText() == 'Transurethraler DK':
            data_antrag5['bladder_checkbox1'] = {'x': 223, 'y': 696, 'value': 'X', 'page_num': 1}
            data_antrag9['bladder-checkbox2'] = {'x': 215, 'y': 661, 'value': 'X', 'page_num': 2}
            data_antrag12['bladder_checkbox4'] = {'x': 265, 'y': 298, 'value': '_______________________', 'page_num': 2}
            data_antrag2['bladder_checkbox6'] = {'x': 382, 'y': 551, 'value': 'X', 'page_num': 2}
            data_antrag4['bladder_checkbox7'] = {'x': 25, 'y': 312, 'value': 'X', 'page_num': 2}
        if self.bladder_combo.currentText() == 'Suprapubischer DK':
            data_antrag5['bladder_checkbox1'] = {'x': 462, 'y': 696, 'value': 'X', 'page_num': 1}
            data_antrag9['bladder-checkbox2'] = {'x': 215, 'y': 679, 'value': 'X', 'page_num': 2}
            data_antrag12['bladder_checkbox4'] = {'x': 178, 'y': 298, 'value': '_______________', 'page_num': 2}
            data_antrag14['bladder_checkbox5'] = {'x': 251, 'y': 398, 'value': 'X', 'page_num': 2}
            data_antrag2['bladder_checkbox6'] = {'x': 382, 'y': 551, 'value': 'X', 'page_num': 2}
            data_antrag4['bladder_checkbox7'] = {'x': 25, 'y': 332, 'value': 'X', 'page_num': 2}



        if self.bladder_combo.currentText() == 'Transurethraler DK' or self.bladder_combo.currentText() == 'Suprapubischer DK':
            data_antrag12['bladder_checkbox3'] = {'x': 462, 'y': 302, 'value': 'X', 'page_num': 2}
        else:
            data_antrag12['bladder_checkbox3'] = {'x': 391, 'y': 301, 'value': 'X', 'page_num': 2}

        if self.magensonde_combo.currentText() == 'Nasogastral':
            # Ankreuzfeld für Nasogastral
            data_antrag5['magensonde_checkbox1'] = {'x': 223, 'y': 711, 'value': 'X', 'page_num': 1}
            data_antrag9['magensonde_checkbox2'] = {'x': 144, 'y': 696, 'value': 'X', 'page_num': 2}
            data_antrag14['magensonde_checkbox3'] = {'x': 380, 'y': 398, 'value': 'X', 'page_num': 2}
            data_antrag12['magensonde_checkbox4'] = {'x': 285, 'y': 288, 'value': 'X', 'page_num': 2}

        if self.magensonde_combo.currentText() == 'PEG':
            # Ankreuzfeld für PEG
            data_antrag5['magensonde_checkbox1'] = {'x': 319, 'y': 711, 'value': 'X', 'page_num': 1}
            data_antrag9['magensonde_checkbox2'] = {'x': 199, 'y': 696, 'value': 'X', 'page_num': 2}
            data_antrag12['magensonde_checkbox4'] = {'x': 210, 'y': 285, 'value': '____', 'page_num': 2}

        if self.magensonde_combo.currentText() == 'PEJ':
            # Ankreuzfeld für PEJ
            data_antrag5['magensonde_checkbox2'] = {'x': 462, 'y': 711, 'value': 'X', 'page_num': 1}
            data_antrag12['magensonde_checkbox4'] = {'x': 180, 'y': 285, 'value': '____', 'page_num': 2}

        if self.magensonde_combo.currentText() == 'PEG' or self.magensonde_combo.currentText() == 'PEJ':
            data_antrag12['magensonde_checkbox3'] = {'x': 356, 'y': 289, 'value': 'X', 'page_num': 2}
            data_antrag14['magensonde_checkbox4'] = {'x': 302, 'y': 398, 'value': 'X', 'page_num': 2}     

        if bmi >= 30:
            data_antrag6['bmi_checkbox1'] = {'x': 42, 'y': 645, 'value': 'X', 'page_num': 1}
            data_antrag8['bmi_checkbox2'] = {'x': 406, 'y': 450, 'value': 'X', 'page_num': 2}
            data_antrag12['bmi_checkbox3'] = {'x': 73, 'y': 463, 'value': 'X', 'page_num': 1}


        if self.checkbox_aht.isChecked():
            data_antrag6['aht_checkbox1'] = {'x': 42, 'y': 557, 'value': 'X', 'page_num': 1}
            data_antrag4['aht_checkbox1'] = {'x': 136, 'y': 633, 'value': 'X', 'page_num': 1}
            data_antrag8['aht_checkbox2'] = {'x': 406, 'y': 430, 'value': 'X', 'page_num': 2}

        if self.checkbox_dm.isChecked():
            data_antrag6['diabetes_checkbox1'] = {'x': 42, 'y': 570, 'value': 'X', 'page_num': 1}
            data_antrag4['diabetes_checkbox2'] = {'x': 136, 'y': 649, 'value': 'X', 'page_num': 1}
            data_antrag8['diabetes_checkbox3'] = {'x': 406, 'y': 469, 'value': 'X', 'page_num': 2}
            data_antrag12['diabetes_checkbox4'] = {'x': 229, 'y': 476, 'value': 'X', 'page_num': 1}

        if self.checkbox_khk.isChecked():
            data_antrag6['khk_checkbox1'] = {'x': 42, 'y': 583, 'value': 'X', 'page_num': 1}
            data_antrag4['khk_checkbox2'] = {'x': 251, 'y': 633, 'value': 'X', 'page_num': 1}
            data_antrag8['khk_checkbox3'] = {'x': 80, 'y': 469, 'value': 'X', 'page_num': 2}
            data_antrag12['khk_checkbox4'] = {'x': 229, 'y': 450, 'value': 'X', 'page_num': 1}
        
        if self.checkbox_herzinsuff.isChecked():
            data_antrag6['herzinsuff_checkbox1'] = {'x': 42, 'y': 595, 'value': 'X', 'page_num': 1}
            data_antrag8['herzinsuff_checkbox2'] = {'x': 406, 'y': 412, 'value': 'X', 'page_num': 2}
            data_antrag12['herzinsuff_checkbox3'] = {'x': 229, 'y': 437, 'value': 'X', 'page_num': 1}

        if self.checkbox_pulmht.isChecked():
            data_antrag8['pulmht_checkbox1'] = {'x': 406, 'y': 488, 'value': 'X', 'page_num': 2}
        
        if self.checkbox_cni.isChecked() or self.checkbox_ani.isChecked():
            data_antrag6['ni_checkbox1'] = {'x': 42, 'y': 608, 'value': 'X', 'page_num': 1}
            data_antrag8['ni_checkbox2'] = {'x': 235, 'y': 468, 'value': 'X', 'page_num': 2}
            data_antrag12['ni_checkbox3'] = {'x': 229, 'y': 463, 'value': 'X', 'page_num': 1}

        if self.checkbox_cni.isChecked():
            data_antrag4['cni_checkbox1'] = {'x': 346, 'y': 649, 'value': 'X', 'page_num': 1}

        if self.checkbox_ani.isChecked():
            data_antrag4['ani_checkbox1'] = {'x': 136, 'y': 665, 'value': 'X', 'page_num': 1}
            data_antrag14['ani_checkbox2'] = {'x': 358, 'y': 120, 'value': 'X', 'page_num': 2}


        if self.checkbox_nikotin.isChecked():
            data_antrag4['nikotin_checkbox1'] = {'x': 136, 'y': 679, 'value': 'X', 'page_num': 1}
            data_antrag8['nikotin_checkbox2'] = {'x': 127, 'y': 609, 'value': 'X', 'page_num': 2}
            data_antrag13['nikotin_checkbox3'] = {'x': 200, 'y': 638, 'value': 'X', 'page_num': 2}

        if self.checkbox_alkohol.isChecked():   
            data_antrag4['alkohol_checkbox1'] = {'x': 251, 'y': 679, 'value': 'X', 'page_num': 1}
            data_antrag8['alkohol_checkbox2'] = {'x': 236, 'y': 583, 'value': 'X', 'page_num': 2}
            data_antrag13['alkohol_checkbox3'] = {'x': 236, 'y': 617, 'value': 'X', 'page_num': 2}

        if self.checkbox_dialyse.isChecked():
            data_antrag6['dialyse_checkbox1'] = {'x': 42, 'y': 620, 'value': 'X', 'page_num': 1}
            data_antrag4['dialyse_checkbox2'] = {'x': 251, 'y': 665, 'value': 'X', 'page_num': 1}
            data_antrag9['dialyse_checkbox3'] = {'x': 418, 'y': 678, 'value': 'X', 'page_num': 2}
            data_antrag2['dialyse_checkbox4'] = {'x': 178, 'y': 566, 'value': 'X', 'page_num': 2}
            data_antrag7['dialyse_checkbox5'] = {'x': 152, 'y': 480, 'value': 'X', 'page_num': 1}
            data_antrag5['dialyse_checkbox6'] = {'x': 230, 'y': 343, 'value': 'X', 'page_num': 2}
            data_antrag14['dialyse_checkbox7'] = {'x': 180, 'y': 120, 'value': 'X', 'page_num': 2}
            data_antrag3['dialyse_checkbox8'] = {'x': 320, 'y': 173, 'value': 'X', 'page_num': 2}
            data_antrag11['dialyse_checkbox9'] = {'x': 186, 'y': 336, 'value': 'X', 'page_num': 2}
            data_antrag12['dialyse_checkbox10'] = {'x': 285, 'y': 97, 'value': 'X', 'page_num': 2}
            data_antrag8['dialyse_checkbox11'] = {'x': 198, 'y': 472, 'value': 'X', 'page_num': 3}
        else:
            data_antrag3['dialyse_checkbox8'] = {'x': 214, 'y': 173, 'value': 'X', 'page_num': 2}
            data_antrag12['dialyse_checkbox10'] = {'x': 214, 'y': 97, 'value': 'X', 'page_num': 2}
            data_antrag8['dialyse_checkbox11'] = {'x': 148, 'y': 472, 'value': 'X', 'page_num': 3}

        
        if self.dialyse_combo.currentIndex() == 0:
            data_antrag10['dialyseart_checkbox1'] = {'x': 233, 'y': 565, 'value': 'X', 'page_num': 1}
        if self.dialyse_combo.currentIndex() == 1:
            data_antrag10['dialyseart_checkbox2'] = {'x': 134, 'y': 565, 'value': 'X', 'page_num': 1}

        
        if self.checkbox_pavk.isChecked():
            data_antrag6['pavk_checkbox1'] = {'x': 42, 'y': 633, 'value': 'X', 'page_num': 1}
            data_antrag4['pavk_checkbox2'] = {'x': 346, 'y': 633, 'value': 'X', 'page_num': 1}

        if self.checkbox_copd.isChecked():
            data_antrag4['copd_checkbox1'] = {'x': 347, 'y': 663    , 'value': 'X', 'page_num': 1}
            data_antrag8['copd_checkbox2'] = {'x': 80, 'y': 430, 'value': 'X', 'page_num': 2}
            data_antrag12['copd_checkbox3'] = {'x': 73, 'y': 437, 'value': 'X', 'page_num': 1}

        if self.checkbox_apoplex.isChecked():
            data_antrag4['apoplex_checkbox1'] = {'x': 251, 'y': 649, 'value': 'X', 'page_num': 1}

        if self.checkbox_neuromusk.isChecked():
            data_antrag4['neuromusk_checkbox1'] = {'x': 347, 'y': 678, 'value': 'X', 'page_num': 1}

        if self.checkbox_cip.isChecked():
            data_antrag8['cip_checkbox1'] = {'x': 80, 'y': 450, 'value': 'X', 'page_num': 2}
            data_antrag8['cip_checkbox2'] = {'x': 240, 'y': 329, 'value': 'X', 'page_num': 4}

        if self.checkbox_cim.isChecked():
            data_antrag8['cim_checkbox2'] = {'x': 240, 'y': 346, 'value': 'X', 'page_num': 4}

        if self.checkbox_cip.isChecked() or self.checkbox_cim.isChecked():
            data_antrag10['cipec_checkbox1'] = {'x': 280, 'y': 639, 'value': 'X', 'page_num': 1}

        if self.checkbox_interstit.isChecked():
            data_antrag8['interstit_checkbox1'] = {'x': 235, 'y': 412, 'value': 'X', 'page_num': 2}

        if self.checkbox_thorakorestr.isChecked():
            data_antrag8['thorakorestr_checkbox1'] = {'x': 235, 'y': 430, 'value': 'X', 'page_num': 2}
            data_antrag12['thorakorestr_checkbox2'] = {'x': 73, 'y': 450, 'value': 'X', 'page_num': 1}

        if self.checkbox_pneumonie.isChecked():
            data_antrag8['pneumonie_checkbox1'] = {'x': 235, 'y': 507, 'value': 'X', 'page_num': 2}

        if self.checkbox_neuromusk.isChecked():
            data_antrag8['neuromusk_checkbox1'] = {'x': 235, 'y': 449, 'value': 'X', 'page_num': 2}

        if self.checkbox_delir.isChecked():
            data_antrag8['delir_checkbox1'] = {'x': 80, 'y': 506, 'value': 'X', 'page_num': 2}

        if self.checkbox_osas.isChecked():
            data_antrag12['osas_checkbox1'] = {'x': 357, 'y': 437, 'value': 'X', 'page_num': 1}

        if self.station_combo.currentIndex() == 0:
            data_antrag8['station_checkbox1'] = {'x': 161, 'y': 604, 'value': 'X', 'page_num': 1}

        if self.station_combo.currentIndex() == 1:
            data_antrag8['station_checkbox2'] = {'x': 79, 'y': 604, 'value': 'X', 'page_num': 1}

        if self.katecholamine_combo.currentText() == 'ja':
            data_antrag2['katecholamine_checkbox1'] = {'x': 178, 'y': 537, 'value': 'X', 'page_num': 2}
            data_antrag3['katecholamine_checkbox2'] = {'x': 320, 'y': 147, 'value': 'X', 'page_num': 2}
            data_antrag7['katecholamine_checkbox3'] = {'x': 169, 'y': 453, 'value': 'X', 'page_num': 1}
            data_antrag9['katecholamine_checkbox4'] = {'x': 143, 'y': 448, 'value': 'X', 'page_num': 2}
            data_antrag11['katecholamine_checkbox5'] = {'x': 186, 'y': 306, 'value': 'X', 'page_num': 2}
            data_antrag12['katecholamine_checkbox6'] = {'x': 285, 'y': 83, 'value': 'X', 'page_num': 2}
            
        else:
            data_antrag2['katecholamine_checkbox1'] = {'x': 223, 'y': 537, 'value': 'X', 'page_num': 2}
            data_antrag3['katecholamine_checkbox2'] = {'x': 214, 'y': 147, 'value': 'X', 'page_num': 2}
            data_antrag12['katecholamine_checkbox6'] = {'x': 214, 'y': 83, 'value': 'X', 'page_num': 2}

        if self.katecholamine_checkbox1.isChecked():
            data_antrag4['noradrenalin-checkbox1'] = {'x': 356, 'y': 145, 'value': 'X', 'page_num': 3}
            data_antrag4['noradrenalin-info2'] = {'x': 473, 'y': 145, 'value': f"0,1% {self.noradrenalin_laufrate.text()} ml/h", 'page_num': 3}

        if self.katecholamine_checkbox2.isChecked():
            data_antrag4['adrenalin-checkbox1'] = {'x': 154, 'y': 145, 'value': 'X', 'page_num': 3}
            data_antrag4['adrenalin-info2'] = {'x': 248, 'y': 145, 'value': f"0,1% {self.adrenalin_laufrate.text()} ml/h", 'page_num': 3}

        if self.katecholamine_checkbox3.isChecked():
            data_antrag4['dobutamin-checkbox1'] = {'x': 154, 'y': 172, 'value': 'X', 'page_num': 3}
            data_antrag4['dobutamin-info2'] = {'x': 248, 'y': 172, 'value': f"0,1% {self.dobutamin_laufrate.text()} ml/h", 'page_num': 3}

        
        if self.sedierung_checkbox1.isChecked() or self.sedierung_checkbox2.isChecked() or self.sedierung_checkbox3.isChecked() or self.sedierung_checkbox4.isChecked() or self.sedierung_checkbox5.isChecked() or self.sedierung_checkbox6.isChecked():
            data_antrag3['sedierung_checkbox1'] = {'x': 323, 'y': 398, 'value': 'X', 'page_num': 2}
        else:
            data_antrag3['sedierung_checkbox2'] = {'x': 214, 'y': 398, 'value': 'X', 'page_num': 2}

        if self.sedierung_checkbox1.isChecked(): # Propofol
            data_antrag4['sedierung_checkbox1'] = {'x': 154, 'y': 252, 'value': 'X', 'page_num': 3}
            data_antrag4['sedierung_info1'] = {'x': 248, 'y': 252, 'value': f"2% {self.propofol_laufrate_input.text()} ml/h", 'page_num': 3}

        if self.sedierung_checkbox2.isChecked(): # Sufenta
            data_antrag4['sedierung_checkbox2'] = {'x': 356, 'y': 198, 'value': 'X', 'page_num': 3}
            data_antrag4['sedierung_info21'] = {'x': 420, 'y': 198, 'value': '5µg/ml', 'page_num': 3}
            data_antrag4['sedierung_info22'] = {'x': 473, 'y': 198, 'value': f"{self.sufenta_laufrate_input.text()} ml/h", 'page_num': 3}

        if self.sedierung_checkbox3.isChecked(): # Fentanyl
            data_antrag4['sedierung_checkbox3'] = {'x': 154, 'y': 198, 'value': 'X', 'page_num': 3}
            data_antrag4['sedierung_info3'] = {'x': 248, 'y': 199, 'value': f"{self.fenta_laufrate_input.text()}", 'page_num': 3}
        if self.ernaehrung_checkbox1.isChecked():
            data_antrag3['parenterale_checkbox1'] = {'x': 214, 'y': 239, 'value': 'X', 'page_num': 2}
            data_antrag4['parenterale_checkbox2'] = {'x': 64, 'y': 86, 'value': 'X', 'page_num': 3}
            data_antrag4['parenterale_info1'] = {'x': 145, 'y': 84, 'value': kcalparenterale, 'page_num': 3}
            data_antrag3['parenterale_info2'] = {'x': 230, 'y': 238, 'value': parenterale, 'page_num': 2} 
            data_antrag5['parenterale_checkbox3'] = {'x': 319, 'y': 726, 'value': 'X', 'page_num': 1}  

        if self.ernaehrung_checkbox1.isChecked() and self.cvc_combo.currentText():
            data_antrag13['parenterale_checkbox5'] = {'x': 377, 'y': 641, 'value': 'X', 'page_num': 3}

        if self.ernaehrung_checkbox2.isChecked():
            data_antrag4['enterale_info1'] = {'x': 480, 'y': 58, 'value': kcalenterale, 'page_num': 3}
            data_antrag4['enterale_checkbox1'] = {'x': 64, 'y': 58, 'value': 'X', 'page_num': 3}
            data_antrag4['enterale_info2'] = {'x': 337, 'y': 58, 'value': f"Fresubin SK {self.ernaehrung_enteral_combo.currentText()}", 'page_num': 3}
            data_antrag5['enterale_checkbox2'] = {'x': 223, 'y': 726, 'value': 'X', 'page_num': 1}

        if self.ernaehrung_checkbox2.isChecked() and self.magensonde_combo.currentText() == 'Nasogastral':
            data_antrag12['enterale_checkbox3'] = {'x': 179, 'y': 571, 'value': 'X', 'page_num': 2}
            data_antrag12['enterale_info3'] = {'x': 290, 'y': 571, 'value': f"Fresubin SK {self.ernaehrung_enteral_combo.currentText()} {self.ernaehrung_enteral_laufrate_input.text()} ml/h", 'page_num': 2}
            data_antrag13['enterale_checkbox4'] = {'x': 94, 'y': 641, 'value': 'X', 'page_num': 3}

        if self.ernaehrung_checkbox2.isChecked() and self.magensonde_combo.currentText() in ['PEG' , 'PEJ']:
            data_antrag12['enterale_checkbox3'] = {'x': 179, 'y': 584, 'value': 'X', 'page_num': 2}
            data_antrag12['enterale_info3'] = {'x': 250, 'y': 584, 'value': f"Fresubin SK {self.ernaehrung_enteral_combo.currentText()} {self.ernaehrung_enteral_laufrate_input.text()} ml/h", 'page_num': 2}

        if self.ernaehrung_checkbox2.isChecked() and self.magensonde_combo.currentText() =='PEG':
            data_antrag13['enterale_checkbox4'] = {'x': 235, 'y': 642, 'value': 'X', 'page_num': 3}

        if self.ernaehrung_checkbox2.isChecked() and self.magensonde_combo.currentText() =='PEJ':
            data_antrag13['enterale_checkbox4'] = {'x': 306, 'y': 642, 'value': 'X', 'page_num': 3}


        if self.ernaehrung_checkbox1.isChecked():
            data_antrag12['parenterale_checkbox4'] = {'x': 179, 'y': 596, 'value': 'X', 'page_num': 2}
            data_antrag12['parenterale_info3'] = {'x': 250, 'y': 596, 'value': parenterale, 'page_num': 2}

        if self.betreuung_combo.currentText() == 'ja':
            data_antrag2['betreuung_checkbox1'] = {'x': 213, 'y': 612, 'value': 'X', 'page_num': 1}
            data_antrag3['betreuung_checkbox2'] = {'x': 227, 'y': 471, 'value': 'X', 'page_num': 1}
            data_antrag8['betreuung_checkbox3'] = {'x': 305, 'y': 407, 'value': 'X', 'page_num': 1}
            data_antrag9['betreuung_checkbox4'] = {'x': 418, 'y': 343, 'value': 'X', 'page_num': 1}
        if self.betreuung_combo.currentText() == 'nein':
            data_antrag2['betreuung_checkbox2'] = {'x': 262, 'y': 612, 'value': 'X', 'page_num': 1}
            data_antrag3['betreuung_checkbox1'] = {'x': 270, 'y': 471, 'value': 'X', 'page_num': 1}
            data_antrag8['betreuung_checkbox3'] = {'x': 355, 'y': 407, 'value': 'X', 'page_num': 1}
            data_antrag9['betreuung_checkbox4'] = {'x': 468, 'y': 343, 'value': 'X', 'page_num': 1}

        if self.vorsorgevollmacht_combo.currentText() == 'ja':
            data_antrag2['vorsorgevollmacht_checkbox1'] = {'x': 213, 'y': 625, 'value': 'X', 'page_num': 1}
            data_antrag3['vorsorgevollmacht_checkbox2'] = {'x': 439, 'y': 471, 'value': 'X', 'page_num': 1}
            data_antrag9['vorsorgevollmacht_checkbox3'] = {'x': 418, 'y': 360, 'value': 'X', 'page_num': 1}
        if self.vorsorgevollmacht_combo.currentText() == 'nein':
            data_antrag2['vorsorgevollmacht_checkbox2'] = {'x': 262, 'y': 625, 'value': 'X', 'page_num': 1}
            data_antrag3['vorsorgevollmacht_checkbox1'] = {'x': 483, 'y': 471, 'value': 'X', 'page_num': 1}
            data_antrag9['vorsorgevollmacht_checkbox3'] = {'x': 468, 'y': 360, 'value': 'X', 'page_num': 1}

        if self.versorgungzuhause_combo.currentIndex() == 0:
            data_antrag2['versorgungzuhause_checkbox1'] = {'x': 290, 'y': 639, 'value': 'X', 'page_num': 1}
            data_antrag3['versorgungzuhause_checkbox2'] = {'x': 239, 'y': 510, 'value': 'X', 'page_num': 1}
        if self.versorgungzuhause_combo.currentIndex() == 1:
            data_antrag2['versorgungzuhause_checkbox2'] = {'x': 411, 'y': 639, 'value': 'X', 'page_num': 1}
            data_antrag3['versorgungzuhause_checkbox1'] = {'x': 334, 'y': 510, 'value': 'X', 'page_num': 1}
        if self.versorgungzuhause_combo.currentIndex() == 2:
            data_antrag2['versorgungzuhause_checkbox3'] = {'x': 290, 'y': 654, 'value': 'X', 'page_num': 1}
            data_antrag3['versorgungzuhause_checkbox3'] = {'x': 402, 'y': 510, 'value': 'X', 'page_num': 1}
        if self.versorgungzuhause_combo.currentIndex() == 3:
            data_antrag2['versorgungzuhause_checkbox4'] = {'x': 411, 'y': 654, 'value': 'X', 'page_num': 1}
            data_antrag3['versorgungzuhause_checkbox4'] = {'x': 485, 'y': 510, 'value': 'X', 'page_num': 1}

        if self.az_combo.currentIndex() == 0:
            data_antrag2['az_checkbox1'] = {'x': 411, 'y': 681, 'value': 'X', 'page_num': 1}
            data_antrag3['az_checkbox2'] = {'x': 214, 'y': 550, 'value': 'X', 'page_num': 1}
        if self.az_combo.currentIndex() == 1:
            data_antrag2['az_checkbox1'] = {'x': 411, 'y': 696, 'value': 'X', 'page_num': 1}
            data_antrag3['az_checkbox2'] = {'x': 383, 'y': 550, 'value': 'X', 'page_num': 1}
        if self.az_combo.currentIndex() == 2:
            data_antrag2['az_checkbox1'] = {'x': 411, 'y': 710, 'value': 'X', 'page_num': 1}
            data_antrag3['az_checkbox2'] = {'x': 420, 'y': 550, 'value': 'X', 'page_num': 1}
        if self.az_combo.currentIndex() == 3:
            data_antrag2['az_checkbox1'] = {'x': 411, 'y': 724, 'value': 'X', 'page_num': 1}
            data_antrag3['az_checkbox2'] = {'x': 213, 'y': 564, 'value': 'X', 'page_num': 1}
        if self.az_combo.currentIndex() == 4:
            data_antrag2['az_checkbox1'] = {'x': 411, 'y': 738, 'value': 'X', 'page_num': 1}
            data_antrag3['az_checkbox2'] = {'x': 383, 'y': 564, 'value': 'X', 'page_num': 1}

        if self.verfuegung_combo.currentText() == 'ja':
            data_antrag8['verfuegung_checkbox1'] = {'x': 180, 'y': 384, 'value': 'X', 'page_num': 1}
        if self.verfuegung_combo.currentText() == 'nein':
            data_antrag8['verfuegung_checkbox1'] = {'x': 237, 'y': 384, 'value': 'X', 'page_num': 1}


        if self.motivation_combo.currentIndex() == 0:
            data_antrag2['motivation_checkbox1'] = {'x': 276, 'y': 677, 'value': 'X', 'page_num': 2}
            data_antrag3['motivation_checkbox2'] = {'x': 262, 'y': 663, 'value': 'X', 'page_num': 2}
            data_antrag9['motivation_checkbox3'] = {'x': 46, 'y': 128, 'value': 'X', 'page_num': 2}
        if self.motivation_combo.currentIndex() == 1:
            data_antrag2['motivation_checkbox1'] = {'x': 397, 'y': 677, 'value': 'X', 'page_num': 2}
            data_antrag3['motivation_checkbox2'] = {'x': 319, 'y': 663, 'value': 'X', 'page_num': 2}
            data_antrag9['motivation_checkbox3'] = {'x': 46, 'y': 145, 'value': 'X', 'page_num': 2}
        if self.motivation_combo.currentIndex() == 2:
            data_antrag2['motivation_checkbox2'] = {'x': 276, 'y': 692, 'value': 'X', 'page_num': 2}
            data_antrag3['motivation_checkbox2'] = {'x': 408, 'y': 663, 'value': 'X', 'page_num': 2}
            data_antrag9['motivation_checkbox3'] = {'x': 46, 'y': 162, 'value': 'X', 'page_num': 2}
        if self.motivation_combo.currentIndex() == 3:
            data_antrag2['motivation_checkbox2'] = {'x': 397, 'y': 692, 'value': 'X', 'page_num': 2}
            data_antrag3['motivation_checkbox2'] = {'x': 472, 'y': 663, 'value': 'X', 'page_num': 2}
            data_antrag9['motivation_checkbox3'] = {'x': 46, 'y': 179, 'value': 'X', 'page_num': 2}

        if self.stimmung_combo.currentIndex() == 0:
            data_antrag2['stimmung_checkbox1'] = {'x': 276, 'y': 705, 'value': 'X', 'page_num': 2}
            data_antrag3['stimmung_checkbox2'] = {'x': 262, 'y': 676, 'value': 'X', 'page_num': 2}
        if self.stimmung_combo.currentIndex() == 1:
            data_antrag2['stimmung_checkbox1'] = {'x': 397, 'y': 705, 'value': 'X', 'page_num': 2}
            data_antrag3['stimmung_checkbox2'] = {'x': 319, 'y': 676, 'value': 'X', 'page_num': 2}
        if self.stimmung_combo.currentIndex() == 2:
            data_antrag2['stimmung_checkbox2'] = {'x': 276, 'y': 720, 'value': 'X', 'page_num': 2}
            data_antrag3['stimmung_checkbox2'] = {'x': 408, 'y': 676, 'value': 'X', 'page_num': 2}
        if self.stimmung_combo.currentIndex() == 3:
            data_antrag2['stimmung_checkbox2'] = {'x': 397, 'y': 720, 'value': 'X', 'page_num': 2}
            data_antrag3['stimmung_checkbox2'] = {'x': 472, 'y': 676, 'value': 'X', 'page_num': 2}


        if self.pflegebeduerftigkeit_combo.currentIndex() == 0:
            data_antrag2['pflegebeduerftigkeit_checkbox1'] = {'x': 205, 'y': 747, 'value': 'X', 'page_num': 2}
            data_antrag3['pflegebeduerftigkeit_checkbox2'] = {'x': 252, 'y': 359, 'value': 'X', 'page_num': 2}
        if self.pflegebeduerftigkeit_combo.currentIndex() == 1:
            data_antrag2['pflegebeduerftigkeit_checkbox1'] = {'x': 297, 'y': 747, 'value': 'X', 'page_num': 2}
            data_antrag3['pflegebeduerftigkeit_checkbox2'] = {'x': 320, 'y': 359, 'value': 'X', 'page_num': 2}
        if self.pflegebeduerftigkeit_combo.currentIndex() == 2:
            data_antrag2['pflegebeduerftigkeit_checkbox2'] = {'x': 396, 'y': 747, 'value': 'X', 'page_num': 2}
            data_antrag3['pflegebeduerftigkeit_checkbox2'] = {'x': 398, 'y': 359, 'value': 'X', 'page_num': 2}

        if self.mobilisation_combo.currentIndex() == 0:
            data_antrag2['mobilisation_checkbox1'] = {'x': 205, 'y': 762, 'value': 'X', 'page_num': 2}  
        if self.mobilisation_combo.currentIndex() == 1:
            data_antrag2['mobilisation_checkbox1'] = {'x': 297, 'y': 762, 'value': 'X', 'page_num': 2}
        if self.mobilisation_combo.currentIndex() == 2:
            data_antrag2['mobilisation_checkbox2'] = {'x': 396, 'y': 762, 'value': 'X', 'page_num': 2}

        if self.consciousness_combo.currentIndex() == 0:
            data_antrag2['consciousness_checkbox1'] = {'x': 212, 'y': 440, 'value': 'X', 'page_num': 2}
            data_antrag3['consciousness_checkbox2'] = {'x': 214, 'y': 411, 'value': 'X', 'page_num': 2}
        if self.consciousness_combo.currentIndex() == 1:
            data_antrag2['consciousness_checkbox1'] = {'x': 418, 'y': 440, 'value': 'X', 'page_num': 2}
            data_antrag3['consciousness_checkbox2'] = {'x': 391, 'y': 411, 'value': 'X', 'page_num': 2}
        if self.consciousness_combo.currentIndex() == 2:
            data_antrag2['consciousness_checkbox2'] = {'x': 212, 'y': 453, 'value': 'X', 'page_num': 2}
            data_antrag3['consciousness_checkbox2'] = {'x': 214, 'y': 424, 'value': 'X', 'page_num': 2}
        if self.consciousness_combo.currentIndex() == 3:
            data_antrag2['consciousness_checkbox2'] = {'x': 418, 'y': 453, 'value': 'X', 'page_num': 2}
            data_antrag3['consciousness_checkbox2'] = {'x': 391, 'y': 424, 'value': 'X', 'page_num': 2}
        if self.consciousness_combo.currentIndex() == 4:
            data_antrag2['consciousness_checkbox3'] = {'x': 212, 'y': 467, 'value': 'X', 'page_num': 2}
            data_antrag3['consciousness_checkbox3'] = {'x': 214, 'y': 438, 'value': 'X', 'page_num': 2}
        if self.consciousness_combo.currentIndex() == 5:
            data_antrag2['consciousness_checkbox3'] = {'x': 418, 'y': 467, 'value': 'X', 'page_num': 2}
            data_antrag3['consciousness_checkbox3'] = {'x': 391, 'y': 438, 'value': 'X', 'page_num': 2}

        if self.darminkontinenz_combo.currentIndex() == 0:
            data_antrag2['darminkontinenz_checkbox1'] = {'x': 178, 'y': 552, 'value': 'X', 'page_num': 2}
        if self.darminkontinenz_combo.currentIndex() == 1:
            data_antrag2['darminkontinenz_checkbox1'] = {'x': 223, 'y': 552, 'value': 'X', 'page_num': 2}

        if self.checkbox_hbsagpos.isChecked():
            data_antrag2['hbsag_checkbox1'] = {'x': 382, 'y': 565, 'value': 'X', 'page_num': 2}
        if self.checkbox_hbsagneg.isChecked():
            data_antrag2['hbsag_checkbox2'] = {'x': 436, 'y': 565, 'value': 'X', 'page_num': 2}
        if self.checkbox_hcvpos.isChecked():
            data_antrag2['hcv_checkbox1'] = {'x': 382, 'y': 579, 'value': 'X', 'page_num': 2}
        if self.checkbox_hcvneg.isChecked():
            data_antrag2['hcv_checkbox2'] = {'x': 436, 'y': 579, 'value': 'X', 'page_num': 2}
        if self.checkbox_hivpos.isChecked():
            data_antrag2['hiv_checkbox1'] = {'x': 178, 'y': 579, 'value': 'X', 'page_num': 2}
        if self.checkbox_hivneg.isChecked():
            data_antrag2['hiv_checkbox2'] = {'x': 223, 'y': 579, 'value': 'X', 'page_num': 2}
        if self.hit_combo.currentIndex() == 0:
            data_antrag2['hit_checkbox1'] = {'x': 223, 'y': 594, 'value': 'X', 'page_num': 2}
        if self.hit_combo.currentIndex() == 1:
            data_antrag2['hit_checkbox2'] = {'x': 178, 'y': 594, 'value': 'X', 'page_num': 2}

        if self.dekubitus_combo.currentText() == 'ja':
            data_antrag9['dekubitus_checkbox1'] = {'x': 418, 'y': 629, 'value': 'X', 'page_num': 2}
        else:
            data_antrag9['dekubitus_checkbox2'] = {'x': 467, 'y': 629, 'value': 'X', 'page_num': 2}

        if self.beatmung_spontan_input.text() and self.beatmung_spontan_input.text() != '0': 
            data_antrag10['beatmung_spontan_checkbox1'] = {'x': 206, 'y': 467, 'value': 'X', 'page_num': 1}
            data_antrag10['beatmung_spontan_info1'] = {'x': 240, 'y': 467, 'value': self.beatmung_spontan_input.text(), 'page_num': 1}
            data_antrag11['beatmung_spontan_info2'] = {'x': 300, 'y': 123, 'value': f"{self.beatmung_spontan_input.text()} Stunden", 'page_num': 2}
            data_antrag14['beatmung_spontan_checkbox3'] = {'x': 383, 'y': 425, 'value': 'X', 'page_num': 1}
            data_antrag14['beatmung_spontan_info3'] = {'x': 500, 'y': 423, 'value': f"{self.beatmung_spontan_input.text()} Stunden", 'page_num': 1}
        else:
            data_antrag10['beatmung_spontan_checkbox1'] = {'x': 155, 'y': 467, 'value': 'X', 'page_num': 1}
            data_antrag14['beatmung_spontan_checkbox3'] = {'x': 335, 'y': 425, 'value': 'X', 'page_num': 1}
            
# ab hier checkbox-abhängiges Einfügen (CAE)
    #if self.checkbox_clemens.isChecked():
        insert_text_into_pdf("antrag1.pdf", "antrag1 clemens.pdf", data_antrag1)

    #if self.checkbox_dortmund_luenen.isChecked():
        insert_text_into_pdf("antrag2.pdf", "antrag2 dortmund_luenen.pdf", data_antrag2)

    #if self.checkbox_dortmund.isChecked():
        insert_text_into_pdf("antrag3.pdf", "antrag3 dortmund.pdf", data_antrag3)

    #if self.checkbox_ibbenbueren.isChecked():
        insert_text_into_pdf("antrag4.pdf", "antrag4 ibbenbueren.pdf", data_antrag4)

    #if self.checkbox_vest.isChecked():
        insert_text_into_pdf("antrag5.pdf", "antrag5 vest.pdf", data_antrag5)

    #if self.checkbox_koeln.isChecked():
        insert_text_into_pdf("antrag6.pdf", "antrag6 koeln.pdf", data_antrag6)

    #if self.checkbox_essen.isChecked():
        insert_text_into_pdf("antrag7.pdf", "antrag7 essen.pdf", data_antrag7)

    #if self.checkbox_soest.isChecked():
        insert_text_into_pdf("antrag8.pdf", "antrag8 soest.pdf", data_antrag8)

    #if self.checkbox_hemer.isChecked():
        insert_text_into_pdf("antrag9.pdf", "antrag9 hemer.pdf", data_antrag9)

    #if self.checkbox_oldenburg.isChecked():
        insert_text_into_pdf("antrag10.pdf", "antrag10 oldenburg.pdf", data_antrag10)

    #if self.checkbox_haltern.isChecked():
        insert_text_into_pdf("antrag11.pdf", "antrag11 haltern.pdf", data_antrag11)

    #if self.checkbox_bad_lippspringe.isChecked():
        insert_text_into_pdf("antrag12.pdf", "antrag12 bad_lippspringe.pdf", data_antrag12)

    #if self.checkbox_schmallenberg.isChecked():
        insert_text_into_pdf("antrag13.pdf", "antrag13 schmallenberg.pdf", data_antrag13)

    #if self.checkbox_bielefeld.isChecked():
        insert_text_into_pdf("antrag14.pdf", "antrag14 bielefeld.pdf", data_antrag14)



if __name__ == '__main__':#
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    #window.fillFormWithTestData()
    #window.submitForm()
    #window.close()
    #app.quit() # Beendet die Anwendung
    app.exec_()
