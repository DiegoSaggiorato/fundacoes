# Guia de Uso: Gerador de Executáveis (Exe Generator)

Este guia explica como usar a ferramenta `exe_generator.py` para transformar seus scripts Python (e Apps Streamlit) em arquivos executáveis (`.exe`) que podem rodar em outros computadores.

## 1. Pré-Requisitos (Ambiente Virtual)

Antes de abrir o gerador, é **essencial** garantir que seu ambiente virtual esteja configurado corretamente. O PyInstaller (ferramenta que gera o exe) usa as bibliotecas instaladas no "Python atual" para criar o programa.

### Passo a Passo:
1.  **Abra o Terminal** na pasta do projeto.
2.  **Ative o Ambiente Virtual** (onde suas bibliotecas estão instaladas):
    *   **Windows:** `.\.venv\Scripts\activate`
    *   (Você verá um `(.venv)` no início da linha de comando).
3.  **Verifique as Instalações:**
    *   Certifique-se de que o `pyinstaller` está instalado: `pip install pyinstaller`.
    *   Certifique-se de que todas as bibliotecas do seu projeto (pandas, selenium, streamlit, docx, etc.) estão instaladas.

## 2. Abrindo o Gerador

Com o ambiente ativado, execute o comando:
```bash
python exe_generator.py
```
Uma janela gráfica abrirá.

## 3. Configurando a Criação do EXE

Preencha os campos da interface conforme abaixo:

### A. Script Principal
*   Selecione o arquivo `.py` do seu programa.
*   **Para Apps Streamlit:** Selecione o seu arquivo principal (ex: `app.py`, `dashboard.py`).
    *   *Nota:* A ferramenta criará automaticamente um "launcher" interno para você. Não precisa mais criar `launcher.py` manualmente!
*   **Para Scripts Normais:** Selecione o script que inicia a execução.

### B. Nome do Executável
*   Digite o nome que o arquivo final terá (ex: `CotacaoTools`). Não precisa colocar `.exe` no final.

### D. Arquivos Adicionais (Muito Importante!)
*   Se seu código é dividido em vários arquivos (ex: `app.py` chama `quotation_tool.py`), você **PRECISA** adicionar os outros arquivos aqui.
*   **No seu caso:**
    *   **Script Principal:** `app.py`
    *   **Arquivos Adicionais:** Adicione `quotation_tool.py` (e outros se houver).
*   Se não adicionar, o programa vai abrir mas dará erro dizendo que não encontrou o módulo.

### E. Preciso selecionar o Ambiente Virtual?
*   **Não na interface.** O gerador usa o ambiente de onde ele foi lançado.
*   **Regra de Ouro:** Se você rodou `python exe_generator.py` com o ambiente ativado (aparecendo `(.venv)` no terminal), o executável será criado corretamente com todas as bibliotecas desse ambiente.

## 4. Gerando o Arquivo
1.  Clique no botão verde **🚀 GERAR EXECUTÁVEL**.
2.  Acompanhe o progresso no "Log de Saída" abaixo.
3.  O processo pode demorar alguns minutos.
4.  Ao final, você verá "✅ SUCESSO!".

## 5. Onde está meu arquivo?
O arquivo `.exe` gerado estará na pasta **`dist`** dentro do diretório do seu projeto.
`c:\python\web_scraping\dist\CotacaoTools.exe`

## 6. Usando em Outros Computadores
*   Copie o arquivo `.exe` da pasta `dist` para o outro computador.
*   **Navegador:** O computador de destino precisa ter um navegador web instalado (Chrome/Edge) para o Streamlit abrir a interface.
*   **Driver:** Se você usa Selenium (Web Scraping), certifique-se de que o computador tem o Google Chrome instalado (o `webdriver` usually gerencia o driver compatível se estiver configurado).

---
**Nota sobre Manutenção:** Se você adicionar novas bibliotecas ao projeto (`pip install nova-lib`), você precisará gerar o `.exe` novamente para que ela seja incluída no pacote.
