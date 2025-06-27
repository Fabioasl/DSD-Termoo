const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const readline = require('readline-sync');
const util = require('util');

const CAMINHO_PROTO = __dirname + '/termoo.proto';

const definicaoPacote = protoLoader.loadSync(
  CAMINHO_PROTO,
  {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  }
);

const termoProto = grpc.loadPackageDefinition(definicaoPacote).termoo;

async function main() {
  const cliente = new termoProto.TermooService('localhost:50051', grpc.credentials.createInsecure());

  // Promisificar os métodos
  const novoJogo = util.promisify(cliente.NovoJogo.bind(cliente));
  const enviarPalpite = util.promisify(cliente.EnviarPalpite.bind(cliente));

  try {
    const resposta = await novoJogo({});
    const jogoId = resposta.jogo_id;
    const tentativasMaximas = resposta.tentativas_maximas;
    const tamanhoPalavra = resposta.tamanho_palavra;
    console.log("para começar digite qualquer palavra com 5 letras.")
    console.log(`Tamanho da palavra: ${tamanhoPalavra}`);
    console.log(`Tentativas máximas: ${tentativasMaximas}`);

    let terminou = false;

    while (!terminou) {
      let palavra = readline.question('Digite sua palavra: ').trim();

      const res = await enviarPalpite({ palavra, jogo_id: jogoId });
      console.log('Resultado:', res.resultados);
      console.log(res.mensagem);

      terminou = res.terminou;
    }

  } catch (erro) {
    console.error('Erro:', erro);
  }
}

main();
