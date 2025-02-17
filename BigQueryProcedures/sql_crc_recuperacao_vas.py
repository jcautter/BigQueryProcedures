from .proc_log import ProcLog

class SQLCRCRecuperacaoVAS:

    def proc_crc_recuperacao_vas(self):
        self.__delete_cons()
        self.__insert_into_cons()
        
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete dm_prod.tbl_cons_crc_recuperacao_vas'
            , query = """
                delete
                dm_prod.tbl_cons_crc_recuperacao_vas AS cons
                where exists
                (
                    select
                    dt_month_ref
                    from
                    (
                        select distinct
                        DATE(dt_month_ref) as dt_month_ref
                        from
                        dm_temp.tbl_car_crc_recuperacao_vas
                    ) AS car
                    where
                    cons.dt_month_ref = DATE(dt_month_ref)
                );
            """
        )
    
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert into dm_prod.tbl_cons_crc_recuperacao_vas'
            , query = """
                insert into
                dm_prod.tbl_cons_crc_recuperacao_vas
                select
                dt_month_ref
                , dt_ref
                , dt_criacao
                , dt_finalizacao
                , num_protocolo
                , num_fatura
                , num_titular_msidn as num_titular_msisdn
                , struct(
                    str_segmento_contestacao
                    , bit_reincidencia
                    , bit_vas_only
                    , str_m_reincidencia
                ) stc_clasificacao
                , struct(
                    str_contestacao
                    , str_motivo_contestacao
                    , str_motivo_1
                    , str_motivo_2
                    , str_motivo_3
                ) stc_motivo
                , sum(num_valor) as num_valor
                , count(*) as num_qtd
                , array_agg(
                    struct(
                    id
                    , num_appid
                    , str_servico
                    , num_valor
                    )
                ) arr_contestacao
                from
                dm_temp.tbl_car_crc_recuperacao_vas
                group by
                dt_month_ref
                , dt_ref
                , dt_criacao
                , dt_finalizacao
                , num_protocolo
                , num_fatura
                , num_titular_msidn
                , str_segmento_contestacao
                , bit_reincidencia
                , bit_vas_only
                , str_m_reincidencia
                , str_contestacao
                , str_motivo_contestacao
                , str_motivo_1
                , str_motivo_2
                , str_motivo_3
            """
        )
