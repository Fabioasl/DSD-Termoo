# DSD-Termoo

## Descrição

Projeto desenvolvido para a disciplina de **Desenvolvimento de Sistemas Distribuídos**, com foco na implementação de um jogo chamado **"Termo"** — semelhante ao popular Wordle.  
O objetivo do jogo é adivinhar uma palavra de 5 letras em até 5 tentativas.

### Tecnologias utilizadas

- **gRPC** para comunicação entre cliente e servidor  
- **Python** para o servidor (lógica do jogo)  
- **Node.js** como cliente (interface/interação com o usuário)

---

## Instalação

Para que a aplicação funcione corretamente, instale os seguintes pacotes: 

```bash
pip install grpcio
pip install grpcio-tools
npm install @grpc/grpc-js @grpc/proto-loader grpc-tools
```

## Como rodar a aplicação?
Primeiro é necessário que o servidor esteja executando para fazer isso é necessário executar o seguinte comando:
```bash
python servidor.py
Servidor gRPC rodando na porta 50051...
```
se a mensagem "Servidor gRPC rodando na porta 50051..." for exibida é porque deu tudo certo e o servidor está rodando. Após clonar o repositório e o servidor rodando você deve entrar na pasta termoo e executar o seguinte comando:
```bash
node cliente.js
```
após esse comando basta jogar o jogo!