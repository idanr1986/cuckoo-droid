'''
Created on 2011-11-22

@author: Jinghao

Parser the dex file.
#TODO: odex support.
'''
import struct
import zlib
import hashlib
import DexError

class DexHeader:
    '''
    The format of dex file header.
    '''
    def __init__(self, file_handle, dex_file):
        self._file_handle= file_handle
        self.dex_file = dex_file
        #dex file handle, currently the length is 112
        (self.magic,
         self.checksum,
         self.signature,
         self.fileSize,
         self.headerSize,
         self.endianTag,
         self.linkSize,
         self.linkOff,
         self.mapOff,
         self.stringIdsSize,
         self.stringIdsOff,
         self.typeIdsSize,
         self.typeIdsOff,
         self.protoIdsSize,
         self.protoIdsOff,
         self.fieldIdsSize,
         self.fieldIdsOff,
         self.methodIdsSize,
         self.methodIdsOff,
         self.classDefsSize,
         self.classDefsOff,
         self.dataSize,
         self.dataOff) = struct.unpack("<8sl20s20l",file_handle.read(112))
         
    def calculate_checksum(self):
        """Calculate the actual check sum from the file"""
        #skip 8b magic + 4b checksum
        skip_nonsum = 8 + 4 
        self._file_handle.seek(skip_nonsum)
        data=self._file_handle.read(self.fileSize - skip_nonsum)
        true_checksum=zlib.adler32(data)
        return true_checksum

    def verify_checksum(self):
        """Verify if the file data matches the checksum
            Note: this will read from the dexfile"""
        true_checksum=self.calculate_checksum()
        return true_checksum == self.checksum

    def calculate_signature(self):
        """Calculate the SHA signature from the file"""
        #skip 8b magic + 4b checksum + sha1
        skip_nonsum = 8 + 4 + 20 
        self._file_handle.seek(skip_nonsum)
        data=self._file_handle.read(self.fileSize - skip_nonsum)
        sha1=hashlib.new('sha1')
        sha1.update(data)
        return sha1.digest()
    
    def verify_signature(self):
        """Verify the sha1 signature"""
        true_sig = self.calculate_signature()
        return true_sig == self.signature
    
    #string ids size
    def get_string_count(self):
        return self.stringIdsSize
    
    #string offset
    def get_string_offset(self):
        return self.stringIdsOff
    

class DexFile:
    '''
        The Struct of Dex File.
    '''
    def __init__(self, file_handle):
        self._file_handle = file_handle
        self.dex_header = None
        self.dex_header = self.get_dex_header()
        self.verify_valid()
        self.offset_list = []
        
    def get_dex_header(self):
        """Get the dex header object, either the existing instance or
           load a new instace"""
        if self.dex_header is not None:
            return self.dex_header
        else:
            self.dex_header= DexHeader(self._file_handle, self)
            return self.dex_header
    
    def verify_valid(self):
        if self.dex_header.verify_checksum() and self.dex_header.verify_signature():
            pass
        else:
            raise DexError.DexError('Not a valid dex file')
            self.close()
    
    def get_string_start(self):
        self._file_handle.seek(self.dex_header.get_string_offset())
        content = self._file_handle.read(4)
        return struct.unpack('<l', content)[0]
    
    def get_string_size(self):
                
        if len(self.offset_list) == 0:
            temp_list = self.get_string_list()
        
        size = 0
        
        size += self.offset_list[-1] - self.offset_list[0]
        
        self._file_handle.seek(self.offset_list[-1])
        
        TAG = True
        while TAG:
            value = self._file_handle.read(1)
            size += 1
            if value == '\x00':
                TAG = False
        return size
    
    #get string list, for each string id, didn't include the '\x00' tag in the end.
    def get_string_list(self):
        size_list = []
        position = self.dex_header.get_string_offset()
        for i in range(self.dex_header.get_string_count()):
            self._file_handle.seek(position + i * 4)
            content = self._file_handle.read(4)
            offset = struct.unpack('<l', content)[0]
            self.offset_list.append(offset)
            self._file_handle.seek(offset)
            length = struct.unpack('<b', self._file_handle.read(1))[0]
            # one for the data size, one for the end tag
            size_list.append(length)
        return size_list
        
    #get the content after the string part
    def get_content_after_string(self):
        starter = self.get_string_start() + self.get_string_size()
        self._file_handle.seek(starter)
        return self._file_handle.read()
    
    #get the content from sha to string block
    def get_content_sha_to_string(self):
        #8 magic, 4 checksum, 20, signature
        starter = 8 + 4 + 20
        string_start = self.get_string_start()
        self._file_handle.seek(starter)
        return self._file_handle.read(string_start - starter)
    
    #get the new header
    def get_new_header(self, new_sha1, new_checksum):
        #new magic, new checksum, new sha1
        new_header = struct.pack('<8sl20s', 'dex\n035\x00', new_checksum, new_sha1)
        return new_header
    
    #get the offset:
    def get_offset_list(self, seq):
        return self.offset_list[seq]
    
    #get the size and string_length
    def get_unicode_str_size(self, seq):
        
        self._file_handle.seek(self.get_offset_list(seq))
        
        #size tag
        size_tag = True
        size_value = 0
        size_binary = ''
        
        #string tag
        str_tag = False
        str_value = 0
        
        #whole tag
        TAG = True
        while TAG:
            value = self._file_handle.read(1)
            if value == '\x00':
                TAG = False
                
            if size_tag:
                size_binary += value
                if struct.unpack('<b', value)[0] < 0:
                    size_value += 1
                    continue
                else:
                    size_value += 1
                    size_tag = False
                    str_tag = True
                    continue
        
            if str_tag:
                str_value += 1 
        return size_binary, size_value, str_value
    
    def seek(self, value):
        self._file_handle.seek(value)
    def read(self, value):
        return self._file_handle.read(value)
    #close the file handle
    def close(self):
        self._file_handle.close()
                
            


        