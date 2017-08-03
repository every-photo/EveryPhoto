
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# from fuzzywuzzy import process

def fuzzy_match(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1,lenstr2 + 1):
        d[(-1, j)] = j + 1
 
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]: cost = 0
            else: cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition
 
    return round(1 - d[lenstr1 - 1,lenstr2-1] / ((lenstr1 + lenstr2) >> 1), 3)


def extract(target_str, source_tags, limit = 1):
    if limit >= len(source_tags):
        return source_tags.sort(reverse = True)
    result = source_tags[:limit]
    weight = list(map(fuzzy_match, result, target_str))
    for tag in source_tags:
        temp_weight = fuzzy_match(target_str, tag)
        if weight[-1] < temp_weight:
            weight[-1] = temp_weight
            i = limit - 1
            while temp_weight > weight[i-1] and i > 0:
                weight[i], weight[i-1] = weight[i-1], weight[i]
                i -= 1
            result.insert(i, tag)
            result.pop()
    return result


if __name__ == '__main__':
    # print(fuzzy_match(sys.argv[1], sys.argv[2]))
    source_tags = ['women', 'man', 'girl', 'boy', 'dog', 'pig', 'moon', 'son', 'sun']
    print(extract('sun', source_tags, 2))
    # print(process.extract('sun', source_tags, limit = 2))