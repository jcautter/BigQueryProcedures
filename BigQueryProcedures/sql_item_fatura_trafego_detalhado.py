from .proc_log import ProcLog

class SQLItemFaturaTrafegoDetalhado:

    def proc_item_fatura_trafego_detalhado(self, dt:str, dt2:str=None):
        print('proc_item_fatura_detalhado -- Iniciado')
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
        print('proc_item_fatura_detalhado -- Finalizado')
        
    def __truncate_car(self):
        self._ProcLog__exec(
            title = 'truncate table dm_temp.tbl_car_item_fatura_trafego_detalhado'
            , query = 'truncate table dm_temp.tbl_car_item_fatura_trafego_detalhado;'    
        )
    
    def __insert_into_car(self, dt:str, dt2:str=None):
        if not dt2:
            dt2 = dt
        self._ProcLog__exec(
            title = 'insert into dm_temp.tbl_car_item_fatura_trafego_detalhado'
            , query = """
                insert into
                dm_temp.tbl_car_item_fatura_trafego_detalhado
                select
                timestamp(dat_corte_fatura) as dat_corte_fatura
                , timestamp(dat_chamada) as dat_chamada
                , num_ano_mes_referencia
                , cod_ciclo_faturamento
                , dsc_conta_contabil_receita
                , num_fatura
                , cast(cod_servico as int) as cod_servico
                , dsc_servico
                , dsc_zona_tarifaria
                , nom_plano_telefonico
                , cast(num_tel_msisdn as int) as num_tel_msisdn
                , vlr_antes_desc_promo
                , vlr_apos_desc_promo
                , cast(qtd_total_utilizado as int) as qtd_total_utilizado
                from
                tim-bigdata-prod-e305.sdx_mktvas.vw_dw_f_traffat_det_chm_faturada
                where
                dat_corte_fatura between '{dt}' and '{dt2}'
                and dsc_conta_contabil_receita in ('M201064019', 'M201064611', 'M201064616', 'M203084217', 'M203084350' # Consumer
                    , 'M201064607', 'M202035217', 'M201065218' # Corporate (M2M)
                    , 'M201064020', 'M201064024', 'M201064027', 'M201064612', 'M203084202' # Corporate
                    , 'M201064796', 'M202034820', 'M202035109', 'M204234026' # Corporate
                );
            """.format(dt=dt, dt2=dt2)
        )
    
    def __delete_cons(self):
        self._ProcLog__exec(
            title = 'delete dm_prod.tbl_cons_item_fatura_trafego_detalhado'
            , query = """
                delete
                dm_prod.tbl_cons_item_fatura_trafego_detalhado AS cons
                where exists
                (
                    select
                    `Dat Corte Fatura`
                    from
                    (
                        select distinct
                        date(`Dat Corte Fatura`) as `Dat Corte Fatura`
                        from
                        dm_temp.tbl_car_item_fatura_trafego_detalhado
                    ) as car
                    where
                    cons.dt_corte_fatura = date(car.`Dat Corte Fatura`)
                );
            """
        )
        
    def __insert_into_cons(self):
        self._ProcLog__exec(
            title = 'insert into tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_item_fatura_trafego_detalhado'
            , query = """
                insert into
                tim-sdbx-mktvas-b2ba.dm_prod.tbl_cons_item_fatura_trafego_detalhado
                with
                TB_PLANO_1 AS (
                select distinct
                    `Nom Plano Telefonico` AS str_plano_detalhado
                    , case
                    when `Nom Plano Telefonico` like '% __-G__' then left(`Nom Plano Telefonico`, length(`Nom Plano Telefonico`)-7)
                    when `Nom Plano Telefonico` like '%-G__' then left(`Nom Plano Telefonico`, length(`Nom Plano Telefonico`)-4)
                    when `Nom Plano Telefonico` like '% - G__' then left(`Nom Plano Telefonico`, length(`Nom Plano Telefonico`)-6)
                    when `Nom Plano Telefonico` like '%-__' then left(`Nom Plano Telefonico`, length(`Nom Plano Telefonico`)-3)
                    when `Nom Plano Telefonico` like '% - __' then left(`Nom Plano Telefonico`, length(`Nom Plano Telefonico`)-5)
                    else `Nom Plano Telefonico`
                    end str_plano_reduzido
                    , case
                    when `Nom Plano Telefonico` LIKE ANY ('% __-G__', '%-G__', '% - G__', '%-__', '% - __') THEN RIGHT(`Nom Plano Telefonico`,2)
                    else null
                    end as str_plano_uf
                from
                    tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_item_fatura_trafego_detalhado
                )
                , TB_PLANO_2 AS (
                select
                    case
                    when regexp_contains(str_plano_reduzido,'. [0-9] [0-9]')
                        then left(str_plano_reduzido, LENGTH(str_plano_reduzido)-4)
                    when regexp_contains(str_plano_reduzido,'. [0-9] [0-9] ')
                        then left(str_plano_reduzido, LENGTH(str_plano_reduzido)-5)
                    else
                        str_plano_reduzido
                    end AS str_plano
                    , str_plano_detalhado
                    , case
                    when regexp_contains(str_plano_reduzido,'. [0-9] [0-9]')
                        then cast(replace(right(str_plano_reduzido, 4), ' ', '') AS FLOAT64)/10
                    when regexp_contains(str_plano_reduzido,'. [0-9] [0-9] ')
                        then cast(replace(right(str_plano_reduzido, 5), ' ', '') AS FLOAT64)/10
                    else
                        NULL
                    end AS num_plano_geracao
                    , str_plano_uf
                from
                    TB_PLANO_1
                )
                select
                generate_uuid() as id
                , parse_date('%Y%m%d',  CAR.`Num Ano Mes Referencia` || '01') as dt_month_ref
                , date(CAR.`Dat Corte Fatura`) as dt_corte_fatura
                , date(CAR.`Dat Chamada`) as dt_chamada
                , CAR.`Cod Ciclo Faturamento` as num_ciclo_fatura
                , CAR.`Dsc Conta Contabil Receita` as str_conta_contabil_receita
                , CAR.`Num Fatura` as num_fatura
                , CAR.`Cod Servico` as num_cod_servico
                , CAR.`Dsc Servico` as str_servico
                , cast(-1000 AS INT64) as num_app_id
                , CAR.`Dsc Zona Tarifaria` as str_servico_vas
                , TB_PLANO_2.str_plano
                , CAR.`Nom Plano Telefonico` as str_plano_detalhado
                , TB_PLANO_2.num_plano_geracao
                , TB_PLANO_2.str_plano_uf
                , CAR.`Num Tel Msisdn` as num_msisdn
                , CAR.`Vlr Antes Desc Promo` as num_valor_antes_desc_promo
                , CAR.`Vlr Apos Desc Promo` as num_receita
                , CAR.`Qtd Total Utilizado` as num_qtd
                , cast(null as string) as str_charging_id
                , cast(null as string) as str_crc_id
                , cast(null as date) as dt_crc
                , cast(1=0 as bool) as bit_pagamento
                , cast(null as date) as dt_pagamento
                from
                tim-sdbx-mktvas-b2ba.dm_temp.tbl_car_item_fatura_trafego_detalhado AS CAR
                inner join
                TB_PLANO_2
                on
                    CAR.`Nom Plano Telefonico` = TB_PLANO_2.str_plano_detalhado
                order by
                dt_month_ref
                , dt_corte_fatura
                , dt_chamada
                , num_app_id
                , str_plano
                , str_plano_detalhado;
            """
        )
        
    def __update_charging_id(self):
        self._ProcLog__exec(
            title = 'update dm_prod.tbl_cons_item_fatura_trafego_detalhado (charging_id)'
            , query = """
                update
                dm_prod.tbl_cons_item_fatura_trafego_detalhado as cons
                set
                str_charging_id = tb_charging.str_charging_id
                from
                (
                    with
                    tb_fat as (
                        select
                        id
                        , dt_chamada
                        , num_app_id
                        , num_msisdn
                        , num_receita
                        from
                        dm_prod.tbl_cons_item_fatura_trafego_detalhado
                        where
                        num_app_id != -1000
                        and str_charging_id is null
                    )
                    , tb_charging_t as (
                    select
                        tb_fat.id
                        , hub.str_charging_id
                    from
                        tb_fat
                    inner join
                        dm_prod.tbl_cons_hub_tarifacao as hub
                        on
                        tb_fat.dt_chamada = date(hub.dt_ref)
                        and tb_fat.num_app_id = hub.num_app_id
                        and tb_fat.num_msisdn = cast(hub.num_msisdn-5500000000000 as int64)
                        and tb_fat.num_receita = hub.num_valor
                    )
                    select
                    id
                    , max(str_charging_id) as str_charging_id
                    from
                    tb_charging_t
                    group by
                    id
                ) as tb_charging
                where
                cons.id = tb_charging.id
            """
        )
        
    def __update_app_id(self):
        self._ProcLog__exec(
            title = 'update dm_prod.tbl_cons_item_fatura_trafego_detalhado (num_app_id)'
            , query = """
                update
                dm_prod.tbl_cons_item_fatura_trafego_detalhado as cons
                set
                num_app_id = l.num_app_id
                from
                (
                    select
                    dpa.num_app_id
                    , cons.id
                    from
                    dm_prod.tbl_cons_item_fatura_trafego_detalhado as cons
                    inner join
                    dm_prod.tbl_dpa_item_fatura_trafego_detalhado_servico as dpa
                    on
                        cons.str_servico_vas = dpa.str_valor
                    where
                    dpa.num_app_id is not null
                ) l
                where
                cons.id = l.id
                and cons.num_app_id = -1000;
            """
        )
        
    def __insert_dpa_servico(self):
        self._ProcLog__exec(
            title = 'insert into dm_prod.tbl_dpa_item_fatura_trafego_detalhado_servico'
            , query = """
                insert into
                dm_prod.tbl_dpa_item_fatura_trafego_detalhado_servico
                select distinct
                str_servico_vas
                , cast(null as string) as str_hub_tarifacao
                , cast(null as int64) as num_app_id
                from
                dm_prod.tbl_cons_item_fatura_trafego_detalhado as cons
                left join
                dm_prod.tbl_dpa_item_fatura_trafego_detalhado_servico as dpa
                on
                    cons.str_servico_vas = dpa.str_valor
                where
                dpa.str_valor is null
                and cons.str_servico_vas is not null;
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
                dm_prod.tbl_cons_item_fatura_trafego_detalhado as cons
                left join
                dm_prod.tbl_dpa_plano as dpa
                on
                    cons.str_plano = dpa.str_plano
                where
                dpa.str_plano is null;
            """
        )
        
    def __update_bit_pagamento(self):
        self._ProcLog__exec(
            title = 'update dm_prod.tbl_cons_item_fatura_trafego_detalhado (pagamento)'
            , query = """
                update
                dm_prod.tbl_cons_item_fatura_trafego_detalhado as fat
                set
                bit_pagamento = 1=1
                , dt_pagamento = pag.dat_referencia
                from
                (
                    with
                    tb_fat as (
                        select distinct
                        num_fatura
                        from
                        dm_prod.tbl_cons_item_fatura_trafego_detalhado
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
