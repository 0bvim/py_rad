import os
import sqlite3

import PySimpleGUI as sg

# this line contain the path from where is the current script
wd = os.path.dirname(os.path.abspath(__file__))

# join the path with our database file name
db_path = os.path.join(wd, "database.db")

conexao = sqlite3.connect(db_path)
query = """CREATE TABLE IF NOT EXISTS SUPLEMENTO (LOT CHAR(10), PRODUTO TEXT, FORNECEDOR TEXT)"""
conexao.execute(query)
conexao.close()

data = []
Title = ["Lote", "Produto", "Fornecedor"]

layout = [
    [sg.Text(Title[0]), sg.Input(size=5, key=Title[0])],
    [sg.Text(Title[1]), sg.Input(size=20, key=Title[1])],
    [
        sg.Text(Title[2]),
        sg.Combo(["Fornecedor 1", "Fornecedor 2", "Fornecedor 3"], key=Title[2]),
    ],
    [
        sg.Button("Adicionar"),
        sg.Button("Editar"),
        sg.Button("Salvar", disabled=True),
        sg.Button("Excluir"),
        sg.Button("Sair"),
    ],
    [sg.Table(data, Title, key="tabela")],
]

window = sg.Window("Sistema de gerencia de suplementos", layout)

while True:
    event, values = window.read()
    print(values)

    if event == "Adicionar":
        data.append([values[Title[0]], values[Title[1]], values[Title[2]]])
        window["tabela"].update(values=data)
        for i in range(3):
            window[Title[i]].update(value="")

        conexao = sqlite3.connect(db_path)
        conexao.execute(
            "INSERT INTO SUPLEMENTO (LOTE, PRODUTO, FORNECEDOR) VALUES(?,?,?)",
            ([values[Title[0]], values[Title[1]], values[Title[2]]]),
        )
        conexao.commit()
        conexao.close()

    if event == "Editar":
        if values["tabela"] == []:
            sg.popup("Nenhuma linha selecionada")
        else:
            editarLinha = values["tabela"][0]
            sg.popup("Editar linha selecionada")
            for i in range(3):
                window[Title[i]].update(value=data[editarLinha][i])
            window["Salvar"].update(disabled=False)

    if event == "Salvar":
        data[editarLinha] = [values[Title[0]], values[Title[1]], values[Title[2]]]
        window["tabela"].update(values=data)
        for i in range(3):
            window[Title[i]].update(value="")
        window["Salvar"].update(disabled=True)

        conexao = sqlite3.connect(db_path)
        conexao.execute(
            "UPDATE SUPLEMENTO set PRODUTO = ?, FORNECEDOR = ? where LOTE = ?",
            ([values[Title[1]], values[Title[2]], values[Title[0]]])
        )
        conexao.commit()
        conexao.close()

    if event == 'Excluir':
        if values['tabela'] == []:
            sg.popup('Nenhuma linha selecionada')
        else:
            if sg.popup_ok_cancel('Essa operacao nao pode ser desfeita. Confirma?') == 'OK':
                conexao = sqlite3.connect(db_path)
                conexao.execute("DELETE FROM SUPLEMENTO WHERE LOTE = ?;", (values[Title[0]],))
                conexao.close()

                del data[values['tabela'][0]]
                window['tabela'].update(values=data)



    if event in (sg.WIN_CLOSED, "Sair"):
        break

window.close()
