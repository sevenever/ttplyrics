short length;			//存放Artist和Title一块内存的长度
char song[20];	//
void show_bytes(unsigned char * start, int len){
	int i;
	for(i=0;i<len;i++)
		printf("%.2x",start[i]);
	printf("\n");
}

int CodeFunc(unsigned int Id){
	int tmp1;
	int tmp2=0;
	unsigned int tmp3=0;
	unsigned int EDX;
	int EBX=0;
	int i;
	unsigned int test;
	//0x00015F18
	tmp1 = (Id & 0x0000FF00) >> 8;							//右移8位后为0x0000015F
															//tmp1 0x0000005F
	if ( (Id & 0x00FF0000) == 0 ) {
		EDX = 0x000000FF & ~tmp1;							//CL 0x000000E7
	} else {
		EDX = 0x000000FF & ((Id & 0x00FF0000) >> 16);		//右移16位后为0x00000001
	}
	EDX = EDX | ((0x000000FF & Id) << 8);					//EDX 0x00001801
	EDX = EDX << 8;
	EDX = EDX | (0x000000FF & tmp1);
	EDX = EDX << 8;
	if ( (Id & 0xFF000000) == 0 ) {
		EDX = EDX | (0x000000FF & (~Id));
	} else {
		EDX = EDX | (0x000000FF & (Id >> 24));//右移24位后为0x00000000
	}
	
	tmp3 = EDX;
	//EDX	18015FE7
	
	i=length-1;
	while(i >= 0){
		tmp2 = (int)(*(song + i)) + tmp2 + (tmp2 << (i%2 + 4));
		i--;
	}
	//tmp2 88203cc2
	i=0;
	while(i<=length-1){
		EBX = ((int)(*(song+i)) + EBX ) + (EBX << (i%2 + 3));
		i++;
	}
	//EBX 5CC0B3BA
	
	EDX = EBX | Id;
	EBX = EBX | tmp3;
	
	return  ((tmp2 ^ tmp3) + EDX) * EBX * (tmp2 ^ Id);
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
	printf("Case 1:\n");
	printf("Id is %d, Code is %d\n", 0x00015F18, CodeFunc(0x00015F18));
	printf("Id is %d, Code is %d\n", 0x00015F18, -760311526);
	//************************************************************************
	printf("Case 2:\n");
	printf("Id is %d, Code is %d\n", 127694, CodeFunc(127694));
	printf("Id is %d, Code is %d\n", 127694, -1363687804);
	//************************************************************************
	printf("Case 3:\n");
	printf("Id is %d, Code is %d\n", 105402, CodeFunc(105402));
	printf("Id is %d, Code is %d\n", 105402, -903531896);
	//************************************************************************
		
	return 0;
}
