import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_sqlite_data():
    """交互式可视化SQLite数据库数据"""
    print("="*50)
    print("SQLite数据库数据可视化工具")
    print("="*50)
    
    # 获取用户输入
    db_name = input("请输入数据库文件名（如 mydb.db）: ").strip()
    table_name = input("请输入要可视化的表名: ").strip()
    
    # 验证输入
    if not db_name or not table_name:
        print("错误：所有字段都必须填写！")
        return
    
    if not os.path.exists(db_name):
        print(f"错误：数据库文件 '{db_name}' 不存在！")
        return
    
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_name)
        
        # 检查表是否存在
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            print(f"错误：表 '{table_name}' 在数据库中不存在！")
            return
        
        # 读取整个表到Pandas DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        
        print("\n" + "="*50)
        print(f"成功加载数据！数据库: {db_name}, 表: {table_name}")
        print(f"数据维度: {df.shape[0]} 行 × {df.shape[1]} 列")
        print("="*50)
        
        # 主菜单循环
        while True:
            print("\n[1] 查看数据预览")
            print("[2] 查看数据统计信息")
            print("[3] 退出")
            
            choice = input("\n请选择操作 (1-3): ").strip()
            
            if choice == '1':  # 数据预览
                preview_rows = input("要预览多少行数据? (默认10行): ").strip()
                n = 10 if not preview_rows else int(preview_rows)
                print(f"\n前{n}行数据预览:")
                print(df.head(n))
                
                # 列名查看选项
                see_columns = input("\n是否查看所有列名? (y/n): ").strip().lower()
                if see_columns == 'y':
                    print("\n所有列名:")
                    for i, col in enumerate(df.columns):
                        print(f"{i+1}. {col}")
            
            elif choice == '2':  # 统计信息
                print("\n数据统计摘要:")
                print(df.describe(include='all'))
                
                # 数据类型信息
                print("\n数据类型信息:")
                print(df.dtypes.to_string())
            elif choice == '3':  # 退出
                print("\n感谢使用数据可视化工具！")
                break
            
            else:
                print("无效的选择，请输入1-3之间的数字！")
    
    except Exception as e:
        print(f"\n错误: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("\n需要安装额外库才能运行此工具。")
        print("请运行以下命令安装所需依赖:")
        print("pip install pandas matplotlib seaborn")
        exit(1)
    
    visualize_sqlite_data()
