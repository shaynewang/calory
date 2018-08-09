# from .detect import *
from lib import detect as api
import sys


def detect_image(path):
    """
    Takes local file path. Outputs list of labels
    """
    labels = api.detect_labels(path)
    llist = []
    for label in labels:
        llist.append(label.description)
    return llist


if __name__=="__main__":
    print("Starting...")
    print("Processing image:", sys.argv[1])

    # Get list of labels
    labellist = detect_image(sys.argv[1])
    print("label list:", labellist)
    

