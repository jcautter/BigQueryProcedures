from .proc_log import ProcLog

class SQLItemFatura(ProcLog):
    
    def proc_item_fatura(self, dt:str, dt2:str=None):
        print('proc item fatura -- Iniciado')
        print('')
        self.__truncate_car()
        self.__insert_into_car(dt, dt2)
        self.__delete_cons()
        self.__insert_into_cons()
        self.__update_dt_pagamento()
        print('')
        print('proc item fatura -- Finalizado')
    
    def __truncate_car(self):
        self._ProcLog__exec(
            title = 'truncate car'
            , module = 'item fatura'
            , crud = 'truncate'
            , name = 'truncate car'
        )
        
    def __insert_into_car(self, dt:str, dt2:str=None):
        if not dt2:
            dt2 = dt
        self._ProcLog__exec(
            title = 'insert car'
            , module = 'item fatura'
            , crud = 'insert'
            , name = 'insert car'
            , parm = {'dt': dt, 'dt2': dt2}
        )
        
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete cons'
            , module = 'item fatura'
            , crud = 'delete'
            , name = 'delete cons'
        )
        
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert cons'
            , module = 'item fatura'
            , crud = 'insert'
            , name = 'insert cons'
        )
        
    def __update_dt_pagamento(self):
        self._ProcLog__exec(
            title = 'update cons (pagamento)'
            , module = 'item fatura'
            , crud = 'insert'
            , name = 'insert cons (pagamento)'
        )
