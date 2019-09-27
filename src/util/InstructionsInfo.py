"""
    This file is part of i386ide.
    i386ide is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

class InstructionsInfo(object):
    # TODO: Ovde treba upisati opise svih instrukcija
    INFO = {
        # ======= ADC ======
        'adc': """<b>adc</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u od,
        redišni operand. Prilikom sabiranja,zatečeni prenos se uzima u obzir.</p>""",
        'adcb': """<b>adcb</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u 
        odredišni operand. Prilikom sabiranja,zatečeni prenos se uzima u obzir.</p>""",
        'adcw': """<b>adcw</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u 
        odredišni operand. Prilikom sabiranja,zatečeni prenos se uzima u obzir.</p>""",
        'adcl': """<b>adcl</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u
         odredišni operand. Prilikom sabiranja,zatečeni prenos se uzima u obzir.</p>""",
        # ======= ADD ======
        'add': """<b>add</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u odredišni operand. Prilikom sabiranja,zatečeni prenos se ne uzima u obzir.</p>""",
        'addb': """<b>addb</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u odredišni operand. Prilikom sabiranja,zatečeni prenos se ne uzima u obzir.</p>""",
        'addw': """<b>addw</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u odredišni operand. Prilikom sabiranja,zatečeni prenos se ne uzima u obzir.</p>""",
        'addl': """<b>addl</b> <em>src</em>, <em>dst</em><p>Sabira izvorni i odredišni operand i rezultat smešta u odredišni operand. Prilikom sabiranja,zatečeni prenos se ne uzima u obzir.</p>""",
        # ======= AND ======
        'and': """<b>and</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda i rezultat
smešta u odredišni.</p>""",
        'andb': """<b>andb</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda i rezultat
smešta u odredišni.</p>""",
        'andw': """<b>andw</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda i rezultat
smešta u odredišni.</p>""",
        'andl': """<b>andl</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda i rezultat
smešta u odredišni.</p>""",
        # ======= CALL ======
        'call': """<b>call</b> <em>dst</em><p>Poziv potprograma. Prilikom poziva, na stek se smešta povratna adresa.</p>""",
        # ======= CLC ======
        'clc': """<b>clc</b> <p>Postavlja carry indikator na 0.</p>""",
        # ======= CLD ======
        'cld': """<b>cld</b> <p>Postavlja direction indikator na 0.</p>""",
        # ======= CMP ======
        'cmp': """<b>cmp</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog, postavlja indikatore u skladu sa tim, ali ne menja
odredišni operand.</p>""",
        'cmpb': """<b>cmpb</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog, postavlja indikatore u skladu sa tim, ali ne menja
odredišni operand.</p>""",
        'cmpw': """<b>cmpw</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog, postavlja indikatore u skladu sa tim, ali ne menja
odredišni operand.</p>""",
        'cmpl': """<b>cmpl</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog, postavlja indikatore u skladu sa tim, ali ne menja
odredišni operand.</p>""",
        # ======= DEC ======
        'dec': """<b>dec</b> <em>dst</em><p>Oduzima 1 od odredišnog operanda.</p>""",
        'decb': """<b>decb</b> <em>dst</em><p>Oduzima 1 od odredišnog operanda.</p>""",
        'decw': """<b>decw</b> <em>dst</em><p>Oduzima 1 od odredišnog operanda.</p>""",
        'decl': """<b>decl</b> <em>dst</em><p>Oduzima 1 od odredišnog operanda.</p>""",
        # ======= DIV ======
        'div': """<b>div</b> <em>src</em><p style='white-space:pre'>Neoznačeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        divb operand # ax/operand -> al, ostatak -> ah
        divw operand # dx:ax/operand -> ax, ostatak -> dx
        divl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe div može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        'divb': """<b>divb</b> <em>src</em><p style='white-space:pre'>Neoznačeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        divb operand # ax/operand -> al, ostatak -> ah
        divw operand # dx:ax/operand -> ax, ostatak -> dx
        divl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe div može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        'divw': """<b>divw</b> <em>src</em><p style='white-space:pre'>Neoznačeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        divb operand # ax/operand -> al, ostatak -> ah
        divw operand # dx:ax/operand -> ax, ostatak -> dx
        divl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe div može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        'divl': """<b>divl</b> <em>src</em><p style='white-space:pre'>Neoznačeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        divb operand # ax/operand -> al, ostatak -> ah
        divw operand # dx:ax/operand -> ax, ostatak -> dx
        divl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe div može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        # ======= IDIV ======
        'idiv': """<b>idiv</b> <em>src</em><p style='white-space:pre'>Označeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:
    
        idivb operand # ax/operand -> al, ostatak -> ah
        idivw operand # dx:ax/operand -> ax, ostatak -> dx
        idivl operand # edx:eax/operand -> eax, ostatak -> edx
    
operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe idiv može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        'idivb': """<b>idivb</b> <em>src</em><p style='white-space:pre'>Označeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        idivb operand # ax/operand -> al, ostatak -> ah
        idivw operand # dx:ax/operand -> ax, ostatak -> dx
        idivl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe idiv može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        'idivw': """<b>idivw</b> <em>src</em><p style='white-space:pre'>Označeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        idivb operand # ax/operand -> al, ostatak -> ah
        idivw operand # dx:ax/operand -> ax, ostatak -> dx
        idivl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe idiv može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        'idivl': """<b>idivl</b> <em>src</em><p style='white-space:pre'>Označeno deljenje. U zavisnosti od veličine izvornog operanda, ima sledeće dejstvo:

        idivb operand # ax/operand -> al, ostatak -> ah
        idivw operand # dx:ax/operand -> ax, ostatak -> dx
        idivl operand # edx:eax/operand -> eax, ostatak -> edx

operand – može biti registar ili memorija/promenljiva

Izvršavanje naredbe idiv može dovesti do pojave izuzetka. Ovo se može desiti u dva slučaja:
        – ukoliko je vrednost operanda jednaka nuli
        – ukoliko je dobijena vrednost prevelika da stane u odredište</p>""",
        # ======= IMUL ======
        'imul': """<b>imul</b> <em>op1[</em><em>op2[</em><em>op3]]</em><p style='white-space:pre'>Označeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:
        
        imulb operand # al*operand -> ax
        imulw operand # ax*operand -> dx:ax
        imull operand # eax*operand -> edx:eax
            
        imulw oper1, oper2 # oper1*oper2 -> oper2
        imull oper1, oper2 # oper1*oper2 -> oper2
            
        imulw const,oper1,oper2 # const*oper1 -> oper2
        imull const,oper1,oper2 # const*oper1 -> oper2
            
Operandi imaju sledeća ograničenja:

        operand – može biti registar ili memorija
        oper1 – može biti konstanta, registar ili memorija
        oper2 – može biti samo registar
        const – može biti samo konstanta</p>""",
        'imulb': """<b>imulb</b> <em>op1[</em><em>op2[</em><em>op3]]</em><p style='white-space:pre'>Označeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        imulb operand # al*operand -> ax
        imulw operand # ax*operand -> dx:ax
        imull operand # eax*operand -> edx:eax

        imulw oper1, oper2 # oper1*oper2 -> oper2
        imull oper1, oper2 # oper1*oper2 -> oper2

        imulw const,oper1,oper2 # const*oper1 -> oper2
        imull const,oper1,oper2 # const*oper1 -> oper2

Operandi imaju sledeća ograničenja:

        operand – može biti registar ili memorija
        oper1 – može biti konstanta, registar ili memorija
        oper2 – može biti samo registar
        const – može biti samo konstanta</p>""",
        'imulw': """<b>imulw</b> <em>op1[</em><em>op2[</em><em>op3]]</em><p style='white-space:pre'>Označeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        imulb operand # al*operand -> ax
        imulw operand # ax*operand -> dx:ax
        imull operand # eax*operand -> edx:eax

        imulw oper1, oper2 # oper1*oper2 -> oper2
        imull oper1, oper2 # oper1*oper2 -> oper2

        imulw const,oper1,oper2 # const*oper1 -> oper2
        imull const,oper1,oper2 # const*oper1 -> oper2

Operandi imaju sledeća ograničenja:

        operand – može biti registar ili memorija
        oper1 – može biti konstanta, registar ili memorija
        oper2 – može biti samo registar
        const – može biti samo konstanta</p>""",
        'imull': """<b>imull</b> <em>op1[</em><em>op2[</em><em>op3]]</em><p style='white-space:pre'>Označeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        imulb operand # al*operand -> ax
        imulw operand # ax*operand -> dx:ax
        imull operand # eax*operand -> edx:eax

        imulw oper1, oper2 # oper1*oper2 -> oper2
        imull oper1, oper2 # oper1*oper2 -> oper2

        imulw const,oper1,oper2 # const*oper1 -> oper2
        imull const,oper1,oper2 # const*oper1 -> oper2

Operandi imaju sledeća ograničenja:

        operand – može biti registar ili memorija
        oper1 – može biti konstanta, registar ili memorija
        oper2 – može biti samo registar
        const – može biti samo konstanta</p>""",

        # ======= INC ======
        'inc': """<b>inc</b> <em>dst</em><p>Dodaje 1 na odredišni operand.</p>""",
        'incb': """<b>incb</b> <em>dst</em><p>Dodaje 1 na odredišni operand.</p>""",
        'incw': """<b>incw</b> <em>dst</em><p>Dodaje 1 na odredišni operand.</p>""",
        'incl': """<b>incl</b> <em>dst</em><p>Dodaje 1 na odredišni operand.</p>""",
        # ======= INC ======
        'int': """<b>int</b> <em>dst</em><p>Generiše softverski prekid.</p>""",
        # ======= JXX ======
        'ja': """<b>ja</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako je veće.
Odnosno c=0 i z=0</p>""",
        'jae': """<b>jae</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako je veće ili jednako.
Odnosno c = 0</p>""",
        'jb': """<b>jb</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako je manje.
Odnosno c=1</p>""",
        'jbe': """<b>jbe</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako je manje ili jednako.
Odnosno c = 1 ili z = 1</p>""",
        'jna': """<b>jna</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako nije veće.
Odnosno c = 1 ili z = 1</p>""",
        'jnae': """<b>jnae</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako nije veće ili jednako.
Odnosno c = 1</p>""",
        'jnb': """<b>jnb</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako nije manje.
Odnosno c = 0</p>""",
        'jnbe': """<b>jnbe</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih brojeva.
Skok ako nije manje ili jednako.
Odnosno c = 0 i z = 0</p>""",
        'je': """<b>je</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih ili označenih brojeva.
Skok ako je jednako.
Odnosno z = 1</p>""",
        'jne': """<b>jne</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja neoznačenih ili označenih brojeva.
Skok ako nije jednako.
Odnosno z = 0</p>""",

        'jg': """<b>jg</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako je veće.
Odnosno z = 0 i s = o</p>""",
        'jge': """<b>jge</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako je veće ili jednako.
Odnosno s = o</p>""",
        'jl': """<b>jl</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako je manje.
Odnosno s <> o</p>""",
        'jle': """<b>jle</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako je manje ili jednako.
Odnosno z = 1 ili s <> o</p>""",
        'jng': """<b>jng</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako nije veće.
Odnosno z = 1 ili s <> o</p>""",
        'jnge': """<b>jnge</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako nije veće ili jednako.
Odnosno s <> o</p>""",
        'jnl': """<b>jnl</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako nije manje.
Odnosno s = o</p>""",
        'jnle': """<b>jnle</b> <em>dst</em><p style='white-space:pre'>Uslovni skok nakon poređenja označenih brojeva.
Skok ako nije manje ili jednako.
Odnosno z = 0 i s = o</p>""",
        'jc': """<b>jc</b> <em>dst</em><p style='white-space:pre'>Skok ako je prenos.
Odnosno c = 1</p>""",
        'jnc': """<b>jnc</b> <em>dst</em><p style='white-space:pre'>Skok ako nije prenos.
Odnosno c = 0</p>""",
        'jz': """<b>jz</b> <em>dst</em><p style='white-space:pre'>Skok ako je nula.
Odnosno z = 1</p>""",
        'jnz': """<b>jnz</b> <em>dst</em><p style='white-space:pre'>Skok ako nije nula.
Odnosno z = 0</p>""",
        'jo': """<b>jo</b> <em>dst</em><p style='white-space:pre'>Skok ako je prekoračenje.
Odnosno o = 1</p>""",
        'jno': """<b>jno</b> <em>dst</em><p style='white-space:pre'>Skok ako nije prekoračenje.
Odnosno o = 0</p>""",
        'js': """<b>js</b> <em>dst</em><p style='white-space:pre'>Skok ako je znak.
Odnosno s = 1</p>""",
        'jns': """<b>jns</b> <em>dst</em><p style='white-space:pre'>Skok ako nije znak.
Odnosno s = 0</p>""",
        'jcxz': """<b>jcxz</b> <em>dst</em><p style='white-space:pre'>Skok ako je cx = 0.</p>""",
        'jecxz': """<b>jecxz</b> <em>dst</em><p style='white-space:pre'>Skok ako je ecx = 0.</p>""",
        # ======= JMP ======
        'jmp': """<b>jmp</b> <em>dst</em><p style='white-space:pre'>Bezuslovni skok.</p>""",
        # ======= LEA ======
        'lea': """<b>lea</b> <em>src</em>, <em>dst</em><p>Smešta efektivnu adresu izvornog operanda u odredišni.</p>""",
        'leab': """<b>leab</b> <em>src</em>, <em>dst</em><p>Smešta efektivnu adresu izvornog operanda u odredišni.</p>""",
        'leaw': """<b>leaw</b> <em>src</em>, <em>dst</em><p>Smešta efektivnu adresu izvornog operanda u odredišni.</p>""",
        'leal': """<b>leal</b> <em>src</em>, <em>dst</em><p>Smešta efektivnu adresu izvornog operanda u odredišni.</p>""",
        # ======= LODS ======
        'lods': """<b>lods</b><p style='white-space:pre'>U zavisnosti od veličine podrazumevanog operanda, ima sledeće dejstvo:
        lodsb # (esi) -> al, esi+1 -> esi za d=0, odnosno esi-1 -> esi za d=1
        lodsw # (esi) -> ax, esi+2 -> esi za d=0, odnosno esi-2 -> esi za d=1
        lodsl # (esi) -> eax, esi+4 -> esi za d=0, odnosno esi-4 -> esi za d=1
Podrazumevani segmentni registar je ds (ds:esi).</p>""",
        'lodsb': """<b>lodsb</b><p style='white-space:pre'>U zavisnosti od veličine podrazumevanog operanda, ima sledeće dejstvo:
        lodsb # (esi) -> al, esi+1 -> esi za d=0, odnosno esi-1 -> esi za d=1
        lodsw # (esi) -> ax, esi+2 -> esi za d=0, odnosno esi-2 -> esi za d=1
        lodsl # (esi) -> eax, esi+4 -> esi za d=0, odnosno esi-4 -> esi za d=1
Podrazumevani segmentni registar je ds (ds:esi).</p>""",
        'lodsw': """<b>lodsw</b><p style='white-space:pre'>U zavisnosti od veličine podrazumevanog operanda, ima sledeće dejstvo:
        lodsb # (esi) -> al, esi+1 -> esi za d=0, odnosno esi-1 -> esi za d=1
        lodsw # (esi) -> ax, esi+2 -> esi za d=0, odnosno esi-2 -> esi za d=1
        lodsl # (esi) -> eax, esi+4 -> esi za d=0, odnosno esi-4 -> esi za d=1
Podrazumevani segmentni registar je ds (ds:esi).</p>""",
        'lodsl': """<b>lodsl</b><p style='white-space:pre'>U zavisnosti od veličine podrazumevanog operanda, ima sledeće dejstvo:
        lodsb # (esi) -> al, esi+1 -> esi za d=0, odnosno esi-1 -> esi za d=1
        lodsw # (esi) -> ax, esi+2 -> esi za d=0, odnosno esi-2 -> esi za d=1
        lodsl # (esi) -> eax, esi+4 -> esi za d=0, odnosno esi-4 -> esi za d=1
Podrazumevani segmentni registar je ds (ds:esi).</p>""",
        # ======= LOOP ======
        'loop': """<b>loop</b> <em>dst</em><p>Smanjuje cx (loopw), odnosno ecx (loopl) za 1 i skače na ciljnu naredbu ako je rezultat različit od
nule.</p>""",
        'loopw': """<b>loopw</b> <em>dst</em><p>Smanjuje cx (loopw), odnosno ecx (loopl) za 1 i skače na ciljnu naredbu ako je rezultat različit od
    nule.</p>""",
        'loopl': """<b>loopl</b> <em>dst</em><p>Smanjuje cx (loopw), odnosno ecx (loopl) za 1 i skače na ciljnu naredbu ako je rezultat različit od
    nule.</p>""",
        # ======= MOV ======
        'mov': """<b>mov</b> <em>src</em>, <em>dst</em><p>Kopira izvorni operand u odredišni.</p>""",
        'movb': """<b>movb</b> <em>src</em>, <em>dst</em><p>Kopira izvorni operand u odredišni.</p>""",
        'movw': """<b>movw</b> <em>src</em>, <em>dst</em><p>Kopira izvorni operand u odredišni.</p>""",
        'movl': """<b>movl</b> <em>src</em>, <em>dst</em><p>Kopira izvorni operand u odredišni.</p>""",
        # ======= MUL ======
        'mul': """<b>mul</b> <em>src</em><p style='white-space:pre'>Neoznačeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        mulb operand # al*operand -> ax
        mulw operand # ax*operand -> dx:ax
        mull operand # eax*operand -> edx:eax

operand – može biti registar ili memorija/promenljiva</p>""",
        'mulb': """<b>mulb</b> <em>src</em><p style='white-space:pre'>Neoznačeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        mulb operand # al*operand -> ax
        mulw operand # ax*operand -> dx:ax
        mull operand # eax*operand -> edx:eax

operand – može biti registar ili memorija/promenljiva</p>""",
        'mulw': """<b>mulw</b> <em>src</em><p style='white-space:pre'>Neoznačeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        mulb operand # al*operand -> ax
        mulw operand # ax*operand -> dx:ax
        mull operand # eax*operand -> edx:eax

operand – može biti registar ili memorija/promenljiva</p>""",
        'mull': """<b>mull</b> <em>src</em><p style='white-space:pre'>Neoznačeno množenje. U zavisnosti od veličine i broja operanada, ima sledeće dejstvo:

        mulb operand # al*operand -> ax
        mulw operand # ax*operand -> dx:ax
        mull operand # eax*operand -> edx:eax

operand – može biti registar ili memorija/promenljiva</p>""",
        # ======= NEG ======
        'neg': """<b>neg</b> <em>dst</em><p>Negira odredišni operand po komplementu 2.</p>""",
        'negb': """<b>negb</b> <em>dst</em><p>Negira odredišni operand po komplementu 2.</p>""",
        'negw': """<b>negw</b> <em>dst</em><p>Negira odredišni operand po komplementu 2.</p>""",
        'negl': """<b>negl</b> <em>dst</em><p>Negira odredišni operand po komplementu 2.</p>""",
        # ======= NOP ======
        'nop': """<b>nop</b><p>Naredba bez efekta (troši nekoliko procesorskih ciklusa).</p>""",
        # ======= NOT ======
        'not': """<b>not</b> <em>dst</em><p>Negira odredišni operand po komplementu 1.</p>""",
        'notb': """<b>notb</b> <em>dst</em><p>Negira odredišni operand po komplementu 1.</p>""",
        'notw': """<b>notw</b> <em>dst</em><p>Negira odredišni operand po komplementu 1.</p>""",
        'notl': """<b>notl</b> <em>dst</em><p>Negira odredišni operand po komplementu 1.</p>""",
        # ======= OR ======
        'or': """<b>or</b> <em>src,</em> <em>dst</em><p>Vrši operaciju logičkog ILI između korespondentnih bita izvornog i odredišnog operanda i rezultat
smešta u odredišni.</p>""",
        'orb': """<b>orb</b> <em>src,</em> <em>dst</em><p>Vrši operaciju logičkog ILI između korespondentnih bita izvornog i odredišnog operanda i rezultat
    smešta u odredišni.</p>""",
        'orw': """<b>orw</b> <em>src,</em> <em>dst</em><p>Vrši operaciju logičkog ILI između korespondentnih bita izvornog i odredišnog operanda i rezultat
    smešta u odredišni.</p>""",
        'orl': """<b>orl</b> <em>src,</em> <em>dst</em><p>Vrši operaciju logičkog ILI između korespondentnih bita izvornog i odredišnog operanda i rezultat
    smešta u odredišni.</p>""",
        # ======= POP ======
        'pop': """<b>pop</b> <em>dst</em><p>Skida vrednost sa vrha steka i smešta je u odredišni operand, nakon čega se vrednost pokazivača
na vrh steka poveća za 4.</p>""",
        'popl': """<b>popl</b> <em>dst</em><p>Skida vrednost sa vrha steka i smešta je u odredišni operand, nakon čega se vrednost pokazivača
na vrh steka poveća za 4.</p>""",
        # ======= PUSH ======
        'push': """<b>push</b> <em>src</em><p>Smanji vrednost pokazivača na vrh steka za 4, a zatim izvorni operand smešta na novi vrh steka.</p>""",
        'pushl': """<b>pushl</b> <em>src</em><p>Smanji vrednost pokazivača na vrh steka za 4, a zatim izvorni operand smešta na novi vrh steka.</p>""",
        # ======= RCL ======
        'rcl': """<b>rcl</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u levo za navedeni broj mesta (neposredni operand ili
registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        'rclb': """<b>rclb</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u levo za navedeni broj mesta (neposredni operand ili
registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        'rclw': """<b>rclw</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u levo za navedeni broj mesta (neposredni operand ili
registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        'rcll': """<b>rcll</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u levo za navedeni broj mesta (neposredni operand ili
registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        # ======= RCR ======
        'rcr': """<b>rcr</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u desno za navedeni broj mesta (neposredni operand
ili registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        'rcrb': """<b>rcrb</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u desno za navedeni broj mesta (neposredni operand
ili registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        'rcrw': """<b>rcrw</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u desno za navedeni broj mesta (neposredni operand
ili registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        'rcrl': """<b>rcrl</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand kroz indikator carry u desno za navedeni broj mesta (neposredni operand
ili registar cl). Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan.</p>""",
        # ======= RET ======
        'ret': """<b>ret</b><p>Povratak iz potprograma. Povratna adresa se skida sa vrha steka, nakon čega se vrednost
pokazivača na vrh steka poveća za 4.</p>""",
        # ======= ROL ======
        'rol': """<b>rol</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najmanje značajnu poziciju.</p>""",
        'rolb': """<b>rolb</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najmanje značajnu poziciju.</p>""",
        'rolw': """<b>rolw</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najmanje značajnu poziciju.</p>""",
        'roll': """<b>roll</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najmanje značajnu poziciju.</p>""",

        # ======= ROR ======
        'ror': """<b>ror</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najviše značajnu poziciju.</p>""",
        'rorb': """<b>rorb</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najviše značajnu poziciju.</p>""",
        'rorw': """<b>rorw</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najviše značajnu poziciju.</p>""",
        'rorl': """<b>rorl</b> <em>cnt</em>, <em>dst</em><p>Rotira odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Ukoliko se rotira za više od jednog mesta, indikator overflow je nedefinisan. Indikator carry ima vrednost
poslednjeg bita upisanog na najviše značajnu poziciju.</p>""",
        # ======= SAR ======
        'sar': """<b>sar</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit zadržava svoju vrednost. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        'sarb': """<b>sarb</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit zadržava svoju vrednost. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        'sarw': """<b>sarw</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit zadržava svoju vrednost. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        'sarl': """<b>sarl</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit zadržava svoju vrednost. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        # ======= SBB ======
        'sbb': """<b>sbb</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se uzima u obzir.</p>""",
        'sbbb': """<b>sbbb</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se uzima u obzir.</p>""",
        'sbbw': """<b>sbbw</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se uzima u obzir.</p>""",
        'sbbl': """<b>sbbl</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se uzima u obzir.</p>""",
        # ======= SHL ======
        'shl': """<b>shl</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Najmanje značajni bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najviše značajne pozicije.</p>""",
        'shlb': """<b>shlb</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Najmanje značajni bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najviše značajne pozicije.</p>""",
        'shlw': """<b>shlw</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Najmanje značajni bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najviše značajne pozicije.</p>""",
        'shll': """<b>shll</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u levo za navedeni broj mesta (neposredni operand ili registar cl).
Najmanje značajni bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow
je nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najviše značajne pozicije.</p>""",
        # ======= SHR ======
        'shr': """<b>shr</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow je
nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        'shrb': """<b>shrb</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow je
nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        'shrw': """<b>shrw</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow je
nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        'shrl': """<b>shrl</b> <em>cnt</em>, <em>dst</em><p>Pomera odredišni operand u desno za navedeni broj mesta (neposredni operand ili registar cl).
Naznačajniji bit dobija vrednost 0. Ukoliko se pomera za više od jednog mesta, indikator overflow je
nedefinisan. Indikator carry ima vrednost poslednjeg bita istisnutog sa najmanje značajne pozicije.</p>""",
        # ======= STC ======
        'stc': """<b>stc</b><p>Postavlja carry indikator na 1.</p>""",
        # ======= STD ======
        'std': """<b>std</b><p>Postavlja direction indikator na 1.</p>""",
        # ======= STOS ======
        'stos': """<b>stos</b><p style='white-space:pre'>U zavisnosti od veličine podrazumevanog operanda, ima sledeće dejstvo:
        stosb # al -> (edi), edi+1 -> edi za d=0, odnosno edi-1 -> edi za d=1
        stosw # ax -> (edi), edi+2 -> edi za d=0, odnosno edi-2 -> edi za d=1
        stosl # eax -> (edi), edi+4 -> edi za d=0, odnosno edi-4 -> edi za d=1
Podrazumevani segmentni registar je es (es:edi).</p>""",
        # ======= SUB ======
        'sub': """<b>sub</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se ne uzima u obzir.</p>""",
        'subb': """<b>subb</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se ne uzima u obzir.</p>""",
        'subw': """<b>subw</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se ne uzima u obzir.</p>""",
        'subl': """<b>subl</b> <em>src</em>, <em>dst</em><p>Oduzima izvorni operand od odredišnog i rezultat smešta u odredišni operand. Prilikom
oduzimanja, zatečeni prenos se ne uzima u obzir.</p>""",
        # ======= TEST ======
        'test': """<b>test</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda, postavlja
indikatore u skladu sa tim, ali ne menja odredišni operand.</p>""",
        'testb': """<b>testb</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda, postavlja
indikatore u skladu sa tim, ali ne menja odredišni operand.</p>""",
        'testw': """<b>testw</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda, postavlja
indikatore u skladu sa tim, ali ne menja odredišni operand.</p>""",
        'testl': """<b>testl</b> <em>src</em>, <em>dst</em><p>Vrši operaciju logičkog I između korespondentnih bita izvornog i odredišnog operanda, postavlja
indikatore u skladu sa tim, ali ne menja odredišni operand.</p>""",
        # ======= XCHG ======
        'xchg': """<b>xchg</b> <em>src</em>, <em>dst</em><p>Zamenjuje vrednosti izvornog i odredišnog operanda.</p>""",
        'xchgb': """<b>xchgb</b> <em>src</em>, <em>dst</em><p>Zamenjuje vrednosti izvornog i odredišnog operanda.</p>""",
        'xchgw': """<b>xchgw</b> <em>src</em>, <em>dst</em><p>Zamenjuje vrednosti izvornog i odredišnog operanda.</p>""",
        'xchgl': """<b>xchgl</b> <em>src</em>, <em>dst</em><p>Zamenjuje vrednosti izvornog i odredišnog operanda.</p>""",
        # ======= XOR ======
        'xor': """<b>xor</b> <em>src</em>, <em>dst</em><p>Vrši operaciju ekskluzivnog ILI između korespondentnih bita izvornog i odredišnog operanda i
rezultat smešta u odredišni.</p>""",
        'xorb': """<b>xorb</b> <em>src</em>, <em>dst</em><p>Vrši operaciju ekskluzivnog ILI između korespondentnih bita izvornog i odredišnog operanda i
rezultat smešta u odredišni.</p>""",
        'xorw': """<b>xorw</b> <em>src</em>, <em>dst</em><p>Vrši operaciju ekskluzivnog ILI između korespondentnih bita izvornog i odredišnog operanda i
rezultat smešta u odredišni.</p>""",
        'xorl': """<b>xorl</b> <em>src</em>, <em>dst</em><p>Vrši operaciju ekskluzivnog ILI između korespondentnih bita izvornog i odredišnog operanda i
rezultat smešta u odredišni.</p>"""
    }
