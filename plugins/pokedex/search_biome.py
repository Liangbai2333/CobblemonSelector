import Levenshtein
from pypinyin import lazy_pinyin

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import biome_map

cn_index = {}
en_index = {}
pinyin_map = {}
biome_set = set()

def build_biome_index():
    biome_set.clear()

    for biome in biome_map.values():
        biome_set.add(biome)

    for biome in biome_set:
        # 处理中文名索引
        cn_first = biome.get_i18n_name()[0]
        if cn_first not in cn_index:
            cn_index[cn_first] = []
        cn_index[cn_first].append(biome)

        # 缓存拼音
        pinyin_map[biome] = ''.join(lazy_pinyin(biome.get_i18n_name()))

        # 处理英文名索引
        en_first = biome.translation_name[0].lower()
        if en_first not in en_index:
            en_index[en_first] = []
        en_index[en_first].append(biome)


def search_biome(query, threshold=0.5) -> list[tuple[Biome, float, str]]:
    """
    搜索宝可梦
    参数:
    query: 搜索关键词
    threshold: 相似度阈值
    返回:
    匹配的宝可梦列表，按相似度排序
    """
    if not query:
        return []
    # 准备查询
    query_lower = query.lower()  # 转为小写
    query_pinyin = ''.join(lazy_pinyin(query))
    # 获取候选
    candidates = set()
    # 通过首字母索引获取候选
    if query and query[0] in cn_index:
        candidates.update(cn_index[query[0]])
    if query and query_lower[0] in en_index:
        candidates.update(en_index[query_lower[0]])
    # 如果候选为空，使用所有
    if not candidates:
        candidates = biome_set
    # 计算相似度
    matches = []
    for biome in candidates:
        cn_name = biome.get_i18n_name()
        en_name = biome.translation_name
        en_name_lower = en_name.lower() if en_name else ""  # 转为小写
        # 使用缓存的拼音
        cn_pinyin = pinyin_map.get(biome, ''.join(lazy_pinyin(cn_name)))
        # 计算相似度 - 对英文名忽略大小写
        cn_similarity = Levenshtein.ratio(query, cn_name)
        cn_pinyin_similarity = Levenshtein.ratio(query_pinyin, cn_pinyin)
        en_similarity = Levenshtein.ratio(query_lower, en_name_lower)  # 两边都用小写比较
        # 取最大相似度
        max_similarity = max(cn_similarity, cn_pinyin_similarity, en_similarity)
        # 匹配类型
        if max_similarity == cn_similarity:
            match_type = "中文匹配"
        elif max_similarity == cn_pinyin_similarity:
            match_type = "拼音匹配"
        else:
            match_type = "英文匹配"
        if max_similarity >= threshold:
            matches.append((biome, max_similarity, match_type))
    return sorted(matches, key=lambda x: x[1], reverse=True)

