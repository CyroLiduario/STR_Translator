import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from deep_translator import GoogleTranslator
import threading

def traduzir_srt(conteudo, progress_bar, root, progress_window):
    """Traduz o conteúdo de um arquivo SRT de inglês para português com barra de progresso sem travar a GUI."""
    tradutor = GoogleTranslator(source='en', target='pt')
    linhas = conteudo.split("\n")
    total_linhas = len(linhas)
    linhas_traduzidas = []

    for i, linha in enumerate(linhas):
        if linha.strip().isdigit() or "-->" in linha or linha.strip() == "":
            linhas_traduzidas.append(linha)
        else:
            try:
                traducao = tradutor.translate(linha)
                linhas_traduzidas.append(traducao)
            except Exception:
                linhas_traduzidas.append(linha)

        # Atualiza a barra de progresso
        progress_bar["value"] = (i + 1) / total_linhas * 100
        root.update_idletasks()

    progress_window.destroy()  # Fecha a janela de progresso
    salvar_arquivo("\n".join(linhas_traduzidas))

def selecionar_arquivo():
    """Abre uma janela para o usuário selecionar um arquivo SRT."""
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos SRT", "*.srt")])
    if caminho_arquivo:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        # Cria a janela de progresso
        progress_window = tk.Toplevel(root)
        progress_window.title("Progresso da Tradução")
        progress_window.geometry("300x100")
        
        label = tk.Label(progress_window, text="Traduzindo...")
        label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, length=250, mode="determinate")
        progress_bar.pack(pady=10)

        # Inicia a tradução em uma nova thread
        thread = threading.Thread(target=traduzir_srt, args=(conteudo, progress_bar, root, progress_window))
        thread.start()

def salvar_arquivo(conteudo):
    """Abre um popup para o usuário salvar o arquivo traduzido."""
    caminho_salvar = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("Arquivos SRT", "*.srt")])
    if caminho_salvar:
        with open(caminho_salvar, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        messagebox.showinfo("Sucesso", "Tradução concluída e salva com sucesso!")

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Tradutor de SRT")
root.geometry("300x150")

label = tk.Label(root, text="Selecione um arquivo SRT para traduzir")
label.pack(pady=10)

botao_selecionar = tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.pack(pady=10)

root.mainloop()
