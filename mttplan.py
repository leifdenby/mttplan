import fileinput
import re

RE_TASK = re.compile(r'^- (?P<label>[^:^[]*)(: ?(?P<notes>[\w\d]+))?( \[(?P<t_est>[\.\d]+)\])?$')

def make_task_string(label, tags=[], project=None, t_est=None):
    task_parts = ["task add"]
    if len(tags) > 0:
        task_parts.append(" ".join("+{}".format(t) for t in tags))
    if project is not None and project != '':
        task_parts.append("pro:{}".format(project))
    if t_est is not None:
        task_parts.append("est:{}".format(t_est))
    task_parts.append(label)

    return " ".join(task_parts)

def _esc(s):
    return s.replace("'", "\\'").replace('"', '\\"')

def main(fn_input, tags=[], project=None):
    text = ''
    with open(fn_input) as fh:
        for line in fh.readlines():
            if line.startswith('#'):
                if line.strip() != "# TODO":
                    break
                else:
                    continue
            # handle markdown lists made with `* ` as well
            if line.startswith('* '):
                line = '- ' + line[2:]
            text += line

    paragraphs = text.strip().split('\n\n')

    paragraphs = [p.replace('\n ', '') for p in paragraphs]

    pro = {}
    for p in paragraphs:
        if p.startswith('..'):
            pro[1] = p[2:]
            label = None
        elif p.startswith('.'):
            pro = {0: p[1:]}
            label = None
        elif p.startswith('- '):
            m = RE_TASK.fullmatch(p)
            if m is not None:
                label = m.groupdict()['label']
                t_est = m.groupdict()['t_est']
                # notes are not currently added
                # notes = m.groupdict()['notes']

            label = label.replace("'", "\\'")

        if label is not None:
            project_parts = pro.values()
            if project is not None:
                project_parts = project_parts.insert(0, project)
            pro_s = ".".join(project_parts)

            print(make_task_string(label=label, tags=tags, project=pro_s,
                                   t_est=t_est))


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input')
    argparser.add_argument('--project', default=None)
    argparser.add_argument('--tags', nargs="*", default=["@work",])
    args = argparser.parse_args()

    main(fn_input=args.input, project=args.project, tags=args.tags)
