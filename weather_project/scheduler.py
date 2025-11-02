import schedule, time, importlib, api_collector  # 첫 import 시 1회 실행

def job():
    importlib.reload(api_collector)  # 매시간 재실행

schedule.every(3).hour.at(":00").do(job)  # 매 정시

while True:
    schedule.run_pending()
    time.sleep(1)
