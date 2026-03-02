<table>
  <tr>
        <th>日期</th>
        <th>功能点</th>
        <th>版本号</th>
  </tr>
  <tr>
    <th>2017.11.30</th>
        <th>基础功能见下文</th>
    <th>1.0</th>
  </tr>
  <tr>
    <th>2018.02.09</th>
        <th>1.日志路径选择 2.设置焦点元素 3.历史记录的批量删除 4.触发元素事件 5.清缓存--菜单</th>
    <th>1.1</th>
  </tr>
</table>

# xul-debugtool
## 一、项目资料
### 1.[项目整体流程](http://github.com/starcor-company/XulDebugTool/blob/README/doc/design/flow.puml)<br/>

### 2.[项目设计图](https://github.com/starcor-company/XulDebugTool/blob/README/doc/design/%E8%AE%BE%E8%AE%A1%E5%9B%BE.png)<br/>

### 3.[项目使用指令说明](https://github.com/starcor-company/XulDebugTool/blob/README/doc/debug%20instruction.txt)<br/>

### 4.[项目预期功能列表](https://github.com/starcor-company/XulDebugTool/blob/README/doc/%E5%8A%9F%E8%83%BD%E5%88%97%E8%A1%A8.txt)<br/>

## 编译依赖说明

- PyQt5版本注意事项说明

因主窗口中间区域使用了PyQtWebEngine，在PyQt5的早期版本（比如5.10及以前），QtWebEngineWidgets这个模块是直接打包在PyQt5这个大包里的。
但是，从PyQt5 5.11版本开始，事情发生了变化。Qt WebEngine本身是一个相当庞大且复杂的组件，它基于Chromium内核，包含了大量的C++代码和资源。
为了减小核心PyQt5包的体积，让不需要Web功能的用户安装更快捷，Riverbank Computing（PyQt的官方维护团队）决定将PyQtWebEngine作为一个独立的包来发布。<br>
所以如果PyQt5版本是>=5.11，则PyQt5默认不再包含网页浏览功能。<br>
运行时可能就会出现一些经典报错：<br>
  `ModuleNotFoundError: No module named 'PyQt5.QtWebEngineWidgets'`<br>
因此需要手动安装PyQtWebEngine。

整个依赖链条是这样的：Python程序 -> PyQtWebEngine (Python包) -> PyQtWebEngine-Qt5 (二进制依赖包) -> 系统层面的图形库和依赖。<br>
任何一个环节出问题，都可能导致安装失败或者运行时白屏。

安装后若运行报错：`ImportError: DLL load failed while importing QtWebEngineWidgets: 找不到指定的模块。`<br>
多半是PyQt5环境的问题，请卸载后重装。



## 二、环境配置

### 1、虚拟环境配置

创建虚拟环境（推荐）：
```bash
python -m venv venv
```

激活虚拟环境：
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2、依赖安装

安装项目依赖：
```bash
pip install -r requirements.txt
```

或单独安装核心依赖：
```bash
pip install PyQt5 PyQtWebEngine
```

**注意**：如果PyQt5版本 >= 5.11，需要额外安装PyQtWebEngine：
```bash
pip install PyQtWebEngine
```

### 3、打包应用

项目根目录已包含 `XulDebugTool.spec` 配置文件，直接使用即可：

**使用项目 spec 文件打包：**
```bash
pyinstaller XulDebugTool.spec
```

**spec 文件配置说明：**

项目 spec 文件 (`XulDebugTool.spec`) 已配置以下内容：
- 入口文件：`XulDebugTool/App.py`
- 资源文件：`config` 和 `resources` 目录
- 隐式导入：PyQt5 全家桶、lxml、xmltodict、urllib3、pyperclip 等
- 调试模式：`console=True`（显示控制台，便于调试）

**如需修改配置：**

```bash
# 编辑 XulDebugTool.spec 文件
# 常见修改项：
# - console: True/False  是否显示控制台窗口
# - icon: 'resources/images/icon.ico'  设置应用图标
# - datas: []  添加更多资源文件
# - hiddenimports: []  添加隐式导入的模块
```

**打包后的目录结构：**
```
dist/
└── XulDebugTool.exe    # 可执行文件
```

**打包注意事项**：
- 确保已安装 pyinstaller：`pip install pyinstaller`
- 打包前确保虚拟环境已激活且依赖完整
- 当前配置为单文件打包（--onefile），所有依赖打包进一个 exe
- 如运行时提示缺少模块，在 `hiddenimports` 中添加

## 三、使用方法
### 1、连接页面功能
#### （1）下拉框可输入ip：adbport:xulport（例如：172.31.11.56:55550:55550）,如示例，ip为所连接设备的ip地址，adbport为adb的端口号，xulport为所调试的apk的xul调试端口，两种端口号都可省略，省略adb端口号格式（ip：:xulport）

#### （2）展开下拉框，可以选择最近连接的设备

#### （3）点击connect按钮，连接设备进入主页面

#### （4）点击detail按钮，展示连接日志

![点击连接按钮连接设备](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/connect.png)<br/>

### 2、主页功能
#### （1）菜单栏功能
* file：选中file，单击鼠标右键：（1）Disconnect（退出连接）；（2）ClearCache（清除缓存）；（3）LogPath（设置日志输出路径）

* edit：选中edit，单击鼠标右键：（1）find（查找中部内容区域关键字）；（2）Focus Item（设置焦点元素）

* help：选中help，单击鼠标右键，选择about，此功能为弹出XulDebugTool此款app的简介
![ClearCache And LogPath](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/log_path.png)<br/>
![Focus Item](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/get_focus.png)<br/>

#### （2）左侧列表
* 页面（page）：读取页面以列表形式展示在左侧列表区域

* 用户数据（user-object）：BitmapCache（缓存图片）、DataService（provider）、插件管理器（PluginManager）等用户数据列表

* 插件页面列表（暂未实现）

* 选中左侧列表元素，单击鼠标右键，可以进行选中项名称复制（copy）；还可对provider的数据进行请求（qury-data），查找过的provider会被保存到右侧Faviorities的History中
![provider数据请求](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/querydata.png)<br/>

#### （3）中部内容区域
* 搜索功能：点击菜单栏的edit->find（或者快捷键ctrl + f）,可以呼出搜索框，输入关键字进行搜索

* 筛选功能：搜索框上方是对展示的数据进行筛选（skip-prop：不展示属性、with-children：展示子元素、with-binding-data:展示绑定数据、with-position:展示元素位置信息）

* 元素id可点击，点击后可在右侧进行元素属性和样式设置

* 触发元素事件（列表列出事件为布局文件已有的事件）
![触发元素事件](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/action_excute.png)<br/>

#### （4）右侧列表
* 右侧的Property展示的是属性和样式，属性和样式修改方式：在中部内容区域点击想要改变属性的元素id，在右侧对其属性和样式进行修改（key和value均可修改）<br>
2026关键特性更新：<br>
✅ UI布局重构，新增QSplitter 支持拖动调整上下比例;<br>
✅ Attr和Style设置区域可支持垂直滚动。<br>
✅ ComboBox 紧贴顶部，固定高度;<br>
✅ ListView 高度自适应内容;<br>

* 右侧的Favorities展示的是操作过的provider的历史记录和收藏，provider的数据请求方式：选中左侧列表元素，单击鼠标右键，对provider的数据进行请求（qury-data），此时会弹出一个data-qury的对话框，在where列填入请求参数key，在is列填入对应值，点击request金字那个查找，结果显示在中部内容区域，查找过的provider会被保存到右侧Faviorities的History中。

* provider收藏功能：选中右侧Favorities->History,选中想要收藏的provider，单击鼠标右键，选择收藏，此时，收藏过的provider会出现在History上面的Favorites列表中

* 批量删除记录
![批量删除](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/multiple_del.png)<br/>


#### （5）底部日志输出
* 日志输出框，输出调试工具运行日志，方便开发人员查看问题

* 点击垃圾桶图标，清空日志

## 三、注意事项
### 1.使用之前请检查检查设备是否支持adb

### 2.使用之前请检查所调试apk是否支持XUL调试

## 四、TODO
### 1.完善日志窗口搜索关键字功能

