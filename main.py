from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from controller import (cluster_controller,
                        index_controller,
                        node_controller,
                        search_controller,
                        )
from config.log_config import create_log

logger = create_log()
app = FastAPI(
    title="ES Cluster API Service",
    description="Elasticsearch Cluster & Elasticsearch API Integration",
    # summary="Elasticsearch Cluster & Elasticsearch API Integration",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "ES Dev Team at GXO",
        "email": "a@xyz.com"
    },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi


''' http://localhost:8001/docs '''

@app.get("/", tags=['API'],  
         status_code=200,
         description="Default GET API", 
         summary="Return Json")
async def root():
    return {"message": "Hello World"}


# @app.get("/test", tags=['API'],  
#          status_code=200,
#          description="Default GET Param API", 
#          summary="Return GET Param Json")
# async def root_with_arg(id):
#     logger.info('root_with_arg - {}'.format(id))
#     return {"message": "Hello World [{}]".format(id)}


# @app.get("/test/{id}", tags=['API'],  
#          status_code=200,
#          description="Default GET with Body API", 
#          summary="Return GET with Body Json")
# async def root_with_param(id):
#     logger.info('root_with_arg - {}'.format(id))
#     return {"message": "Hello World [{}]".format(id)}


# router
app.include_router(search_controller.app, tags=["Search API"], )
app.include_router(cluster_controller.app, tags=["Cluster API"], )
app.include_router(index_controller.app, tags=["Index API"], )
app.include_router(node_controller.app, tags=["Nodes API"], )
