import tkinter as tk
from threading import Thread
import socket

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat")

        self.histórico_chat = tk.Text(master, state='disabled')
        self.histórico_chat.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.campo_entrada = tk.Entry(master)
        self.campo_entrada.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.campo_entrada.bind("<Return>", self.enviar_mensagem)

        self.botão_enviar = tk.Button(master, text="Enviar", command=self.enviar_mensagem)
        self.botão_enviar.grid(row=1, column=1, padx=10, pady=10)

        self.configurar_cliente()

    def configurar_cliente(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect(('localhost', 9999))

        self.thread_recebimento = Thread(target=self.receber_mensagens)
        self.thread_recebimento.daemon = True
        self.thread_recebimento.start()

    def enviar_mensagem(self, event=None):
        mensagem = self.campo_entrada.get()
        self.campo_entrada.delete(0, tk.END)
        self.exibir_mensagem("Você:", mensagem)
        self.cliente.send(mensagem.encode('utf-8'))

    def receber_mensagens(self):
        while True:
            try:
                msg = self.cliente.recv(1024).decode('utf-8')
                if msg == 'tt':
                    break
                self.exibir_mensagem("Outro usuário:", msg)
            except ConnectionAbortedError:
                break

    def exibir_mensagem(self, autor, mensagem):
        self.histórico_chat.config(state='normal')
        self.histórico_chat.insert(tk.END, f"{autor}: {mensagem}\n")
        self.histórico_chat.config(state='disabled')
        self.histórico_chat.see(tk.END)

root = tk.Tk()
app = ChatGUI(root)
root.mainloop()