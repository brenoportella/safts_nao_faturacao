# SUBMISSÕES DE SAFTS SEM FATURAÇÃO

🇬🇧 [Versão em Inglês](https://github.com/brenoportella/safts_nao_faturacao/blob/main/readme.md)

### Requisitos

Antes de começar, certifique-se de que tem o Python e o pip instalados no seu sistema.

- Pode verificar executando:

```bash
python --version
pip --version
```
ou, em Linux:

```bash
python3 --version
pip3 --version
```
### WINDOWS INSTALAÇÃO :

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### LINUX INSTALAÇÃO:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Input File
Crie um ficheiro xlsx seguindo a seguinte estrutura. (Comece em A1):
| Empresa |	NIPC |	Login |	Senha | Mes	| Ano |	C. Previa |	Ficheiro S | Com. N. Fat. |	Obs |
|-|-|-|-|-|-|-|-|-|-|
|ABCDE|123456789|123456789|Senha123|Jan|2024| | | | |
|FGHIJ|987654321|987654321|Senha987|Jan|2024| | | | |

Deixe em branco os campos "C. Previa", "Ficheiro S", "Com. N. Fat.", e "Obs", estes serão preenchidos pelo programa.
<br>

Antes de usar o programa, verifique se indicou o caminho relativo do seu ficheiro .xlsx na variável FILE dentro de src/defines.py