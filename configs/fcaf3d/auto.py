from distutils import extension
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Target:
    watchDir = '/home/jetson/result'
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                                                       recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함

    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(event)

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        
        a = event
        filename = a.key[1].split('/')[-1]
        ex = filename.split('.')[-1]

        if ex == 'txt':
            command = 'python3 /home/jetson/dofbot_ws/src/dofbot_snake_follow/scripts/snake_ctrl2.py' + \
                      + '/home/jetson/result/' + filename 
            os.system(command)

        if ex == 'ply':
            command = 'python3 /home/jetson/dofbot_ws/src/dofbot_snake_follow/scripts/snake_ctrl2.py' + \
                      + '/home/jetson/result/' + filename 
            os.system(command)

        
        
    
    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(event)
        print('stop')

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        pass



w = Target()
w.run()

