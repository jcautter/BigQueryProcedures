from .proc_log import ProcLog

class SQLItemFatura(ProcLog):
    
    def proc_item_fatura(self, dt:str, dt2:str=None):
        print('proc_item_fatura -- Iniciado')
        print('')
        self.__truncate_car()
        self.__insert_into_car(dt, dt2)
        self.__delete_cons()
        self.__insert_into_cons()
        self.__update_dt_pagamento()
        print('')
        print('proc_item_fatura -- Finalizado')
    
    def __truncate_car(self):
        self._ProcLog__exec(
            title = 'truncate table dm_temp.tbl_car_item_fatura'
            , query = 'truncate table dm_temp.tbl_car_item_fatura;'    
        )
        
    def __insert_into_car(self, dt:str, dt2:str=None):
        if not dt2:
            dt2 = dt
        self._ProcLog__exec(
            title = 'insert into dm_temp.tbl_car_item_fatura'
            , query = """
            insert into dm_temp.tbl_car_item_fatura
            select
            -- nivel fatura
            parse_date('%Y%m%d',  num_ano_mes_referencia || '01') as dt_month_ref
            , num_cep_envio_fat as num_cep
            , dat_criacao_cliente_rp as dt_criacao_cliente_rp
            , cod_customer_id_rp as num_customer_id_rp
            , dsc_plano as str_dsc_plano
            , dat_corte_fatura as dt_corte
            , dat_vencimento_fatura as dt_vencimento
            , dat_emissao as dt_emissao
            , num_fatura
            , flg_debito_automatico = 'S' as bit_debito_automatico
            , cast(null as date) as dt_pagamento
            -- nivel cliente
            , cod_contrato as num_cod_contrato
            , num_telefone as num_msisdn
            -- nivel servico
            , cod_servico as num_cod_servico
            , nom_servico as str_nome_servico
            , dsc_item_original as str_item_original
            , dsc_item_tratado as str_item_tratado
            , cast(vlr_fator_prorata_mens as float64) as num_prorata
            , qtd_itens as num_qtd
            , vlr_bruto_sem_desconto as num_bruto_sem_desconto
            , vlr_bruto as num_bruto
            , conta_contabil_receita as str_conta_contabil
            from
            tim-bigdata-prod-e305.sdx_mktvas.vw_f_fat_item_fatura
            where
            dat_corte_fatura between '{dt}' and '{dt2}';
            """.format(dt=dt, dt2=dt2)
        )
        
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete dm_prod.tbl_cons_item_fatura'
            , query = """
                delete
                    dm_prod.tbl_cons_item_fatura AS cons
                where exists
                    (
                    select
                        dt_corte
                    from
                        (
                        select distinct
                            dt_corte
                        from
                            dm_temp.tbl_car_item_fatura
                        ) as car
                    where
                        cons.dt_corte = car.dt_corte
                    );
            """
        )
        
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert into dm_prod.tbl_cons_item_fatura'
            , query = """
                INSERT INTO
                tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_item_fatura
                WITH
                TB_PLANO_1 AS (
                SELECT DISTINCT
                    str_dsc_plano AS str_plano_detalhado
                    , CASE
                    WHEN str_dsc_plano LIKE '% __-G__' THEN LEFT(str_dsc_plano, LENGTH(str_dsc_plano)-7)
                    WHEN str_dsc_plano LIKE '%-G__' THEN LEFT(str_dsc_plano, LENGTH(str_dsc_plano)-4)
                    WHEN str_dsc_plano LIKE '% - G__' THEN LEFT(str_dsc_plano, LENGTH(str_dsc_plano)-6)
                    WHEN str_dsc_plano LIKE '%-__' THEN LEFT(str_dsc_plano, LENGTH(str_dsc_plano)-3)
                    WHEN str_dsc_plano LIKE '% - __' THEN LEFT(str_dsc_plano, LENGTH(str_dsc_plano)-5)
                    ELSE str_dsc_plano
                    END str_plano_reduzido
                    , CASE
                    WHEN str_dsc_plano LIKE ANY ('% __-G__', '%-G__', '% - G__', '%-__', '% - __') THEN RIGHT(str_dsc_plano,2)
                    ELSE NULL
                    END AS str_plano_uf
                FROM
                    tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_item_fatura
                )
                , TB_PLANO_2 AS (
                SELECT
                    CASE
                    WHEN REGEXP_CONTAINS(str_plano_reduzido,'. [0-9] [0-9]')
                        THEN LEFT(str_plano_reduzido, LENGTH(str_plano_reduzido)-4)
                    WHEN REGEXP_CONTAINS(str_plano_reduzido,'. [0-9] [0-9] ')
                        THEN LEFT(str_plano_reduzido, LENGTH(str_plano_reduzido)-5)
                    ELSE
                        str_plano_reduzido
                    END AS str_plano
                    , str_plano_detalhado
                    , CASE
                    WHEN REGEXP_CONTAINS(str_plano_reduzido,'. [0-9] [0-9]')
                        THEN CAST(REPLACE(RIGHT(str_plano_reduzido, 4), ' ', '') AS FLOAT64)/10
                    WHEN REGEXP_CONTAINS(str_plano_reduzido,'. [0-9] [0-9] ')
                        THEN CAST(REPLACE(RIGHT(str_plano_reduzido, 5), ' ', '') AS FLOAT64)/10
                    ELSE
                        NULL
                    END AS num_plano_geracao
                    , str_plano_uf
                FROM
                    TB_PLANO_1
                )
                SELECT
                GENERATE_UUID() AS id
                , dt_month_ref
                , num_cep
                , dt_criacao_cliente_rp
                , num_customer_id_rp
                , TB_PLANO_2.str_plano
                , CAR.str_dsc_plano AS str_plano_detalhado
                , TB_PLANO_2.num_plano_geracao
                , TB_PLANO_2.str_plano_uf
                , dt_corte
                , dt_vencimento
                , dt_emissao
                , num_fatura
                , bit_debito_automatico
                , dt_pagamento
                , num_cod_contrato
                , num_msisdn
                , num_cod_servico
                , str_nome_servico
                , str_item_original
                , str_item_tratado
                , num_prorata
                , num_qtd
                , num_bruto_sem_desconto
                , num_bruto
                , str_conta_contabil
                FROM
                tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_item_fatura AS CAR
                INNER JOIN
                TB_PLANO_2
                ON
                    CAR.str_dsc_plano = TB_PLANO_2.str_plano_detalhado;
            """
        )
        
    def __update_dt_pagamento(self):
        self._ProcLog__exec(
            title = 'update dm_prod.tbl_cons_item_fatura (pagamento)'
            , query = """
                update
                dm_prod.tbl_cons_item_fatura as fat
                set
                dt_pagamento = pag.dat_referencia
                from
                (
                    with
                    tb_fat as (
                        select distinct
                        num_fatura
                        from
                        dm_prod.tbl_cons_item_fatura
                        where
                        dt_pagamento is null
                    )
                    select distinct
                    tb_fat.num_fatura
                    , max(tb_pag.dat_referencia) as dat_referencia
                    from
                    tb_fat
                    inner join
                    tim-bigdata-prod-e305.sdx_mktvas.vw_rel_pgto_detalhado as tb_pag
                    on
                        tb_fat.num_fatura = tb_pag.num_fatura
                    group by
                    tb_fat.num_fatura
                ) as pag
                where
                fat.num_fatura = pag.num_fatura;
            """
        )
