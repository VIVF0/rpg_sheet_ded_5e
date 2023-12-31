import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from dotenv import load_dotenv
import os
import psycopg_pool
import psycopg2.pool

load_dotenv()

class Db:
    def __init__(self):
        self.host = os.getenv('HOST')
        self.database = os.getenv('DATABASE')
        self.port = os.getenv('PORT')
        self.user_db = os.getenv('USER')
        self.password_db = os.getenv('PASSWORD')
        self.pool = None
            
    async def connection_db(self):
        conninfo = f'host={self.host} dbname={self.database} port={self.port} user={self.user_db} password={self.password_db}'
        self.pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
        await self.pool.open()
        await self.pool.wait()
        
    async def select(self, query, parameters = (), all=True):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    result = await cursor.fetchall() if all is True else await cursor.fetchone()
                    return result
        except Exception as e:
            print(e)
            return None
        finally:
            await self.pool.close()
    
    async def insert(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    result = await cursor.fetchone()
                    return result[0]
        except Exception as e:
            print(e)
            return None
        finally:
            await self.pool.close()
            
    async def update(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            await self.pool.close()
            
    async def delete(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            await self.pool.close()
    
    async def exists(self, query, parameters):
        try:
            async with self.pool.connection() as conn:
                await conn.set_autocommit(True)
                async with conn.cursor() as cursor:
                    await cursor.execute(query, parameters)
                    result = await cursor.fetchone()
                    if result[0] == 1:
                        return True
        except Exception as e:
            print(e)
            return False
        finally:
            await self.pool.close()
    
    def sync_connection_db(self):
        conninfo = f'host={self.host} dbname={self.database} port={self.port} user={self.user_db} password={self.password_db}'
        self.pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=5, dsn=conninfo)

    def sync_select(self, query, parameters=(), all=True):
        connection = None
        try:
            connection = self.pool.getconn()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
                result = cursor.fetchall() if all else cursor.fetchone()
                return result
        except Exception as e:
            print(e)
            return None
        finally:
            if connection:
                self.pool.putconn(connection)

    def sync_insert(self, query, parameters):
        connection = None
        try:
            connection = self.pool.getconn()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            print(e)
            return None
        finally:
            if connection:
                self.pool.putconn(connection)

    def sync_update(self, query, parameters):
        connection = None
        try:
            connection = self.pool.getconn()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            if connection:
                self.pool.putconn(connection)

    def sync_delete(self, query, parameters):
        connection = None
        try:
            connection = self.pool.getconn()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            if connection:
                self.pool.putconn(connection)

    def sync_exists(self, query, parameters):
        connection = None
        try:
            connection = self.pool.getconn()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
                result = cursor.fetchone()
                if result and result[0] == 1:
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            if connection:
                self.pool.putconn(connection)

        