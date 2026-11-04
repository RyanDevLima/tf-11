# TF - ES - 11 - Object Calisthenics

## 1. Normalização

Normalizar é manter cada dado em um único objeto e fazer os pedidos referenciarem esse objeto. A Ana é criada uma vez, e os pedidos 1 e 3 usam a mesma cliente, evitando cópias divergentes dos dados dela.

## 2. Obsessão por tipos primitivos

`Cpf` concentra a validação do documento, então um valor inválido é recusado no momento da criação, em vez de circular como uma string sem regra. `Dinheiro` guarda centavos inteiros para somar e aplicar descontos sem erros de precisão de ponto flutuante.

## 3. Diga, não pergunte

O pagamento agora é solicitado com `pedido.pagar()`, que retorna se conseguiu pagar; quem usa o pedido não lê nem altera seu status. As regras ficam em `Pedido`, que tem os dados necessários para decidir se está aberto e se possui itens.

## 4. Fail first

O hadouken da validação percorria condições aninhadas para conferir email, CPF e CEP; agora cada tipo rejeita cedo seu próprio valor inválido. Retornos antecipados tratam falhas de pagamento e cancelamento, e tipos polimórficos calculam o desconto sem uma cadeia de alternativas.

## 5. Modularização

`Cpf`: valida e representa o CPF.  
`Email`: valida e representa o email.  
`Cep`: valida e representa o CEP.  
`Dinheiro`: calcula e formata valores monetários em centavos.  
`Status`: controla transições e descreve o estado do pedido.  
`Pessoa`: reúne nome, CPF e email.  
`Endereco`: reúne rua, cidade e CEP.  
`TipoNormal`: calcula desconto de cliente normal.  
`TipoVip`: calcula desconto de cliente VIP.  
`TipoFuncionario`: calcula desconto de funcionário.  
`Cliente`: conecta pessoa, endereço e política de desconto.  
`Produto`: representa nome e preço unitário.  
`ItemDoPedido`: associa um produto à sua quantidade.  
`ItensDoPedido`: adiciona, totaliza e imprime itens.  
`Pedido`: aplica regras de pagamento e apresenta seus dados.  
`Pedidos`: registra pedidos, imprime o relatório e calcula totais.

## 6. Dívida técnica

Não ficou uma regra pendente nem um atalho intencional. A parte mais trabalhosa foi respeitar a Lei de Demeter sem expor atributos: cada objeto passou a imprimir ou executar sua própria parte do relatório.
