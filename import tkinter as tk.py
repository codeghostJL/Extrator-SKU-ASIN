import tkinter as tk
from tkinter import filedialog, messagebox
import re
import csv

def processar_dados():
    texto = text_box.get("1.0", "end-1c").strip()

    if not texto:
        messagebox.showwarning("Aviso", "O campo de texto está vazio. Insira os dados antes de continuar.")
        return

    # Ajustando regex para diferentes formatos de "Código SKU" e "ASIN"
    sku = re.findall(r"Código SKU\s*[:\-]?\s*([\w\d_]{1,14})", texto)
    asin = re.findall(r"ASIN\s*[:\-]?\s*([\w\d]{10})", texto)  # Regex para capturar ASIN (ex: B0DZJ2V2BT)

    if not sku and not asin:
        messagebox.showwarning("Aviso", "Nenhum código SKU ou ASIN encontrado.")
        return

    # Salvar os dados em um arquivo CSV
    file_path = filedialog.asksaveasfilename(
        title="Salvar Planilha",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Código SKU", "ASIN"])  # Cabeçalho

                # Adicionar SKU e ASIN, se existirem
                max_len = max(len(sku), len(asin))
                for i in range(max_len):
                    sku_value = sku[i] if i < len(sku) else ""  # Garantir que se houver menos SKUs que ASINs, o campo não seja vazio
                    asin_value = asin[i] if i < len(asin) else ""  # Garantir o mesmo para ASINs
                    writer.writerow([sku_value, asin_value])

            messagebox.showinfo("Sucesso", f"Planilha salva com sucesso!\nLocal: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo: {e}")

def limpar_texto():
    text_box.delete("1.0", tk.END)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Extrator de Código SKU e ASIN")
root.geometry("500x400")
root.resizable(False, False)

# Campo de entrada de texto
text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=20)

# Frame para os botões
button_frame = tk.Frame(root)
button_frame.pack()

process_button = tk.Button(button_frame, text="Gerar Planilha", command=processar_dados)
process_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="Limpar", command=limpar_texto)
clear_button.grid(row=0, column=1, padx=5)

# Iniciar a interface gráfica
root.mainloop()
