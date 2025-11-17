from .proc_log import ProcLog

class SQLFullBaseFatura(ProcLog):
    
    def proc_full_base_fatura(self, dt:str):
        print('proc full base fatura -- Iniciado')
        print('')

        self.__create_view()
        self.__create_data_temp(dt)
        self.__create_car()
        self.__delete_acum()
        self.__insert_acum()
        self.__drop_view()

        print('')
        print('proc full base fatura -- Finalizado')

    def __create_view(self):
        self._ProcLog__exec(
            title = 'create view'
            , module = 'base full fatura'
            , crud = 'create'
            , name = 'create view'
        )

    def __create_data_temp(self, dt:str):
        self._ProcLog__exec(
            title = 'create data temp'
            , module = 'base full fatura'
            , crud = 'create'
            , name = 'create data temp'
            , parm = {'dt': dt}
        )

    def __create_car(self):
        self._ProcLog__exec(
            title = 'create car'
            , module = 'base full fatura'
            , crud = 'create'
            , name = 'create car'
        )

    def __delete_acum(self):
        self._ProcLog__exec(
            title = 'delete acum'
            , module = 'base full fatura'
            , crud = 'delete'
            , name = 'delete acum'
        )

    def __insert_acum(self):
        self._ProcLog__exec(
            title = 'insert acum'
            , module = 'base full fatura'
            , crud = 'insert'
            , name = 'insert acum'
        )

    def __drop_view(self):
        self._ProcLog__exec(
            title = 'drop view'
            , module = 'base full fatura'
            , crud = 'drop'
            , name = 'drop view'
        )
