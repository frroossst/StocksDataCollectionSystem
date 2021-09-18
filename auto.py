import time

start = time.time()

def program():
    import flags
    import scraper
    import algorithm
    import backtest

try:
    program()
except Exception as e:
    print(f"[ERROR] {e}")
    program()

end = time.time()

print() 
print(f"completed execution in {round((end - start),2)} second(s)")