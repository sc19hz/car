#include <stdio.h>   
#include <stdlib.h>   
#include <string.h>
#include <math.h>   
#include <time.h>
int map[20][20] =
{
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0 },
    { 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
};

//节点结构体   
typedef struct Node
{
    int f, g, h;
    int row;        //该节点所在行
    int col;        //该节点所在列
    int direction;      //parent节点要移动的方向就能到达本节点
    struct Node* parent;
} Node, * PNode;
//复用结构体
typedef struct reusedPath
{
    PNode start;
    PNode end;
    float length;
    int times;
};

//OPEN CLOSED 表结构体
typedef struct Stack
{
    PNode npoint;
    struct Stack* next;
} Stack, * PStack;

int it = 0;//循环次数
int directionIndex = 0;     //方向
int direction[256];     //方向数组
int rows = 20;          //地图行数
int cols = 20;          //地图列数
int G_OFFSET = 1;       //每个图块G值的增加值
int destinationRow;     //目标所在行
int destinationCol;     //目标所在列
int startRow;           //起始行
int startCol;           //起始列
int canMoveIndex = 0;       //可以通行的地图图块索引
int tileSize = 1;       //图块大小
int ran[2]; //随机点
int snode[6][200];
int pnode[6][200];

PStack Open = NULL;
PStack Closed = NULL;

float caculateMean(int i,int a[6][200]) {
    int j;
    float sum = 0;
    for (j = 0; j < 200; j++) {
        sum = sum + a[i][j];
    }
    sum = sum / 200;
    return sum;
}

//选取OPEN表上f值最小的节点，返回该节点地址
Node* getNodeFromOpen()
{
    PStack temp = Open->next, min = Open->next, minp = Open;
    PNode minx;

    if (temp == NULL)
        return NULL;

    while (temp->next != NULL)
    {
        if ((temp->next->npoint->f) < (min->npoint->f))
        {
            min = temp->next;
            minp = temp;
        }

        temp = temp->next;
    }

    minx = min->npoint;
    temp = minp->next;
    minp->next = minp->next->next;

    free(temp);

    return minx;
}

//判断节点是否相等，相等，不相等   
short Equal(PNode a, PNode b)
{
    if ((a->row == b->row) && (a->col == b->col))
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

//判断节点是否属于OPEN表，是则返回节点地址，否则返回空地址
PNode BelongInOpen(PNode u)
{
    PStack temp = Open->next;

    if (temp == NULL)
        return NULL;

    while (temp != NULL)
    {
        if (Equal(u, temp->npoint))
        {
            return temp->npoint;
        }
        else
        {
            temp = temp->next;
        }
    }

    return NULL;
}

//判断节点是否属于CLOSED表，是则返回节点地址，否则返回空地址
PNode BelongInClosed(PNode u)
{
    PStack temp = Closed->next;

    if (temp == NULL)
        return NULL;

    while (temp != NULL)
    {
        if (Equal(u, temp->npoint))
        {
            return temp->npoint;
        }
        else
        {
            temp = temp->next;
        }
    }

    return NULL;
}

//把节点放入OPEN表中
void PutintoOpen(Node* u)
{
    Stack* temp;
    temp = (Stack*)malloc(sizeof(Stack));
    temp->npoint = u;
    temp->next = Open->next;
    Open->next = temp;
}

//把节点放入CLOSED表中
void PutintoClosed(Node* u)
{
    Stack* temp;
    temp = (Stack*)malloc(sizeof(Stack));
    temp->npoint = u;
    temp->next = Closed->next;
    Closed->next = temp;
}

//得到该图块的H值
//曼哈顿
int getH(int row, int col)
{
    int a = abs(destinationRow - row) + abs(destinationCol - col);
    float b = a / 2;
    return (b);
}
//计算对角线距离
float getH_dia(int row, int col)
{
    int dr = abs(destinationRow - row);
    int dc = abs(destinationCol - col);
    int min;
    int h = getH(row, col);
    float dia;
    if (dr >= dc) {
        min = dc;
    }
    else
    {
        min = dr;
    }
    dia = sqrt(2) * min + abs(dr-dc);
    return dia;
}
//计算欧式距离
float getH_eul(int row, int col) {
    int dr = abs(destinationRow - row);
    int dc = abs(destinationCol - col);
    float h = sqrt((dr * dr) + (dc * dc));
    return h;
}
//计算欧式平方距离
float getH_eulsqu(int row, int col) {
    int dr = abs(destinationRow - row);
    int dc = abs(destinationCol - col);
    float h = (dr * dr) + (dc * dc);
    return h;
}
//新启发
float getH_new(int row, int col) {
    float da[2], db[2];//a[0]:row diffrence
    float moda, modb,cos,sin;
    float h = getH_dia(row,col);
    da[0] = row - startRow;
    da[1] = col - startCol;
    db[0] = destinationRow - startRow;
    db[1] = destinationCol - startCol;
    moda = sqrt((da[0] * da[0]) + (da[1] * da[1]));
    modb = sqrt((db[0] * db[0]) + (db[1] * db[1]));
   
    cos = ((da[0] * db[0]) + (da[1] * db[1]))/(moda* modb);
    sin = sqrt(1 - (cos * cos));
    return h + sin;
}

//得到该位置所在地图行
int getRowPosition(int y)
{
    return (y / tileSize);
}

//得到该位置所在地图列   
int getColPosition(int x)
{
    return (x / tileSize);
}

//检测该图块是否可通行
short isCanMove(int col, int row)
{
    if (col < 0 || col >= cols)
        return 0;
    if (row < 0 || row >= rows)
        return 0;

    return map[col][row] == canMoveIndex;
}

/*检查坐标是否在open列表里*/
PNode checkOpen(int row, int col)
{
    PStack temp = Open->next;

    if (temp == NULL)
        return NULL;

    while (temp != NULL)
    {
        if ((temp->npoint->row == row) && (temp->npoint->col == col))
        {
            return temp->npoint;
        }
        else
        {
            temp = temp->next;
        }
    }

    return NULL;
}

/*检查坐标是否在closed列表里*/
short isInClose(int row, int col)
{
    PStack temp = Closed->next;

    if (temp == NULL)
        return 0;

    while (temp != NULL)
    {
        if ((temp->npoint->row == row) && (temp->npoint->col == col))
        {
            return 1;
        }
        else
        {
            temp = temp->next;
        }
    }

    return 0;
}

/*一步处理逻辑*/
void creatSeccessionNode(PNode bestNode, int row, int col,int ind=0)
{
    int g = bestNode->g + G_OFFSET;

    if (!isInClose(row, col))
    {
        PNode oldNode = NULL;

        //如果在open列表里则更新, 如果不在则添加至open列表
        if ((oldNode = checkOpen(row, col)) != NULL)
        {
            if (oldNode->g < g)
            {
                oldNode->parent = bestNode;
                oldNode->g = g;
                oldNode->f = g + oldNode->h;
            }
        }
        else
        {
            PNode node = (PNode)malloc(sizeof(Node));
            node->parent = bestNode;
            node->g = g;
            switch (ind)
            {
            case 0:
            {
                node->h = getH(row, col);
                break;
            }
            case 1:
            {
                node->h = getH_dia(row, col);
                break;
            }
            case 2:
            {
                node->h = getH_eul(row, col);
                break;
            }
            case 3: 
            {
                node->h = getH_eulsqu(row, col);
                break;
            }
            case 4:
            {
                node->h = getH_new(row, col);
                break;
            }
            }
            node->f = node->g + node->h;
            node->row = row;
            node->col = col;
            directionIndex++;
            node->direction = directionIndex;
            PutintoOpen(node);
        }
    }
}

/**
 * 根据传入的节点生成子节点
 * @param bestNode
 * @param destinationRow
 * @param destinationCol
 */
void seachSeccessionNode(PNode bestNode,int ind=0)
{
    int row, col;

    //上部节点
    if (isCanMove(row = bestNode->row - 1, col = bestNode->col))
    {
        creatSeccessionNode(bestNode, row, col,ind);
    }

    //下部节点
    if (isCanMove(row = bestNode->row + 1, col = bestNode->col))
    {
        creatSeccessionNode(bestNode, row, col, ind);
    }

    //左部节点
    if (isCanMove(row = bestNode->row, col = bestNode->col - 1))
    {
        creatSeccessionNode(bestNode, row, col, ind);
    }

    //右部节点
    if (isCanMove(row = bestNode->row, col = bestNode->col + 1))
    {
        creatSeccessionNode(bestNode, row, col,ind);
    }

    //右上
    if (isCanMove(row = bestNode->row-1, col = bestNode->col + 1))
    {
        creatSeccessionNode(bestNode, row, col, ind);
    }

    //左上
    if (isCanMove(row = bestNode->row-1, col = bestNode->col - 1))
    {
        creatSeccessionNode(bestNode, row, col, ind);
    }

    //右下
    if (isCanMove(row = bestNode->row+1, col = bestNode->col + 1))
    {
        creatSeccessionNode(bestNode, row, col, ind);
    }
    //左下
    if (isCanMove(row = bestNode->row+1, col = bestNode->col - 1))
    {
        creatSeccessionNode(bestNode, row, col, ind);
    }
    
    //传入节点放入close列表
    PutintoClosed(bestNode);
}

//遍历open链表
void printfOpenData()
{
    PStack temp = Open->next;
    PNode p_node;

    if (temp == NULL)
        return;

    while (temp != NULL)
    {
        PStack head = temp;
        temp = temp->next;
        p_node = head->npoint;
        printf("Open库数据! [%d,%d]\n", p_node->col, p_node->row);
        free(p_node);
        free(head);
        Open->next = temp;
    }

    printf("\nOpen库数据 数据全部清除\n");

    return;
}

//遍历close链表
void printfClosedData()
{
    PStack temp = Closed->next;
    PNode p_node;

    if (temp == NULL)
        return;

    while (temp != NULL)
    {
        PStack head = temp;
        temp = temp->next;
        p_node = head->npoint;
        printf("Closed库数据! [%d,%d]\n", p_node->col, p_node->row);
        free(p_node);
        free(head);
        Closed->next = temp;
    }

    printf("\nClosed库数据 数据全部清除\n");

    return;
}

void getPath(int startX, int StartY, int destinationX, int destinationY, int ind = 0)
{
    PNode startNode = (PNode)malloc(sizeof(Node));
    PNode bestNode = NULL;
    int index = 0;

    destinationRow = getRowPosition(destinationY);
    destinationCol = getColPosition(destinationX);
    startRow = getRowPosition(StartY);
    startCol = getColPosition(startX);
    startNode->parent = NULL;
    startNode->row = getRowPosition(StartY);
    startNode->col = getColPosition(startX);
    startNode->g = 0;

   

    switch (ind)
    {
    case 0:
    {
        startNode->h = getH(startNode->row, startNode->col);
        break;
    }
    case 1:
    {
        startNode->h = getH_dia(startNode->row, startNode->col);
        break;
    }
    case 2:
    {
        startNode->h = getH_eul(startNode->row, startNode->col);
        break;
    }
    case 3:
    {
        startNode->h = getH_eulsqu(startNode->row, startNode->col);
        break;
    }
    case 4:
    {
        startNode->h = getH_new(startNode->row, startNode->col);
        break;
    }
    case 5:
    {
        startNode->h = getH(startNode->row, startNode->col);
        break;
    }
    }
   
    if (ind != 5) {
        startNode->f = startNode->g + startNode->h;
    }
    else
    {
        startNode->f = startNode->h;
    }
    startNode->direction = 0;

    PutintoOpen(startNode);

    while (1)
    {
        //从OPEN表中取出f值最小的节点
        bestNode = getNodeFromOpen();

        if (bestNode == NULL)
        {
            printf("未找到路径\n");
            return;
        }
        else if (bestNode->row == destinationRow && bestNode->col == destinationCol)
        {
            //寻路结束，打印相关信息
            PNode _Node = bestNode;
            int nodeSum = 0;
            int nodeIndex = 0;

            //printf("搜索节点=%d\n", index);
            snode[ind][it] = index;

            while (_Node->parent != NULL)
            {
                //printf("x:%d  y:%d  direction = %d \n", _Node->col, _Node->row, _Node->direction);
                _Node = _Node->parent;
                nodeSum += 1;
            }

            //printf("路径距离=%d\n", nodeSum);
            pnode[ind][it] = nodeSum;

            _Node = bestNode;
            nodeIndex = nodeSum - 1;

            while (_Node->parent != NULL && nodeIndex >= 0)
            {
                PNode _NodeParent = _Node->parent;

               //printf("x:%d  y:%d  direction = %d \n", _Node->col, _Node->row, _Node->direction);

                if (_NodeParent->col - _Node->col == 0 && _NodeParent->row - _Node->row == +1)
                {
                    direction[nodeIndex] = 1;
                }
                else if (_NodeParent->col - _Node->col == 0 && _NodeParent->row - _Node->row == -1)
                {
                    direction[nodeIndex] = 2;
                }
                else if (_NodeParent->col - _Node->col == +1 && _NodeParent->row - _Node->row == 0)
                {
                    direction[nodeIndex] = 3;
                }
                else if (_NodeParent->col - _Node->col == -1 && _NodeParent->row - _Node->row == 0)
                {
                    direction[nodeIndex] = 4;
                }
                else if (_NodeParent->col - _Node->col == -1 && _NodeParent->row - _Node->row == -1)
                {
                    direction[nodeIndex] =5;
                }
                else if (_NodeParent->col - _Node->col == +1 && _NodeParent->row - _Node->row == -1)
                {
                    direction[nodeIndex] = 6;
                }
                else if (_NodeParent->col - _Node->col == -1 && _NodeParent->row - _Node->row == +1)
                {
                    direction[nodeIndex] = 7;
                }
                else if (_NodeParent->col - _Node->col == +1 && _NodeParent->row - _Node->row == +1)
                {
                    direction[nodeIndex] = 8;
                }
                else
                {
                    direction[nodeIndex] = 0;
                }

                nodeIndex -= 1;
                _Node = _Node->parent;
            }

            for (nodeIndex = 0; nodeIndex < nodeSum; nodeIndex++)
            {
                //printf("direction[%d]=%d\n", nodeIndex, direction[nodeIndex]);
            }

            return;
        }

        index++;
        seachSeccessionNode(bestNode,ind);
    }
}

void rd() {
    
    int a, b;
    int c[2];
    a = rand() % 20;
    b = rand() % 20;
    while (map[a][b] == 1) {
        a = rand() % 20;
        b = rand() % 20;
    }
    //printf("a=%i,j=%i\n",a,b);
    ran[0] = a;
    ran[1] = b;
}



//主函数
void main()
{
    
    srand((unsigned)time(NULL));
    int i = 0;
    int j = 0;
    float t;
    int sx, sy,tx,ty;
    for (j = 0; j < 200; j++) {
        it = j;
        rd();
        sx = ran[1];
        sy = ran[0];
        rd();
        tx = ran[1];
        ty = ran[0];

        for (i = 0; i < 6; i++) {
            
            //初始操作，建立open和closed表
            Open = (PStack)malloc(sizeof(Stack));
            Open->next = NULL;
            Closed = (PStack)malloc(sizeof(Stack));
            Closed->next = NULL;

            getPath(sx, sy, tx, ty, i);
            
            /*printfOpenData();
            printfClosedData();*/

            free(Open);
            free(Closed);
           
           
        }

        //printf("\n\n");
    }
    for (i = 0; i < 6; i++) {
        t = caculateMean(i, snode);
        printf("搜索节点个数：%f\n",t);
        t = caculateMean(i, pnode);
        printf("路径长度：%f\n", t);
        printf("\n");
    }
}