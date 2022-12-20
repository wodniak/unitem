## About
Zaproponuj architekturę Producent-Konsument, w której:
- Producent (zrealizowany jako wątek) ma do dyspozycji źródło danych o rozmiarze
szerokość=1024 px, wysokość=768 px, liczba kanałów=3. Co 50 ms producent pobiera nowe dane z Source i wrzuca je do kolejki A,
- Konsument (zrealizowany jako wątek) ściąga dostępne dane z kolejki A i dokonuje następujących operacji przetwarzania:
    - dwukrotne zmniejszenie rozmiaru obrazu,
    - aplikuje filtr medianowy o kernelu 5x5.

Po zakończeniu przetwarzania, nowy obraz wrzucony jest do kolejki B.

## Docker
```docker build . -f Dockerfile -t unitem```

```docker run -it unitem /bin/bash```

```docker exec -it <container_name> /bin/bash```

## To start the script

```python src/main.py```

