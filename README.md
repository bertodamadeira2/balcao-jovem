# e-Balcão Jovem — Funchal

Plataforma web de página única (HTML + CSS + JavaScript, sem dependências nem servidor) que junta num só sítio
tudo o que é útil para os jovens do Funchal, e uma rede de jovens porta-vozes por freguesia e por área.

É a proposta de continuação digital do **Balcão Jovem** que a Câmara Municipal do Funchal abriu em São Martinho
(Edifício Várzea, 6/6/2025). **Protótipo de trabalho — não é um serviço oficial da CMF.**

## Funcionalidades
- 📍 **Escolher a cidade**: mapa de Portugal por distritos e regiões autónomas → concelhos → freguesias (limites oficiais CAOP/DGT). Por agora só o Funchal está ativo.
- 🗺️ **Mapa do Funchal**: 10 freguesias com Junta de Freguesia fixada, Balcão Jovem, IPSS, serviços públicos, escolas e jovens da rede.
- 💶 **Apoios**: 18 bolsas, programas, estágios e benefícios (CMF, Governo Regional, DRJ, IEM) com estado do prazo calculado automaticamente e alerta para os que terminam em menos de 30 dias.
- 🏛️ **Serviços**: Balcão Jovem, programas Funchal.Jovem, DRJ, DRE, IEM, contactos úteis e sites oficiais.
- 🏫 **Escolas**: 54 estabelecimentos, do 1.º ciclo ao ensino superior, com filtros por nível e freguesia.
- 📣 **Porta-vozes** por área e por freguesia · 🧭 **Moderadores** por freguesia · 💡 **Ideias** · 📅 **Atividades** · 📰 **Notícias**
- 🙋 **Juntar-me** (Porta-voz / Jovem, 14–30 anos, com consentimento RGPD) · 🛡️ **Painel de Admin** · ❓ Guia interativo

## Abrir no Visual Studio Code
1. Abrir a pasta `balcao-jovem` no VS Code.
2. Instalar a extensão recomendada **Live Server** (o VS Code sugere-a automaticamente).
3. Botão direito em `index.html` → **Open with Live Server**.

## Publicar no GitHub
Repositório: https://github.com/bertodamadeira2/balcao-jovem

```bash
cd balcao-jovem
git init
git add .
git commit -m "e-Balcão Jovem v1.0"
git branch -M main
git remote add origin https://github.com/bertodamadeira2/balcao-jovem.git
git push -u origin main
```
Se o repositório já tiver um README criado no GitHub, antes do `push` correr `git pull origin main --allow-unrelated-histories`.

Link público: no GitHub, **Settings → Pages → Branch: main / (root) → Save**. Fica em
https://bertodamadeira2.github.io/balcao-jovem/

## Onde ficam os dados
| Onde corre | Como grava |
|---|---|
| claude.ai (artefacto) | A página republica-se a si própria: os dados ficam em `<script id="data-store">` e são partilhados por quem a edita |
| Fora do claude.ai (Live Server, GitHub Pages) | Modo autónomo: grava no `localStorage` **do teu browser** (não é partilhado) e as ferramentas de Admin ficam ativas |

Para uso real com várias pessoas é preciso um backend (ex.: Supabase ou infraestrutura da CMF) com autenticação.
A privacidade dos contactos é hoje aplicada só na interface.

## Pasta `data/`
Cópia em JSON, fácil de converter para CSV, de tudo o que está embutido no `index.html`:

| Ficheiro | Conteúdo |
|---|---|
| `escolas.json` / `niveis.json` | Escolas, nível, freguesia (`f`), morada, telefone, email; `fc:1` = freguesia a confirmar |
| `apoios.json` / `entidades_apoio.json` | Apoios com datas de candidatura (`ab`/`fe`), montantes, elegibilidade, ligação oficial |
| `servicos.json` / `contactos.json` / `links.json` | Serviços municipais e regionais, contactos institucionais e sites oficiais |
| `noticias.json` | Notícias iniciais (out. 2025 – out. 2026) |
| `entidades.json` | Juntas de Freguesia, IPSS, Governo Regional e Balcão Jovem (dados públicos) |
| `mapa-portugal-distritos-concelhos.json` | Caminhos SVG de distritos e concelhos (gerado por `tools/build_geo.py`) |
| `mapa-funchal-freguesias.json` | Caminhos SVG das 10 freguesias (gerado por `tools/build_map_funchal.py`) |

## Privacidade (RGPD)
Este repositório tem **apenas dados públicos** e 8 perfis de demonstração com nomes fictícios ("… Exemplo"),
que se apagam no Painel de Admin → *Limpar exemplos*. **Nunca fazer commit de dados pessoais** de jovens,
inscrições ou administradores.

## A confirmar com a Divisão de Juventude
- Morada exata, horário e contacto direto do Balcão Jovem (hoje usa 291 211 000 e djuventude@funchal.pt)
- Freguesia de 33 escolas (as fontes oficiais não a indicam)
- Manual de marca Funchal.Jovem (as cores atuais são provisórias: preto, branco e cinzentos)
- Alojamento, Encarregado de Proteção de Dados e acessibilidade

## Fontes
Ver [`docs/FONTES.md`](docs/FONTES.md). Informação pública recolhida a 16/10/2026.
