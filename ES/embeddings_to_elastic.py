# from elasticsearch import Elasticsearch, helpers
# import json
# import hashlib
# import os
#
# def main():
#     # 连接 Elasticsearch
#     es = Elasticsearch(
#         "http://127.0.0.1:9200",
#         sniff_on_start=True,
#         sniff_on_node_failure=True,
#         min_delay_between_sniffing=60
#     )
#
#     # 检查连接是否成功
#     if not es.ping():
#         raise ValueError("Elasticsearch 服务未启动，请检查服务状态！")
#
#     # 定义索引名称和类型（Elasticsearch 6.x 需要指定 _type）
#     index_name = "embeddings"  # 修改为你的实际索引名称
#     doc_type = "_doc"  # Elasticsearch 6.x 推荐使用 "_doc" 作为类型
#
#     # 创建索引（如果不存在）
#     if not es.indices.exists(index=index_name):
#         es.indices.create(index=index_name)
#
#     # 定义要导入的文件列表
#     json_files = [
#         "embedding_01.json",
#         "embedding_02.json",
#         "embedding_03.json",
#         "embedding_04.json"
#     ]
#
#     # 准备批量插入数据
#     insert_infos = []
#
#     # 遍历 JSON 文件并导入数据
#     for file_name in json_files:
#         if os.path.exists(file_name):
#             with open(file_name, "r", encoding="utf-8") as file:
#                 data = json.load(file)
#                 # 生成唯一的 ID
#                 unique_id = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
#                 # 构造批量插入的文档
#                 insert_info = {
#                     '_op_type': 'index',
#                     '_index': index_name,
#                     '_type': doc_type,
#                     '_id': unique_id,
#                     '_source': data
#                 }
#                 insert_infos.append(insert_info)
#         else:
#             print(f"文件 {file_name} 不存在，跳过。")
#
#     # 执行批量插入
#     try:
#         response = helpers.bulk(client=es, actions=insert_infos)
#         print(f"成功插入 {response[0]} 条文档")
#         if response[1]:  # 如果有失败的文档
#             print("部分文档插入失败，失败详情：")
#             print(response[1])
#     except Exception as e:
#         print(f"插入数据时发生错误: {str(e)}")
#
#     # 检查索引中的文档数量
#     try:
#         index_status = es.indices.stats(index=index_name)
#         doc_count = index_status['_all']['primaries']['docs']['count']
#         print(f"索引 {index_name} 中的文档数量: {doc_count}")
#     except Exception as e:
#         print(f"检查索引状态时发生错误: {str(e)}")
#
#     # 示例：查询所有文档
#     query = {
#         "query": {
#             "match_all": {}
#         }
#     }
#
#     # 执行检索
#     try:
#         search_response = es.search(index=index_name, body=query)
#         total_hits = search_response['hits']['total']
#
#         # 在 6.x 中，total 是一个整数
#         print(f"检索到 {total_hits} 条符合条件的文档")
#
#         # 输出检索结果
#         for hit in search_response['hits']['hits']:
#             print(hit['_source'])  # 输出每条文档的内容
#
#     except Exception as e:
#         print(f"检索数据时发生错误: {str(e)}")
#
#
# if __name__ == '__main__':
#     main()



from elasticsearch import Elasticsearch, helpers
import json
import hashlib
import os

def main():
    # 连接 Elasticsearch
    es = Elasticsearch(
        "http://127.0.0.1:9200",
        sniff_on_start=True,
        sniff_on_node_failure=True,
        min_delay_between_sniffing=60
    )

    # 检查连接是否成功
    if not es.ping():
        raise ValueError("Elasticsearch 服务未启动，请检查服务状态！")

    # 定义索引名称和类型（Elasticsearch 6.x 需要指定 _type）
    index_name = "embeddings"  # 修改为你的实际索引名称
    doc_type = "_doc"  # Elasticsearch 6.x 推荐使用 "_doc" 作为类型

    # 创建索引（如果不存在）
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"索引 {index_name} 创建成功")
    else:
        print(f"索引 {index_name} 已存在")

    # 定义要导入的文件列表
    json_files = [
        "embedding_01.json",
        "embedding_02.json",
        "embedding_03.json",
        "embedding_04.json"
    ]

    # 准备批量插入数据
    insert_infos = []

    # 遍历 JSON 文件并导入数据
    for file_name in json_files:
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                try:
                    data_list = json.load(file)  # 读取整个数组
                    for data in data_list:  # 遍历数组中的每个对象
                        # 生成唯一的 ID
                        unique_id = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
                        # 构造批量插入的文档
                        insert_info = {
                            '_op_type': 'index',
                            '_index': index_name,
                            '_type': doc_type,
                            '_id': unique_id,
                            '_source': data
                        }
                        insert_infos.append(insert_info)
                except json.JSONDecodeError as e:
                    print(f"JSON 文件 {file_name} 格式错误: {e}")
                    continue
        else:
            print(f"文件 {file_name} 不存在，跳过。")

    # 执行批量插入
    try:
        response = helpers.bulk(client=es, actions=insert_infos)
        print(f"成功插入 {response[0]} 条文档")
        if response[1]:  # 如果有失败的文档
            print("部分文档插入失败，失败详情：")
            print(response[1])
    except Exception as e:
        print(f"插入数据时发生错误: {str(e)}")

    # 手动刷新索引
    es.indices.refresh(index=index_name)

    # 检查索引中的文档数量
    try:
        index_status = es.indices.stats(index=index_name)
        doc_count = index_status['_all']['primaries']['docs']['count']
        print(f"索引 {index_name} 中的文档数量: {doc_count}")
    except Exception as e:
        print(f"检查索引状态时发生错误: {str(e)}")

    # 示例：查询所有文档
    query = {
        "query": {
            "match_all": {}
        }
    }

    # 执行检索
    try:
        search_response = es.search(index=index_name, body=query)
        total_hits = search_response['hits']['total']

        # 在 6.x 中，total 是一个整数
        print(f"检索到 {total_hits} 条符合条件的文档")

        # 输出检索结果
        for hit in search_response['hits']['hits']:
            print(hit['_source'])  # 输出每条文档的内容

    except Exception as e:
        print(f"检索数据时发生错误: {str(e)}")


if __name__ == '__main__':
    main()