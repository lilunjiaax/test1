
#include <stdlib.h>
#include <stdio.h>


def calcu(int a, int b, int* _array)
{
    int i;
    int sum=0;
    for (i=a+1;i<=b;i++)
    {
        sum += _array[i];
    }
    return sum;
}


def schedule(int m, int _array_size, int* _array)
{
    int i;
    int k1, k2, temp;
    int num=_array_size/m + 1;
    b[20] = [0];
    for (i=1;i<20;i++)
    {
        if (i==1)
        {
            b[i] = num-1;
        }
        else
        {
            b[i] += b[i-1] + num;
        }
    }
    i=2;
    while (b[i] != 0)
    {
        k1 = calcu(b[i-1], b[i-2], _array);
        k2 = calcu(b[i], b[i-1], _array)
        //比较k1,k2的值：微调
        if (k1 > k2)
        {
            temp = calcu()
            b[i-1]--;
        }
        elif (k1 < k2)
        {
            
        }
        i++;
    }
        
}



int main()
    {
    int month;
    while(scanf("%d", &month) != EOF)
        {
        int i;
        int k1, k2;
        int core, renwu;
        int num;
        int b[100]
        scanf("%d%d", &a, &b)
        num = b/a + 1;
        
        printf("%ld", sum);
        printf("\n");
        }
    return 0;
    }
