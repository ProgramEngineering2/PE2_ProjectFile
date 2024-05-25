import os

from typing import List

def search_xml(target_folder) -> List[str]:
    # 从一个目标文件夹中找到所有的 xml 文件
    xml_files = []
    
    for item in os.listdir(target_folder):
        item_path = os.path.join(target_folder, item)

        if os.path.isdir(item_path):
            xml_files.extend(search_xml(item_path))

        elif 'LMZ' in item and item.endswith('.xml'):
            xml_files.append(item_path)
        
    return xml_files

if __name__ == '__main__':
    data_folder = './dat'
    xml_files = search_xml(data_folder)
    print(xml_files)