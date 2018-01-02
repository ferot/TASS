import Queue
import threading
import glob

import time

exitFlag = 0

"""Class wrapping threading library. Extends it with queue-processing scheme.
Worker picks up data to process it in synchronized manner"""


class WorkerThread (threading.Thread):
    queueLock = threading.Lock()

    def __init__(self, threadID, queue, callback):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.work_queue = queue
        self.worker_callback = callback

    def run(self):
        print "Starting " + self.name
        self.process_data()
        print "Exiting " + self.name

    def process_data(self):
        while not exitFlag:
            WorkerThread.queueLock.acquire()
            if not self.work_queue.empty():
                data = self.work_queue.get()
                WorkerThread.queueLock.release()
                print "{0} processing {1}".format(self.threadID, data)
                self.worker_callback(data)
            else:
                # this should be in fact realised with cond. variable.
                # for now left with no-elegant sleep
                WorkerThread.queueLock.release()
                time.sleep(1)


"""Base framework for processing content"""


class ProcessingEngine:
    def __init__(self, pattern, threads_nr):
        self.dir_pattern = pattern
        self.thr_nr = threads_nr
        self.item_queue = Queue.Queue()
        self.threads = []
        self.queue_lock = threading.Lock()
        self.init_threadID = 1

    """ Main processing unit. 
    Needs to be implemented as specific-use behaviour."""
    def worker_callback(self, data):
        print data

    """Main processing method"""
    def start_processing(self):
        self._get_item_names()
        print "Number of elements to be processed : {0}".format(self.get_queue_size())
        self._spawn_workers()

        # wait for processing to clean queue
        while not self.item_queue.empty():
            time.sleep(5)

        self._clean_up()


    """Spawns thread workers"""
    def _spawn_workers(self):
        for w_id in range(self.init_threadID, self.thr_nr):
            thread = WorkerThread(w_id, self.item_queue, self.worker_callback)
            thread.start()
            self.threads.append(thread)

    """Joins worker threads and do other cleaning"""
    def _clean_up(self):
        for thread in self.threads:
            thread.join()
        print "Finished cleaning."

    """Gets item relative paths and stores them in item queue.
    Note : As this operation is perfomed by single thread 
    - no synchronization is needed."""
    def _get_item_names(self):
        for name in glob.glob(self.dir_pattern):
            self.item_queue.put(name)

    "Returns size of queue"
    def get_queue_size(self):
        return self.item_queue.qsize()