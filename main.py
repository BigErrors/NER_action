# 系统包
import os
import tensorflow as tf
import pickle

# 自定义的包
import data_loader as dl
import data_utils as du
import model_utils as mu

flags = tf.app.flags

# 训练相关的
flags.DEFINE_boolean('train', True, '是否开始训练')
flags.DEFINE_boolean('clean', True, '是否清理文件')

# 配置相关
flags.DEFINE_integer('seg_dim', 20, 'seg embedding size')
flags.DEFINE_integer('word_dim', 120, 'word embedding')
flags.DEFINE_integer('lstm_dim', 120, 'number of hidden unis in lstm')
flags.DEFINE_string('tag_schema', 'BIOES', '编码方式')

# 训练相关
flags.DEFINE_float('clip', 5, 'Grandient clip')
flags.DEFINE_float('dropout', 0.5, 'Dropout rate')
flags.DEFINE_integer('batch_size', 120, 'batch_size')
flags.DEFINE_float('lr', 0.001, 'learning rate')
flags.DEFINE_string('optimizer', 'adam', '优化器')
flags.DEFINE_boolean('pre_emb', True, '是否使用预训练')

flags.DEFINE_integer('max_epoch', 100, '最大轮训次数')
flags.DEFINE_integer('setps_chech', 100, 'step per checkpoint')
flags.DEFINE_string('ckpt_path', os.path.join('model', 'ckpt'), '模型保存的位置')
flags.DEFINE_string('log_file', 'train.log', '训练过程中的日志')
flags.DEFINE_string('map_file', 'maps.pld', '存放我们的字典及标签映射')
flags.DEFINE_string('vocab_file', 'vocab.json', '词典')
flags.DEFINE_string('config_file', 'config_file', '配置文件')
flags.DEFINE_string('train_file', os.path.join('data', 'ner.train'), '训练数据集的路径')
flags.DEFINE_string('dev_file', os.path.join('data', 'ner.dev'), '校验数据集的路径')
flags.DEFINE_string('test_file', os.path.join('data', 'ner.test'), '测试集的路径')

FLAGS = tf.app.flags.FLAGS
assert FLAGS.clip < 5.1,  '梯度裁剪不能过大'
assert 0 <FLAGS.dropout < 1, 'dropout必须在0和1之间'
assert FLAGS.lr > 0, 'lr必须大于零'
assert FLAGS.optimizer in ['adam', 'sgd', 'adagrad'], '优化器必须在adam, sgd, adagrad 之间'


def train():
    # 加载数据集
    train_sentences = dl.load_sentences(FLAGS.train_file)
    dev_sentences = dl.load_sentences(FLAGS.dev_file)
    test_sentences = dl.load_sentences(FLAGS.test_file)

    # 转换编码 bio转bioes
    dl.update_tag_scheme(train_sentences, FLAGS.tag_schema)
    dl.update_tag_scheme(test_sentences, FLAGS.tag_schema)
    dl.update_tag_scheme(dev_sentences, FLAGS.tag_schema)

    # 创建单词映射及标签映射
    if not os.path.isfile(FLAGS.map_file):
        _, word_to_id, id_to_word = dl.word_mapping(train_sentences)
        _, tag_to_id, id_to_tag = dl.tag_mapping(train_sentences)

        with open(FLAGS.map_file, 'wb') as f:
            pickle.dump([word_to_id, id_to_word, tag_to_id, id_to_tag], f)
    else:
        with open(FLAGS.map_file, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            scores = unpickler.load()
            word_to_id, id_to_word, tag_to_id, id_to_tag = scores

    train_data = dl.prapare_dataset(train_sentences, word_to_id, tag_to_id)
    dev_data = dl.prapare_dataset(train_sentences, word_to_id, tag_to_id)
    test_data = dl.prapare_dataset(train_sentences, word_to_id, tag_to_id)

    print('train_data %i, dev_data_num %i, test_data_num %i' % (len(train_data), len(dev_data), len(test_data)))

    mu.make_path(FLAGS)
    if os.path.isfile(FLAGS.config_file):
        config = mu.load_config(FLAGS.config_file)
    else:
        config = mu.config_model(FLAGS, word_to_id, tag_to_id)
        mu.save_config(config, FLAGS.config_file)
    log_path = os.path.join('log', FLAGS.log_file)
    logger = mu.get_log(log_path)
    mu.print_config(config, logger)
    print('aa')



def main(_):
    if FLAGS.train:
        train()
    else:
        pass

if __name__ == '__main__':

    tf.compat.v1.app.run(main)