from .proc_log import ProcLog

class SQLEconomicResult:

    def proc_economic_resut(self, dt_ini:str, dt_fim:str=None):
        if not dt_fim:
            dt_fim = dt_ini
        print('proc economic result -- Iniciado')
        print('')
        self.__create_view()
        self.__execute(dt_ini, dt_fim)
        self.__drop_view()
        print('')
        print('proc economic result -- Finalizado')
    
    def __create_view(self):
        self._ProcLog__exec(
            title = 'create view'
            , module = 'economic result'
            , crud = 'create'
            , name = 'create view' 
        )

    def __execute(self, dt_ini:str, dt_fim:str=None):
        if not dt_fim:
            dt_fim = dt_ini
        self._ProcLog__exec(
            title = 'execute'
            , module = 'economic result'
            , crud = 'execute'
            , name = 'execute'
            , parm = {'data_ini': dt_ini, 'data_fim': dt_fim} 
        )

    def __drop_view(self):
        self._ProcLog__exec(
            title = 'drop view'
            , module = 'economic result'
            , crud = 'drop'
            , name = 'drop view' 
        )
