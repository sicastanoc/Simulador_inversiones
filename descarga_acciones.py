from config.database import engine, Base, Session
from request import RequestData
from services import StockServices, HistoryStocksServices
from schemas import HistoryStock
from datetime import datetime,time

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Serviria para crear la base de datos, se da por hecho que ya se encuentra creada
# Base.metadata.create_all(bind=engine)


def main():

    db = Session()
    stock_list = StockServices(db).get_all_values()

    for stock in stock_list:
        
        try:

            res = RequestData.get_request(stock.nombre_abreviado)

            last_value = HistoryStocksServices(db).get_value(stock.accion_id)

            market_time = datetime.fromtimestamp(res.get("regularMarketTime"))
            close = res.get("close")

            if last_value:

                if last_value.fecha == market_time and last_value.precio == close:
                    logger.info("La info ya esta en la base de datos")
                    continue
                
            HistoryStocksServices(db).create_value(value = HistoryStock(
                accion_id = stock.accion_id,
                fecha = market_time,
                precio = close
            ))

        except (TypeError, ):
            logger.info(f"No se encuentra la accion: {stock}")

        except Exception:
            logger.error("Error desconocido", exc_info=True)

        
    db.close()


if __name__ == "__main__":
    main()
