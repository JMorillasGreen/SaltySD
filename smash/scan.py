from __future__ import print_function
import struct, sys, zlib, os
def b2str(bytes):
    return "".join(map(chr, bytes))
    
def r32(data, pos):
    try:
        return struct.unpack('<I', data.encode('latin-1')[pos:pos+4])[0]
    except:
        return struct.unpack('<I', data[pos:pos+4])[0]

crc_sig = b2str([0xD0, 0x10, 0xD0, 0xE1, 0x00, 0x20, 0xE0, 0xE3, 0x00, 0x00, 0x51, 0xE3, 0x30, 0x30, 0x9F, 0x15])
mount_sdmc_sig = b2str([0x38, 0x40, 0x2D, 0xE9, 0x00, 0x40, 0xA0, 0xE1, 0x09, 0x10, 0xA0, 0xE3, 0x0D, 0x00, 0xA0, 0xE1])
IFile_Init_sig = b2str([0x10, 0x40, 0x2D, 0xE9, 0x00, 0x40, 0xA0, 0xE1, 0x54, 0x00, 0x9F, 0xE5, 0x00, 0x00, 0x84, 0xE5, 0x1C, 0x00, 0xA0, 0xE3])
IFile_Open_sig = b2str([0xF0, 0x47, 0x2D, 0xE9, 0x86, 0xDF, 0x4D, 0xE2, 0x02, 0x40, 0xA0, 0xE1, 0x01, 0x60, 0xA0, 0xE1, 0x04, 0x50, 0x90, 0xE5])
IFile_GetSize_sig = b2str([0x30, 0x40, 0x2D, 0xE9, 0x0C, 0xD0, 0x4D, 0xE2, 0x04, 0x40, 0x90, 0xE5])
IFile_Read_sig = b2str([0xF8, 0x40, 0x2D, 0xE9, 0x03, 0x50, 0xA0, 0xE1, 0x01, 0x70, 0xA0, 0xE1, 0x04, 0x40, 0x90, 0xE5, 0x02, 0x60, 0xA0, 0xE1])
IFile_Close_sig = b2str([0x70, 0x40, 0x2D, 0xE9, 0x00, 0x60, 0xA0, 0xE1, 0x04, 0x40, 0x90, 0xE5, 0x44, 0x00, 0x9F, 0xE5, 0x00, 0x00, 0x54, 0xE3, 0x00, 0x00, 0x86, 0xE5, 0x0C, 0x00, 0x00, 0x0A, 0x04, 0x50, 0xA0, 0xE1])
strcat_sig = b2str([0x42, 0x1E, 0x52, 0x1C, 0x13, 0x78, 0x00, 0x2B, 0xFB, 0xD1, 0x0B, 0x78, 0x49, 0x1C, 0x13, 0x70, 0x52, 0x1C, 0x00, 0x2B])
strcpy_sig = b2str([0x01, 0x30, 0x80, 0xE1, 0x00, 0x20, 0xA0, 0xE1, 0x03, 0x00, 0x13, 0xE3, 0x50, 0xC0, 0x9F, 0x05, 0x04, 0xE0, 0x2D, 0xE5, 0x09, 0x00, 0x00, 0x1A, 0x04, 0x30, 0x91, 0xE4, 0xF3, 0xEF, 0x6C, 0xE6])
strlen_sig = b2str([0x01, 0x30, 0x80, 0xE2, 0x03, 0x00, 0x00, 0xEA, 0x01, 0x10, 0xD0, 0xE4, 0x00, 0x00, 0x51, 0xE3, 0x03, 0x00, 0x40, 0x00, 0x1E, 0xFF, 0x2F, 0x01, 0x03, 0x00, 0x10, 0xE3, 0x38, 0x20, 0x9F, 0x05])
resalloc_sig = b2str([0xFF, 0x4F, 0x2D, 0xE9, 0x44, 0xD0, 0x4D, 0xE2, 0x01, 0x30, 0xA0, 0xE1, 0x00, 0x40, 0xA0, 0xE1])
path_str_sig = b2str([0xF0, 0x41, 0x2D, 0xE9, 0x20, 0xD0, 0x4D, 0xE2, 0x00, 0x80, 0xA0, 0xE3, 0xB0, 0x20, 0xD1, 0xE1])
res_deallocate_sig = b2str([0x00, 0x00, 0xA0, 0xE1, 0x00, 0x00, 0x51, 0xE3, 0x1E, 0xFF, 0x2F, 0x01])
idk_sig = b2str([0x00, 0x20, 0x91, 0xE5, 0x02, 0x28, 0xA0, 0xE1, 0x22, 0x28, 0xB0, 0xE1, 0x0C, 0x00, 0x00, 0x0A])
referenced_by_ls_init_sig = b2str([0x03, 0x00, 0x2D, 0xE9, 0x00, 0x10, 0xA0, 0xE3, 0xB0, 0x10, 0xC0, 0xE1, 0xB4, 0x20, 0xDD, 0xE1])
read_dtls_sig = b2str([0xF0, 0x47, 0x2D, 0xE9, 0x00, 0x60, 0xA0, 0xE1, 0x8A, 0xDF, 0x4D, 0xE2, 0x01, 0x40, 0xA0, 0xE1])
liballoc_sig = b2str([0x70, 0x40, 0x2D, 0xE9, 0x00, 0x40, 0xA0, 0xE1, 0x38, 0x60, 0x9F, 0xE5, 0x04, 0x50, 0xA0, 0xE3, 0x00, 0x10, 0xA0, 0xE1, 0x05, 0x20, 0xA0, 0xE1, 0x0C, 0x00, 0x96, 0xE5])
libdealloc_sig = b2str([0x00, 0x00, 0x50, 0xE3, 0x03, 0x00, 0x00, 0x0A, 0x00, 0x10, 0xA0, 0xE1, 0x08, 0x00, 0x9F, 0xE5, 0x0C, 0x00, 0x90, 0xE5])
memcpy_sig = b2str([0x03, 0x00, 0x52, 0xE3, 0x17, 0x00, 0x00, 0x9A, 0x03, 0xC0, 0x10, 0xE2, 0x08, 0x00, 0x00, 0x0A])
memmove_sig = b2str([0x03, 0x00, 0x52, 0xE3, 0x02, 0x00, 0x80, 0xE0, 0x02, 0x10, 0x81, 0xE0])
memclr_sig = b2str([0x00, 0x20, 0xA0, 0xE3, 0x04, 0x00, 0x51, 0xE3, 0x07, 0x00, 0x00, 0x3A])
strcmp_sig = b2str([0x03, 0x00, 0x10, 0xE3, 0x03, 0x00, 0x11, 0x03, 0x1E, 0x00, 0x00, 0x1A])
crit_this_sig = b2str([0x90, 0x00, 0x9F, 0xE5, 0x10, 0x40, 0x2D, 0xE9])
crit_init_sig = b2str([0x00, 0x00, 0xA0, 0xE3, 0x04, 0x00, 0x84, 0xE5, 0x08, 0x00, 0x84, 0xE5, 0x10, 0x80, 0xBD, 0xE8]) #-0xC

OpenDirectory_sig = b2str([0xF0, 0x40, 0x2D, 0xE9, 0x00, 0x50, 0xA0, 0xE1, 0x14, 0xD0, 0x4D, 0xE2, 0x01, 0x70, 0xA0, 0xE1, 0x01, 0x00, 0xA0, 0xE1])
ReadDirectory_sig = b2str([0x00, 0x00, 0x50, 0xE3, 0x00, 0x00, 0x51, 0x13, 0x3C, 0x00, 0x9F, 0x05, 0x1E, 0xFF, 0x2F, 0x01, 0xF0, 0x41, 0x2D, 0xE9])
CloseDirectory_sig = b2str([0x00, 0x00, 0x50, 0xE3, 0x02, 0x00, 0x00, 0x0A, 0x00, 0x10, 0x90, 0xE5, 0x04, 0x10, 0x91, 0xE5, 0x11, 0xFF, 0x2F, 0xE1, 0x1E, 0xFF, 0x2F, 0xE1])

resalloc_sig_legacy = b2str([0xF0, 0x4F, 0x2D, 0xE9, 0x34, 0xD0, 0x4D, 0xE2, 0x01, 0x80, 0xA0, 0xE1, 0x00, 0x50, 0xA0, 0xE1])
idk_sig_legacy = b2str([0x04, 0x10, 0x91, 0xE5, 0x00, 0x00, 0x51, 0xE3, 0x0B, 0x10, 0xD1, 0x15, 0x00, 0x00, 0x51, 0x13])
read_dtls_sig_legacy = b2str([0xF0, 0x41, 0x2D, 0xE9, 0x01, 0x40, 0xA0, 0xE1, 0x00, 0x70, 0xA0, 0xE1, 0x08, 0x50, 0x90, 0xE5])

# Make this compatible with Python 2 and 3
try:
    f = open(sys.argv[1], 'r', encoding='latin-1', newline="").read()
except TypeError:
    f = open(sys.argv[1], 'rb').read()
    
common = open('common.asm','w')

# Print to stderr a helpful message in case someone tries to patch the Demo.
# This will also stop the Makefile
if f.find(mount_sdmc_sig) == -1:
    print("mount_sdmc does not exist!\nIs your code.bin from a retail copy of Smash, and not the demo?\n", file=sys.stderr)
    exit(1)  

print(".equ mount_sdmc, \t\t\t\t" + hex(f.find(mount_sdmc_sig)+0x100000), file=common)
print(".equ IFile_Init, \t\t\t\t" + hex(f.find(IFile_Init_sig)+0x100000), file=common)
print(".equ IFile_Open, \t\t\t\t" + hex(f.find(IFile_Open_sig)+0x100000), file=common)
print(".equ IFile_GetSize, \t\t\t" + hex(f.find(IFile_GetSize_sig)+0x100000), file=common)
print(".equ IFile_Read, \t\t\t\t" + hex(f.find(IFile_Read_sig)+0x100000), file=common)
print(".equ IFile_Close, \t\t\t\t" + hex(f.find(IFile_Close_sig)+0x100000), file=common)
print(".equ OpenDirectory, \t\t\t" + hex(f.find(OpenDirectory_sig)+0x100000), file=common)
print(".equ ReadDirectory, \t\t\t" + hex(f.find(ReadDirectory_sig)+0x100000), file=common)
print(".equ CloseDirectory, \t\t\t" + hex(f.find(CloseDirectory_sig)+0x100000), file=common)
print(".equ strcat, \t\t\t\t\t" + hex(f.find(strcat_sig)+0x100000), file=common)
print(".equ strcpy, \t\t\t\t\t" + hex(f.find(strcpy_sig)+0x100000), file=common)
print(".equ strlen, \t\t\t\t\t" + hex(f.find(strlen_sig)+0x100000), file=common)
print(".equ resalloc, \t\t\t\t\t" + hex(f.find(resalloc_sig_legacy if f.find(resalloc_sig) == -1 else resalloc_sig)+0x100000), file=common)  
print(".equ path_str, \t\t\t\t\t" + hex(f.find(path_str_sig)+0x100000), file=common)
print(".equ res_deallocate, \t\t\t" + hex(f.find(res_deallocate_sig)+0x100000+0x4), file=common)
print(".equ idk, \t\t\t\t\t\t" + hex(f.find(idk_sig_legacy if f.find(idk_sig) == -1 else idk_sig)+0x100000), file=common) 
print(".equ referenced_by_ls_init, \t" + hex(f.find(referenced_by_ls_init_sig)+0x100000), file=common)
print(".equ read_dtls, \t\t\t\t" + hex(f.find(read_dtls_sig_legacy if f.find(read_dtls_sig) == -1 else read_dtls_sig)+0x100000-0x4), file=common)
print(".equ liballoc, \t\t\t\t\t" + hex(f.find(liballoc_sig)+0x100000), file=common)
print(".equ libdealloc, \t\t\t\t" + hex(f.find(libdealloc_sig)+0x100000), file=common)
print(".equ memcpy, \t\t\t\t\t" + hex(f.find(memcpy_sig)+0x100000), file=common)
print(".equ memmove, \t\t\t\t\t" + hex(f.find(memmove_sig)+0x100000-0xC), file=common)
print(".equ memclr, \t\t\t\t\t" + hex(f.find(memclr_sig)+0x100000), file=common)
print(".equ strcmp, \t\t\t\t\t" + hex(f.find(strcmp_sig)+0x100000), file=common)
print(".equ crit_this, \t\t\t\t" + hex(f.find(crit_this_sig)+0x100000), file=common)
print(".equ crit_init, \t\t\t\t" + hex(f.find(crit_init_sig)+0x100000-0xC), file=common)
print(".equ crc, \t\t\t\t\t\t" + hex(f.find(crc_sig)+0x100000), file=common)
if(r32(f,f.find(path_str_sig)-4) == 0x0):
    print(".equ something_resource_lock, \t" + hex(r32(f,f.find(path_str_sig)-8)) + "\n", file=common)
else:
    print(".equ something_resource_lock, \t" + hex(r32(f,f.find(path_str_sig)-4)) + "\n", file=common)

print("common.asm generated successfully!")

common = open('common.h','w')
print("#define mount_sdmc_ADDR " + hex(f.find(mount_sdmc_sig)+0x100000), file=common)
print("#define IFile_Init_ADDR " + hex(f.find(IFile_Init_sig)+0x100000), file=common)
print("#define IFile_Open_ADDR " + hex(f.find(IFile_Open_sig)+0x100000), file=common)
print("#define IFile_GetSize_ADDR " + hex(f.find(IFile_GetSize_sig)+0x100000), file=common)
print("#define IFile_Read_ADDR " + hex(f.find(IFile_Read_sig)+0x100000), file=common)
print("#define IFile_Close_ADDR " + hex(f.find(IFile_Close_sig)+0x100000), file=common)
print("#define OpenDirectory_ADDR " + hex(f.find(OpenDirectory_sig)+0x100000), file=common)
print("#define ReadDirectory_ADDR " + hex(f.find(ReadDirectory_sig)+0x100000), file=common)
print("#define CloseDirectory_ADDR " + hex(f.find(CloseDirectory_sig)+0x100000), file=common)

print("#define strcat_ADDR " + hex(f.find(strcat_sig)+0x100000), file=common)
print("#define strcpy_ADDR " + hex(f.find(strcpy_sig)+0x100000), file=common)
print("#define strlen_ADDR " + hex(f.find(strlen_sig)+0x100000), file=common)
print("#define resalloc_ADDR " + hex(f.find(resalloc_sig_legacy if f.find(resalloc_sig) == -1 else resalloc_sig)+0x100000), file=common)  
print("#define path_str_ADDR " + hex(f.find(path_str_sig)+0x100000), file=common)
print("#define res_deallocate_ADDR " + hex(f.find(res_deallocate_sig)+0x100000+0x4), file=common)
print("#define idk_ADDR " + hex(f.find(idk_sig_legacy if f.find(idk_sig) == -1 else idk_sig)+0x100000), file=common) 
print("#define referenced_by_ls_init_ADDR " + hex(f.find(referenced_by_ls_init_sig)+0x100000), file=common)
print("#define read_dtls_ADDR " + hex(f.find(read_dtls_sig_legacy if f.find(read_dtls_sig) == -1 else read_dtls_sig)+0x100000-0x4), file=common)
print("#define liballoc_ADDR " + hex(f.find(liballoc_sig)+0x100000), file=common)
print("#define libdealloc_ADDR " + hex(f.find(libdealloc_sig)+0x100000), file=common)
print("#define memcpy_ADDR " + hex(f.find(memcpy_sig)+0x100000), file=common)
print("#define memmove_ADDR " + hex(f.find(memmove_sig)+0x100000-0xC), file=common)
print("#define memclr_ADDR " + hex(f.find(memclr_sig)+0x100000), file=common)
print("#define strcmp_ADDR " + hex(f.find(strcmp_sig)+0x100000), file=common)
print("#define crit_this_ADDR " + hex(f.find(crit_this_sig)+0x100000), file=common)
print("#define crit_init_ADDR " + hex(f.find(crit_init_sig)+0x100000-0xC), file=common)
print("#define crc_ADDR " + hex(f.find(crc_sig)+0x100000), file=common)
if(r32(f,f.find(path_str_sig)-4) == 0x0):
    print("#define something_resource_lock_ADDR " + hex(r32(f,f.find(path_str_sig)-8)) + "\n", file=common)
else:
    print("#define something_resource_lock_ADDR " + hex(r32(f,f.find(path_str_sig)-4)) + "\n", file=common)
    
print("common.h generated successfully!")