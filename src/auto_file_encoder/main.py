import os
from chardet import detect
import argparse


def search_dir(dirname):
    result_list = []
    all_names = os.listdir(dirname)

    for name in all_names:
        full_path = os.path.join(dirname, name)
        if os.path.isdir(full_path):
            result_list.extend(search_dir(full_path))
        else:
            result_list.append(full_path)

    return result_list


def get_encoding_type(filepath):
    with open(filepath, 'rb') as f:
        raw_data = f.read()
    codec = detect(raw_data)
    return codec['encoding']


INCLUDE_EXT_LIST = [".txt", ".smi"]

parse = argparse.ArgumentParser()
parse.add_argument("-f", type=str)
parse.add_argument("-e", nargs="+")  # 쭉 이어서 리스트로 넘어오게됌
args = parse.parse_args()

if args.f is not None:
    path = args.f
    file_list = search_dir(path)

    if args.e is not None:
        if len(args.e) > 0:
            INCLUDE_EXT_LIST = [ext.lower() if ext[0:1] == "." else ".{}".format(ext.lower()) for ext in args.e]
            # INCLUDE_EXT_LIST = []
            # for ext in args.e:
            #     if ext[0:1] == ".":
            #         INCLUDE_EXT_LIST.append(ext)
            #     else:
            #         INCLUDE_EXT_LIST.append("." + ext)

    for file in file_list:
        filename, ext = os.path.splitext(file)

        tempfile = filename + "_tmp" + ext
        if ext.lower() in INCLUDE_EXT_LIST:
            encoding = get_encoding_type(file)
            if encoding.lower().find("utf") < 0:
                try:
                    with open(file, 'r') as read, open(tempfile, 'w', encoding='utf-8') as write:
                        write.write(read.read())

                    os.unlink(file)  # 원본 삭제
                    os.rename(tempfile, file)  # tmp의 파일명을 원본으로 바꿔줌
                    print("{} 이 포맷 변환되어 저장되었습니다.".format(file))
                except:
                    pass
                finally:
                    if os.path.exists(tempfile):
                        os.unlink(tempfile)
