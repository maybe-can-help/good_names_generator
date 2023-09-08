# good_names_generator

## How to use 
### Пример генерации имен сертификатов
```bash
cat some_file.txt | python3 good_names_generator.py generate certnames -dg -p > output_file.txt
```
Пример без использования pipe'ов:
```bash
python3 good_names_generator.py generate certnames --from some_file.txt --to output_file.txt
```

### Пример генерации имен сертификатов с добавлением их в конец нужного файла
```bash
cat some_file.txt | python3 good_names_generator.py generate certnames -dg -p > output_file.txt
```
Пример без использования pipe'ов:
```bash
python3 good_names_generator.py generate certnames --from some_file.txt --to output_file.txt -a
```

## How to compile
### Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install pyinstaller
pyinstaller --onefile src/good_names_generator.py
```
