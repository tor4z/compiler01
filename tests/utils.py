from typing import List
import shlex


def line_split(text: str) -> List[str]:
    output = []
    for line in text.split('\n'):
        if len(line) == 0 or line.isspace():
            continue
        output.append(line)
    return output


def line_cmp(line1: str, line2: str) -> bool:
    line1_splited = shlex.split(line1)
    line2_splited = shlex.split(line2)

    if len(line1_splited) == len(line2_splited):
        for term1, term2 in zip(line1_splited, line2_splited):
            term1 = term1.strip()
            term2 = term2.strip()
            if term1 != term2:
                return False
        return True
    else:
        return False


def doc_cmp(text1: str, text2: str) -> bool:
    text1_lines = line_split(text1)
    text2_lines = line_split(text2)

    text1_line_len = len(text1_lines)
    text2_line_len = len(text2_lines)

    for i in range(min(text1_line_len, text2_line_len)):
        t1_line = text1_lines[i]
        t2_line = text2_lines[i]
        if not line_cmp(t1_line, t2_line):
            return False
    return True
