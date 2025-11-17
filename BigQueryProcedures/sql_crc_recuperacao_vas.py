from .proc_log import ProcLog

class SQLCRCRecuperacaoVAS:

    def proc_crc_recuperacao_vas(self, ano_mes:str):
        print('proc crc vas -- Iniciado')
        print('')
        self.__create_car(ano_mes)
        self.__delete_cons()
        self.__insert_into_cons()
        print('')
        print('proc crc vas -- Finalizado')
        
    def __create_car(self, ano_mes:str):
        self._ProcLog__exec(
            title = 'create car'
            , module = 'crc vas'
            , crud = 'create'
            , name = 'create car'
            , parm = {'ano_mes': ano_mes}
        )
    
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete cons'
            , module = 'crc vas'
            , crud = 'delete'
            , name = 'delete cons'
        )
    
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert cons'
            , module = 'crc vas'
            , crud = 'insert'
            , name = 'insert cons'
        )
