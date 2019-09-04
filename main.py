import data_loader as dl
import data_utils as du

def update_tag_scheme(sentences, tag_scheme):
    """
    更新为指定编码
    :param sentences:
    :param tag_scheme:
    :return:
    """
    for i, s in enumerate(sentences):
        tags = [w[-1] for w in s]
        if not du.check_bio(tags):
            s_str = '\n'.join(" ".join(w) for w in s)
            raise Exception("输入的句子应为BIO编码，请检查输入句子%i:\n%s" % (i, s_str))
        if tag_scheme == 'BIOES':
            new_tags = du.bio_to_bioes(tags)
            for word, new_tag in zip(s, new_tags):
                word[-1] = new_tag

if __name__ == '__main__':
    res = dl.load_sentences('./data/ner.dev')
    update_tag_scheme(res, "BIOES")
    dico, word_to_id, id_to_word = dl.word_mapping(res)
    dico, tag_to_id, id_to_tag = dl.tag_mapping(res)
    dl.prapare_dataset(res, word_to_id, tag_to_id)