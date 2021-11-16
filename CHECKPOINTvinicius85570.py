#VINICIUS DE JESUS CORREIA 
#Este programa ira monitorar o repositorio onde ele se encontra, por isso execute-o no dentro do diretorio que deseja monitorar
from time import sleep
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatchdogHandlerAny(FileSystemEventHandler):
    def __init__(self, watch_path):
        self.watch_path = watch_path

    def on_any_event(self, event):
        print("Atenção, algo aconteceu!")
        print(f"Event type: {event.event_type}")
        print(event)
        



class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, watch_path):
        self.watch_path = watch_path

    def on_modified(self, event):
        print(f"Arquivo Modificado: {event.src_path}")

    def on_created(self, event):
        print(f"Arquivo criado: {event.src_path}")

    def on_deleted(self, event):
        print(f"Arquivo Deletado: {event.src_path}")

    def on_moved(self, event):
        print(f"{'Folder' if event.is_directory else 'File'} {event.event_type} "
              f"from: {path.relpath(event.src_path, self.watch_path)} "
              f"to: {path.relpath(event.dest_path, self.watch_path)}")

class FolderWatchDog:
    def __init__(self, handler):
        self.handler = handler
        self.watch_path = handler.watch_path
        self.observer = Observer()  

    def start(self):
        self.observer.schedule(self.handler,
                               path=self.handler.watch_path,
                               recursive=True)  

        try:
            print(f"Starting to watch folder: {self.handler.watch_path}")
            self.observer.start()
            while True:
                sleep(5)

        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f"Algo deu errado!")
            print(e)

        finally:
            print("Termino!")

    def stop(self):
        self.observer.stop()
        self.observer.join()


if __name__ == '__main__':
    
    while True:
        print("Para parar a execução do programa, presione CRTL+C")
        print("Digite o caminho do diretorio que voce deseja que seja monitorado (Exemplo: C:/Users/Vinicius J/Downloads)")
        dir = input("Caminho do Diretorio:")
        dir2t = input("Digite algum arquivo que deseja criar backup:")
        arq = dir + dir2t
        to_watch = dir
        w_dog = FolderWatchDog(handler=WatchdogHandlerAny(watch_path=to_watch))
        w_dog.start()
        with open(arq, "r" ) as arquivo:
            for linha in arquivo:
                with open(arq, "r") as arquivo:
                    conteudo=arquivo.readlines()
            with open('backup' + arq, "w") as arquivo:
                arquivo.writelines(conteudo)
            arquivo.close()
