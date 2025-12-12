from .proc_log import ProcLog

class SQLRecarga:

    def proc_recarga(self, dt:str):
        print('proc recarga -- Iniciado')
        print('')
        self.__delete_cons(dt)
        self.__insert_into_cons(dt)
        self.__update_plano()
        print('')
        print('proc recarga -- Finalizado')
    
    def __delete_cons(self, dt:str):
        self._ProcLog__exec(
            title = 'delete cons'
            , module = 'recarga'
            , crud = 'delete'
            , name = 'delete cons'
            , parm = {'dt': dt} 
        )

    def __insert_into_cons(self, dt:str):
        self._ProcLog__exec(
            title = 'insert cons'
            , module = 'recarga'
            , crud = 'insert'
            , name = 'insert cons'
            , parm = {'dt': dt} 
        )

    def __update_plano(self):
        self._ProcLog__exec(
            title = 'update cons (plano)'
            , module = 'recarga'
            , crud = 'update'
            , name = 'update cons (plano)'
        )
