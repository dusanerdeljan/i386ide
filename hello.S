# Autor Dusan Erdeljan sw-43/2018
# Program ispisuje "Hello world!!!"
.section .data
    poruka: .ascii "Hello world!\0"
    poruka_len = .-poruka
.section .text
.globl main
main:
    movl $4, %eax
    movl $1, %ebx
    leal poruka, %ecx
    movl $poruka_len, %edx
    int $0x80
kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80
