# KFC自研引擎DAT文件解包/封包工具

## 项目简介
本工具集专为Kid Fans Club（KFC）自研Galgame引擎设计的DAT资源包处理工具，包含：
- **解包工具**：`unpacker.py`（单文件解包）和`unpacker_batch.py`（批量解包）
- **封包工具**：`packer.py`（文件夹打包为DAT）

理论上可以通过自行修改封包，实现用该引擎开发其他的Galgame

## 功能特性
- 支持单文件/批量解包模式
- 自动识别文件标识符并适配输出文件格式（wav/png/xml）
- 保留原始文件名与目录结构
- 一键封包，实现游戏资源的高效重建。


## 使用说明
### 环境准备
1. 安装Python 3.x
2. 安装必要依赖：
   ```bash
   pip install pycryptodome
   ```

### 解包操作
- 你可以访问此链接下载Kid Fans Club自研引擎的代表作 秋之回忆2 Pure Story ～雪萤～ 进行试验

  地址：https://www.lanzouq.com/b00q0siape 密码:3fnf

#### 单文件解包
```bash
python unpacker.py
输入文件名：Bgm.dat
输出目录: D:\Memories Off Yukihota\output\Bgm
条目 0: BGM01 [偏移量: 328, 大小: 3335264 bytes]
成功解密并保存: output\Bgm\BGM01.wav (3335258 bytes)
......
========================================

DAT文件解包完成！
```

#### 批量解包
```bash
python unpacker_batch.py
KFC自研引擎DAT解包工具 v1.0

输出目录: D:\Memories Off Yukihota\output\Bg
条目 0: BG06AS [偏移量: 1272, 大小: 148472 bytes]
成功解密并保存: output\Bg\BG06AS.png (148465 bytes)
............
输出目录: D:\Memories Off Yukihota\output\Bgm
条目 0: BGM01 [偏移量: 328, 大小: 3335264 bytes]
成功解密并保存: output\Bgm\BGM01.wav (3335258 bytes)
............
输出目录: D:\Memories Off Yukihota\output\Chara
条目 0: BGM01 [偏移量: 328, 大小: 3335264 bytes]
成功解密并保存: output\Bgm\BGM01.wav (3335258 bytes)
............
输出目录: D:\Memories Off Yukihota\output\Script
条目 0: BGM01 [偏移量: 328, 大小: 3335264 bytes]
成功解密并保存: output\Bgm\BGM01.wav (3335258 bytes)
............
========================================

全部DAT文件解包完成！
```

### 封包操作
```bash
python packer.py
KFC自研引擎DAT封包工具 v2.0

请输入要封包的文件夹路径: .\output\bg1
输出文件: D:\Memories Off Yukihota\bg1.dat

条目 0: BG06AS.png [加密后大小: 148472 bytes]
条目 1: BG06AW.png [加密后大小: 132128 bytes]
.............
条目 78: SBG26.png [加密后大小: 114648 bytes]
========================================

打包完成! 输出文件: D:\Memories Off Yukihota\bg1.dat
```

## 关键参数说明
| 参数 | 说明 |
|------|------|
| 密钥 | 默认密钥：`b'MullenMullenMullenMullen'`（32字节）|
| IV | 默认IV：`b'Yukihota'`（8字节）|

## 技术细节说明
| 参数 | 说明 |
|------|------|
| 文件头结构 | 4字节条目数 + 4字节标识符 + (16字节×条目数) |
| 加密模式 | 3DES-CBC |
| 填充方式 | PKCS#7 |

## 使用注意事项
1. **文件后缀一致性**：封包文件夹内所有文件必须使用相同后缀（如全为.wav），标识符取自首个文件后缀
2. **文件名限制**：文件名最多支持7个有效字符（如`LongFilename`→`LongFil`）
3. **密钥设置**：内置密钥/IV为Memories Off Yukihota游戏内提取，如果需要解包其他同引擎游戏需要修改密钥
4. **路径规范**：
   - 解包输出目录自动创建（如`output/audio`）
   - 封包输出文件名为`文件夹名.dat`

## 常见问题解决
### 解包失败处理
- 检查DAT文件是否完整（可通过文件头条目数验证）
- 确认文件未被其他程序占用
- 尝试使用备份文件重新解包

### 封包失败处理
- 确认文件夹内文件后缀一致
- 检查文件名是否包含特殊字符
- 确保磁盘空间充足

## 贡献指南
欢迎提交Issue反馈问题或贡献代码，请遵循以下规范：
- 提交前请运行`flake8`进行代码风格检查
- 新增功能需包含单元测试
- 文档更新需同步修改README

## 许可证
本工具采用GNU GPL v3.0许可证开源，允许商业使用，但需遵守相关条款。
