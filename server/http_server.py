# from simple_http_server import route, server
from flask import Flask
from flask_cors import CORS, cross_origin
import sys
import json
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


app = Flask(__name__)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# def main():
#     @route("/")
#     def index():
#         return {"hello": "world"}   

#     @route("/get_es_health")
#     def index():
#         response = {"hello": "get world"} 
#         logging.info(f"response json : {json.dumps(response, indent=2)}")
#         return response

@app.route('/')
@cross_origin()
def index():
    response = {"hello": "world"}
    logging.info(f"response json : {json.dumps(response, indent=2)}")
    return response


@app.route('/get_es_health')
@cross_origin()
def get_es_health():
    response = {
        "cluster_name": "docker-elasticsearch",
        "status": "yellow",
        "timed_out": False,
        "number_of_nodes": 1,
        "number_of_data_nodes": 1,
        "active_primary_shards": 29,
        "active_shards": 29,
        "relocating_shards": 0,
        "initializing_shards": 0,
        "unassigned_shards": 8,
        "delayed_unassigned_shards": 0,
        "number_of_pending_tasks": 0,
        "number_of_in_flight_fetch": 0,
        "task_max_waiting_in_queue_millis": 0,
        "active_shards_percent_as_number": 78.3783783783784
    }
    logging.info(f"response json : {json.dumps(response, indent=2)}")
    return response


def run_server():
    from waitress import serve
    app.debug = True
    serve(app, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    # app.run()
    run_server()
    # try:
    #     main()
    #     server.start(port=5000)
    # except KeyboardInterrupt:
    #     logging.error(f"Key interrupted")
    #     sys.exit(0)