import sqlite3

class IterableProducto(type):
    def __iter__(cls):
        return iter(cls.__name__)


class Producto(object):
    __metaclass__ = IterableProducto
    def __init__(self, codigo:str = None, nombre: str= None, descripcion: str= None, precio: float= None, stock: int= None, categoria: int= None, tienda:str= None):
        self.codigo       = codigo
        self.nombre       = nombre
        self.descripcion  = descripcion
        self.precio       = precio
        self.stock        = stock
        self.categoria    = categoria
        self.tienda       = tienda

    ## GETTER ##
    @property
    def codigo(self) -> str:
        return self.__codigo
    @codigo.setter
    def codigo(self, new_value):
        self.__codigo = new_value
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self, new_value):
        self.__nombre = new_value

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, new_value):
        self.__descripcion = new_value

    @property
    def precio(self):
        return self.__precio
    @precio.setter
    def precio(self, new_value):
        self.__precio = new_value

    @property
    def stock(self):
        return self.__stock
    @stock.setter
    def stock(self, new_value):
        self.__stock = new_value

    @property
    def categoria(self):
        return self.__categoria
    @categoria.setter
    def categoria(self, new_value):
        self.__categoria = new_value

    @property
    def tienda(self):
        return self.__tienda
    @tienda.setter
    def tienda(self, new_value):
        self.__tienda = new_value


    ## GENERERAR CODIGO DE PRODUCTO
    def generarCodigo(self) -> str:
        count = 0
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM producto'''
            cursor.execute(query)
            count = cursor.fetchone()
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return "PROD" + "0" * (4 - len(str(count[0] + 1))) + str(count[0] + 1)

    ## AGREGAR NUEVO PRODUCTO
    def agregar_producto(self) -> bool:
        estado_op = False
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    INSERT INTO producto(codigo, nombre, descripcion, precio, stock, categoria, tienda)
                    VALUES ('{}', '{}', '{}', {}, {}, {}, '{}')
                    '''.format(self.generarCodigo(), self.__nombre, self.__descripcion,
                            self.__precio, self.__stock, self.__categoria, self.__tienda)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    ## OBTENER TODOS LOS PRODUCTOS
    def obtenerProductos(self):
        list_product = None
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT * FROM producto
            '''
            cursor.execute(query)  # EJECUTA LA OPERACION
            list_product = cursor.fetchall()
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            raise e
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return list_product

    ## OBTENER UN SOLO PRODUCTO POR CODIGO
    def obtenerProducto(self, codigo:str):
        list_product = None
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM producto
                WHERE codigo = '{}'
                '''.format(codigo)

            cursor.execute(query)  # EJECUTA LA OPERACION
            list_product = cursor.fetchone()
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            raise e
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return list_product

    ## ACTUALIZAR UN PRODUCTO
    def actualizar_dato(self) -> bool:
        estado_ope: bool = False
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS

        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            UPDATE producto
            SET descripcion = '{}', precio = {}, stock = {}
            WHERE codigo = '{}'
            '''.format(self.__descripcion, self.__precio, self.__stock, self.__codigo)
            cursor.execute(query)  # EJECUTA LA OPERACION
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_ope = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            raise e
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
        return estado_ope
    
    ## BUSCADOR POR NOMBRE
    def buscarProductoCategoria(self, id_Prod:int):
        lista_productos = None
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    SELECT *
                    FROM producto
                    WHERE categoria = {}
                    '''.format(id_Prod)
            cursor.execute(query)
            lista_productos = cursor.fetchall()
            return lista_productos
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            return lista_productos


    ## BUSCADOR POR NOMBRE
    def buscarProducto(self, nombre:str):
        lista_productos = None
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                    SELECT *
                    FROM producto
                    WHERE nombre LIKE '%{}%'
                    '''.format(nombre)
            cursor.execute(query)
            lista_productos = cursor.fetchall()
            return lista_productos
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

    ## ACTUALIZAR STOCK DE UN PRODUCTO
    def actualizarProductoStock(self, id_prod:str) -> bool:
        estado = False
        database = sqlite3.connect("data/linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                UPDATE producto SET stock=stock-1 
                WHERE codigo='{}' '''.format(id_prod)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado = True
            return estado
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

    