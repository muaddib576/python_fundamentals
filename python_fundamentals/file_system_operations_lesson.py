from pathlib import Path

def excercise9():

    cwd = Path.cwd()

    for f in cwd.iterdir():
        if f.name.startswith('.') or f.name.startswith('__'):
            continue
        if f.is_dir():
            print(f"{f.name}/")
            continue
        print(f.name)
        

def excercise10():

    cwd = Path.cwd()

    for f in cwd.rglob("*.txt"):
        print(f.name)

def excercise11():

    tmp = Path.cwd() / "data" / "tmp"
    tmp.mkdir(exist_ok=True)

def excercise12():

    tmp = Path.cwd() / "data" / "tmp"
    tmp.rmdir()


def excercise13():

    tmp = Path.cwd() / "data" / "tmp"
    for f in range(1,10):
        tmp2 = tmp / f"file_{f}.txt"
        tmp2.touch()

def excercise14():

    tmpdel = Path("data/tmp/file_2.txt")
    user_check = input(f"Are you sure you want to delete?").lower()

    if user_check in ("yes","y"):
        tmpdel.unlink(missing_ok=True)


def excercise15():
    path = Path.cwd() / "data" / "tmp" / "file_2.txt"
    target = Path.cwd() / "data" / "tmp" / "file_02.txt"

    if target.exists():
        print(f"-----{target} already exists.-----")
        return
    path = path.replace(target)
    print(f"-----{path} remamed to {target}-----")



def excercise16():

    path = Path.cwd() / "data" / "tmp"

    for f in path.glob("file_*.txt"):
        if len(f.name) > 10:
            continue

        num = f.name[5:6]
        target = path / f"file_0{num}.txt"

        if target.exists():
            print(f"-- {target.name} already exists --")
            continue
        
        f.replace(target)
        print(f"-- {f.name} changed to {target.name} --")
        

excercise16()