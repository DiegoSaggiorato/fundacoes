import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

class ExeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Executável (PyInstaller)")
        self.root.geometry("600x500")

        # --- Verificação de Segurança (Ambiente Virtual) ---
        self.check_environment()

    def check_environment(self):
        # Tenta verificar se o módulo PyInstaller está acessível pelo Python atual
        import importlib.util
        if importlib.util.find_spec("PyInstaller") is None:
            # Detectar se existe venv por perto para sugerir
            venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
            msg = (
                "❌ PERIGO: PyInstaller NÃO encontrado!\n\n"
                "Você está rodando este script com o Python ERRADO.\n"
                f"Python Atual: {sys.executable}\n\n"
                "PARA CORRIGIR:\n"
                "Execute o script usando o Python do seu ambiente virtual (.venv).\n"
            )
            if os.path.exists(venv_path):
                msg += f"\nSUGESTÃO DE COMANDO:\n{venv_path} {sys.argv[0]}"
            
            messagebox.showerror("Erro Crítico de Ambiente", msg)
            # Não fecha o app para deixar o usuário ler, mas avisa
            self.root.title("⚠️ AMBIENTE INCORRETO - O GERADOR VAI FALHAR")

        # --- Variáveis ---
        self.main_script_path = tk.StringVar()
        self.app_name = tk.StringVar(value="MeuApp")
        self.is_streamlit = tk.BooleanVar(value=True)
        self.additional_files = []

        # --- Layout ---
        pad_opts = {'padx': 10, 'pady': 5}

        # 1. Script Principal
        tk.Label(root, text="Script Principal (Se for Streamlit, selecione o app.py):").pack(anchor='w', **pad_opts)
        frame_script = tk.Frame(root)
        frame_script.pack(fill='x', **pad_opts)
        
        tk.Entry(frame_script, textvariable=self.main_script_path).pack(side='left', fill='x', expand=True)
        tk.Button(frame_script, text="Selecionar...", command=self.select_main_script).pack(side='right', padx=(5, 0))

        # 2. Nome do App
        tk.Label(root, text="Nome do Executável:").pack(anchor='w', **pad_opts)
        tk.Entry(root, textvariable=self.app_name).pack(fill='x', **pad_opts)

        # 3. Opções
        tk.Checkbutton(root, text="É um App Streamlit? (Inclui dependências automáticas)", variable=self.is_streamlit).pack(anchor='w', **pad_opts)

        # 3.5 Bibliotecas Extras
        tk.Label(root, text="Bibliotecas Extras (separadas por vírgula, ex: ezdxf, numpy):").pack(anchor='w', **pad_opts)
        self.extra_libs = tk.StringVar()
        tk.Entry(root, textvariable=self.extra_libs).pack(fill='x', **pad_opts)

        # 4. Arquivos Adicionais
        tk.Label(root, text="Arquivos Adicionais (Ex: app.py, utils.py):").pack(anchor='w', **pad_opts)
        frame_add = tk.Frame(root)
        frame_add.pack(fill='x', **pad_opts)
        
        tk.Button(frame_add, text="Adicionar Arquivos...", command=self.add_files).pack(side='left')
        tk.Button(frame_add, text="Limpar Lista", command=self.clear_files).pack(side='left', padx=10)
        
        self.lbl_files = tk.Label(root, text="Nenhum arquivo adicional selecionado.", fg="gray", wraplength=550, justify="left")
        self.lbl_files.pack(anchor='w', **pad_opts)

        # 5. Botão Gerar
        tk.Button(root, text="🚀 GERAR EXECUTÁVEL", command=self.start_build, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(fill='x', padx=10, pady=15)

        # 6. Console de Saída
        tk.Label(root, text="Log de Saída:").pack(anchor='w', padx=10)
        self.log_area = scrolledtext.ScrolledText(root, height=10, state='disabled')
        self.log_area.pack(fill='both', expand=True, padx=10, pady=(0, 10))

    def select_main_script(self):
        filename = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if filename:
            self.main_script_path.set(filename)

    def add_files(self):
        filenames = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if filenames:
            self.additional_files.extend(filenames)
            self.update_files_label()

    def clear_files(self):
        self.additional_files = []
        self.update_files_label()

    def update_files_label(self):
        if not self.additional_files:
            self.lbl_files.config(text="Nenhum arquivo adicional selecionado.")
        else:
            basenames = [os.path.basename(f) for f in self.additional_files]
            self.lbl_files.config(text=f"Selecionados: {', '.join(basenames)}")

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_build(self):
        script = self.main_script_path.get()
        name = self.app_name.get()

        if not script:
            messagebox.showerror("Erro", "Selecione o script principal!")
            return
        if not name:
            messagebox.showerror("Erro", "Defina um nome para o executável!")
            return

        # Thread para não travar a GUI
        threading.Thread(target=self.run_pyinstaller, daemon=True).start()

    def run_pyinstaller(self):
        self.log("--- Iniciando Processo de Criação ---")
        
        main_script = self.main_script_path.get()
        app_name = self.app_name.get()
        is_streamlit = self.is_streamlit.get()
        
        # Construir comando base
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--clean",
            "--noconfirm",
            f"--name={app_name}",
            "--additional-hooks-dir=."
        ]
        
        # Lógica para Streamlit Auto-Launcher
        target_script_for_pyinstaller = main_script
        
        if is_streamlit:
            self.log("Modo Streamlit ativado: Gerando Launcher automático...")
            
            # Nome do arquivo de script original (ex: agendamento.py)
            script_basename = os.path.basename(main_script)
            
            # Criar conteúdo do launcher dinâmico
            launcher_code = f"""import sys
import os
from streamlit.web import cli as stcli

def main():
    if getattr(sys, 'frozen', False):
        script_path = os.path.join(sys._MEIPASS, '{script_basename}')
    else:
        script_path = os.path.join(os.path.dirname(__file__), '{script_basename}')

    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false", "--server.headless=true"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    main()
"""
            # Salvar launcher temporário
            launcher_filename = f"launcher_auto_{app_name}.py"
            launcher_path = os.path.join(os.path.dirname(main_script), launcher_filename)
            
            try:
                with open(launcher_path, "w", encoding="utf-8") as f:
                    f.write(launcher_code)
                self.log(f"Launcher criado: {launcher_filename}")
            except Exception as e:
                self.log(f"Erro ao criar launcher: {e}")
                return

            # O launcher passa a ser o script principal do PyInstaller
            target_script_for_pyinstaller = launcher_path
            
            # O script original deve ser incluído como DADOS (--add-data)
            cmd.extend(["--add-data", f"{main_script};."])
            self.log(f"Incluindo script original: {script_basename}")

            # Dependências do Streamlit
            cmd.extend([
                "--collect-all", "streamlit",
                "--collect-all", "pandas",
                "--collect-all", "docx",
                "--collect-all", "selenium",
                "--recursive-copy-metadata", "streamlit",
            ])
        
        # Adicionar bibliotecas extras definidas pelo usuário
        extras = self.extra_libs.get().split(',')
        for lib in extras:
            lib = lib.strip()
            if lib:
                cmd.extend(["--collect-all", lib])
                self.log(f"Coletando biblioteca extra: {lib}")
        
        # Adicionar arquivos extras
        for f in self.additional_files:
            # Evita adicionar o script principal duplicado se o usuário tiver selecionado sem querer
            if os.path.abspath(f) == os.path.abspath(main_script):
                continue
                
            basename = os.path.basename(f)
            cmd.extend(["--add-data", f"{f};."])
            self.log(f"Adicionando arquivo extra: {basename}")

        # Adicionar o script alvo (Launcher ou Script Normal)
        cmd.append(target_script_for_pyinstaller)

        self.log(f"Comando: {' '.join(cmd)}")
        self.log("---------------------------------------")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )

            for line in process.stdout:
                self.log(line.strip())

            process.wait()

            if process.returncode == 0:
                self.log("\n✅ SUCESSO! Executável criado na pasta 'dist'.")
                self.log("Você pode deletar o arquivo launcher_auto gerado se desejar.")
                messagebox.showinfo("Sucesso", f"O executável '{app_name}.exe' foi criado na pasta 'dist'.")
            else:
                self.log("\n❌ ERRO: O processo falhou. Verifique o log acima.")
                messagebox.showerror("Erro", "Falha na criação do executável.")

        except Exception as e:
            self.log(f"\n❌ Exceção: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExeGeneratorApp(root)
    root.mainloop()
