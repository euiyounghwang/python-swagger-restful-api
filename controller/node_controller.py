from fastapi import APIRouter
import json
import datetime
from injector import (logger,
                      SearchAPIHandlerInject,
                      SearchOmniHandlerInject
                      )
from service.status_handler import (StatusHanlder, StatusException)

app = APIRouter(
    prefix="/node",
)


@app.get("/node_lists", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/node/node_lists?es_url=http://localhost:9200", 
          summary="Return nodes List")
async def node_lists(es_url="http://localhost:9200"):
    response =  await SearchAPIHandlerInject.get_node_lists(es_url)
    if isinstance(response, dict):
        logger.info(f"SearchOmniHandler:index_name_id_search - {json.dumps(response, indent=2)}")
    return response
