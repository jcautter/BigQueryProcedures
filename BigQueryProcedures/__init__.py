import BigQuery

from .sql_item_fatura import SQLItemFatura
from .sql_item_fatura_trafego_detalhado import SQLItemFaturaTrafegoDetalhado
from .sql_recarga_ocs import SQLRecargaOCS
from .sql_crc_recuperacao_vas import SQLCRCRecuperacaoVAS
from .sql_full_base import SQLFullBaseFatura

class BigQueryProcedures(
    SQLItemFatura
    , SQLItemFaturaTrafegoDetalhado
    , SQLRecargaOCS
    , SQLCRCRecuperacaoVAS
    , SQLFullBaseFatura
):
    
    def __init__(self, *, bq:BigQuery=None, project:str=None, token:str=None):
        if bq:
            self.bq = bq
        elif project and token:
            self.bq = BigQuery(project, token)
        else:
            raise Exception("Sorry, conection or project and token are needed!")
