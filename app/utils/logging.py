from datetime import datetime
import sys
import loguru

logger = loguru.logger
logger.remove(0)
logger.add(sys.stderr, format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}")

def runtime_capture(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        function_name = func.__name__
        logger.info(f"Running {function_name}...")
        result = func(*args, **kwargs)
        logger.info(f"{function_name} Runtime: {(datetime.now() - start).seconds} seconds")
        return result
    
    return wrapper

def runtime_capture_async(func):
    async def wrapper(*args, **kwargs):
        start = datetime.now()
        function_name = func.__name__
        logger.info(f"Running {function_name}...")
        result = await func(*args, **kwargs)
        logger.info(f"{function_name} Runtime: {(datetime.now() - start).seconds} seconds")
        return result
    
    return wrapper