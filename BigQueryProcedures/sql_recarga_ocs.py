from proc_log import ProcLog

class SQLRecargaOCS:
    
    def proc_recarga_ocs(self):
        self.__truncate_car()
        self.__insert_into_car()
        self.__delete_cons()
        self.__insert_into_cons()
        self.__update_charging_id()
        self.__update_cons_plano()
        self.__insert_dpa_plano()
    
    def __truncate_car(self):
        self._ProcLog__exec(
            title = 'truncate table tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_ocs'
            , query = 'truncate table tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_ocs;'    
        )
        
    def __insert_into_car(self):
        self._ProcLog__exec(
            title = 'insert into tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_ocs'
            , query = """
                insert into tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_ocs
                select
                charging_party_number
                , cast(service_provider_id as int) as service_provider_id
                , cast(application_id as int) as application_id
                , cast(dat_ref as date) as dat_ref
                , dsc_plano_tarifario
                , dsc_oferta
                , dsc_servico_vas
                , debit_amount
                , rowid
                , tpo_interf_origem
                from
                tim-bigdata-prod-e305.sdx_mktvas.vw_f_ocs_traftar_vas
                where
                dat_ref > (
                    select
                    DATE_ADD(max(dt_ref), INTERVAL -7 day) as dt_ref
                    from
                    tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs
                );
            """
        )
        
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete dm_prod.tbl_cons_ocs'
            , query = """
                delete
                dm_prod.tbl_cons_ocs as cons
                where
                cons.dt_ref in (
                    select
                    dt_ref
                    from
                    (
                        select distinct
                        date(dat_ref) as dt_ref
                        from
                        dm_temp.tbl_car_ocs
                    ) as car
                );
            """
        )
        
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert into tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs'
            , query = """
                insert into tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs
                select
                date_add(dat_ref, interval -(cast(extract(day from dat_ref) as int)-1) day) as dt_month_ref
                , dat_ref as dt_ref
                , dsc_oferta as str_oferta
                , dsc_plano_tarifario as str_plano_detalhado
                , cast(null as string) as str_plano_uf
                , cast(null as float64) as num_plano_geracao
                , cast(null as string) as str_plano
                , service_provider_id as num_csp_id
                , application_id as num_app_id
                , dsc_servico_vas as str_servico_vas
                , cast(charging_party_number as int) as num_msisdn
                , debit_amount as num_valor
                , rowid as num_id
                , cast(null as string) as str_charging_id
                from
                tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_ocs;
            """
        )
    
    def __update_charging_id(self):
        self._ProcLog__exec(
            title = 'update tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs (charging_id)'
            , query = """
                update
                tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs as cons
                set
                str_charging_id = tb_charging.str_charging_id
                from
                (
                    with
                    tb_ocs as (
                        select
                        num_id
                        , cast('55' || cast(cast(num_msisdn as int) as string) as float64) as num_msisdn
                        , dt_ref
                        , num_app_id
                        , num_valor
                        from
                        tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs
                        where
                        str_charging_id is null
                    )
                    , tb_hub as (
                        select
                        ocs.num_msisdn
                        , ocs.dt_ref
                        , ocs.num_app_id
                        , ocs.num_valor
                        , ocs.num_id
                        , hub.str_charging_id
                        from
                        tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_hub_tarifacao as hub
                        inner join
                        tb_ocs as ocs
                        on
                            hub.num_msisdn = ocs.num_msisdn
                            and cast(hub.dt_ref as date) = ocs.dt_ref
                            and hub.num_app_id = ocs.num_app_id
                    )
                    select
                        tb_hub.num_id
                        , max(tb_hub.str_charging_id) as str_charging_id
                    from
                        tb_hub
                    group by
                        tb_hub.num_id
                ) as tb_charging
                where
                cons.num_id = tb_charging.num_id
            """
        )
    
    def __update_cons_plano(self):
        self._ProcLog__exec(
            title = 'update tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs (plano)'
            , query = """
                UPDATE
                tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs as upd
                set
                str_plano = replace(tb_plano.str_plano, 'PLANO ', '')
                , num_plano_geracao = tb_plano.num_plano_geracao
                , str_plano_uf = tb_plano.str_plano_uf
                from
                (
                    WITH
                    TB_PLANO_1 AS (
                    SELECT DISTINCT
                        str_plano_detalhado AS str_plano_detalhado
                        , CASE
                        WHEN str_plano_detalhado LIKE '% __-G__' THEN LEFT(str_plano_detalhado, LENGTH(str_plano_detalhado)-7)
                        WHEN str_plano_detalhado LIKE '%-G__' THEN LEFT(str_plano_detalhado, LENGTH(str_plano_detalhado)-4)
                        WHEN str_plano_detalhado LIKE '% - G__' THEN LEFT(str_plano_detalhado, LENGTH(str_plano_detalhado)-6)
                        WHEN str_plano_detalhado LIKE '%-__' THEN LEFT(str_plano_detalhado, LENGTH(str_plano_detalhado)-3)
                        WHEN str_plano_detalhado LIKE '% - __' THEN LEFT(str_plano_detalhado, LENGTH(str_plano_detalhado)-5)
                        ELSE str_plano_detalhado
                        END str_plano_reduzido
                        , CASE
                        WHEN str_plano_detalhado LIKE ANY ('% __-G__', '%-G__', '% - G__', '%-__', '% - __') THEN RIGHT(str_plano_detalhado,2)
                        ELSE NULL
                        END AS str_plano_uf
                    FROM
                        tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs
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
                    SELECT DISTINCT
                    TB_PLANO_2.str_plano
                    , CONS.str_plano_detalhado
                    , TB_PLANO_2.num_plano_geracao
                    , TB_PLANO_2.str_plano_uf
                    FROM
                    tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs AS CONS
                    INNER JOIN
                    TB_PLANO_2
                    ON
                        CONS.str_plano_detalhado = TB_PLANO_2.str_plano_detalhado
                ) as tb_plano
                where
                upd.str_plano_detalhado = tb_plano.str_plano_detalhado;
            """
        )
    
    def __insert_dpa_plano(self):
        self._ProcLog__exec(
            title = 'insert into dm_prod.tbl_dpa_plano'
            , query = """
                insert into
                dm_prod.tbl_dpa_plano
                (str_plano)
                select distinct
                cons.str_plano
                from
                tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_ocs as cons
                left join
                dm_prod.tbl_dpa_plano as dpa
                on
                    cons.str_plano = dpa.str_plano
                where
                dpa.str_plano is null;
            """
        )
