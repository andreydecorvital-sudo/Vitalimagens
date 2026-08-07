# Vital Imagens

Sistema determinístico para produzir capas e galerias de marketplace com consistência visual e fidelidade ao produto.

O projeto nasceu da auditoria dos repositórios da VITAL DECOR e reúne os princípios mais úteis encontrados neles:

- produto e fatos bloqueados contra invenção;
- design guiado por tokens e um foco dominante;
- leitura mobile e hierarquia forte;
- geração em lote rastreável por kit/SKU;
- auditoria técnica antes da publicação;
- Upscayl e remoção de fundo como etapas anteriores à diagramação, nunca como licença para reconstruir o produto.

## Instalação

```bash
python -m venv .venv
.venv/bin/pip install -e .
```

No Windows, use `.venv\Scripts\python` e `.venv\Scripts\pip`.

## Gerar as capas do tijolinho 70 × 77

```bash
python scripts/generate_covers.py \
  --preset presets/tijolinho-70x77.json \
  --white caminho/placa-branca.png \
  --black caminho/placa-preta.png \
  --output outputs/tijolinho-70x77
```

O comando cria cada capa separadamente, gera uma prévia somente para revisão e salva `audit.json` com dimensões, arquivos e alertas.

## Testes

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Documentos

- `STYLESEED.md`: contrato visual obrigatório;
- `docs/DESIGN_AUDIT.md`: o que foi aproveitado de cada projeto;
- `presets/`: conteúdo confirmado, crops e kits;
- `src/vitalimagens/`: motor de composição e auditoria.
