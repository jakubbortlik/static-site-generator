import os
import shutil


def copy_directory_content(source, destination, level):
    if os.path.exists(destination):
        print(f"{' ' * level}deleting existing destination folder `{destination}`")
        shutil.rmtree(destination)

    print(f"{' ' * level}creating destination folder `{destination}`")
    os.mkdir(destination)

    print(f"{' ' * level}copying from `{source}` to `{destination}`:")
    level += 1
    for file in os.listdir(source):
        full_path = os.path.join(source, file)
        dest_path = os.path.join(destination, file)
        if os.path.isfile(full_path):
            print(f"{' ' * level}cp {full_path} -> {dest_path}")
            shutil.copy(full_path, dest_path)
        else:
            copy_directory_content(full_path, dest_path, level)


def main():
    copy_directory_content("static", "public", 0)


if __name__ == "__main__":
    main()
