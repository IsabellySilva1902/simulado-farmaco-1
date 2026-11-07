"""Gera index.html (o simulado) a partir de data/*.json e tools/template.html.

Uso, na raiz do repositório:  python3 tools/build.py

Cada arquivo em data/ é uma aula (ou a prova anterior) e tem o formato:
  {"assunto": "...", "category": "...", "prefixo": "XXX", "questoes": [
     {"s": subtema, "d": "B|I|A", "q": enunciado, "a": [4 alternativas],
      "j": [4 justificativas], "c": indice da correta (0 se ausente),
      "p": ponto-chave, "ap": aprofundamento (opcional), "f": fonte}
  ]}

O script converte para o formato do motor do simulado, distribui a letra do
gabarito entre A e D (só muda a ordem das alternativas, nunca o texto) e
numera as questões.
"""
import json, os, glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETRAS = 'ABCD'
DIF = {'B': 'Básica', 'I': 'Intermediária', 'A': 'Avançada'}
NOME = 'Farmacologia Clínica I'
STORAGE = 'farmaco1'
# ordem em que as aulas aparecem no filtro por assunto
ORDEM = ['a07', 'a08', 'a09', 'a10', 'a11', 'a12', 'prova']


def converter(q, codigo, assunto, categoria):
    c = q.get('c', 0)
    opts = [{'letter': LETRAS[k], 'text': q['a'][k].strip(),
             'rationale': ('CORRETA. ' if k == c else 'Incorreta. ') + q['j'][k].strip()}
            for k in range(4)]
    saida = {
        'code': codigo, 'assunto': assunto, 'category': categoria,
        'subcategory': q['s'], 'difficulty': DIF[q['d']],
        'origem': 'prova_antiga' if q.get('o') == 'slide' or assunto == 'prova-vat1' else 'nova',
        'sourceLabel': q['f'],
        'prompt': q['q'].strip(), 'options': opts, 'correctLetter': LETRAS[c],
        'clinicalPointers': q['p'], 'revisada': True,
    }
    if q.get('ap'):
        saida['bookContext'] = {'text': q['ap'], 'fonte': q['f']}
    return saida


def main():
    banco = []
    arquivos = sorted((f for f in glob.glob(os.path.join(RAIZ, 'data', '*.json'))
                       if os.path.basename(f)[:-5] in ORDEM),
                      key=lambda f: ORDEM.index(os.path.basename(f)[:-5]))
    for caminho in arquivos:
        d = json.load(open(caminho, encoding='utf-8'))
        for n, q in enumerate(d['questoes'], 1):
            banco.append(converter(q, f"{d['prefixo']}-{n:02d}", d['assunto'], d['category']))
        print(f"{os.path.basename(caminho)}: {len(d['questoes'])} questões ({d['category']})")

    # distribui o gabarito entre A-D: troca só a posição das alternativas
    for i, q in enumerate(banco):
        alvo = LETRAS[(i * 3 + 2) % 4]
        o = q['options']
        correta = o.pop(LETRAS.index(q['correctLetter']))
        o.insert(LETRAS.index(alvo), correta)
        for k, x in enumerate(o):
            x['letter'] = LETRAS[k]
        q['correctLetter'] = alvo

    for i, q in enumerate(banco, 1):
        q['id'] = i

    ordem = ['id', 'code', 'assunto', 'category', 'subcategory', 'difficulty', 'origem',
             'sourceLabel', 'prompt', 'options', 'correctLetter', 'clinicalPointers',
             'bookContext', 'revisada']
    banco = [{k: q[k] for k in ordem if k in q} for q in banco]

    json.dump(banco, open(os.path.join(RAIZ, 'data', 'questoes.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    tpl = open(os.path.join(RAIZ, 'tools', 'template.html'), encoding='utf-8').read()
    pagina = (tpl.replace('{{NOME_MAIUSCULO}}', NOME.upper()).replace('{{NOME}}', NOME)
                 .replace('{{STORAGE}}', STORAGE)
                 .replace('{{BANCO}}', json.dumps(banco, ensure_ascii=False, indent=1)))
    open(os.path.join(RAIZ, 'index.html'), 'w', encoding='utf-8').write(pagina)

    letras = {}
    for q in banco:
        letras[q['correctLetter']] = letras.get(q['correctLetter'], 0) + 1
    print(f"\nindex.html gerado: {len(banco)} questões, "
          f"{len({q['category'] for q in banco})} assuntos, gabarito {letras}")


if __name__ == '__main__':
    main()
