import csv
import sqlite3
import os
import pandas as pd

def import_csv_to_sqlite():
    """交互式将CSV文件导入SQLite数据库"""
    print("="*50)
    print("CSV文件导入SQLite数据库工具")
    print("="*50)
    
    # 获取用户输入
    csv_file = 'room_info.csv'.strip()
    db_name = 'room_info.db'.strip()
    table_name = 'room'.strip()
    
    # 验证输入
    if not csv_file or not db_name or not table_name:
        print("错误：所有字段都必须填写！")
        return
    
    if not os.path.exists(csv_file):
        print(f"错误：文件 '{csv_file}' 不存在！")
        return
    
    conn = None
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # 读取CSV文件并获取列名
        with open(csv_file, 'r', encoding='utf-8') as file:
            # 自动检测分隔符
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            
            csv_reader = csv.reader(file, dialect)
            csv_headers = next(csv_reader)  # 读取第一行作为列名
            
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # 获取现有表的列信息
                cursor.execute(f"PRAGMA table_info({table_name})")
                table_columns = [col[1] for col in cursor.fetchall()]
                
                # 检查CSV列是否与表列匹配
                if set(csv_headers) != set(table_columns):
                    print("\n错误：CSV文件列与数据库表列不匹配！")
                    print(f"CSV列: {csv_headers}")
                    print(f"表列: {table_columns}")
                    return
                
                print(f"表已存在，将追加数据到: {table_name}")
            else:
                # 创建新表
                columns = ', '.join([f'"{col}" TEXT' for col in csv_headers])
                create_table_sql = f"CREATE TABLE {table_name} ({columns})"
                cursor.execute(create_table_sql)
                print(f"创建新表: {table_name}")
            
            # 插入数据
            insert_sql = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(csv_headers))})"
            total_rows = 0
            
            # 批量插入（每次1000行）
            batch_size = 1000
            batch = []
            
            for row in csv_reader:
                # 跳过空行
                if not any(row):
                    continue
                    
                batch.append(row)
                if len(batch) >= batch_size:
                    cursor.executemany(insert_sql, batch)
                    total_rows += len(batch)
                    batch = []
            
            # 插入剩余行
            if batch:
                cursor.executemany(insert_sql, batch)
                total_rows += len(batch)
        
        # 提交事务
        conn.commit()
        
        print("\n" + "="*50)
        print(f"导入成功！数据库: {db_name}, 表: {table_name}")
        print(f"共导入 {total_rows} 行数据")
        print("="*50)
        
        # 询问用户是否预览数据
        preview = input("\n是否预览数据？(y/n): ").strip().lower()
        if preview == 'y':
            try:
                # 使用Pandas读取并显示前5行
                df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
                print("\n前5行数据预览:")
                print(df)
            except ImportError:
                # 如果Pandas不可用，使用普通方法
                print("\n前5行数据预览:")
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                for row in cursor.fetchall():
                    print(row)
        
        # 询问用户是否查看表结构
        schema = input("\n是否查看表结构？(y/n): ").strip().lower()
        if schema == 'y':
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("\n表结构:")
            for col in columns:
                print(f"列名: {col[1]}, 类型: {col[2]}")
    
    except Exception as e:
        print(f"\n错误: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
        print("\n操作完成！")

if __name__ == "__main__":
    import_csv_to_sqlite()
