import data_utils as du
import codecs
def load_sentences(path):
    """"
    加载数据集，每一行至少包含一个汉字和一个标记
    句子和句子之间是以空格作为分割
    最后返回句子集合
    :param path:
    :return
    """
    # 存放数据集
    sentences = []
    # 临时存放每一个句子
    sentence = []
    for line in codecs.open(path, 'r', encoding='utf-8'):
        # 去除两边的空格
        line = line.strip()
        # 首先判断是不是空，如果是则表示句子和句子之间的分割点
        if not line:
            if len(sentence) > 0:
                sentences.append(sentence)
                # 清空sentence表示一句话完结
                sentence = []
        else:
            if line[0] == " ":
                continue
            else:
                word = line.split()
                assert len(word) >= 2
                sentence.append(word)
    # 循环走完要判断一下，防止最后一个句子没有进入到句子集合中
    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences


def word_mapping(sentences):
    """
    构建字典
    :param sentences:
    :return:
    """
    word_list = [[x[0] for x in s] for s in sentences]
    dico = du.create_dico(word_list)
    dico["<PAD>"] = 10000001
    dico["<UNK>"] = 10000000
    word_to_id, id_to_word = du.create_mapping(dico)
    return dico, word_to_id, id_to_word


def tag_mapping(sentences):
    """
    构建标签字典
    :param sentences:
    :return:
    """
    tag_list = [[x[1] for x in s] for s in sentences]
    dico = du.create_dico(tag_list)
    tag_to_id, id_to_tag = du.create_mapping(dico)
    return dico, tag_to_id, id_to_tag


def prapare_dataset(sentences, word_to_id, tag_to_id, train=True):
    """
    数据预处理，返回list其包含
    -word_list
    -word_id_list
    -word_char_index
    -tag_id_list
    :param sentences:
    :param word_to_id:
    :param tag_to_id:
    :param train:
    :return:
    """
    none_index = tag_to_id['O']
    data = []
    for s in sentences:
        word_list = [ w[0] for w in s]
        word_id_list = [word_to_id[w if w in word_to_id else '<UNK>'] for w in word_list]
        segs = du.get_seg_features("".join(word_list))
        print('aaa')