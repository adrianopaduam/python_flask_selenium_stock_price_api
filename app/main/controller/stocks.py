""" Stocks controller class """
from flask import request
from flask_restful import Resource

from app.main.config import logger
from app.main.util.data_validation import validate_region_name
from app.main.service.stocks_service import recover_region_stocks
from app.main.util.exceptions import UserError, InternalError


class StocksController(Resource):

    def get(self):
        valid_region, region, error_message = validate_region_name(
            request.args.get("region")
        )
        if not valid_region:
            return {"error": error_message, "region_informed": region}, 400

        try:
            return recover_region_stocks(region), 200
        except UserError as usr_ex:
            return {"error": str(usr_ex)}, 400
        except InternalError:
            return {"error": "API failed, please try again later"}, 500
        except Exception:
            logger.error("Unknown API error")
            return {"error": "Internal server error"}, 500
