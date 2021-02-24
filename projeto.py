from PyQt5 import uic, QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_placas"
)
# defs para voltar e passar os frames


def frame_consultar():
    tela.frame_4.close()
    tela.frame_3.close()


def frame_cadastro():
    tela.frame_4.close()


def frame_vagas_listadas():
    tela.frame_2.close()
    tela.frame_3.close()
    tela.frame_4.close()


def voltar():
    tela.frame_2.show()
    tela.frame_3.show()
    tela.frame_4.show()

    tela.label_5.setText('')
    tela.label_6.setText('')
    tela.label_10.setText('')


# telas e funções

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


def excluir_lista():
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
    placa = placa.upper()
    tela.lineEdit_10.setText('')
    tela.lineEdit_11.setText('')
    tela.lineEdit_12.setText('')

    cadastro = banco.cursor()
    cadastro.execute("SELECT * FROM placas WHERE bloco = " +
                     str(bloco) + " " + "AND apartamento = " + str(apt))
    teste = cadastro.fetchall()
    cadastro.execute("SELECT * FROM aluguel WHERE bloco = " +
                     str(bloco) + " " + "AND apartamento = " + str(apt))
    aluguel = cadastro.fetchall()

    if not teste:
        if not aluguel:
            cursor = banco.cursor()
            comando_SQL = "INSERT INTO placas (placa,bloco,apartamento) VALUES (%s,%s,%s)"
            dados = (str(placa), str(bloco), str(apt))
            cursor.execute(comando_SQL, dados)
            banco.commit()
            tela.label_6.setText("Cadastro concluído.")
        else:
            tela.label_6.setText(
                "Vaga listada para aluguel, retire-a para cadastra-la.")
    else:
        tela.label_6.setText("Bloco e apartamento ou placa já cadastrado(s).")


def aluguel():
    bloco = tela.lineEdit.text()
    apt = tela.lineEdit_2.text()
    tela.lineEdit.setText('')
    tela.lineEdit_2.setText('')

    tela.label_10.setText('')

    aluguel = banco.cursor()
    aluguel.execute("SELECT * FROM aluguel WHERE bloco =" +
                    str(bloco) + ' ' + "AND apartamento =" + str(apt))
    aluguel1 = aluguel.fetchall()
    aluguel.execute("SELECT * FROM placas WHERE bloco = " +
                    str(bloco) + ' ' + "AND apartamento = " + str(apt))
    aluguel2 = aluguel.fetchall()

    if not aluguel1:
        if not aluguel2:
            cursor = banco.cursor()
            comando_SQL = "INSERT INTO aluguel (bloco,apartamento) VALUES (%s,%s)"
            dados = (str(bloco), str(apt))
            cursor.execute(comando_SQL, dados)
            banco.commit()
        else:
            tela.label_10.setText("O morador possui um carro nessa vaga.")
    else:
        tela.label_10.setText("Vaga já está listada para aluguel.")

    cursor = banco.cursor()
    comando_SQL = "SELECT * from aluguel"
    cursor.execute(comando_SQL)
    info = cursor.fetchall()

    tela.tableWidget.setRowCount(len(info))
    tela.tableWidget.setColumnCount(3)

    for i in range(0, len(info)):
        for j in range(0, 3):
            tela.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(info[i][j])))


def excluir_aluguel():
    item = tela.tableWidget.currentRow()
    tela.tableWidget.removeRow(item)

    cursor = banco.cursor()
    cursor.execute("SELECT id from aluguel")
    ids = cursor.fetchall()
    valor_id = ids[item][0]
    cursor.execute("DELETE FROM aluguel WHERE id=" + str(valor_id))

    tela.label_10.setText('')


def consulta():
    cons = tela.lineEdit_4.text()
    cons = cons.upper()
    tela.lineEdit_4.setText('')

    while True:
        consulta = banco.cursor()
        consulta.execute("SELECT * FROM placas WHERE placa =" + str(cons))
        placa = consulta.fetchall()

        if len(placa) == 0:
            tela.label_5.setText('A placa não está cadastrada no sistema.')
            break
        else:
            tela.label_5.setText('A placa está cadastrada no sistema.')
            break


app = QtWidgets.QApplication([])
tela = uic.loadUi("tela.ui")
tabela = uic.loadUi("tabela.ui")

tela.pushButton_8.clicked.connect(frame_consultar)
tela.pushButton_9.clicked.connect(frame_cadastro)
tela.pushButton_10.clicked.connect(frame_vagas_listadas)
tela.pushButton_7.clicked.connect(voltar)
tela.pushButton_5.clicked.connect(voltar)
tela.pushButton_3.clicked.connect(voltar)
tela.pushButton_6.clicked.connect(cadastro)
tela.pushButton_4.clicked.connect(consulta)
tela.pushButton_2.clicked.connect(aluguel)
tela.pushButton_11.clicked.connect(lista)
tela.pushButton.clicked.connect(excluir_aluguel)
tabela.pushButton.clicked.connect(excluir_lista)


tela.show()
app.exec()
