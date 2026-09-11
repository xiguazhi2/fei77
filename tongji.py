import os
import tkinter as tk
from tkinter import scrolledtext


def scan_folder(path, level=0):
    """
    递归统计文件夹总文件数量（包含所有子文件夹）
    """

    total_files = 0
    children = []

    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)

            if os.path.isfile(full_path):
                total_files += 1

            elif os.path.isdir(full_path):
                child_total, child_data = scan_folder(
                    full_path,
                    level + 1
                )

                total_files += child_total
                children.append(child_data)

    except PermissionError:
        pass


    folder_name = os.path.basename(path)

    if folder_name == "":
        folder_name = path


    current = {
        "name": folder_name,
        "count": total_files,
        "level": level,
        "children": children
    }

    return total_files, current



def format_result(node, lines):

    indent = "    " * node["level"]

    lines.append(
        f"{indent}📁 {node['name']}   文件总数：{node['count']}"
    )

    for child in node["children"]:
        format_result(child, lines)



def start_scan():

    output.delete(
        "1.0",
        tk.END
    )

    folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    output.insert(
        tk.END,
        f"统计目录：\n{folder}\n\n"
    )

    _, result = scan_folder(folder)

    lines = []

    format_result(
        result,
        lines
    )

    output.insert(
        tk.END,
        "\n".join(lines)
    )



# 窗口
root = tk.Tk()
root.title("文件数量统计工具")
root.geometry("650x550")


output = scrolledtext.ScrolledText(
    root,
    font=("微软雅黑", 12)
)

output.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


button = tk.Button(
    root,
    text="重新统计",
    command=start_scan,
    font=("微软雅黑", 12)
)

button.pack(
    pady=5
)


# 打开自动统计
start_scan()


root.mainloop()