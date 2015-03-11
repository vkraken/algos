#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
-- can be imported as submodule to build feature vectors from emails collections,
using different presets of loaded heuristics

-- returns NxM matrix --> N samples from collection x M features +label value
(or "test" label if not defined) in numpy array type
"""

import sys, os, logging, re, email, argparse, stat, tempfile, math

from email.parser import Parser
from collections import defaultdict, OrderedDict

from franks_factory import MetaFrankenstein
from pattern_wrapper import BasePattern

from sklearn.ensemble import RandomForestClassifier


#PYTHON_VERSION=(2,7)

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

# define some functions

#def check_python_version(version):
#    if version != (sys.version_info.major, sys.version_info.minor):
#        major, minor = version
#        sys.stderr.write( '[%s] - Error: Your Python interpreter must be %d.%d\n' % (sys.argv[0], major, minor))
#        sys.exit(-1)
#        return

# create feature vector for email from doc_path,
# if label is set => feature set is also predifined by pattern for this label
def vectorize(doc_path, label, score):

    logger.debug("\n\nStart processing: " + doc_path + ' from "' + label + '" set')
    vect_dict = OrderedDict()

    parser = Parser()
    with open(doc_path, 'rb') as f:
        msg = parser.parse(f)

    vect_dict['size'] = math.ceil(float((os.stat(doc_path).st_size)/1024))
    logger.debug('----->'+str(vect_dict))

    try:

        Frankenstein = MetaFrankenstein.New(msg, label)
        logger.debug('\n\n\t CHECK_' + label.upper()+'\n')
        vect_dict.update(Frankenstein.run(score))

    except Exception as details:
        logger.error(str(details))
        raise

    return (vect_dict, label)

def __normalize(vect_dict):
    # remove feature tags ?
    #
    pass


#def get_jaccard_distance():
        # return nltk.jaccard_distance()


def __pathes_gen(path,st_mode):

    sample_path = path
    if st_mode == stat.S_IFREG:
        yield(sample_path)

    elif st_mode == stat.S_IFDIR:
        for path, subdir, docs in os.walk(path):
            for d in docs:
                sample_path = os.path.join(path,d)
                yield(sample_path)


'''''
def dump_data_set(data_set):

			f = open('data_from_'+os.path.basename(dir_path)+'.txt','w+b')
			for features_vect, class_vect, abs_path  in zip(X, Y, Z):
				logger.debug('-->'+str(features_vect+(class_vect,abs_path)))
				f.writelines(str(features_vect+(class_vect,abs_path))+'\n')
			f.close()


'''''

if __name__ == "__main__":

    usage = 'usage: %prog [ samples_directory | file ] -c category -s score -v debug'
    parser = argparse.ArgumentParser(prog='helper')
    parser.add_argument('PATH', type=str, metavar = 'PATH', help="path to samples dir or to email")
    parser.add_argument('-c', action = "store", dest = 'category',default = 'test',
                            help = "samples category, default=test, i.e. not defined")
    parser.add_argument('-s', type = float,  action = 'store', dest = "score", default = 1.0,
                            help = "score penalty for matched feature, def = 1.0")
    parser.add_argument('-v', action = "store_true", dest = "debug", default = False, help = "be verbose")
    parser.add_argument('-v', type=str, action = "store", dest = "criterion", default = 'gini', help = "the function name to measure the quality of a split")

    args = parser.parse_args()

    required_version = (2,7)


    formatter = logging.Formatter(' --- %(filename)s --- \n %(message)s')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(os.path.join(tempfile.gettempdir(), args.category+'.log'), mode = 'w')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    # 1. check and determine pathes
    checks = {
                stat.S_IFREG : lambda fd: os.stat(fd).st_size,
                stat.S_IFDIR : lambda d: os.listdir(d)
    }

    mode = filter(lambda key: os.stat(args.PATH).st_mode & key, checks.keys())
    f = checks.get(*mode)
    if not f(args.PATH):
        raise Exception(args.PATH + '" is empty.')

    # 2. make datasets
    try:
        X = defaultdict(list)
        pathes_iterator = __pathes_gen(args.PATH, *mode)
        clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0, criterion=args.criterion)

        while(True):
            sample_path = next(pathes_iterator)
            logger.debug('PATH: '+sample_path)
            if args.category == 'test':
                for label in ('ham', 'spam', 'info', 'net'):

                    vector_x = vectorize(sample_path, label, args.score)
                    logger.debug('----->'+str(vector_x))
                    #vector_x = normilize(vector_x)
                    logger.debug('----->'+str(vector_x))
                    X[label].append(vector_x)
            else:

                vector_x = vectorize(sample_path, args.category, args.score)
                logger.debug('----->'+str(vector_x))
                X[args.category].append(vector_x)

        logger.debug(X)
        clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0, criterion=args.criterion)



    except StopIteration as details:
        pass

    except Exception as details:
        logger.error(str(details))
        #sys.exit(1)
        raise


'''
class forest(object):

    DEFAULT_LABELS = ('ham', 'spam', 'info', 'net')

    def vectorize(doc_path, label, score)
    def get_labeled_data_set (label)
    def fit(label)
    def predict(path)
    def get_trained_forest(label)
    def dump_data_set(label)
'''







