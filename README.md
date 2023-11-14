这是自用的一个基于Python+PYQT的界面应该程序的模板，为方便于日后开发类似程序方便，所以特此整理，以后会不断的迭代的，有需要的可以拿去！开发环境为 VSCode+Python+PYQT Integration<br>
proot.py 这个是Python程序的启动文件，一般不用修改,负责初始化目录结构和载入配置文件以及调用programs.py中的Program.main启动程序<br>
programs.py 主要负责进行程序的初始化工作(创建QApplication对象，显示主窗体等)<br>
uidefines 窗体描述文件和描述类<br>
uievents 窗体的基类和MainWindow的实现类<br>
uiutil一些常用函数,其中的CFEnv是环境变量及配置文件类,负责初始化配置文件和目录结构<br>
CFEnv负责生成如下目录结构： <br>
bin (用于存放主程序,因为使用PyInstaller等工具编译后的程序文件很多，所以把它们和配置文件及相关数据分开便于管理) <br>
data (用于存放数据)<br>
&nbsp;&nbsp;plugins (用于存放插件数据) <br>
&nbsp;&nbsp;scripts (用于存放脚本数据) <br>
config.json (用于存放配置数据) <br>
config.json.backup (用于存放配置数据的备份，当config.json解析失败时恢复用！)<br>
