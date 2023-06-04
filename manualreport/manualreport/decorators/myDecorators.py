from .entities import ProgressBarPrinter
import sys
from functools import wraps
import re

def ProgressBar(width=50, step=0.1, stream=sys.stdout):
    """Decorator, prints a progress bar when a decored function yields it's
    current progress.
    When you want the progress bar to be updated you should yield the progress
    of your function between 0 and 1. The general calcul for this is:
    (current_iteration + 1) / total_iterations.
    When yielding None, the progress bar goes up by `current progress + step`.
    This is usefull to show some feedback instead of a dead terminal when it's
    not possible to calculate the progress of a function.
    Limitation: It uses yield statements as callbacks for the decorator. That
    means you can't yield your result, meaning this progress bar doesn't
    work if your function is intended to be a generator.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            pb = ProgressBarPrinter(width, step, stream, func.__name__)
            progress_generator = func(*args, **kwargs)
            try:
                while True:
                    progress = next(progress_generator)
                    pb.update(progress)
            except StopIteration as result:
                pb.end()
                return result.value
        return wrapper
    return decorator

def myTimer(origFunc):
    import time   
    @wraps(origFunc)
    def wrapper(*args, **kwargs):
        start=time.time()
        result=origFunc(*args, **kwargs)
        end=time.time()
        period=end-start
        print(f'{origFunc.__name__} ran in: {period} sec')
        return result
    
    return wrapper

def myRetry(maxTries=3, delaySeconds=1):
    import time
    def decoratorRetry(origFunc):
        @wraps(origFunc)
        def wrapper(*args, **kwargs):
            tries=0
            while tries<maxTries:
                try:
                    return origFunc(*args, **kwargs)
                except Exception as e:
                    tries+=1
                    if tries ==maxTries:
                        raise e
                    time.sleep(delaySeconds)
        return wrapper
    return decoratorRetry

def myLog(origFunc):
    import logging
    logging.basicConfig(level=logging.INFO)
    @wraps(origFunc)
    def wrapper(*args, **kwargs):
        logging.info(f'Executing {origFunc.__name__}')
        result=origFunc(*args, **kwargs)
        logging.info(f'Finished executing {origFunc.__name__}')
        return result
    return wrapper

def extract_href_from_a_tag(innerHtml:str):
    regex = "(?P<url>https?://[^\s]+)"
    matches = re.findall(regex, innerHtml)
    return matches


