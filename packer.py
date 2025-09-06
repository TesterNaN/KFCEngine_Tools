import struct
import os
import sys
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad

class EnhancedDATPacker:
    def __init__(self):
        self.key = b'MullenMullenMullenMullen'    # 3DES加密使用的密钥
        self.iv = b'Yukihota'    # DES加密使用的偏移量
        self.identifier = ""

    def pack_directory(self, input_dir, output_path):
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"输入目录不存在: {input_dir}")
        
        # 获取所有文件并验证后缀一致性
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        if not files:
            raise ValueError("文件夹中没有有效文件")
            
        # 提取标识符（文件后缀名）
        sample_file = files[0]
        self.identifier = os.path.splitext(sample_file)[1][1:].ljust(3, ' ')[:3]
        
        # 收集文件并加密
        entries = []
        current_offset = self._calculate_header_size(len(files))
        
        for i, filename in enumerate(files):
            filepath = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            
            # 名称处理：截断到7字符+填充空字节
            name_bytes = base_name.encode('utf-8')[:7]
            name_padded = name_bytes + b'\x00' * (8 - len(name_bytes))
            
            try:
                with open(filepath, 'rb') as f:
                    raw_data = f.read()
                encrypted = self._encrypt_data(raw_data)
                size = len(encrypted)
                
                entries.append({
                    'name': name_padded,
                    'size': size,
                    'offset': current_offset,
                    'data': encrypted
                })
                
                print(f"条目 {i}: {filename} [加密后大小: {size} bytes]")
                current_offset += size
            except Exception as e:
                print(f"处理文件 {filename} 失败: {str(e)}")
        
        # 写入DAT文件
        self._write_dat_file(output_path, entries)
        print('='*40)
        print('\n')
        print(f"打包完成! 输出文件: {os.path.abspath(output_path)}")

    def _calculate_header_size(self, num_entries):
        # 头部结构: [4字节条目数] + [4字节标识符] + [每个条目16字节]
        return 4 + 4 + (16 * num_entries)

    def _encrypt_data(self, data):
        cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        # PKCS#7填充确保块大小对齐
        padded = pad(data, DES3.block_size, style='pkcs7')
        return cipher.encrypt(padded)

    def _write_dat_file(self, output_path, entries):
        total_size = self._calculate_header_size(len(entries))
        for entry in entries:
            total_size += entry['size']
        
        with open(output_path, 'wb') as f:
            # 写入头部
            f.write(struct.pack('<i', len(entries)))  # 条目数
            # 标识符写入4字节（前3字节有效，第4字节保留）
            f.write(self.identifier.encode('ascii', errors='ignore')[:3].ljust(4, b'\x00')[:4])
            
            # 写入条目信息
            for entry in entries:
                f.write(entry['name'])     # 8字节名称
                f.write(struct.pack('<i', entry['size']))   # 4字节大小
                f.write(struct.pack('<i', entry['offset'])) # 4字节偏移量
            
            # 写入加密数据
            for entry in entries:
                f.seek(entry['offset'])
                f.write(entry['data'])

if __name__ == "__main__":
    print("KFC自研引擎DAT封包工具 v2.0\n")
    input_dir = input("请输入要封包的文件夹路径: ").strip()
    
    if not os.path.isdir(input_dir):
        print("错误: 路径不是有效的目录")
        sys.exit(1)
    
    # 确保输出路径有效
    output_path = os.path.join(os.getcwd(), os.path.basename(input_dir) + ".dat")
    print(f"输出文件: {output_path}\n")
    
    packer = EnhancedDATPacker()
    try:
        packer.pack_directory(input_dir, output_path)
    except Exception as e:
        print(f"封包过程中出错: {str(e)}")
    

