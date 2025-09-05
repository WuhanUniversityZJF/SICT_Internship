from elasticsearch import Elasticsearch
from elasticsearch import helpers
import hashlib

def main():
    # 连接ES
    es = Elasticsearch(
        #["127.0.0.1:9200"],
        ["http://127.0.0.1:9200"],
        sniff_on_start=True,
        sniff_on_connection_fail=True,
        sniffer_timeout=60
    )

    # 定义索引名称（确保索引已经存在）
    #index_name = "your_index_name"  # 修改为你的实际索引名称
    index_name="first"
    doc_type = "doc"  # 修改为你的实际类型，默认可以用 "doc"

    # 准备批量插入数据
    insert_infos = []

    # 第一条记录
    person2 = {
        '_op_type': 'index',  # 明确指定操作类型
        '_index': index_name,
        '_type': doc_type,  # 添加 type 字段
        '_id': hashlib.md5('李四20'.encode('utf-8')).hexdigest(),  # 生成唯一的 ID
        '_source': {
            'name': '李四',
            'age': 20,
            'tags': '有极强的领导艺术，公正严明铁面无私，公私分明。关心他人无微不至，体贴入微。精力充沛，并有很强的事业心。气吞山河正气凛然，善于同各种人员打交道。'
        }
    }

    # 第二条记录
    person3 = {
        '_op_type': 'index',
        '_index': index_name,
        '_type': doc_type,  # 添加 type 字段
        '_id': hashlib.md5('王五19'.encode('utf-8')).hexdigest(),  # 生成唯一的 ID
        '_source': {
            'name': '王五',
            'age': 19,
            'tags': '尊敬师长团结同学，乐于助人学习勤奋，用心向上，用心参加班级学校组织的各种课内外活动。用心开展批评与自我批评。'
        }
    }

    # 第一条记录
    person4 = {
        '_op_type': 'index',  # 明确指定操作类型
        '_index': index_name,
        '_type': doc_type,  # 添加 type 字段
        '_id': hashlib.md5('老六22'.encode('utf-8')).hexdigest(),  # 生成唯一的 ID
        '_source': {
            'name': '老六',
            'age': 22,
            'tags': '666'
        }
    }

    insert_infos.append(person2)
    insert_infos.append(person3)
    insert_infos.append(person4)

    # 执行批量插入
    try:
        response = helpers.bulk(client=es, actions=insert_infos)
        print(f"成功插入 {response[0]} 条文档")
    except Exception as e:
        print(f"插入数据时发生错误: {str(e)}")

    # 根据 age 字段检索年龄大于等于 20 的文档
    query = {
        "query": {
            "range": {
                "age": {
                    "gte": 20  # gte: greater than or equal to
                }
            }
        }
    }

    # 执行检索
    try:
        search_response = es.search(index=index_name, body=query)
        total_hits = search_response['hits']['total']

        # 如果是 Elasticsearch 7.x 或更高版本，total 是一个整数
        if isinstance(total_hits, dict):
            total_hits = total_hits['value']

        print(f"检索到 {total_hits} 条符合条件的文档")

        # 输出检索结果
        for hit in search_response['hits']['hits']:
            print(hit['_source'])  # 输出每条文档的内容

    except Exception as e:
        print(f"检索数据时发生错误: {str(e)}")


if __name__ == '__main__':
    main()

