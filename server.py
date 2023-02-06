from datetime import datetime
import aiopg
import asyncio
from gino import Gino
from aiohttp import web
from asyncpg import UniqueViolationError


ADS_DSN = "postgresql://drimtim:302911 @127.0.0.1:5432/db_new"
db = Gino()


class BaseModel:

    @classmethod
    async def get_404(cls, id_):
        response = await cls.get(id_)
        if not response:
            raise web.HTTPNotFound()
        return response

    @classmethod
    async def create_response(cls, **kwargs):
        try:
            response = await cls.create(**kwargs)
            return response
        except UniqueViolationError:
            raise web.HTTPBadRequest()


class AdModel(db.Model, BaseModel):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), primary_key=False)
    description = db.Column(db.String(1000), primary_key=False)
    created_at = db.Column(db.DateTime, primary_key=False)
    owner = db.Column(db.String(200),primary_key=False)

    def to_dict(self):
        advertisements = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at),
            "owner": self.owner
        }
        return advertisements


async def return_all_advertisements():
    get = await AdModel.query.gino.all()
    some_list = []
    for post in get:
        some_list.append({"id": post.id, "title": post.title, "description": post.description,
                          "created_at": post.created_at, "owner": post.owner})
    return some_list


class ServerStatus(web.View):

    async def get(self):
        return web.json_response({'status': 'OK'})


async def register_pg_pool(app):
    print('APP START')
    async with aiopg.create_pool(ADS_DSN) as pool:
        app['pg_pool'] = pool
        yield
        pool.close()
    print('APP FINISH')


async def register_db(app):
    await db.set_bind(ADS_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


class AdModelsView(web.View):

    async def get(self):
        get_all = await return_all_advertisements()
        return web.json_response(get_all)


class AdModelView(web.View):
    async def get(self):
        admodel_id = int(self.request.match_info['admodel_id'])
        admodel = await AdModel.get_404(admodel_id)
        return web.json_response(admodel.to_dict())

    async def post(self):
        admodel_data = await self.request.json()
        if bool("title" and "description" and "owner" not in admodel_data.keys()):
            raise web.HTTPBadRequest()
        new_admodel = await AdModel.create_response(**admodel_data)
        return web.json_response(new_admodel.to_dict())


app = web.Application()
app.add_routes([web.get('/status', ServerStatus)])
app.add_routes([web.get('/admodels', AdModelsView)])
app.add_routes([web.get('/admodel/{admodel_id:\d+}', AdModelView)])
app.add_routes([web.post('/admodel', AdModelView)])
app.cleanup_ctx.append(register_pg_pool)
app.cleanup_ctx.append(register_db)
web.run_app(app, port=7070)
