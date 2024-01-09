# BongoCat Mver 配置管理器<br>BongoCat Mver configuration manager

由于 [BongoCat Mver] 目前未实装切换不同配置的功能，我编写了此套脚本以便快速在不同配置间切换。

[BongoCat Mver]: https://www.bilibili.com/read/readlist/rl191271

## 运行需求

运行本程序只要求 Python（3.6 及以上版本）已安装且添加到 PATH 环境变量。如果不确定，您可以使用命令行运行 `python -V` 来检查。如果 Python 已安装并添加到 PATH，则会显示当前 Python 的版本号。

（注意像 3.10、3.11 这样的版本号读作“三点十”、“三点十一”，它们远比 3.6 要新。）

## 使用

下载本仓库后，将名称包含 `lnnconf` 的各脚本文件复制至 Bongo Cat Mver 主程序所在的文件夹。使用时，双击运行 `lnnconf.bat`（类型：Windows 批处理文件）即可以交互模式启动 lnnconf。另外，也可以使用命令行在该文件夹中执行 `lnnconf`（PowerShell 下为 `.\lnnconf`）后加空格和单条指令来运行。

`lnnconf_apply.bat` 可用来快速运行 `apply` 指令（见下文），例如，您可为 `lnnconf_apply.bat` 创建快捷方式，在快捷方式的属性中，在“目标”末尾添加空格和需要加载的配置名称（如 `"D:\path\to\BongoCat Mver\lnnconf_apply.bat" myconfig`），这样，打开该快捷方式即可快速加载相应的配置。

以下为可用的指令：

### `save`（或 `s`、`add`）

    save 配置名称 包含内容...

保存当前配置。*包含内容*为需要包含的文件或文件夹（用空格分隔），如果不指定，默认为 `img`。另外，保存时也会默认包含 `config.json` 文件，无需指定。

示例：

  *     save myconfig

    将当前的配置保存为 `myconfig`。

  *     save myconfig img\standard

    只保存标准（键鼠）模式的资源文件。

  *     save myconfig img\standard img\keyboard

    只保存标准（键鼠）模式和纯键盘模式的资源文件。

注意，虽然可以只保存部分配置的资源文件，但 `config.json` 仍然包含了所有模式的配置项。因此，加载这种只有部分模式资源文件的配置后，不要尝试将 BongoCat Mver 切换到其他模式，否则可能会导致 BongoCat Mver 崩溃。

<details><summary>没啥用的细节</summary>

保存时如果不希望包含 `config.json` 文件，可在配置名称前添加选项 `--no-config-json`，如：

    save --no-config-json myresources Resources

如果只想保存 `config.json` 文件，而不保存 `img` 文件夹（谁会这样干啊喂！），可以手动指定 `config.json`：

    save myconfigjson config.json

如果配置名称以 `--` 开头（谁会这样起名啊喂！），会出现语法错误，此时需要在名称前加上 `--` 分隔（对 `apply` 和 `delete` 指令也适用）：

    save -- --myconfig img/gamepad

</details>

### `list`（或 `l`、`ls`）

    list

显示所有已保存的配置名称。

### `apply`（或 `a`）

    apply 配置名称

加载已保存的配置。此操作会先删除当前配置的部分文件，不可撤销，请谨慎操作。

### `delete`（或 `d`、`del`、`rm`）

    delete 配置名称...

删除一个或多个（用空格分隔）已保存的配置。此操作不可撤销，请谨慎操作。

示例：

  *     delete config1 config2

---

您也可以使用 `help`、`h` 或 `?` 指令来阅读帮助（不过出于未知原因(?)，用这种方法会显示英文帮助）。

另外，在交互模式下，您可以输入 `exit`、`quit` 或 `q` 来退出。
