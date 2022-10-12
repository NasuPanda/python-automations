import re

# [find and remove common substring with python - Stack Overflow](https://stackoverflow.com/questions/27963222/find-and-remove-common-substring-with-python)
# [Remove specific characters from a string in Python - Stack Overflow](https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python)


def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if i + j < len1 and string1[i + j] == string2[j]:
                match += string2[j]
            else:
                if len(match) > len(answer):
                    answer = match
                match = ""
        if len(match) > len(answer):
            answer = match  # this was missing
    return answer


sentence1 = "DAI0303Z_offset-200::PT4_EngExh_NOX1_Rq_ST3::NOx1_Md67Conf_Rq_ST3"
sentence2 = "DAI0303Z_offset-200::PT4_EngExh_NOX1_Rq_ST3::NOx1_EngExh_Vers_Rq_ST3"

print(sentence1)

ans = longestSubstringFinder(sentence1, sentence2)
print(ans)

# 共通する文字列を削除する


print(re.sub(ans, "", sentence1))
