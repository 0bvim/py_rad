import PySimpleGUI as sg

data = []
Title = [ 'Lote', 'Produto', 'Fornecedor']

layout = [
    [sg.Text(Title[0]), sg.Input(size=5, key=Title[0])],
    [sg.Text(Title[1]), sg.Input(size=20, key=Title[1])],
    [sg.Text(Title[2]), sg.Combo(['Fornecedor 1', 'Fornecedor 2', 'Fornecedor 3'], key=Title[2])],
    [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Salvar', disabled=True), sg.Button('Excluir'), sg.Button('Sair')],
    [sg.Table(data, Title, key='tabela')]
]

window = sg.Window('Sistema de gerencia de suplementos', layout)

while True:
    event, values = window.read()
    print(values)

    if event == 'Adicionar':
        data.append([values[Title[0]], values[Title[1]], values[Title[2]]])
        window['tabela'].update(values=data)
        for i in range(3):
            window[Title[i]].update(value='')

    if event == 'Editar':
        if values['tabela'] == []:
            sg.popup('Nenhuma linha selecionada')
        else:
            editarLinha=values['tabela'][0]
            sg.popup('Editar linha selecionada')
            for i in range(3):
                window[Title[i]].update(value=data[editarLinha][i])

    if event in (sg.WIN_CLOSED, 'Sair'):
        break

window.close()
