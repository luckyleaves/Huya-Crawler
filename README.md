# 虎牙直播数据分析平台

这个项目是一个全面的虎牙直播数据分析平台，能够从虎牙直播平台抓取房间信息、弹幕数据（普通弹幕和礼物弹幕）以及用户信息，并将这些数据存储到SQLite数据库中，最后提供可视化分析功能。

## 项目结构

```
project/
├── data_processing/           # 数据处理模块
│   ├── csv_to_db1.py          # 房间信息导入数据库
│   ├── csv_to_db2.py          # 普通弹幕导入数据库
│   ├── csv_to_db3.py          # 礼物弹幕导入数据库
│   └── data_visualizer.py     # 数据可视化工具
├── data_collection/           # 数据采集模块
│   ├── get_link.py            # 获取游戏分类链接
│   ├── get_Anchor_link.py     # 获取直播间链接
│   ├── huya_Bulletscreen.py   # 弹幕监听采集
│   ├── huya_room_info_crawler.py  # 房间信息采集
│   └── usermessage.py         # 用户信息采集
├── server.py                  # 主控制程序
└── README.md                  # 项目说明文档
```

## 主要功能

1. **数据采集**
   - 获取虎牙平台游戏分类链接
   - 提取直播间链接
   - 采集房间详细信息（标题、热度、主播信息等）
   - 实时监听普通弹幕和礼物弹幕
   - 采集弹幕用户信息（性别、等级、地理位置等）

2. **数据处理**
   - 将CSV数据导入SQLite数据库
   - 支持批量导入和增量导入
   - 自动检测CSV文件分隔符

3. **数据分析与可视化**
   - 数据预览与统计信息查看
   - 表结构查看
   - 数据维度分析
   - 交互式数据探索

## 安装与使用

### 环境要求

- Python 3.7+
- Edge浏览器
- Edge WebDriver

### 依赖安装

```bash
pip install -r requirements.txt
```

### 使用说明

1. **启动主控制程序**

```bash
python server.py
```

2. **主菜单选项**

```
1. 获取全部房间信息
2. 获取所有房间10000条弹幕信息
3. 监听单个房间弹幕
4. 采集弹幕用户信息
5. 获取单个房间主播信息
6. 启动交互式可视化SQLite数据库
7. 退出
```

3. **数据采集流程**
   - 选择1获取所有房间信息
   - 选择2采集所有房间的弹幕数据
   - 选择3监听特定房间的弹幕
   - 选择5获取特定房间的主播信息
4. **数据分析**
   - 选择6启动可视化工具
   - 输入数据库文件名和表名
   - 选择数据预览或统计信息查看

## 额外注意事项

1. **Edge WebDriver 安装**
   - 下载与您Edge浏览器版本匹配的 [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
   - 将 `msedgedriver.exe` 放在项目目录或系统PATH路径中
   - 在 `huya_room_info_crawler.py` 中更新WebDriver路径：

```python
edgedriver_path = r'C:\path\to\your\msedgedriver.exe'  # 修改为你的实际路径
```

1. **浏览器兼容性**

   - 确保已安装最新版 Microsoft Edge 浏览器
   - Selenium 与浏览器版本需匹配，否则可能出现兼容性问题

2. **无头模式支持**

   - 如果需要在服务器环境运行，确保系统支持无头浏览器模式

   - Linux系统可能需要安装额外依赖：

     ```bash
     sudo apt-get install xvfb
     ```

## 技术栈

- **数据采集**：Selenium, BeautifulSoup, Requests
- **数据处理**：Pandas, SQLite3, CSV
- **数据可视化**：Matplotlib, Seaborn
- **交互界面**：命令行交互菜单

## 文件说明

| 文件                        | 功能                 |
| --------------------------- | -------------------- |
| `get_link.py`               | 获取虎牙游戏分类链接 |
| `get_Anchor_link.py`        | 提取直播间链接       |
| `huya_room_info_crawler.py` | 采集房间详细信息     |
| `huya_Bulletscreen.py`      | 实时监听弹幕         |
| `usermessage.py`            | 采集用户信息         |
| `csv_to_db*.py`             | CSV数据导入数据库    |
| `data_visualizer.py`        | 数据可视化工具       |
| `server.py`                 | 主控制程序           |

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目仓库
2. 创建新的功能分支 (`git checkout -b feature/new-feature`)
3. 提交修改 (`git commit -am 'Add new feature'`)
4. 推送分支 (`git push origin feature/new-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。
