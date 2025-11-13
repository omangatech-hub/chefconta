# 💰 Módulo de Caixa - ChefConta

## 📋 Visão Geral

O módulo de Caixa é um sistema completo de controle financeiro diário que permite:
- **Abertura** de caixa com valor inicial
- Registro automático de **vendas por comanda ou balcão**
- Controle de **formas de pagamento** (Dinheiro, Cartão, PIX, Outros)
- **Sangria** (retirada de dinheiro)
- **Reforço** (entrada de dinheiro)
- **Fechamento** de caixa com contagem e conferência
- **Histórico** de todos os caixas

---

## 🚀 Como Usar

### 1. Abertura de Caixa

**Quando:** No início do expediente, antes de realizar qualquer venda.

**Passos:**
1. Acesse **💰 Caixa** no menu lateral
2. Clique em **🔓 Abrir Caixa**
3. Informe o **valor inicial** (troco do dia)
4. Adicione **observações** (opcional)
5. Clique em **✅ Abrir Caixa**

**Dica:** Se você tem R$ 100,00 de troco para começar o dia, esse é o valor inicial.

---

### 2. Registro de Vendas

**Automático!** Quando você faz uma venda pelo módulo **🛒 Vendas**, ela é automaticamente registrada no caixa aberto.

**Ao fazer uma venda, você escolhe:**

#### 🛎️ Tipo de Venda:
- **Balcão:** Venda direta no balcão (rápida)
- **Comanda:** Venda por comanda/mesa (delivery ou mesa)

#### 💳 Forma de Pagamento:
- **💵 Dinheiro**
- **💳 Cartão** (débito/crédito)
- **📱 PIX**
- **🔄 Outros** (vale, crediário, etc.)

**Importante:** Se não houver caixa aberto, a venda será realizada mas **não será registrada no caixa**.

---

### 3. Visualização do Caixa

**Tela Principal do Caixa mostra:**

#### 📊 Cards de Resumo:
- **💵 Saldo Inicial:** Valor com que o caixa foi aberto
- **💰 Total Vendas:** Soma de todas as vendas do dia
- **📋 Comandas:** Total de vendas por comanda
- **🛎️ Balcão:** Total de vendas por balcão
- **💸 Saldo Atual:** Dinheiro esperado no caixa
- **🧾 Qtd Vendas:** Número total de vendas

#### 💳 Formas de Pagamento:
- Total recebido em **Dinheiro**
- Total recebido em **Cartão**
- Total recebido em **PIX**

---

### 4. Operações Durante o Dia

#### 💸 Sangria (Retirada de Dinheiro)
**Quando usar:** Quando precisa retirar dinheiro do caixa (ex: pagar fornecedor, comprar suprimentos).

**Passos:**
1. Clique em **💸 Sangria**
2. Informe o **valor** a retirar
3. Informe o **motivo** (ex: "Pagamento fornecedor Padaria do João")
4. Confirme

#### 💰 Reforço (Entrada de Dinheiro)
**Quando usar:** Quando precisa adicionar dinheiro ao caixa (ex: troco adicional).

**Passos:**
1. Clique em **💰 Reforço**
2. Informe o **valor** a adicionar
3. Informe o **motivo** (ex: "Troco adicional R$ 50")
4. Confirme

#### 📜 Ver Movimentações
Lista TODAS as movimentações do dia:
- Vendas realizadas
- Sangrias
- Reforços
- Hora de cada operação

---

### 5. Fechamento de Caixa

**Quando:** No final do expediente.

**Passos:**

1. Clique em **🔒 Fechar Caixa**

2. **Confira o Resumo do Dia:**
   - Valor de abertura
   - Total de vendas
   - Vendas por comanda e balcão
   - Quantidade de vendas
   - Saídas/sangrias
   - Saldo esperado

3. **Conte o Dinheiro Físico:**
   - 💵 Dinheiro: Conte o dinheiro em espécie no caixa
   - 💳 Cartão: Some os recibos de cartão
   - 📱 PIX: Some os comprovantes PIX
   - 🔄 Outros: Some outras formas

4. Clique em **🔢 Calcular Total** para ver a diferença

5. **Analise a Diferença:**
   - ✅ **Zero:** Perfeito! Caixa bateu exatamente
   - 🟢 **Positivo (+):** Sobra no caixa (tem mais dinheiro que deveria)
   - 🔴 **Negativo (-):** Falta no caixa (tem menos dinheiro que deveria)

6. Adicione **observações** se necessário

7. Clique em **🔒 Fechar Caixa**

**Importante:** Após o fechamento, não é possível reabrir o mesmo caixa!

---

## 📈 Exemplos Práticos

### Exemplo 1: Dia Normal

**Manhã (08:00):**
```
Operação: Abertura de Caixa
Valor Inicial: R$ 100,00 (troco)
```

**Durante o Dia:**
```
10:30 - Venda #001 - Balcão - Dinheiro - R$ 25,50
11:45 - Venda #002 - Comanda - Cartão - R$ 78,00
12:20 - Sangria - "Pagar entregador" - R$ 30,00
14:15 - Venda #003 - Balcão - PIX - R$ 45,00
15:30 - Venda #004 - Comanda - Dinheiro - R$ 120,00
16:00 - Reforço - "Troco adicional" - R$ 50,00
```

**Noite (18:00) - Fechamento:**
```
Resumo:
- Abertura: R$ 100,00
- Total Vendas: R$ 268,50
- Comandas: R$ 198,00
- Balcão: R$ 70,50
- Sangrias: R$ 30,00
- Reforços: R$ 50,00
- Saldo Esperado: R$ 388,50

Contagem:
- Dinheiro: R$ 265,50 (R$ 100 inicial + R$ 25,50 + R$ 120 + R$ 50 - R$ 30)
- Cartão: R$ 78,00
- PIX: R$ 45,00
- Total: R$ 388,50

Diferença: R$ 0,00 ✅ PERFEITO!
```

### Exemplo 2: Dia com Diferença

**Fechamento:**
```
Saldo Esperado: R$ 500,00

Contagem:
- Dinheiro: R$ 445,00
- Cartão: R$ 50,00
- PIX: R$ 10,00
- Total: R$ 505,00

Diferença: +R$ 5,00 (Sobra)

⚠️ Verificar: Pode ter esquecido de registrar uma sangria de R$ 5,00
```

---

## 📊 Relatórios e Análises

### No Dashboard
O módulo de Caixa alimenta automaticamente:
- **💰 Vendas do Mês:** Soma de todas as vendas
- **💸 Saldo:** Resultado das operações

### Relatórios Disponíveis
No módulo **📈 Relatórios**, você pode gerar:
- **Relatório Financeiro:** Inclui dados do caixa
- **Relatório de Vendas:** Separado por tipo (comanda/balcão)

---

## 🔒 Segurança e Controle

### Auditoria
Todas as movimentações ficam gravadas permanentemente:
- Quem abriu/fechou o caixa
- Hora exata de cada operação
- Referência às vendas originais
- Descrição de sangrias/reforços

### Histórico de Caixas
Acesse **📋 Ver Histórico de Caixas** para ver:
- Todos os caixas anteriores
- Datas de abertura/fechamento
- Totais de vendas
- Diferenças (quebras de caixa)
- Status (ABERTO/FECHADO)

---

## ⚠️ Avisos Importantes

### ❌ Não há caixa aberto
Se você tentar fazer uma venda sem caixa aberto:
- ✅ A venda será realizada normalmente
- ⚠️ Mas NÃO será registrada no caixa
- 💡 O sistema avisará com um popup

**Solução:** Sempre abra o caixa no início do expediente!

### 🔄 Caixa já está aberto
Se tentar abrir um segundo caixa:
- ❌ O sistema não permitirá
- 💡 Você precisa fechar o caixa atual primeiro

### 💰 Controle de Dinheiro
- **Sangrias** reduzem o saldo do caixa
- **Reforços** aumentam o saldo do caixa
- Registre TUDO para manter o controle correto!

---

## 🎯 Boas Práticas

### ✅ Faça Sempre:
1. **Abra o caixa** no início do expediente
2. **Registre todas as sangrias e reforços** imediatamente
3. **Feche o caixa** no final do expediente
4. **Anote observações** sobre diferenças grandes
5. **Conte o dinheiro** com calma no fechamento

### ❌ Evite:
1. Fazer vendas sem caixa aberto
2. Esquecer de registrar sangrias
3. Misturar dinheiro de dias diferentes
4. Deixar caixa aberto de um dia para outro
5. Fechar caixa sem conferir valores

### 💡 Dicas:
- **Mantenha troco padrão:** Use sempre o mesmo valor inicial (ex: R$ 100)
- **Faça sangrias regulares:** Se acumular muito dinheiro, faça sangria para o cofre
- **Documente diferenças:** Se o caixa não bater, anote o que pode ter acontecido
- **Revise o dia:** Antes de fechar, revise as movimentações

---

## 🔧 Estrutura Técnica

### Tabelas do Banco de Dados:

#### `cash_registers` (Caixas)
- ID do caixa
- Usuário responsável
- Data/hora de abertura
- Data/hora de fechamento
- Valores (inicial, vendas, totais, diferença)
- Totais por tipo (comanda/balcão)
- Totais por forma de pagamento
- Status (aberto/fechado)

#### `cash_movements` (Movimentações)
- ID da movimentação
- Caixa relacionado
- Tipo (entrada/saida/sangria/reforco)
- Tipo de venda (comanda/balcao)
- Forma de pagamento
- Valor
- Descrição
- Referência à venda (se aplicável)

---

## 📞 Perguntas Frequentes

**Q: Posso editar um caixa já fechado?**
A: Não. Uma vez fechado, o caixa não pode ser reaberto ou editado.

**Q: E se eu esquecer de abrir o caixa?**
A: As vendas serão realizadas normalmente, mas não ficarão no controle de caixa. Você precisará registrar manualmente no fechamento.

**Q: Posso ter mais de um caixa aberto ao mesmo tempo?**
A: Não. Apenas um caixa pode estar aberto por vez no sistema.

**Q: Como corrigir uma venda registrada errada?**
A: Cancele a venda no módulo de Vendas. Ela será automaticamente descontada dos totais do caixa.

**Q: O que fazer se a diferença for grande?**
A: Revise todas as movimentações do dia, confira se registrou todas as sangrias, verifique se não houve vendas sem registrar no sistema.

**Q: Posso ver o caixa de dias anteriores?**
A: Sim! Use o botão "📋 Ver Histórico de Caixas".

---

## 🎉 Resumo

O módulo de Caixa do ChefConta oferece controle total sobre suas movimentações financeiras diárias:

✅ **Abertura simples** com valor inicial
✅ **Registro automático** de vendas
✅ **Separação** entre comanda e balcão
✅ **Controle** de formas de pagamento
✅ **Sangria e reforço** quando necessário
✅ **Fechamento** com conferência automática
✅ **Histórico** completo e permanente

**Use o Caixa diariamente e mantenha seu controle financeiro em dia!** 💰

---

**Desenvolvido para:** ChefConta v1.0  
**Última atualização:** 11/11/2025
