from gui.interface import InterfaceBancaria  # Importa a classe InterfaceBancaria do módulo gui.interface
import tkinter as tk  # Importa o tkinter para a criação de interfaces gráficas

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    root = tk.Tk()  # Cria a janela principal (raiz) do tkinter
    app = InterfaceBancaria(root)  # Inicializa a classe InterfaceBancaria com a janela raiz
    root.mainloop()  # Inicia o loop principal da interface gráfica
