import hashlib

def get_file_hash(file, block_size=2**20):
    md5 = hashlib.md5()
    bytes = file.read(block_size)
    md5.update(bytes)
    file.seek(0)
    return md5.hexdigest()
