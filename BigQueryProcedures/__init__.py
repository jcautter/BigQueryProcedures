import BigQuery

from sql_item_fatura import SQLItemFatura
from sql_item_fatura_trafego_detalhado import SQLItemFaturaTrafegoDetalhado
from sql_recarga_ocs import SQLRecargaOCS
from sql_crc_recuperacao_vas import SQLCRCRecuperacaoVAS

class BigQueryProcedures(
    SQLItemFatura
    , SQLItemFaturaTrafegoDetalhado
    , SQLRecargaOCS
    , SQLCRCRecuperacaoVAS
):
    
    def __init__(self, *, bq:BigQuery=None, project:str=None, token:str=None):
        if bq:
            self.bq = bq
        elif project and token:
            self.bq = BigQuery(project, token)
        else:
            raise Exception("Sorry, conection or project and token are needed!")
            
    def proc_acum_full_base__replace_table(self):
        query = """
        create or replace table tim-sdbx-mktvas-b2ba.dm_prod.tbl_acum_full_base
        cluster by dt_month_ref, dt_month_tarifacao, num_msisdn, num_app_id
        as
          select
            *
          from
            dm_prod.vw_acum_full_base
        """
        self.bq.execute_query(query, commit=True)
