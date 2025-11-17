from .proc_log import ProcLog

class SQLItemFaturaTrafegoDetalhado:

    def proc_item_fatura_trafego_detalhado(self, dt:str, dt2:str=None):
        print('proc item fatura detalhado -- Iniciado')
        print('')
        self.__truncate_car()
        self.__insert_into_car(dt, dt2)
        self.__delete_cons()
        self.__insert_into_cons()
        self.__update_charging_id()
        self.__update_app_id()
        self.__insert_dpa_servico()
        self.__insert_dpa_plano()
        self.__update_bit_pagamento()
        print('')
        print('proc item fatura detalhado -- Finalizado')
        
    def __truncate_car(self):
        self._ProcLog__exec(
            title = 'truncate car'
            , module = 'item fatura trafego detalhado'
            , crud = 'truncate'
            , name = 'truncate car'   
        )
    
    def __insert_into_car(self, dt:str, dt2:str=None):
        if not dt2:
            dt2 = dt
        self._ProcLog__exec(
            title = 'insert car'
            , module = 'item fatura trafego detalhado'
            , crud = 'insert'
            , name = 'insert car'
            , parm = {'dt': dt, 'dt2': dt2}
        )
    
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete cons'
            , module = 'item fatura trafego detalhado'
            , crud = 'delete'
            , name = 'delete cons'
        )
        
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert cons'
            , module = 'item fatura trafego detalhado'
            , crud = 'insert'
            , name = 'insert cons'
        )
        
    def __update_charging_id(self):
        self._ProcLog__exec(
            title = 'update cons (charging_id)'
            , module = 'item fatura trafego detalhado'
            , crud = 'update'
            , name = 'update cons (charging_id)'
        )
        
    def __update_app_id(self):
        self._ProcLog__exec(
            title = 'update cons (num_app_id)'
            , module = 'item fatura trafego detalhado'
            , crud = 'update'
            , name = 'update cons (num_app_id)'
        )
        
    def __insert_dpa_servico(self):
        self._ProcLog__exec(
            title = 'insert dpa (servico)'
            , module = 'item fatura trafego detalhado'
            , crud = 'insert'
            , name = 'insert dpa (servico)'
        )
        
    def __insert_dpa_plano(self):
        self._ProcLog__exec(
            title = 'insert dpa (plano)'
            , module = 'item fatura trafego detalhado'
            , crud = 'insert'
            , name = 'insert dpa (plano)'
        )
        
    def __update_bit_pagamento(self):
        self._ProcLog__exec(
            title = 'update cons (pagamento)'
            , module = 'item fatura trafego detalhado'
            , crud = 'update'
            , name = 'update cons (pagamento)'
        )
