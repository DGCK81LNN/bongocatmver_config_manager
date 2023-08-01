# BongoCat Mver 配置管理器<br>BongoCat Mver configuration manager

由于 [BongoCat Mver] 目前未实装切换不同配置的功能，我编写了此套脚本以便快速在不同配置间切换。

[BongoCat Mver]: https://www.bilibili.com/read/readlist/rl191271

## 运行需求

运行本程序只要求 Python（3.6 及以上版本）已安装且添加到 PATH 环境变量。如果不确定，您可以使用命令行运行 `python -V` 来检查。如果 Python 已安装并添加到 PATH，则会显示当前 Python 的版本号。

（注意像 3.10、3.11 这样的版本号读作“三点十”、“三点十一”，它们远比 3.6 要新。）

## 使用

下载本仓库后，将名为 lnnconf 的各脚本文件和 _lnnconf 文件夹复制至 Bongo Cat Mver 主程序所在的文件夹。使用时，在该文件夹打开命令行（Windows 下在文件夹内空白处按 **Shift+鼠标右键**后选择“**在此处打开命令窗口**”或“**在此处打开 Powershell 窗口**”），然后输入 `.\lnnconf` 后接空格和要执行的指令。

如果您在您的电脑上安装了 Git for Windows 或 MinGW，您可以使用 Bash（Bourne-Again Shell）运行没有扩展名的 `lnnconf` 脚本，进入交互命令行，即可获得更好的使用体验，无需在后续每条指令前加上 `.\lnnconf`；普通（PowerShell）版本暂无此功能。

以下为可用的指令：

### `save`（或 `s`、`add`）

    .\lnnconf save 配置名称 包含内容...

保存当前配置。*包含内容*为需要包含的文件或文件夹（用空格分隔），如果不指定，默认为 `img`。另外，保存时也会默认包含 `config.json` 文件，无需指定。

示例：

  *     .\lnnconf save myconfig

    将当前的配置保存为 `myconfig`。

  *     .\lnnconf save myconfig img\standard

    只保存标准（键鼠）模式的资源文件。以后应用该配置时，不会影响纯键盘和手柄模式的资源文件。

  *     .\lnnconf save myconfig img\standard img\keyboard

    只保存标准（键鼠）模式和纯键盘模式的资源文件。

注意，虽然可以只保存部分配置的资源文件，但 `config.json` 仍然包含了所有模式的配置项。因此，加载这种只有部分模式资源文件的配置后，不要尝试切换模式，否则可能会导致 BongoCat Mver 崩溃。

<details><summary>没啥用的细节</summary>

保存时如果不希望包含 `config.json` 文件，可在配置名称前添加选项 `--no-config-json`，如：

    .\lnnconf save --no-config-json myresources Resources

如果只想保存 `config.json` 文件，而不保存 `img` 文件夹（谁会这样干啊喂！），可以手动指定 `config.json`：

    .\lnnconf save myconfigjson config.json

如果配置名称以 `--` 开头（谁会这样起名啊喂！），会出现语法错误，此时需要在名称前加上 `--` 分隔符（对 `apply` 和 `delete` 指令也适用）：

    .\lnnconf save -- --myconfig img/gamepad

</details>

### `list`（或 `l`、`ls`）

    .\lnnconf list

显示所有已保存的配置名称。

### `apply`（或 `a`）

    .\lnnconf apply 配置名称

加载已保存的配置。此操作会先删除当前配置的部分文件，不可撤销，请谨慎操作。

### `delete`（或 `d`、`del`、`rm`）

    .\lnnconf delete 配置名称...

删除一个或多个（用空格分隔）已保存的配置。此操作不可撤销，请谨慎操作。

示例：

  *     .\lnnconf delete config1 config2

---

您也可以使用 `help`、`h` 或 `?` 指令来阅读帮助（不过出于未知原因(?)，用这种方法会显示英文帮助）。

另外，在交互命令行模式下，您可以输入 `exit`、`quit` 或 `q` 来退出。

<br>

<br>

<br>

---

i hate python<br>
maybe idk
