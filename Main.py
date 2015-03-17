__author__ = 'Malte-Christian Scharenberg'

import multiprocessing
import time
import json
import sys

from Node.NodeClass import NodeClass
from Evaluation.Evaluator import Evaluator
from Evaluation.Delay import Delay
from Evaluation.Throughput import Throughput
from Helper.Logger import Logger
from Helper.MatlabExporter import MatlabExporter
from Hardware.HardwareMock import HardwareMock
from Hardware.XBeeWrapper import XBeeWrapper
from Node.Source import Source
from Node.Sink import Sink

if __name__ == '__main__':
    # Init
    log_data_queue = multiprocessing.Queue()
    evaluator = Evaluator(log_data_queue)
    logger = Logger()
    nodes = []

    # Parse config file
    try:
        config = json.load(open('config.json'))
        matlab_exporter = MatlabExporter(config['matlab_exporter']['file'])
        for behavior in config['evaluator_behaviors']:
            behavior = globals()[behavior['type']](**behavior['arguments'])
            evaluator.add_behavior(behavior)
        for node_config in config['nodes']:
            hardware = globals()[node_config['hardware']['type']](**node_config['hardware']['arguments'])
            node = NodeClass(log_data_queue, hardware)
            for behavior in node_config['behaviors']:
                behavior = globals()[behavior['type']](**behavior['arguments'])
                node.add_behavior(behavior)
            nodes.append(node)
    except KeyError, e:
        print 'Key Error in config file:', e
        sys.exit(1)
    except TypeError, e:
        print 'Type Error in config file:', e
        sys.exit(1)

    map(NodeClass.start, nodes)  # Start node processes

    try:
        while any(map(NodeClass.is_alive, nodes)):  # Check if nodes are still alive
            results = evaluator.get_short_results()
            logger.print_short_results(results)  # output live results
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass

    results = evaluator.get_results()
    logger.print_results(results)
    matlab_exporter.export(results)