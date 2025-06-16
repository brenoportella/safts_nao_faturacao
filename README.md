# NON-BILLING SAFTS' SUBIMISSIONS

 🇵🇹 [Portuguese version](https://github.com/brenoportella/safts_nao_faturacao/blob/master/readme_pt.md)

A script to submit non-billing SAFTs and check the submitted billing SAFTs. 

### Requirements
Before starting, make sure you have Python and pip installed on your system.
- You can check by running:

 ```bash
python --version
pip --version
```
or, on Linux:

 ```bash
python3 --version
pip3 --version
```

### WINDOWS INSTALLATION:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### LINUX INSTALLATION:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Input File
Create a xlsx file following this structure. (Begins in A1):
| Empresa |	NIPC |	Login |	Senha | Mes	| Ano |	C. Previa |	Ficheiro S | Com. N. Fat. |	Obs |
|-|-|-|-|-|-|-|-|-|-|
|ABCDE|123456789|123456789|Senha123|Jan|2024| | | | |
|FGHIJ|987654321|987654321|Senha987|Jan|2024| | | | |

<br>

Leave the colomns "C. Previa", "Ficheiro S", "Com. N. Fat.", and "Obs" blank. These fields will be automatically populated by the program.

Before using the program, make sure to set the relative path (relative to main.py) to your .xlsx input in the FILE variable inside src/defines.py
