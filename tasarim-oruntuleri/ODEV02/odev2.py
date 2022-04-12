import threading, time, logging
from dataclasses import dataclass
from typing import List

logging.basicConfig(level=logging.INFO, format="[+] %(levelname)s: %(message)s")

# Uyuma süreleri sabit olarak tanımlandı
SLEEP_SHORT: float = 1.0
SLEEP_LONG: float = 5.0


class ObjectPoolNotAwailable(RuntimeError):
    """
    Poolda müsait nesne bulunmadığında kullanılacak hata/exception
    """
    pass


class DBConnection:
    def __init__(self):
        # nesne oluştuğunda veritabanına bağlan
        self.connect()

    def db_operation(self):
        # veritabanı işlemi yap
        logging.info(f"Performing db operation")
        time.sleep(SLEEP_LONG)

    def connect(self):
        logging.info(f"Connecting to db")
        time.sleep(SLEEP_SHORT)


@dataclass
class DbPoolObj:
    # thread id si / ismi
    tid: str

    # nesne müsait mi?
    available: bool

    # nesnenin kendisi
    obj: DBConnection


class DBConnectionPool:
    # ilk nesne oluşturulurken kullanılacak lock
    _obj_mutex = threading.Lock()

    # Python dili için singeleton yapısı __new__ özel metodu ile kurulabilir.
    def __new__(cls):
        # sınıf üzerinde bir nesne banımlanmış ise onu döndür.
        # değilse yeni bir tane oluştur
        with cls._obj_mutex:
            if not hasattr(cls, "instance"):
                cls.instance = super(DBConnectionPool, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # nesne oluşturulduğunda mutex ve poll değişkenlerini oluştur
        # değişkenlerin _ ile başlaması private olduklarını gösterir!!!
        self._mutex = threading.Lock()
        self._poll: List[DbPoolObj] = tuple(
            DbPoolObj(tid=None, available=True, obj=DBConnection()) for _ in range(10)
        )

    def getObject(self, th: threading.Thread) -> DBConnection:
        # mutex. multi thread safe
        with self._mutex:
            logging.info(f"Getting DB: {len(self._poll)}")
            for i in self._poll:
                # uygun connection bulunduğunda kullanım için işaretle.
                # hangi threadin hangi connectionı kullandığının kaydını saklıyoruz
                if i.available == True and i.tid == None:
                    i.available = False
                    i.tid = th.getName()
                    return i.obj
            # uygun connection yok. hata fırlat
            raise ObjectPoolNotAwailable("No awaible db connection")

    def releaseObject(self, dbconn: DBConnection, th: threading.Thread):
         # mutex. multi thread safe
        logging.info(f"Releasing DB: from {th.getName()}")
        with self._mutex:
            for i in self._poll:
                # thread için kaydedilmiş conenctionu serbest bırak
                if i.available == False and i.tid == th.getName():
                    i.available = True
                    i.tid = None


def run_database_operations(dbpool: DBConnectionPool, th: threading.Thread):
    while True:
        try:
            # uygun bir connection alasıya kadar dene / bekle
            db_connection = dbpool.getObject(th)
            break
        except ObjectPoolNotAwailable:
            logging.warning(
                f"Pool is not available. Waiting {SLEEP_SHORT} sec for {th.getName()}"
            )
            time.sleep(SLEEP_SHORT) # bekle

    # db işlemini yap
    db_connection.db_operation()
    # connectionu poola geri veer
    dbpool.releaseObject(db_connection, th)


def main():
    # connection poolu oluştur
    logging.info(f"Testing connection pool!")
    dbpool = DBConnectionPool()

    # test connection pool
    dbconn = dbpool.getObject(threading.main_thread())
    dbpool.releaseObject(dbconn, threading.main_thread())

    threads: List[threading.Thread] = list()
    # 15 tane thread oluştur ve çalıştır
    for index in range(15):
        logging.info(f"create and start thread {index}")

        x: threading.Thread = None
        args = [dbpool, x]
        x = threading.Thread(target=run_database_operations, args=args)
        args[1] = x
        logging.info(f"Rugging thread: {x.getName()}")
        threads.append(x)
        x.start()
        logging.info(f"Active threads: {threading.active_count()}") # aktif thread sayısı

    # threadlar bitene kadar programdan çıkma
    for index, thread in enumerate(threads):
        logging.info(f"before joining thread {index}")
        thread.join()
        logging.info(f"thread {index} done")


if __name__ == "__main__":
    main()
