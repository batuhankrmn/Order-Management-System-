# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 22:58:06 2021

@author: ylmzc
"""


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from GP_SON import *
from HakkindaUI import *

Uygulama=QApplication(sys.argv)
Ana_pen=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(Ana_pen)
Ana_pen.show()

Hakkinda_pen=QDialog()
ui2=Ui_Dialog()
ui2.setupUi(Hakkinda_pen)


import sqlite3
global curs
global conn

conn=sqlite3.connect('musteri_Takip_db.db')
curs=conn.cursor()
sorguCreTblMusteri=("CREATE TABLE IF NOT EXISTS Musteri(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                 MusteriAdi TEXT NOT NULL UNIQUE,                  \
                 MusteriTelefon TEXT NOT NULL UNIQUE,             \
                 OdemeSekli TEXT NOT NULL,                       \
                 OdemeAraligi TEXT NOT NULL,                     \
                 TeslimatSorumlusu TEXT NOT NULL,                \
                 TeslimatSaati TEXT NOT NULL,                    \
                 Tic_Tarihi TEXT NOT NULL)")                     \
                     
curs.execute(sorguCreTblMusteri)
conn.commit()

def EKLE():
    _lneName=ui.lneName.text()
    _lneNumber=ui.lneNumber.text()
    _cmbOdeme=ui.cmbOdeme.currentText()
    _cmbArac=ui.cmbArac.currentText()
    _calendarWidget=ui.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
    _listWidget=ui.listWidget.currentItem().text()
    
         
    if ui.rdNakit.isChecked():
        _OdemeSekli="Nakit"

    if ui.radioButton_2.isChecked():
        _OdemeSekli="Kart"
    
            
    curs.execute("INSERT INTO Musteri \
                 (MusteriAdi,MusteriTelefon,OdemeSekli,OdemeAraligi,TeslimatSorumlusu,TeslimatSaati,Tic_Tarihi) \
                     VALUES (?,?,?,?,?,?,?)", \
                      (_lneName,_lneNumber,_OdemeSekli,_cmbOdeme,_cmbArac,_listWidget, \
                       _calendarWidget))
    conn.commit()
    LISTELE()
    
def LISTELE():
    
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(('Id','MusteriAdi','MusteriTelefon','OdemeSekli', \
                            'OdemeAraligi', 'TeslimatSorumlusu', 'TeslimatSaati', 'Tic_Tarihi'))
    
    ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    curs.execute("SELECT * FROM Musteri")
    
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tableWidget.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
            
    ui.lneName.clear()
    ui.lneNumber.clear()
    ui.cmbArac.setCurrentIndex(-1)
    
    
    curs.execute("SELECT COUNT(*) FROM Musteri")
    kayitSayisi=curs.fetchone()
    ui.lb.setText(str(kayitSayisi[0]))
    
    
           
LISTELE()
            
def CIKIS():
    cevap=QMessageBox.question(Ana_pen,"ÇIKIŞ","Lütfen işlemlerinizi kayıt ettiğinizden emin olun,çıkış yapmak istiyor musunuz ?.",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        Ana_pen.show()
        
    
def SIL():
    cevap=QMessageBox.question(Ana_pen,"KAYIT SİL","Silinen kayıt geri getirelemez,işleme devam etmek ister misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secim=ui.tableWidget.selectedItems()
        silinecek=secim[0].text()
        try:
            curs.execute("DELETE FROM Musteri WHERE Id='%s'" %(silinecek))
            conn.commit()
            
            LISTELE()
            
            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ GERÇEKLEŞTİ...",3000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi...",10000)
        
def ARA():
    aranan1=ui.lneName.text()
    aranan2=ui.lneNumber.text()    
    curs.execute("SELECT * FROM Musteri WHERE MusteriAdi=? OR MusteriTelefon=? OR (MusteriAdi=? AND MusteriTelefon=?)",  \
                 (aranan1,aranan2,aranan1,aranan2))
    conn.commit()
    ui.tableWidget.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tableWidget.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
        
def DOLDUR():
    secili=ui.tableWidget.selectedItems()
    ui.lneName.setText(secili[1].text())
    ui.lneNumber.setText(secili[2].text())
    
    if secili[3].text()=="Nakit":
        ui.rdNakit.setChecked(True)
    if secili[3].text()=="Kart":
        ui.radioButton_2.setChecked(True)
        
    ui.cmbOdeme.setCurrentText(secili[4].text())
    ui.cmbArac.setCurrentText(secili[5].text())
    
    if secili[6].text()=="05:00":
        ui.listWidget.item(0).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(0))
    if secili[6].text()=="06:00":
        ui.listWidget.item(1).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(1))
    if secili[6].text()=="07:00":
        ui.listWidget.item(2).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(2))
    if secili[6].text()=="08:00":
        ui.listWidget.item(3).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(3))
    if secili[6].text()=="09:00":
        ui.listWidget.item(4).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(4))
    if secili[6].text()=="10:00":
        ui.listWidget.item(5).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(5))
    if secili[6].text()=="11:00":
        ui.listWidget.item(6).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(6))
    if secili[6].text()=="12:00":
        ui.listWidget.item(7).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(7))
    if secili[6].text()=="13:00":
        ui.listWidget.item(8).setSelected(True)
        ui.listWidgett.setCurrentItem(ui.listWidget.item(8))
    if secili[6].text()=="14:00":
        ui.listWidget.item(9).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(9))
    if secili[6].text()=="15:00":
        ui.listWidgett.item(10).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(10))
    if secili[6].text()=="16:00":
        ui.listWidget.item(11).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(11))
    if secili[6].text()=="17:00":
        ui.listWidget.item(12).setSelected(True)
        ui.listWidgett.setCurrentItem(ui.listWidget.item(12))
    if secili[6].text()=="18:00":
        ui.listWidget.item(13).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(13))
    if secili[6].text()=="19:00":
        ui.listWidget.item(14).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(14))
    if secili[6].text()=="20:00":
        ui.listWidget.item(15).setSelected(True)
        ui.listWidget.setCurrentItem(ui.listWidget.item(15))
            
    yil=int(secili[7].text()[0:4])
    ay=int(secili[7].text()[5:7])
    gun=int(secili[7].text()[8:10])
    ui.calendarWidget.setSelectedDate(QtCore.QDate(yil,ay,gun))
        
def GUNCELLE():
    cevap=QMessageBox.question(Ana_pen,"KAYIT GÜNCELLE","Güncelleme işleminden sonra eski bilgileriniz silenecektir devam etmek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.tableWidget.selectedItems()
            _Id=int(secili[0].text())
            _lneName=ui.lneName.text()
            _lneNumber=ui.lneNumber.text()
            _cmbOdeme=ui.cmbOdeme.currentText()
            _cmbArac=ui.cmbArac.currentText()
            _calendarWidget=ui.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
            _listWidget=ui.listWidget.currentItem().text()
    
         
            if ui.rdNakit.isChecked():
                _OdemeSekli="Nakit"

            if ui.radioButton_2.isChecked():
                _OdemeSekli="Kart"
    
            
            curs.execute("UPDATE Musteri SET MusteriAdi=?, MusteriTelefon=?, OdemeSekli=?, OdemeAraligi=?,   \
                        TeslimatSorumlusu=?,TeslimatSaati=?,Tic_Tarihi=? WHERE Id=?",\
                         (_lneName,_lneNumber,_OdemeSekli,_cmbOdeme,_cmbArac,_listWidget,_calendarWidget,_Id))
            
            conn.commit()
            
            
            LISTELE()
            
        except Exception as Hata:
            ui.statusbar.showMessage("Bir Hata Oluştu:" +str(Hata))
    else:
        ui.statusbar.showMessage("Güncellme iptal edildi",5000)
        
def HAKKINDA():
    Hakkinda_pen.show()
        
        
        



ui.btnEkle.clicked.connect(EKLE)
ui.btnListele.clicked.connect(LISTELE)
ui.btnCikis.clicked.connect(CIKIS)
ui.btnSil.clicked.connect(SIL)
ui.btnAra.clicked.connect(ARA)
ui.tableWidget.itemSelectionChanged.connect(DOLDUR)
ui.btnGuncelle.clicked.connect(GUNCELLE)
ui.actionHakk_nda.triggered.connect(HAKKINDA)



sys.exit(Uygulama.exec_())