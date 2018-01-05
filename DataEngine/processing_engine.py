import Queue
import threading
import glob

import time

import unidecode as unidecode

from DataEngine.dataengine import DataEngine
from RoutesGraph import RoutesGraph


exitFlag = 0
#this graph contain concatenated routes
graph = RoutesGraph()

"""Class wrapping threading library. Extends it with queue-processing scheme.
Worker picks up data to process it in synchronized manner"""


class WorkerThread (threading.Thread):
    queueLock = threading.Lock()

    def __init__(self, thread_id, queue, callback):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.work_queue = queue
        self.worker_callback = callback

    def run(self):
        print "Starting thread with ID {0}".format(self.threadID)
        self.process_data()
        print "Exiting thread with ID {0}".format(self.threadID)

    def process_data(self):
        while not exitFlag:
            WorkerThread.queueLock.acquire()
            if not self.work_queue.empty():
                data = self.work_queue.get()
                WorkerThread.queueLock.release()
                print "Thread nr : {0} processing: {1}".format(self.threadID, data)
                self.worker_callback(data)
            else:
                # this should be in fact realised with cond. variable.
                # for now left with no-elegant sleep
                WorkerThread.queueLock.release()
                time.sleep(1)

        #write routes to json file
        graph.writeToGeojson("lines.json")


"""Base framework for processing content"""


class ProcessingEngine:
    gml_lock = threading.Lock ()
    add_to_graph_lock = threading.Lock ()
    de = DataEngine()

    root = de.open_prng("utils/decoded_miejsc_krainy.xml")

    def __init__(self, pattern, threads_nr):
        self.dir_pattern = pattern
        self.thr_nr = threads_nr
        self.item_queue = Queue.Queue()
        self.threads = []
        self.init_threadID = 0

    """ Main processing unit. 
    Needs to be implemented as specific-use behaviour."""
    def worker_callback(self, data):

        content = ProcessingEngine.de.read_content(data)
        name_list = ProcessingEngine.de.get_upper_case_names(content)

        for names in name_list:
            ProcessingEngine.gml_lock.acquire()
            elements = ProcessingEngine.root.findall("row")
            ProcessingEngine.gml_lock.release()


            coord_list = ProcessingEngine.de.build_track_list(elements, names)
            #print("end of one post" + str(coord_list))

            #do not add to graph simple place or empty list
            if len(coord_list) < 2:
                continue


            ProcessingEngine.add_to_graph_lock.acquire()
            #add route to graph
            for i in range(0, len(coord_list) - 1):
                graph.addEdge(coord_list[i], coord_list[i + 1])

            ProcessingEngine.add_to_graph_lock.release()



    """Main processing method"""
    def start_processing(self):
        self._get_item_names()
        print "Number of elements to be processed : {0}".format(self.get_queue_size())
        self._spawn_workers()

        # wait for processing to clean queue
        while not self.item_queue.empty():
            pass
            #time.sleep(1)

        self._clean_up()


    """Spawns thread workers"""
    def _spawn_workers(self):
        for w_id in range(self.init_threadID, self.thr_nr):
            thread = WorkerThread(w_id, self.item_queue, self.worker_callback)
            thread.start()
            self.threads.append(thread)

    """Joins worker threads and do other cleaning"""
    def _clean_up(self):
        global exitFlag
        exitFlag = 1
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
