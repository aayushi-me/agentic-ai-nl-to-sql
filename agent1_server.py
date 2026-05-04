import grpc
from concurrent import futures
from dotenv import load_dotenv
import os
import nl2sql_pb2
import nl2sql_pb2_grpc

# Load .env
load_dotenv()

AGENT1_PORT = os.environ.get("AGENT1_PORT", "5001")
AGENT2_ADDRESS = os.environ.get("AGENT2_ADDRESS", "localhost:5002")

# gRPC Servicer for Agent1
class Agent1Servicer(nl2sql_pb2_grpc.NL2SQLAgentServicer):
    def __init__(self):
        # Set up client to Agent2
        self.channel = grpc.insecure_channel(AGENT2_ADDRESS)
        self.stub = nl2sql_pb2_grpc.NL2SQLAgentStub(self.channel)

    def Translate(self, request, context):
        # Forward request to Agent2 and return response
        print(f"[Agent1] gRPC server received request. Forwarding to Agent2...")
        response = self.stub.Translate(request)
        print(f"[Agent1] SQL response from Agent2: {response.sql}")
        return response

    # Internal use for Gradio and CLI
    def nl2sql(self, nl_query, schema):
        request = nl2sql_pb2.NL2SQLRequest(nl_query=nl_query, schema=schema)
        print(f"[Agent1] Sending NL2SQL request to Agent2: {nl_query} | Schema: {schema}")
        try:
            response = self.stub.Translate(request)
            print(f"[Agent1] Received SQL: {response.sql}")
            return response.sql
        except Exception as e:
            print(f"[Agent1] Error communicating with Agent2: {e}")
            return "Error: Unable to contact Agent2."

def serve():
    # Start Agent1 as a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    agent1_servicer = Agent1Servicer()
    nl2sql_pb2_grpc.add_NL2SQLAgentServicer_to_server(agent1_servicer, server)
    server.add_insecure_port(f'[::]:{AGENT1_PORT}')
    print(f"Agent1 gRPC server running on port {AGENT1_PORT}, connecting to Agent2 at {AGENT2_ADDRESS}")
    server.start()
    return agent1_servicer, server

# For Gradio UI
def agent1_nl2sql(nl_query, schema):
    # create a new servicer (client) for every call
    agent1 = Agent1Servicer()
    return agent1.nl2sql(nl_query, schema)

if __name__ == "__main__":
    agent1_servicer, server = serve()
    try:
        while True:
            inp = input("Enter NLQ (blank to exit): ").strip()
            if not inp:
                break
            schema = input("Enter schema: ").strip()
            sql = agent1_servicer.nl2sql(inp, schema)
            print("SQL:", sql)
    except KeyboardInterrupt:
        print("\nShutting down Agent1 server.")
        server.stop(0)
