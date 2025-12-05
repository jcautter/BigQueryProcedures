class SQLPrebillingAvulso:

    def proc_prebillAvulso(self, dt_corte:str):
        print('proc prebilling avulso -- Iniciado')
        print('')a
        self.__delete_acum(dt_corte)
        self.__insert_acum(dt_corte)
        self.__insert_acum_supressao()
        self.sub_proc_previa_brebilling()
        print('')
        print('proc prebilling avulso -- Finalizado')

    def __delete_acum(self, dt_corte:str):
        self._ProcLog__exec(
            title = 'delete acum'
            , module = 'prebilling avulso'
            , crud = 'delete'
            , name = 'delete acum'
            , parm = {'dt_corte': dt_corte}
        )

    def __insert_acum(self, dt_corte:str):
        self._ProcLog__exec(
            title = 'insert acum'
            , module = 'prebilling avulso'
            , crud = 'insert'
            , name = 'insert acum'
            , parm = {'dt_corte': dt_corte}
        )

    def __insert_acum_supressao(self):
        self._ProcLog__exec(
            title = 'insert acum supressao'
            , module = 'prebilling avulso'
            , crud = 'insert'
            , name = 'insert acum supressao'
        )

    def sub_proc_previa_brebilling(self):
        print('subproc previa prebilling -- Iniciado')
        self.__create_cons_previa_prebilling()
        self.__update_cons_previa_prebilling_1()
        self.__update_cons_previa_prebilling_2()
        self.__update_cons_previa_prebilling_3()
        self.__update_cons_previa_prebilling_4()
        self.__update_cons_previa_prebilling_5()
        self.__update_cons_previa_prebilling_6()
        self.__update_cons_previa_prebilling_7()
        self.__update_cons_previa_prebilling_8()
        print('subproc previa prebilling -- Finalizado')

    def __create_cons_previa_prebilling(self):
        self._ProcLog__exec(
            title = 'create cons prebilling'
            , module = 'prebilling avulso'
            , crud = 'create'
            , name = 'create cons prebilling'
        )

    def __update_cons_previa_prebilling_1(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 1'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 1'
        )

    def __update_cons_previa_prebilling_2(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 2'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 2'
        )

    def __update_cons_previa_prebilling_3(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 3'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 3'
        )

    def __update_cons_previa_prebilling_4(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 4'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 4'
        )

    def __update_cons_previa_prebilling_5(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 5'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 5'
        )

    def __update_cons_previa_prebilling_6(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 6'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 6'
        )

    def __update_cons_previa_prebilling_7(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 7'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 7'
        )

    def __update_cons_previa_prebilling_8(self):
        self._ProcLog__exec(
            title = 'update cons prebilling 8'
            , module = 'prebilling avulso'
            , crud = 'update'
            , name = 'update cons prebilling 8'
        )
