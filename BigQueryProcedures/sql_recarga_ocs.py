from .proc_log import ProcLog

class SQLRecargaOCS:

    def proc_recarga_ocs(self):
        print('proc ocs -- Iniciado')
        print('')
        self.__truncate_car()
        self.__insert_into_car()
        self.__delete_cons()
        self.__insert_into_cons()
        self.__update_charging_id()
        self.__update_cons_plano()
        self.__insert_dpa_plano()
        print('')
        print('proc ocs -- Finalizado')
    
    def __truncate_car(self):
        self._ProcLog__exec(
            title = 'truncate car'
            , module = 'ocs'
            , crud = 'truncate'
            , name = 'truncate car'   
        )
        
    def __insert_into_car(self):
        self._ProcLog__exec(
            title = 'insert car'
            , module = 'ocs'
            , crud = 'insert'
            , name = 'insert car'
        )
        
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete cons'
            , module = 'ocs'
            , crud = 'delete'
            , name = 'delete cons'
        )
        
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert cons'
            , module = 'ocs'
            , crud = 'insert'
            , name = 'insert cons'
        )
    
    def __update_charging_id(self):
        self._ProcLog__exec(
            title = 'update cons (charging_id)'
            , module = 'ocs'
            , crud = 'update'
            , name = 'update cons (charging_id)'
        )
    
    def __update_cons_plano(self):
        self._ProcLog__exec(
            title = 'update cons (plano)'
            , module = 'ocs'
            , crud = 'update'
            , name = 'update cons (plano)'
        )
    
    def __insert_dpa_plano(self):
        self._ProcLog__exec(
            title = 'insert dpa (plano)'
            , module = 'ocs'
            , crud = 'insert'
            , name = 'insert dpa (plano)'
        )
