import jieba
import math
import random

def check_bio(tags):
    """
    检测输入的tags是否是bio编码
    如果不是bio编码
    那么错误的类型
    1.编码不在bio中
    2.第一个编码是I
    3.当前编码不是B，前一个编码是O
    :param tags:
    :return:
    """
    for i, tag in enumerate(tags):
        if tag == 'O':
            continue
        tag_list = tag.split('-')
        if len(tag_list) != 2 or tag_list[0] not in set(['B', 'I']):
            # 表示非法编码
            return False
        if tag_list[0] == 'B':
            continue
        elif i == 0 or tags[i-1] == "O":
            # 如果第一个位置不是B，或者当前编码不是B并且前一个编码是O，则全部转化为B
            tags[i] = 'B' + tag[1:]
        elif tags[i - 1][1:] == tag[1:]:
            # 如果当前编码的后面类型编码与tags中的前一个编码中后面类型编码相同则跳过
            continue
        else:
            # 如果类型不一致，则重新从B开始编码
            tags[i] = "B" + tag[1:]
    return True


def bio_to_bioes(tags):
    """
    把bio编码转化为bioes编码
    返回新的tags
    :param tags:
    :return:
    """
    new_tags = []
    for i, tag in enumerate(tags):
        if tag == "O":
            # 直接保留，不变化
            new_tags.append(tag)
        elif tag.split('-')[0] == 'B':
            # 如果tag是以B开头，那么我们做如下判断
            # 首先，如果当前tag不是最后一个，并且紧跟着的后一个是I
            if i + 1 < len(tags) and tags[i+1].split('-')[0] == 'I':
                # 直接保留，不变化
                new_tags.append(tag)
            else:
                # tag是一个元素，或着紧跟着后一个不是I，那么表示单字，需要把B换成S表示单字
                new_tags.append(tag.replace('B-', 'S-'))
        elif tag.split('-')[0] == 'I':
            # 如果tag是以I开头，那么部门需要进行下面的判断：
            # 首先，如果当前的tag不是最后一个，并且紧跟着的一个是I
            if i + 1 < len(tags) and tags[i+1].split('-')[0] == 'I':
                # 直接保留，不变化
                new_tags.append(tag)
            else:
                # 如果是最后一个，或者后一个不是I开头的，那么就表示一个词的结尾，就把I换成E
                new_tags.append(tag.replace('I-', 'E-'))
        else:
            raise Exception('非法编码')
    return new_tags


def create_dico(item_list):
    """
    对于item_list中每一个items，统计items中的item在item_list中的次数
    item:出现的次数
    :param item_list:
    :return:
    """
    assert type(item_list) is list
    dico = {}
    for items in item_list:
        for item in items:
            if item not in dico:
                dico[item] = 1
            else:
                dico[item] += 1
    return dico


def create_mapping(dico):
    """
    创建item to id , id to item
    item的排序按词典中出现的次数
    :param dico:
    :return:
    """
    sorted_items = sorted(dico.items(), key=lambda x:(-x[1], x[0]))
    id_to_item = { i:v[0] for i, v in enumerate(sorted_items)}
    item_to_id = {k: v for v, k in id_to_item.items()}
    return item_to_id,id_to_item


def get_seg_features(words):
    """
    利用jieba分词
    采用类似bio的编码，0表示单字成词，1表示一个词的开始，2表示一个词的中间，3表示一个词的结尾
    :param words:
    :return:
    """
    seg_features = []
    word_list = list(jieba.cut(words))
    for word in word_list:
        if len(word) == 1:
            seg_features.append(0)
        else:
            temp = [2] * len(word)
            temp[0] = 1
            temp[-1] = 3
            seg_features.extend(temp)
    return seg_features


class BatchManager(object):
    def __init__(self, data, batch_size):
        self.batch_data = self.sort_and_pad(data, batch_size)
        self.len_data = len(self.batch_data)

    def sort_and_pad(self, data, batch_size):
        num_batch = int(math.ceil(len(data) / batch_size))
        sorted_data = sorted(data, key=lambda x: len(x[0]))
        batch_data = list()
        for i in range(num_batch):
            batch_data.append(self.pad_data(sorted_data[i * batch_size: (i+1)*batch_size]))
        return batch_data
    @staticmethod
    def pad_data(data):
        word_list = []
        word_id_list = []
        seg_list = []
        tag_id_list = []
        max_length = max([len(sentence[0]) for sentence in data])
        for line in data:
            words, word_ids, segs, tag_ids = line
            padding = [0] * (max_length - len(words))
            word_list.append(words + padding)
            word_id_list.append(word_ids + padding)
            seg_list.append(segs + padding)
            tag_id_list.append(tag_ids + padding)
        return [word_list, word_id_list, seg_list, tag_id_list]

    def iter_batch(self, shuffle=False):
        if shuffle:
            random.shuffle(self.batch_data)
        for idx in range(self.len_data):
            yield self.batch_data[idx]