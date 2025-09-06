import struct  
import os  
import sys  
from Crypto.Cipher import DES3  
from Crypto.Util.Padding import unpad  
  
class EnhancedDATProcessor:  
    def __init__(self):  
        self.names = []
        self.offsets = []
        self.sizes = []
        self.identifier = ""

        self.key = b'MullenMullenMullenMullen'    # 3DES加密使用的密钥
        self.iv = b'Yukihota'    # DES加密使用的偏移量
      
    def process_file(self, input_path, output_dir):  
        os.makedirs(output_dir, exist_ok=True)  
        print(f"输出目录: {os.path.abspath(output_dir)}")  
        
        if not os.path.exists(input_path):  
            raise FileNotFoundError(f"文件不存在: {input_path}")  
          
        file_size = os.path.getsize(input_path)  
          
        with open(input_path, 'rb') as f:  
            num_entries = self._read_int(f)  
            self.identifier = self._read_identifier(f)  
            for i in range(num_entries):  
                if f.tell() >= file_size - 16:
                    print(f"警告: 条目 {i} 数据不完整，文件可能损坏")  
                    break  
                
                name = self._read_name(f)  
                size = self._read_int(f)  
                offset = self._read_int(f)  
                
                if offset < 0 or size < 0:  
                    print(f"跳过无效条目 {i}: 偏移量={offset}, 大小={size}")  
                    continue  
                if offset + size > file_size:  
                    print(f"警告: 条目 {i} 数据超出文件范围，偏移量: {offset}, 大小: {size}")  
                  
                self.names.append(name)  
                self.offsets.append(offset)  
                self.sizes.append(size)  
                  
                print(f"条目 {i}: {name} [偏移量: {offset}, 大小: {size} bytes]")  
                
                self._process_entry(input_path, output_dir, i, name, offset, size)  
      
    def _read_int(self, f):  
        return struct.unpack('<i', f.read(4))[0]  
      
    def _read_identifier(self, f):   
        identifier_bytes = f.read(4)[:3]
        return ''.join([chr(b) if 0x20 <= b <= 0x7E else '' for b in identifier_bytes])[:3]  
      
    def _read_name(self, f):  
        name_bytes = f.read(8)  
        if len(name_bytes) < 8:  
            raise EOFError("文件名读取不完整")  
        
        null_pos = name_bytes.find(b'\x00')  
        if null_pos == -1:  
            return name_bytes.decode('utf-8', errors='replace')  
        else:  
            return name_bytes[:null_pos].decode('utf-8')  
      
    def _process_entry(self, input_path, output_dir, entry_index, name, offset, size):   
        output_path = os.path.join(output_dir, f"{name}.{self.identifier}")  
          
        try:
            with open(input_path, 'rb') as f:  
                f.seek(offset)  
                encrypted_data = f.read(size)  
                  
                if len(encrypted_data) != size:  
                    print(f"警告: 条目 {entry_index} 读取的数据量不足，预期: {size} 字节，实际: {len(encrypted_data)} 字节")  
              
            decrypted_data = self._decrypt_data(encrypted_data)  
            
            with open(output_path, 'wb') as out:  
                out.write(decrypted_data)  
            print(f"成功解密并保存: {output_path} ({len(decrypted_data)} bytes)\n")  
              
        except Exception as e:  
            print(f"处理条目 {entry_index} 时出错: {str(e)}")  
      
    def _decrypt_data(self, encrypted_data):  
        cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)  
        
        decrypted = cipher.decrypt(encrypted_data)  

        try:  
            return unpad(decrypted, DES3.block_size)  
        except ValueError as e:  
            raise ValueError(f"解密失败: {str(e)}")

    
  
if __name__ == "__main__":
    input_file = input("输入文件名：")
    output_dir = "output\\"+input_file[:-4]
    
    processor = EnhancedDATProcessor()  

    try:  
        processor.process_file(input_file, output_dir)
        print('='*40)
        print("\nDAT文件解包完成！")
    except Exception as e:  
        print(f"处理过程中出错: {str(e)}")


