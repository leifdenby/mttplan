import fileinput
import re

RE_TASK = re.compile(r'^- ([^:]*):? ?([^\[\]]*) \[([\.\d]+)\]')
TASK_FMT = "task add +@work pro:{project} {desc} est:{est}"

def _esc(s):
    return s.replace("'", "\\'").replace('"', '\\"')

def main(fn_input, project):
    text = ''
    with open(fn_input) as fh:
        for line in fh.readlines():
            if line.startswith('#'):
                if line.strip() != "# TODO":
                    break
                else:
                    continue
            text += line

    paragraphs = text.strip().split('\n\n')

    paragraphs = [p.replace('\n ', '') for p in paragraphs]

    pro = {}
    for p in paragraphs:
        if p.startswith('..'):
            pro[1] = p[2:]
            desc = None
        elif p.startswith('.'):
            pro = {0: p[1:]}
            desc = None
        elif p.startswith('- '):
            desc, notes, t_est = RE_TASK.findall(p)[0]

        if desc is not None:
            pro_s = ".".join([project] + pro.values())
            print(TASK_FMT.format(project=pro_s, desc=_esc(desc), est=t_est))


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input')
    argparser.add_argument('project')
    args = argparser.parse_args()

    main(fn_input=args.input, project=args.project)
