#!/bin/bash

# 检查参数数量
if [ "$#" -ne 3 ]; then
    echo "用法: $0 <搜索内容> <输入文件> <输出文件>"
    exit 1
fi

# 定义变量
search_term=$1
input_file=$2
output_file=$3

# 检查输入文件是否存在
if [ ! -f "$input_file" ]; then
    echo "错误: 文件 '$input_file' 不存在。"
    exit 1
fi

# 执行搜索并保存结果
grep -n "$search_term" "$input_file" > "$output_file"

# 输出搜索结果到控制台
echo "搜索结果已保存到 '$output_file':"
cat "$output_file"    
