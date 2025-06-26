import grpc
from concurrent import futures
import time
import uuid
import termoo_pb2
import termoo_pb2_grpc
import random

PALAVRAS = ["carro", "festa", "garfo", "porta", "aureo", "teste", "testa", "corpo", "focos", "termo" ]


class TermooServicer(termoo_pb2_grpc.TermooServiceServicer):
    def __init__(self):
        self.jogos = {}

    def NovoJogo(self, request, context):
        palavra = random.choice(PALAVRAS)
        resposta_do_jogo = palavra
        jogo_id = str(uuid.uuid4())
        self.jogos[jogo_id] = {
            "palavra": palavra,
            "tentativas": 0,
            "tentativas_maximas": 5,
            "terminou": False
        }
        return termoo_pb2.NovoJogoResponse(
            jogo_id=jogo_id,
            tentativas_maximas=5,
            tamanho_palavra=len(palavra)
        )

    def EnviarPalpite(self, request, context):
        jogo = self.jogos.get(request.jogo_id)
        if not jogo or jogo["terminou"]:
            return termoo_pb2.PalpiteResponse(
                resultados=[],
                venceu=False,
                terminou=True,
                mensagem="Jogo inválido ou já finalizado"
            )

        palpite = request.palavra.lower()
        alvo = jogo["palavra"]

        if len(palpite) != len(alvo):
            return termoo_pb2.PalpiteResponse(
                resultados=[],
                venceu=False,
                terminou=False,
                mensagem="Palavra com tamanho incorreto"
            )

        jogo["tentativas"] += 1

        resultados = []
        for i in range(len(palpite)):
            if palpite[i] == alvo[i]:
                resultados.append("correto")
            elif palpite[i] in alvo:
                resultados.append("posicao_errada")
            else:
                resultados.append("errado")

        venceu = palpite == alvo
        terminou = venceu or (jogo["tentativas"] >= jogo["tentativas_maximas"])
        jogo["terminou"] = terminou
        
        if venceu:
            mensagem = f"Você venceu! com um total de {jogo["tentativas"] } tentativas."
        elif terminou:
            mensagem = f"Fim de jogo! a resposta era {alvo}."
        else:
            mensagem = "Tente novamente!"

        return termoo_pb2.PalpiteResponse(
            resultados=resultados,
            venceu=venceu,
            terminou=terminou,
            mensagem=mensagem
        )


def servir():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    termoo_pb2_grpc.add_TermooServiceServicer_to_server(TermooServicer(), servidor)
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    print("Servidor gRPC rodando na porta 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        servidor.stop(0)


if __name__ == '__main__':
    servir()
