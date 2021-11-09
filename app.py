from calculator.calculate_bmi import bmi_calculation
from config import logger

if __name__ == "__main__":
    try:
        bmi_calculation()
    except Exception as err:
        logger.exception(err)
