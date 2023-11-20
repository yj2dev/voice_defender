from fastapi import APIRouter, Request

router = APIRouter()

#
# @router.get("/", include_in_schema=False)
# async def root():
#     payload = {
#         "/": "root",
#         "method": "GET",
#     }
#     return payload
#
#
# @router.post("/", include_in_schema=False)
# async def root():
#     payload = {
#         "/": "root",
#         "method": "POST",
#     }
#     return payload
#
#
# @router.get("/json-test", include_in_schema=False)
# async def json_test(req: Request):
#     return {"/": await req.json()}
