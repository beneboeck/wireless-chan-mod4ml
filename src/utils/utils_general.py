import sys
import os
# add the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
import os
import json
import os.path as path

def create_log(global_dic_path, global_dic, overall_path, comment = ''):
    # CREATING FILES AND DIRECTORY
    date_time_now = datetime.datetime.now()
    date_time = date_time_now.strftime('%Y-%m-%d_%H-%M-%S')  # convert to str compatible with all OSs

    key = date_time + comment
    for n in global_dic_path:
        key = key + '_' + n + '=' + str(global_dic_path[n])

    os.makedirs(overall_path, exist_ok = True)
    dir_path = path.join(overall_path, key)
    os.makedirs(dir_path)

    path_exp = path.join(dir_path, "experiment_config.json")

    global_dic.update({'dir_path': dir_path})

    with open(path_exp, "w") as f:
        json.dump(global_dic, f, indent=4)  # indent=4 makes it pretty-printed

    return global_dic