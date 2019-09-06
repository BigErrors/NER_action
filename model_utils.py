from collections import OrderedDict
import os
import json
import logging

def get_log(log_file):
    """
    定义日志方法
    :param log_file:
    :return:
    """
    # 创建一个logging的实例logger
    logger = logging.getLogger(log_file)
    # 设置logger的全局日志级别DEBUG
    logger.setLevel(logging.DEBUG)
    # 创建一个日志文件的handler，并且设置日志级别为DEBUG
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # 创建一个控制台handler， 并设置日志级别为DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger




def config_model(FLAGS, word_to_id, tag_to_id):
    config = OrderedDict()
    config['num_words'] = len(word_to_id)
    config['word_dim'] = FLAGS.word_dim
    config['num_tags'] = len(tag_to_id)
    config['seg_dim'] = FLAGS.seg_dim
    config['lstm_dim'] = FLAGS.lstm_dim
    config['batch_size'] = FLAGS.batch_size

    config['clip'] = FLAGS.clip
    config['dropout_keep'] = 1.0 - FLAGS.dropout
    config['optimizer'] = FLAGS.optimizer
    config['lr'] = FLAGS.lr
    config['tag_schema'] =FLAGS.tag_schema
    config['pre_emb'] = FLAGS.pre_emb
    return config


def make_path(params):
    """
    创建文件夹
    :param params:
    :return:
    """
    if not os.path.isdir(params.ckpt_path):
        os.makedirs(params.ckpt_path)
    if not os.path.isdir('log'):
        os.makedirs('log')

def save_config(config, config_file):
    """
    保存配置文件
    :param config:
    :param config_path:
    :return:
    """
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def load_config(config_file):
    """
    加载配置文件
    :param config_file:
    :return:
    """
    with open(config_file, encoding='utf-8') as f:
        return json.load(f)


def print_config(config, logger):
    """
    打印模型参数
    :param config:
    :param log:
    :return:
    """
    for k, v in config.items():
        logger.info('{}:\t{}'.format(k.ljust(5), v))
