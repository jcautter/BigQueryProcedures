import BigQuery

from .sql_item_fatura import SQLItemFatura
from .sql_item_fatura_trafego_detalhado import SQLItemFaturaTrafegoDetalhado
from .sql_recarga_ocs import SQLRecargaOCS
from .sql_crc_recuperacao_vas import SQLCRCRecuperacaoVAS
from .sql_full_base import SQLFullBaseFatura
from .sql_prebilling_avulso import SQLPrebillingAvulso
from .sql_economic_result import SQLEconomicResult
from .sql_recarga import SQLRecarga

class BigQueryProcedures(
    SQLItemFatura
    , SQLItemFaturaTrafegoDetalhado
    , SQLRecargaOCS
    , SQLCRCRecuperacaoVAS
    , SQLFullBaseFatura
    , SQLPrebillingAvulso
    , SQLEconomicResult
    , SQLRecarga
):
    
    def __init__(self, *, bq:BigQuery=None, project:str=None, token:str=None):
        if bq:
            self.bq = bq
        elif project and token:
            self.bq = BigQuery(project, token)
        else:
            raise Exception("Sorry, conection or project and token are needed!")


