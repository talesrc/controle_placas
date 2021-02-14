from PyQt5 import uic, QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_placas"
)
# defs para voltar o frame


def voltar_cadastro():
    tela.frame_4.show()


def voltar_consulta():
    tela.frame_3.show()
    tela.frame_4.show()


def frame_consultar():
    tela.frame_4.close()
    tela.frame_3.close()


def voltar_aluguel():
    tela.frame_2.show()
    tela.frame_3.show()
    tela.frame_4.show()

# defs para passar de frame e utilização dos outros widgets


def frame_cadastro():
    tela.frame_4.close()


def frame_vagas_listadas():
    tela.frame_2.close()
    tela.frame_3.close()
    tela.frame_4.close()


def lista():
    tabela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * from placas"
    cursor.execute(comando_SQL)
    info = cursor.fetchall()

    tabela.tableWidget.setRowCount(len(info))
    tabela.tableWidget.setColumnCount(4)

    for i in range(0, len(info)):
        for j in range(0, 4):
            tabela.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(info[i][j])))


def excluir():
    item = tabela.tableWidget.currentRow()
    tabela.tableWidget.removeRow(item)

    cursor = banco.cursor()
    cursor.execute("SELECT id from placas")
    ids = cursor.fetchall()
    valor_id = ids[item][0]
    cursor.execute("DELETE FROM placas WHERE id=" + str(valor_id))


def cadastro():
    bloco = tela.lineEdit_10.text()
    placa = tela.lineEdit_11.text()
    apt = tela.lineEdit_12.text()
    tela.lineEdit_10.setText('')
    tela.lineEdit_11.setText('')
    tela.lineEdit_12.setText('')
    if bloco == '' or placa == '' or apt == '':
        bloco = placa = apt = 0
    if bloco > 0:
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO placas (placa,bloco,apartamento) VALUES (%s,%s,%s)"
        dados = (str(placa), str(bloco), str(apt))
        cursor.execute(comando_SQL, dados)
        banco.commit()


def aluguel():
    bloco = tela.lineEdit.text()
    apartamento = tela.lineEdit_2.text()
    tela.lineEdit.setText('')
    tela.lineEdit_2.setText('')

    tela.listWidget.addItem('Bloco' + ' ' + bloco +
                            ' ' + 'apt' + ' ' + apartamento)


def consulta():
    tela.lineEdit_4.text()
    tela.lineEdit_4.setText('')


app = QtWidgets.QApplication([])
tela = uic.loadUi("tela.ui")
tabela = uic.loadUi("tabela.ui")

tela.pushButton_8.clicked.connect(frame_consultar)
tela.pushButton_9.clicked.connect(frame_cadastro)
tela.pushButton_10.clicked.connect(frame_vagas_listadas)
tela.pushButton_7.clicked.connect(voltar_cadastro)
tela.pushButton_5.clicked.connect(voltar_consulta)
tela.pushButton_3.clicked.connect(voltar_aluguel)
tela.pushButton_6.clicked.connect(cadastro)
tela.pushButton_4.clicked.connect(consulta)
tela.pushButton_2.clicked.connect(aluguel)
tela.pushButton_11.clicked.connect(lista)
tabela.pushButton.clicked.connect(excluir)


tela.show()
app.exec()
