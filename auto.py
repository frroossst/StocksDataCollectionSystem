import time

start = time.time()

def program():
    print("[OK] gathering flags")
    import flags
    print("[OK] collecting scrip data")
    import scraper
    print("[OK] running technical analysis")
    import algorithm
    print("[OK] running trading algorithm")
    import backtest

try:
    program()
except Exception as e:
    print(f"[ERROR] {e}")
    program()

end = time.time()

print() 
print(f"completed execution in {round((end - start),2)} second(s)")
