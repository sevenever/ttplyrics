60352FCD   55               PUSH EBP
60352FCE   8BEC             MOV EBP,ESP
60352FD0   83EC 0C          SUB ESP,0C
60352FD3   53               PUSH EBX
60352FD4   8B5D 08          MOV EBX,DWORD PTR SS:[EBP+8]
60352FD7   8BC3             MOV EAX,EBX
60352FD9   8BD3             MOV EDX,EBX
60352FDB   8BCB             MOV ECX,EBX
60352FDD   56               PUSH ESI
60352FDE   C1E8 10          SHR EAX,10
60352FE1   C1EA 08          SHR EDX,8
60352FE4   C1E9 18          SHR ECX,18
60352FE7   84C0             TEST AL,AL
60352FE9   57               PUSH EDI
60352FEA   8855 FF          MOV BYTE PTR SS:[EBP-1],DL

60352FED   75 04            JNZ SHORT ttp_lrcs.60352FF3
60352FEF   8AC2             MOV AL,DL
60352FF1   F6D0             NOT AL

60352FF3   84C9             TEST CL,CL
60352FF5   75 04            JNZ SHORT ttp_lrcs.60352FFB
60352FF7   8ACB             MOV CL,BL
60352FF9   F6D1             NOT CL

60352FFB   33D2             XOR EDX,EDX
60352FFD   8365 F8 00       AND DWORD PTR SS:[EBP-8],0
60353001   8AF3             MOV DH,BL
60353003   8AD0             MOV DL,AL
60353005   0FB645 FF        MOVZX EAX,BYTE PTR SS:[EBP-1]
60353009   C1E2 08          SHL EDX,8
6035300C   0BD0             OR EDX,EAX
6035300E   0FB6C1           MOVZX EAX,CL
60353011   C1E2 08          SHL EDX,8
60353014   0BD0             OR EDX,EAX
60353016   8B45 0C          MOV EAX,DWORD PTR SS:[EBP+C]					# EBP+C 存放一个指针，指向指针A，指针A指向一个结构B，结构B的前2个字节存放((UTF8编码的(Artist和Title字符串相接))的字节长度),从第9个字节起存放(UTF8编码的(Artist和Title字符串相接)
60353019   8955 F4          MOV DWORD PTR SS:[EBP-C],EDX
6035301C   8B30             MOV ESI,DWORD PTR DS:[EAX]
6035301E   8B7E F8          MOV EDI,DWORD PTR DS:[ESI-8]
60353021   8D5F FF          LEA EBX,DWORD PTR DS:[EDI-1]
60353024   85DB             TEST EBX,EBX
************************************************************************************************************
60353026   7C 21            JL SHORT ttp_lrcs.60353049
60353028   8BC3             MOV EAX,EBX
6035302A   6A 02            PUSH 2
6035302C   99               CDQ
6035302D   59               POP ECX
6035302E   F7F9             IDIV ECX
60353030   8B45 F8          MOV EAX,DWORD PTR SS:[EBP-8]
60353033   8BCA             MOV ECX,EDX
60353035   83C1 04          ADD ECX,4
60353038   D3E0             SHL EAX,CL
6035303A   0FBE0C1E         MOVSX ECX,BYTE PTR DS:[ESI+EBX]
6035303E   034D F8          ADD ECX,DWORD PTR SS:[EBP-8]
60353041   03C8             ADD ECX,EAX
60353043   4B               DEC EBX
60353044   894D F8          MOV DWORD PTR SS:[EBP-8],ECX
60353047  ^79 DF            JNS SHORT ttp_lrcs.60353028
************************************************************************************************************
60353049   33DB             XOR EBX,EBX
6035304B   3BFB             CMP EDI,EBX
6035304D   895D 0C          MOV DWORD PTR SS:[EBP+C],EBX
************************************************************************************************************
60353050   7E 26            JLE SHORT ttp_lrcs.60353078
60353052   8B45 0C          MOV EAX,DWORD PTR SS:[EBP+C]
60353055   6A 02            PUSH 2
60353057   99               CDQ
60353058   59               POP ECX
60353059   F7F9             IDIV ECX
6035305B   8BC3             MOV EAX,EBX
6035305D   8BCA             MOV ECX,EDX
6035305F   83C1 03          ADD ECX,3
60353062   D3E0             SHL EAX,CL
60353064   8B4D 0C          MOV ECX,DWORD PTR SS:[EBP+C]
60353067   0FBE0C0E         MOVSX ECX,BYTE PTR DS:[ESI+ECX]
6035306B   03CB             ADD ECX,EBX
6035306D   FF45 0C          INC DWORD PTR SS:[EBP+C]
60353070   397D 0C          CMP DWORD PTR SS:[EBP+C],EDI
60353073   8D1C01           LEA EBX,DWORD PTR DS:[ECX+EAX]
60353076  ^7C DA            JL SHORT ttp_lrcs.60353052
************************************************************************************************************
60353078   8B4D F8          MOV ECX,DWORD PTR SS:[EBP-8]
6035307B   8BD3             MOV EDX,EBX
6035307D   0B55 08          OR EDX,DWORD PTR SS:[EBP+8]
60353080   0B5D F4          OR EBX,DWORD PTR SS:[EBP-C]
60353083   8BC1             MOV EAX,ECX
60353085   334D 08          XOR ECX,DWORD PTR SS:[EBP+8]
60353088   3345 F4          XOR EAX,DWORD PTR SS:[EBP-C]
6035308B   5F               POP EDI
6035308C   5E               POP ESI
6035308D   03C2             ADD EAX,EDX
6035308F   0FAFC3           IMUL EAX,EBX
60353092   0FAFC1           IMUL EAX,ECX
60353095   5B               POP EBX
60353096   C9               LEAVE
60353097   C3               RETN

