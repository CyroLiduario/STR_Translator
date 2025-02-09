import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from deep_translator import GoogleTranslator
import threading

# Lista de idiomas suportados pelo Google Translator
IDIOMAS = {
    "Inglês": "en",
    "Português": "pt",
    "Espanhol": "es",
    "Francês": "fr",
    "Alemão": "de",
    "Italiano": "it",
    "Chinês (Simplificado)": "zh-CN",
    "Japonês": "ja",
    "Russo": "ru",
    "Árabe": "ar",
    "Holandês": "nl",
    "Coreano": "ko",
    "Hindi": "hi"
}

def traduzir_srt(conteudo, idioma_origem, idioma_destino, progress_bar, root, progress_window):
    """Traduz o conteúdo de um arquivo SRT do idioma escolhido para outro."""
    tradutor = GoogleTranslator(source=idioma_origem, target=idioma_destino)
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

        idioma_origem = IDIOMAS[idioma_origem_cb.get()]
        idioma_destino = IDIOMAS[idioma_destino_cb.get()]

        # Cria a janela de progresso
        progress_window = tk.Toplevel(root)
        progress_window.title("Progresso da Tradução")
        progress_window.geometry("300x100")

        label = tk.Label(progress_window, text="Traduzindo...")
        label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, length=250, mode="determinate")
        progress_bar.pack(pady=10)

        # Inicia a tradução em uma nova thread
        thread = threading.Thread(target=traduzir_srt, args=(conteudo, idioma_origem, idioma_destino, progress_bar, root, progress_window))
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
root.geometry("400x250")

# Label para idioma de origem
label_origem = tk.Label(root, text="Idioma Original:")
label_origem.pack(pady=5)

# Dropdown de idioma de origem
idioma_origem_cb = ttk.Combobox(root, values=list(IDIOMAS.keys()))
idioma_origem_cb.set("Inglês")  # Padrão: Inglês
idioma_origem_cb.pack()

# Label para idioma de destino
label_destino = tk.Label(root, text="Idioma de Tradução:")
label_destino.pack(pady=5)

# Dropdown de idioma de destino
idioma_destino_cb = ttk.Combobox(root, values=list(IDIOMAS.keys()))
idioma_destino_cb.set("Português")  # Padrão: Português
idioma_destino_cb.pack()

# Botão para selecionar o arquivo
botao_selecionar = tk.Button(root, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.pack(pady=20)

root.mainloop()
