# Auditoria de design dos projetos VITAL DECOR

Auditoria realizada nos repositórios acessíveis da conta `andreydecorvital-sudo`. O objetivo foi extrair princípios reutilizáveis sem copiar identidades, campanhas ou código incompatível.

## Síntese por projeto

| Projeto | Achado útil | Aplicação no Vital Imagens |
|---|---|---|
| `vital-marketplace-hub` | fatos classificados, galeria por objeção, Upscayl e auditoria de fidelidade | produto bloqueado e fluxo original → tratamento → layout → QA |
| `vitalhub` | tokens centralizados, hierarquia por superfície, acessibilidade e movimento funcional | paleta central, leitura clara e ausência de efeitos genéricos |
| `Ned` | StyleSeed, um foco dominante, gate visual e combate à aparência genérica de IA | `STYLESEED.md` obrigatório e checklist antes da entrega |
| `Maflorestour` | emoção sustentada por informação real, CTA óbvio e mídia factual | capas persuasivas sem preços, provas ou promessas inventadas |
| `aya` | mobile-first e informação decisiva por produto | teste em miniatura e redução de copy na capa |
| `Impress-o-` | renderização determinística, segurança de template e testes | gerador repetível por kit e testes de dimensão/fonte intacta |
| `tatibarbi` | produto como protagonista e ritmo editorial | fotografia dominante com copy de apoio, sem card wall |
| `Manu` | transparência sobre escopo e referências | cenários e estudos devem ser rotulados, nunca apresentados como resultado real |
| `saas` | estrutura de aplicação, mas identidade visual ainda genérica | nenhuma decisão visual copiada; serve apenas como alerta contra defaults |
| `Optimize` | direção para otimização local | Upscayl permanece etapa externa e anterior ao layout |
| `vital-marketplace-hub` | separação entre cálculo e criação | metragem calculada pelo preset, não digitada em cada capa |
| `Vitalimagens` | repositório estava vazio | recebeu contrato visual, gerador, preset e testes como nova fonte de verdade |

`Ned-Marketing` não continha arquivos auditáveis no momento da análise.

## Decisões consolidadas

1. Quantidade e metragem mudam por dados; o layout não é recriado manualmente.
2. As fotografias do produto são recortadas e redimensionadas mantendo proporção.
3. A marca aparece como assinatura; o produto continua sendo o foco.
4. A capa usa quatro blocos de leitura: kit, medida, cobertura e produto/cor.
5. A revisão em mosaico existe apenas para QA; cada arquivo final permanece separado.
6. Super-resolution é opcional e nunca serve como prova de textura ou acabamento.
7. Toda informação comercial deve ser confirmada ou removida.

## Próximas integrações recomendadas

- incorporar o auditor de imagens do `vital-marketplace-hub`;
- adicionar preset para placas 30 × 60 e 60 × 60;
- criar exportações específicas para Shopee, Mercado Livre e TikTok Shop;
- conectar a ponte local do Upscayl somente quando o diagnóstico Vulkan estiver saudável;
- adicionar uma interface web sobre o motor determinístico sem mover o processamento de imagens privadas para a nuvem.

