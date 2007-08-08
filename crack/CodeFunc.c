short length;			//存放Artist和Title一块内存的长度
char song[20];	//
void show_bytes(unsigned char * start, int len){
	int i;
	for(i=len-1;i>=0;i--)
		printf("%.2x",start[i]);
	printf("\n");
}

int CodeFunc(unsigned int Id){
	int tmp1;
	int tmp2=0;
	int tmp3=0;
	int i;
	
	//0x00015F18
	tmp1 = (Id & 0x0000FF00) >> 8;							//右移8位后为0x0000015F
															//tmp1 0x0000005F
	if ( (Id & 0x00FF0000) == 0 ) {
		tmp3 = 0x000000FF & ~tmp1;							//CL 0x000000E7
	} else {
		tmp3 = 0x000000FF & ((Id & 0x00FF0000) >> 16);		//右移16位后为0x00000001
	}
	tmp3 = tmp3 | ((0x000000FF & Id) << 8);					//tmp3 0x00001801
	tmp3 = tmp3 << 8;										//tmp3 0x00180100
	tmp3 = tmp3 | (0x000000FF & tmp1);						//tmp3 0x0018015F
	tmp3 = tmp3 << 8;										//tmp3 0x18015F00
	if ( (Id & 0xFF000000) == 0 ) {
		tmp3 = tmp3 | (0x000000FF & (~Id));					//tmp3 0x18015FE7
	} else {
		tmp3 = tmp3 | (0x000000FF & (Id >> 24));			//右移24位后为0x00000000
	}
	
	//tmp3	18015FE7
	
	i=length-1;
	while(i >= 0){
		printf("%d\n",*(song + i));
		tmp2 = (*(song + i)) + tmp2 + (tmp2 << (i%2 + 4));
		show_bytes(&tmp2,4);
		i--;
	}
	//tmp2 88203cc2
	i=0;
	tmp1=0;
	while(i<=length-1){
		tmp1 = (*(song+i)) + tmp1 + (tmp1 << (i%2 + 3));
		i++;
	}
	//EBX 5CC0B3BA
	
	//EDX = EBX | Id;
	//EBX = EBX | tmp3;
	show_bytes(&tmp1,4);
	show_bytes(&tmp2,4);
	show_bytes(&tmp3,4);
	return  ((tmp2 ^ tmp3) + (tmp1 | Id)) * (tmp1 | tmp3) * (tmp2 ^ Id);
}

int main(){
	length = 20;
	song[0] = 0xE5;
	song[1] = 0xA4;
	song[2] = 0xA7;
	song[3] = 0xE5;
	song[4] = 0xA1;
	song[5] = 0x9A;
	song[6] = 0xE7;
	song[7] = 0x88;
	song[8] = 0xB1;
	song[9] = 0x50;
	song[10] = 0x4C;
	song[11] = 0x41;
	song[12] = 0x4E;
	song[13] = 0x45;
	song[14] = 0x54;
	song[15] = 0x41;
	song[16] = 0x52;
	song[17] = 0x49;
	song[18] = 0x55;
	song[19] = 0x4D;
	
	//************************************************************************
	//printf("Case 1:\n");
	//printf("Id is %d, Code is %d\n", 0x00015F18, CodeFunc(0x00015F18));
	//printf("Id is %d, Code is %d\n", 0x00015F18, -760311526);
	//************************************************************************
	//printf("Case 2:\n");
	//printf("Id is %d, Code is %d\n", 127694, CodeFunc(127694));
	//printf("Id is %d, Code is %d\n", 127694, -1363687804);
	//************************************************************************
	//printf("Case 3:\n");
	//printf("Id is %d, Code is %d\n", 105402, CodeFunc(105402));
	//printf("Id is %d, Code is %d\n", 105402, -903531896);
	//************************************************************************
	//printf("Case 4:\n");
	//printf("Id is %d, Code is %d\n", 73918, CodeFunc(73918));
	//printf("Id is %d, Code is %d\n", 73918, 2016822932);
	//************************************************************************
	length = 39;
	song[0] = 0xe9;
	song[1] = 0xbd;
	song[2] = 0x90;
	song[3] = 0xe8;
	song[4] = 0xb1;
	song[5] = 0xab;
	song[6] = 0xe3;
	song[7] = 0x80;
	song[8] = 0x81;
	song[9] = 0xe6;
	song[10] = 0xbd;
	song[11] = 0x98;
	song[12] = 0xe8;
	song[13] = 0xb6;
	song[14] = 0x8a;
	song[15] = 0xe4;
	song[16] = 0xba;
	song[17] = 0x91;
	song[18] = 0xe9;
	song[19] = 0x87;
	song[20] = 0x8e;
	song[21] = 0xe7;
	song[22] = 0x99;
	song[23] = 0xbe;
	song[24] = 0xe5;
	song[25] = 0x90;
	song[26] = 0x88;
	song[27] = 0xe4;
	song[28] = 0xb9;
	song[29] = 0x9f;
	song[30] = 0xe6;
	song[31] = 0x9c;
	song[32] = 0x89;
	song[33] = 0xe6;
	song[34] = 0x98;
	song[35] = 0xa5;
	song[36] = 0xe5;
	song[37] = 0xa4;
	song[38] = 0xa9;
	printf("Case 5:\n");
	printf("Id is %d, Code is %d\n", 115313, CodeFunc(115313));
	printf("Id is %d, Code is %d\n", 115313, 1719309312);
		
	return 0;
}
