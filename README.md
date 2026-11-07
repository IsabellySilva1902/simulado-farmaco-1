# simulado-farmaco-1

Simulado de **Farmacologia Clínica I** (143 questões comentadas, estilo ENAMED/residência), pronto para GitHub Pages.

Conteúdo, por assunto:

| Assunto | Questões |
| --- | --- |
| Aula 7 · Insulinas e insulinoterapia | 19 |
| Aula 8 · Antidiabéticos não insulínicos | 20 |
| Aula 9 · Anestésicos gerais e locais | 24 |
| Aula 10 · Sistema nervoso autônomo | 21 |
| Aula 11 · Antibióticos não betalactâmicos | 20 |
| Aula 12 · Anti-inflamatórios esteroidais (glicocorticoides) | 19 |
| Prova anterior · VAT1 2026.2 | 20 |

As questões foram escritas a partir dos 6 slides da professora (aulas 7 a 12) e dos livros de
farmacologia (Katzung, Rang & Dale, Whalen). As 20 questões da prova anterior são as da devolutiva
da VAT1 2026.2, com o comentário original da professora na justificativa. As questões que já vinham
prontas nos slides estão marcadas como "prova antiga" e foram mantidas com o texto original.

Cada questão tem justificativa para as quatro alternativas, ponto-chave e, na maioria, um
aprofundamento com a fonte (slide ou livro).

## Como atualizar

- `data/<aula>.json`: banco de questões de cada aula (fonte única).
- `tools/template.html`: motor do simulado (modos Exame e Tutor, filtros, revisão espaçada).
- `tools/build.py`: gera `index.html` e `data/questoes.json`, distribuindo a letra do gabarito.

Depois de mexer nas questões:

```bash
python3 tools/build.py
```

O progresso de quem responde fica salvo apenas no navegador dela (`localStorage`).
