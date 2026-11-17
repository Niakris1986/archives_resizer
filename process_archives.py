import os

def split_file(file_path, chunk_size_gb=1.6):
    file_size = os.path.getsize(file_path)
    chunk_size = int(chunk_size_gb * 1024 * 1024 * 1024)
    
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    download_dir = os.path.join(dir_name, 'download')
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")
    
    part_num = 1
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            part_name = f"{base_name}.part{part_num}"
            part_path = os.path.join(download_dir, part_name)
            
            with open(part_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            
            print(f"Created: {part_path} ({len(chunk)} bytes)")
            part_num += 1

def main():
    root_dir = 'сливы'
    # Расширения архивов
    archive_extensions = ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz')
    # Размер 1.5 - 1.7 ГБ -> возьмем 1.5 ГБ (1.5 * 1024^3 bytes)
    min_size = 1.5 * 1024 * 1024 * 1024
    
    for root, dirs, files in os.walk(root_dir):
        # Пропускаем папки download, чтобы не обрабатывать уже разбитые части
        if 'download' in dirs:
            dirs.remove('download')
            
        for file in files:
            if file.lower().endswith(archive_extensions):
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    if size > min_size:
                        print(f"Processing: {file_path} (Size: {size / (1024**3):.2f} GB)")
                        split_file(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    main()
