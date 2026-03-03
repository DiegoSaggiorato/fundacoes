# Guia Básico de Git e GitHub

Este guia responde às suas perguntas sobre como gerenciar seu código com Git.

## 1. Como inicializo uma pasta?
Para transformar uma pasta comum em um repositório Git, abra o terminal dentro da pasta e digite:
```powershell
git init
```
*Isso cria uma pasta oculta `.git` que rastreia todas as mudanças.*

## 2. Como mando os arquivos? (O Fluxo Git)
O envio de arquivos funciona em 3 etapas:

1.  **Adicionar à área de preparação (Staging):**
    Escolha quais arquivos você quer salvar.
    ```powershell
    git add .
    ```
    *(O ponto `.` adiciona todos os arquivos modificados e novos)*

2.  **Confirmar as alterações (Commit):**
    Salve a "foto" atual dos arquivos com uma mensagem.
    ```powershell
    git commit -m "Minha mensagem explicando o que mudei"
    ```

3.  **Enviar para a nuvem (Push):**
    Envie seus commits locais para o GitHub.
    ```powershell
    git push origin main
    ```
    *(Se for a primeira vez, pode ser `git push -u origin main`)*

## 3. O que é Branch?
Uma **Branch** (ramificação) é como uma linha do tempo paralela ou uma cópia do seu projeto onde você pode testar coisas novas sem quebrar o código principal.
- **main (ou master):** É a linha do tempo "oficial" do seu projeto.
- **Nova branch:** Você cria uma branch para desenvolver uma nova funcionalidade (ex: `nova-interface`). Se der errado, a `main` continua intacta. Se der certo, você junta (merge) as duas.

```powershell
# Criar e mudar para uma nova branch
git checkout -b nome-da-branch

# Voltar para a main
git checkout main
```

## 4. Como envio arquivos sem o `.venv`?
Você deve usar um arquivo chamado `.gitignore`.
O Git lê esse arquivo e ignora tudo o que estiver listado nele.

**Passo a passo:**
1. Crie um arquivo chamado `.gitignore` na raiz do projeto.
2. Escreva nele os nomes das pastas ou arquivos que quer ignorar. Exemplo:
    ```
    .venv/
    __pycache__/
    build/
    dist/
    ```
3. O Git não vai mais "ver" esses arquivos quando você der `git add .`.

*(Eu já atualizei seu `.gitignore` para incluir essas pastas)*.

## 5. Como puxar as modificações de outro PC?
Se você trabalhou no computador A, enviou para o GitHub, e agora está no computador B:

1.  **Na primeira vez no Computador B:**
    Baixe o projeto completo (Clonar).
    ```powershell
    git clone https://github.com/SEU_USUARIO/NOME_DO_REPO.git
    cd NOME_DO_REPO
    ```

2.  **Nas próximas vezes (Atualizar):**
    Se você já tem a pasta, apenas atualize com o que está na nuvem.
    ```powershell
    git pull
    ```
    Isso baixa as mudanças do GitHub e atualiza seus arquivos locais automaticamente.

## Resumo dos Comandos
| Ação | Comando |
| :--- | :--- |
| Iniciar repositório | `git init` |
| Ver status | `git status` |
| Preparar arquivos | `git add .` |
| Salvar versão | `git commit -m "mensagem"` |
| Enviar para GitHub | `git push` |
| Baixar atualizações | `git pull` |
| Clonar projeto | `git clone URL` |

## 6. Como verificar o Status?
Sempre que estiver na dúvida, digite:
```powershell
git status
```
Ele vai te dizer:
- Quais arquivos mudaram.
- Quais arquivos são novos (untracked).
- Se está tudo limpo (nothing to commit).
*Use esse comando o tempo todo!*

## 7. Como logar no GitHub pelo terminal?
Como você não tem o aplicativo extra (GitHub CLI), o login acontece **automaticamente** na primeira vez que você tentar enviar algo (`git push`).
1. O terminal vai abrir uma janelinha (Popup).
2. Clique em "Sign in with browser" (Entrar com navegador).
3. Autorize o acesso.
*Pronto! O Windows vai salvar sua senha para as próximas vezes.*

## 8. A Regra 80/20 do Git (O Essencial)
Você não precisa decorar tudo. 80% do tempo você só vai usar estes 5 comandos:

1.  **`git status`**: "O que está acontecendo?" (Vê as mudanças).
2.  **`git add .`**: "Junta tudo." (Prepara os arquivos).
3.  **`git commit -m "..."`**: "Salva." (Cria o ponto de história).
4.  **`git push`**: "Sobe." (Envia para nuvem).
5.  **`git pull`**: "Desce." (Baixa da nuvem).

*Decore esses 5 e você estará bem servido!*

## 9. Dúvidas: O nome da pasta importa?
**Não!** O Git não liga para o nome da pasta no seu computador.
O que importa é o "Remote" (o link do GitHub).

**Cenário A: Começando do zero (Clonar com outro nome)**
Se você quer baixar o projeto, mas quer que a pasta tenha um nome diferente do GitHub:
```powershell
git clone https://github.com/usuario/repo.git MinhaPastaFavorita
```

**Cenário B: Já tenho a pasta e quero baixar nela**
Se você tem uma pasta `MeuProjetoLocal` e quer puxar os arquivos do repo `ProjetoX`:
1. Entre na pasta: `cd MeuProjetoLocal`
2. Inicie o git (se não tiver): `git init`
3. Conecte: `git remote add origin https://github.com/usuario/ProjetoX.git`
4. Baixe: `git pull origin main`

*Nota: Se der erro de "unrelated histories", use: `git pull origin main --allow-unrelated-histories`*

## 10. Como ver quem sou eu?
Para ver qual nome e email estão configurados no seu PC:
```powershell
git config user.name
git config user.email
```
*Isso é apenas a etiqueta que vai nos seus commits, não necessariamente seu login no site.*

## 11. Como listar meus repositórios?
O Git sozinho **não tem esse comando**. Ele gerencia **arquivos**, não sua conta.
Para listar projetos via terminal, você precisa instalar a ferramenta oficial do GitHub (GitHub CLI):

1.  Se quiser instalar, digite: `winget install GitHub.cli`
2.  Depois, faça login: `gh auth login`
3.  Aí sim você pode ver a lista: `gh repo list`

## 12. Mensagens Comuns (O que significam?)
- **"Reinitialized existing Git repository..."**:
  Significa que você rodou `git init` numa pasta que **já tinha** git.
  **Não se preocupe!** Isso não apaga nada. Ele apenas reiniciou as configurações ocultas.

- **"nothing to commit, working tree clean"**:
  Ótima notícia! Significa que não há mudanças pendentes. Tudo o que você fez já está salvo no Git local.

- **"fatal: remote origin already exists"**:
  Você tentou adicionar o link do GitHub (remote) de novo.
  Se quiser mudar o link, use: `git remote set-url origin NOVO_LINK`

- **"fatal: The current branch main has no upstream branch"**:
  O Git não sabe "em qual gaveta" do GitHub ele deve guardar seus arquivos.
  Isso acontece na primeira vez. Rode o comando que ele sugere:
  `git push --set-upstream origin main`

- **"fatal: repository '...' not found"**:
  **O Erro mais comum!**
  Você criou o Git no seu PC, definiu o link, mas **esqueceu de criar o repositório no site do GitHub**.
  O Git não cria o repositório no site para você.
  1. Vá em github.com e clique no "+" -> "New Repository".
  2. Coloque o **MESMO NOME** que você definir no link (ex: `exe_generator`).
  3. Não crie README nem .gitignore lá (você já tem aqui).
  4. Clique em "Create".
  5. Agora tente o `git push` de novo.

- **"error: src refspec main does not match any"**:
  **Tradução:** "Você tentou enviar a caixa vazia."
  Isso acontece quando você tenta dar `git push` **sem ter feito o commit antes**.
  O Git não envia pastas vazias nem arquivos soltos.
  **Solução:**
  1. `git add .`
  2. `git commit -m "primeiro commit"`
  3. `git push`

- **"error: remote origin already exists"**:
  **Tradução:** "Já existe um link configurado aqui."
  Você provavelmente está na pasta errada ou tentando adicionar um link novo numa pasta velha.
  
  **Opção A: Verifique onde você está**
  Digite `dir` ou `ls` e veja se está na pasta certa do projeto.
  
  **Opção B: Trocar o link (Se você quiser mudar mesmo)**
  Não use `add` (adicionar), use `set-url` (definir url):
  `git remote set-url origin https://novo-link.com`

- **"fatal: unable to access ... Could not resolve host: https"**:
  **O Erro:** Você digitou `https://https://...` (duplicado).
  Isso acontece quando você copia o link do navegador e escreve "https://" antes no comando.
  **Correção:**
  `git remote set-url origin https://github.com/SEU_USUARIO/SEU_REPO.git`

- **"error: remote origin already exists"**:
  **Tradução:** "Já existe um link (origin) configurado."
  Você não pode adicionar dois "origins". Você deve **trocar** o existente.
  **Comando para TROCAR o link:**
  ```powershell
  git remote set-url origin https://novo-link-correto.com
  ```

- **"fatal: unable to access ... Could not resolve host: https"**:
  **O Erro:** Você digitou `https://https://...` (duplicado) sem querer.
  **A Solução:** Use o comando de trocar (acima) para arrumar o link.
  `git remote set-url origin https://github.com/SEU_USER/REPO.git`

## 13. Curiosidade: Como ele sabe para onde enviar?
"Se o nome da pasta não importa, como ele acerta o destino?"

A mágica está num endereço salvo que chamamos de **remote**.
Lá no começo, você rodou:
```powershell
git remote add origin https://github.com/DiegoSaggiorato/exe_generator.git
```
É **esse link** que manda. O Git pensa assim:
1. Você diz "envia aí" (`git push`).
2. Ele olha na configuração: "Quem é o `origin`?"
3. Ele acha o link `https://github.com/.../exe_generator.git`.
4. Ele envia para esse endereço, não importa se sua pasta chama `banana` ou `projeto`.

Para ver para onde seu Git está apontando agora, digite:
```powershell
git remote -v
```
*(O `-v` significa "verbose" / detalhado).*

**O que deve aparecer:**
Você verá duas linhas (uma para baixar/fetch e uma para enviar/push):
```
origin  https://github.com/SEU_USER/SEU_REPO.git (fetch)
origin  https://github.com/SEU_USER/SEU_REPO.git (push)
```
Se aparecer isso, está tudo certo! O "apelido" **origin** está ligado corretamente ao seu link do GitHub.

## 14. "Colei o link e deu erro!" (Como usar links)
O terminal é como um robô que só entende verbos (comandos).
Você não pode jogar o link solto lá. Ele vai dizer: "Não conheço esse comando".

**Errado:**
```powershell
https://github.com/meu/projeto
```

**Certo:** (Você precisa dizer o que fazer com o link)
- Quer baixar? `git clone https://...`
- Quer conectar? `git remote add origin https://...`

O link é sempre o **ingrediente**, nunca o **cozinheiro**.

