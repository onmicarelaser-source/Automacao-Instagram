
---

## 📄 ARQUIVO 2: `CONTRIBUTING.md` (COMPLETO)

```markdown
# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o **Automacao-Instagram**! Este guia irá ajudá-lo a entender como contribuir de forma eficaz.

## 📜 Código de Conduta

Este projeto segue o [Código de Conduta do Contribuidor](https://www.contributor-covenant.org/pt-br/version/2/0/code_of_conduct/). Ao participar, você concorda em respeitar este código.

### Comportamento Esperado
- ✅ Ser respeitoso e inclusivo
- ✅ Aceitar críticas construtivas
- ✅ Focar no que é melhor para a comunidade
- ✅ Demonstrar empatia com outros membros

### Comportamento Inaceitável
- ❌ Assédio ou discriminação
- ❌ Comentários ofensivos
- ❌ Ataques pessoais ou políticos
- ❌ Spam ou promoção não solicitada

## 🚀 Como Contribuir

### Tipos de Contribuição

1. **Reportar Bugs** 🐛
2. **Sugerir Features** 💡
3. **Melhorar Documentação** 📚
4. **Corrigir Issues** 🔧
5. **Adicionar Testes** 🧪
6. **Revisar Código** 👀

### Passos para Contribuir

1. **Fork o repositório**
   ```bash
   # Clique em "Fork" no GitHub
Clone seu fork

bash
git clone https://github.com/seu-usuario/Automacao-Instagram.git
cd Automacao-Instagram
Crie uma branch para sua feature

bash
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
Faça suas alterações

Siga os padrões de código

Adicione testes

Atualize a documentação

Commit suas alterações

bash
git add .
git commit -m "tipo: descrição da alteração"
Push para seu fork

bash
git push origin feature/nome-da-feature
Abra um Pull Request

Vá para o repositório original

Clique em "New Pull Request"

Descreva suas alterações

📝 Padrões de Código
Python (PEP 8)
Formatação
python
# ✅ Bom
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# ❌ Ruim
def calculate_total(items):
    total = 0
    return sum(item.price for item in items)
Nomenclatura
python
# Classes: CamelCase
class InstagramPublisher:
    pass

# Funções/Métodos: snake_case
def publish_post():
    pass

# Variáveis: snake_case
user_name = "onmicare"

# Constantes: UPPER_CASE
MAX_RETRIES = 3
Docstrings
python
def publish_post(image_path, caption):
    """
    Publica um post no Instagram.

    Args:
        image_path (str): Caminho da imagem
        caption (str): Legenda do post

    Returns:
        dict: Resposta da API com status e dados

    Raises:
        APIError: Se a API retornar erro

    Example:
        >>> publish_post("image.jpg", "Meu post")
        {'success': True, 'post_id': '123'}
    """
    pass
Type Hints
python
from typing import Optional, List, Dict

def get_user_posts(user_id: int, limit: Optional[int] = 10) -> List[Dict]:
    """
    Busca posts de um usuário.

    Args:
        user_id: ID do usuário
        limit: Número máximo de posts

    Returns:
        Lista de posts
    """
    pass
🔄 Processo de Pull Request
Checklist do PR
Código segue os padrões de estilo

Testes foram adicionados/atualizados

Documentação foi atualizada

Todos os testes passam

Sem conflitos com a branch principal

Commits são descritivos e atômicos

Template do PR
markdown
## Descrição
Descreva brevemente o que este PR faz.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação
- [ ] Refatoração

## Testes Realizados
Descreva os testes que você realizou.

## Screenshots
Se aplicável, adicione screenshots.

## Issues Relacionadas
Closes #123
🐛 Relatando Issues
Template para Bug
markdown
**Descrição do Bug**
Descrição clara do problema.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Veja o erro '...'

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável.

**Ambiente**
- SO: [e.g., Windows 10]
- Python: [e.g., 3.9.7]
- Versão do Projeto: [e.g., 1.0.0]

**Contexto Adicional**
Qualquer informação adicional.
Template para Feature
markdown
**Descrição da Feature**
Descreva a feature solicitada.

**Motivação**
Por que esta feature é necessária?

**Solução Proposta**
Como você imagina a implementação?

**Alternativas Consideradas**
Outras soluções que você pensou.

**Contexto Adicional**
Qualquer informação adicional.
📋 Convenções de Commit
Formato
text
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
Tipos
Tipo	Descrição
feat	Nova funcionalidade
fix	Correção de bug
docs	Documentação
style	Formatação
refactor	Refatoração
test	Testes
chore	Tarefas rotineiras
perf	Performance
Exemplos
bash
git commit -m "feat(scheduler): adiciona suporte a múltiplos agendamentos"
git commit -m "fix(api): corrige erro de autenticação no Instagram"
git commit -m "docs(readme): atualiza documentação de instalação"
git commit -m "style(format): aplica formatação PEP 8 em todo o código"
📞 Dúvidas?
📧 Email: onmicarelaser@gmail.com

💬 Discord: [Link do Discord]

🐦 Twitter: [@onmicarelaser]

Agradecemos sua contribuição! 🎉