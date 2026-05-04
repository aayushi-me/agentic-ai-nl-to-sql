import grpc
from concurrent import futures
import os
import openai
from dotenv import load_dotenv

import nl2sql_pb2
import nl2sql_pb2_grpc

# Load .env
load_dotenv()
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

AGENT2_PORT = os.environ.get("AGENT2_PORT", "5002")

class NL2SQLServicer(nl2sql_pb2_grpc.NL2SQLAgentServicer):
    def Translate(self, request, context):
        schema = request.schema
        nl_query = request.nl_query
        prompt = f"Convert the following natural language question to SQL using the schema provided.\n\nSchema:\n{schema}\nQuestion:\n{nl_query}\nSQL:"
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert SQL generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            sql = response.choices[0].message.content.strip()
            print(f"[Agent2] Translated: {sql}")
            return nl2sql_pb2.NL2SQLResponse(sql=sql)
        except Exception as e:
            print(f"[Agent2] Error: {e}")
            return nl2sql_pb2.NL2SQLResponse(sql=f"Error: {str(e)}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    nl2sql_pb2_grpc.add_NL2SQLAgentServicer_to_server(NL2SQLServicer(), server)
    server.add_insecure_port(f'[::]:{AGENT2_PORT}')
    print(f"Agent2 (SQLAgent) running and listening on port {AGENT2_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
