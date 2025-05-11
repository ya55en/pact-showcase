import os
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from tortoise.exceptions import DoesNotExist as ModelDoesNotExist

from todoapp import db, get_logger
from todoapp.orm import TodoItem, TodoGroup

logger = get_logger(__name__)


def create_app() -> Starlette:
    routes = [
      Route('/todos', get_todos, methods=['GET']),
      Route('/todos/{id:int}', get_todo, methods=['GET']),
      Route('/groups', get_groups, methods=['GET']),
      Route('/groups/{id:int}', get_group, methods=['GET']),
    ]

    return Starlette(
        debug=True,
        routes=routes,
        lifespan=lifespan,
        exception_handlers=exception_handlers,
    )


async def get_todos(request):
    todos = await TodoItem.all().values()

    return JSONResponse(todos)


async def get_todo(request):
    todo_id = request.path_params['id']
    todo = await TodoItem.get(id=todo_id)

    if not todo:
        return JSONResponse({'error': 'Todo not found'}, status_code=404)

    return JSONResponse(await todo.as_dict())


async def get_groups(request):
  todo_groups = await TodoGroup.all().values()

  return JSONResponse(todo_groups)


async def get_group(request):
  group_id = request.path_params['id']
  todo_group = await TodoGroup.get(id=group_id)

  if not todo_group:
    return JSONResponse({'error': 'TodoGroup not found'}, status_code=404)

  return JSONResponse(todo_group.as_dict(with_comment=True))


@asynccontextmanager
async def lifespan(app):
    await db.init(db_url=os.getenv('TODOAPP_DB_URL', 'sqlite://:memory:'), seed_db=True)
    logger.info('Database initialized')

    yield

    await db.close()
    logger.info('Database closed')


async def http_exception(request: Request, exc: HTTPException):
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)


exception_handlers = {
    HTTPException: http_exception,
    ModelDoesNotExist: lambda request, err: JSONResponse({'detail': str(err)}, status_code=404),

    Exception: lambda request, err: JSONResponse(
       {'detail': "Internal server error"}, status_code=500,
    ),
}
