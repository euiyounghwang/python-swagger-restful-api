from fastapi import APIRouter
import json
import datetime
from injector import logger, SearchOmniHandlerInject, SearchAPIHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
from repository.repository_schema import IndexMapping
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi import BackgroundTasks


app = APIRouter(
    prefix="/index",
)



@app.get("/{index_name}/{id}",
         status_code=StatusHanlder.HTTP_STATUS_200,
         responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
         },
         description="Sample Payload : http://localhost:8001/index/test/inXWho4BwnqgZ-zcD8O-?source_cluster=http://localhost:9200", 
         summary="Return id for index_name")
async def index_name_id_search(index_name="test", id="1", source_cluster="http://localhost:9200"):
    response =  await SearchAPIHandlerInject.get_index_by_id(source_cluster, index_name, id)
    if isinstance(response, dict):
        logger.info(f"SearchOmniHandler:index_name_id_search - {json.dumps(response, indent=2)}")
    return response


@app.get("/index_list", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/index/index_list?source_cluster=http://localhost:9200", 
          summary="Return Index List")
async def index_list(source_cluster="http://localhost:9200"):
    response =  SearchAPIHandlerInject.get_index_lists(source_cluster)
    if isinstance(response, dict):
        logger.info(f"SearchOmniHandler:index_list - {json.dumps(response, indent=2)}")
    return response



@app.get("/mapping", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/index/mapping?index_name=test&source_cluster=http://localhost:9200/", 
          summary="Return Index Mapping")
async def index_mapping(index_name="test", source_cluster="http://localhost:9200"):
    response =  SearchAPIHandlerInject.get_index_mapping(source_cluster, index_name)
    if isinstance(response, dict):
        logger.info(f"SearchOmniHandler:index_mapping - {json.dumps(response, indent=2)}")
    return response



@app.get("/mapping_compare", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/index/mapping_compare?index_name=test&source_cluster=http://localhost:9200&target_cluster=http://localhost:9292", 
          summary="* Return Index Mapping Compare")
async def index_mapping_compare(index_name="test", source_cluster="http://localhost:9200", target_cluster="http://localhost:9200"):
    StartTime, EndTime, Delay_Time = 0, 0, 0
    try:
        StartTime = datetime.datetime.now()
        
        response = SearchAPIHandlerInject.get_index_mapping_compare(index_name, source_cluster, target_cluster)

        if isinstance(response, dict):
            logger.info(f"SearchOmniHandler:index_mapping_compare - {json.dumps(response, indent=2)}")
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        return response
    finally:
        logger.info(f"Delay Time : {Delay_Time}")


@app.get("/all_indices_mapping_compare", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/index/all_indices_mapping_compare?source_cluster=http://localhost:9200&target_cluster=http://localhost:9292", 
          summary="* Return json for all iondex mpping compare")
async def all_index_mapping_compare(source_cluster="http://localhost:9200", target_cluster="http://localhost:9200"):
    StartTime, EndTime, Delay_Time = 0, 0, 0
    try:
        StartTime = datetime.datetime.now()
        
        response = SearchAPIHandlerInject.get_index_all_mapping_compare(source_cluster, target_cluster)

        if isinstance(response, dict):
            logger.info(f"SearchOmniHandler:all_index_mapping_compare - {json.dumps(response, indent=2)}")
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        return response
    finally:
        logger.info(f"Delay Time : {Delay_Time}")



@app.get("/lookup_index_not_mapped_to_aliase", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/index/lookup_index_not_mapped_to_aliase?source_cluster=http://localhost:9200", 
          summary="* Return json for the unmapped to any aliases")
async def lookup_index_not_mapped_to_aliase(source_cluster="http://localhost:9200"):
    StartTime, EndTime, Delay_Time = 0, 0, 0
    try:
        StartTime = datetime.datetime.now()
        
        response = SearchAPIHandlerInject.get_lookup_old_indices_from_aliases(source_cluster)

        if isinstance(response, dict):
            logger.info(f"SearchOmniHandler:lookup_index_not_mapped_to_aliase - {json.dumps(response, indent=2)}")
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        return response
    finally:
        logger.info(f"Delay Time : {Delay_Time}")


"""
@app.get("/mapping_compare_all", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/index/mapping_compare?index_name=test&source_cluster=http://localhost:9200&target_cluster=http://localhost:9292", 
          summary="* Return Source cluster's Indexes Mapping Compare all")
async def index_mapping_compare_all( background_tasks : BackgroundTasks, source_cluster="http://localhost:9200", target_cluster="http://localhost:9200"):
    StartTime, EndTime, Delay_Time = 0, 0, 0
    try:
        StartTime = datetime.datetime.now()

        # response = await SearchOmniHandlerInject.get_index_mapping_compare_all(source_cluster, target_cluster)
        background_tasks.add_task(SearchOmniHandlerInject.get_index_mapping_compare_all, source_cluster, target_cluster)
        
        # if isinstance(response, (list, dict)):
        #     logger.info(f"SearchOmniHandler:index_mapping_compare_all - {json.dumps(response, indent=2)}")
        
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

        # return response
        return {"job" : "created.."}
    finally:
        logger.info(f"Delay Time : {Delay_Time}")
"""

@app.post("/mapping_compare_test", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="* Return Index Mapping Compare", 
          summary="* Return Index Mapping Compare")
async def index_mapping_compare_test(request: IndexMapping):
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        request_json = request.to_json()
        logger.info(request_json) 

        response = await SearchAPIHandlerInject.get_index_mapping_compare_test(request_json['source_mapping'],request_json['target_mapping'])

        if isinstance(response, dict):
            logger.info(f"SearchOmniHandler:index_mapping_compare_test - {json.dumps(response, indent=2)}")
        
        EndTime = datetime.datetime.now()

        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        
        return response
    
    finally:
        # metrics_service.track_performance_metrics(Delay_Time)
        print(Delay_Time)
