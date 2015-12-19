# /usr/bin/env python
# -*- coding: cp936 -*-
from Tkinter import *
class ChessBoard:#��������Ϊһ����
    def __init__(self,root):
        self.row=8
        self.column=8
        self.canvas=Canvas(root,width=400,height=400,bg='#008000')
        self.label=Label(root,text='',bg='#a0522d')
        self.label.grid(columnspan=5,sticky=E+W)
        Label(root,text='',bg='#a0522d',width=2).grid(row=1,sticky=S+N)
        self.canvas.grid(row=1,column=1,columnspan=3)
        Label(root,text='',bg='#a0522d',width=2).grid(row=1,column=4,sticky=S+N)
        Label(root,text='',bg='#a0522d').grid(row=2,columnspan=5,sticky=E+W)
        Button(root,text='Start',command=self.putStep,width=20).grid(row=3,column=0,columnspan=2)
        #START��ť����ʾ��ʼһ����Ϸ
        Label(root,text='',bg='#a0522d').grid(row=3,column=2,sticky=W+E+N+S)
        Button(root,text='Ok',command=self.putStep,width=20).grid(row=3,column=3,columnspan=2)
        #OK��ť��ʾ�ֵ�������
        for i in range(1,8):
            self.canvas.create_line(0,50*i,400,50*i)
            self.canvas.create_line(50*i,0,50*i,400)
    def putStep(self):#ÿ���忪ʼ
        global step#��ʾ�ڼ���
        white,black=0,0#��ʾ�ڡ���������
        x,y,num=findmax(step%2)
        for i in range (8):
            for j in range(8):
                if chess[i][j].fill==0:
                    white=white+1
                if chess[i][j].fill==1:
                    black=black+1
        if white==0:#û��һ������
            self.GameEnd('black win!')
        elif black==0:#û��һ������
            self.GameEnd('white win!')

        elif (black+white)==64:#������������������������ʱ
                if black>white:
                    self.GameEnd('black win!')
                elif black<white:
                    self.GameEnd('white win!')
                elif black==white:
                    self.GameEnd('no winner!')
        elif num==0:#û�п����µ��壬�򰴹���ͣһ��
            step=step+1
            chessboard.label.config(text='you have no place to put chess,please press \'ok\'')
        elif step%2==0 and auto==1:
            autoput(0)
        else:
            self.canvas.bind('<Button-1>',put)
            self.label.config(text='please put your chess')

    #��Ϸ����
    def GameEnd(self,string):#��Ϸ��������ӡ����
            self.label.config(text=string)

class Chess:#�����Ӷ���һ����
    def __init__(self,canvas,x,y,fill):
        self.canvas=canvas
        self.x=x
        self.y=y
        self.fill=fill
        self.oval=canvas.create_oval((self.x*50+5,self.y*50+5),(self.x*50+45,self.y*50+45),width=0)
    def changecolor(self):#�ı���ɫ������Ϳɫ
        if self.fill==0:
            self.canvas.itemconfig(self.oval,fill='white')
        else:
            self.canvas.itemconfig(self.oval,fill='black')

def ChangeChess(row,column,fill):#����һ�������ı�����ס��������ɫ
    fx=[-1,-1,0,1,1,1,0,-1]
    fy=[0,-1,-1,-1,0,1,1,1]

    for i in range(8):
        x=row+fx[i]
        y=column+fy[i]
        cal=0
        while (x<=7)and(y<=7)and(x>=0)and(y>=0):
            if chess[x][y].fill==-1:
                break
            elif chess[x][y].fill==(1-fill):

                x=x+fx[i]
                y=y+fy[i]
                cal=cal+1
            elif chess[x][y].fill==fill:
                for j in range(cal):
                    chess[row+(j+1)*fx[i]][column+(j+1)*fy[i]].fill=fill
                    chess[row+(j+1)*fx[i]][column+(j+1)*fy[i]].changecolor()

                break

def changenumber(row,column,fill):#ÿһ���������Ըı���ɫ����������
    global chess
    fx=[-1,-1,0,1,1,1,0,-1]
    fy=[0,-1,-1,-1,0,1,1,1]
    num=0
    for i in range(8):
        x=row+fx[i]
        y=column+fy[i]
        cal=0
        while (x<=7)and(y<=7)and(x>=0)and(y>=0):
            if chess[x][y].fill==-1:
                break
            elif chess[x][y].fill==(1-fill):
                x=x+fx[i]
                y=y+fy[i]
                cal=cal+1
            elif chess[x][y].fill==fill:
                num=num+cal
                break
    return num

def put(event):#�����¼�����������������
    global chess
    global root
    global step
    global chessboard
    x=event.x
    y=event.y
    fill=step%2
    row=int(x)/50
    column=int(y)/50
    if (chess[row][column].fill==-1)and(changenumber(row,column,fill)>=1):
        #�ж��Ƿ���û�¹������� �� �ܷ����ٸı�һ�����ӵ���ɫ
        chess[row][column].fill=fill
        chess[row][column].changecolor()
        ChangeChess(row,column,chess[row][column].fill)
        chessboard.canvas.unbind('<Button-1>')
        chessboard.label.config(text='press \'ok\'')
        step=step+1


def autoput(fill):#����ģʽ�µ�AI�Զ�����
    global step
    global chess

    row,column,num=findmax(fill)
    if num>0:
        chess[row][column].fill=fill
        chess[row][column].changecolor()
        ChangeChess(row,column,chess[row][column].fill)
    step=step+1
    chessboard.putStep()

def findmax(fill):#�ҳ�����������һ���壬̰�ķ�
    global chess
    max_row=0
    max_column=0
    max_num=0
    for i in range(8):
        for j in range(8):
            num = changenumber(i,j,fill)
            if (chess[i][j].fill==-1)and(num>=max_num):
                max_num=num
                max_row=i
                max_column=j
    return max_row,max_column,max_num

def SelectMode():#ѡ�����˻���˫��ģʽ
    global top
    top=Toplevel(root)
    Button(top,text='one player',command=onePlayer).pack()
    Button(top,text='two player',command=twoPlayer).pack()

def onePlayer():
    global top
    global auto
    auto=1
    top.destroy()
def twoPlayer():
    global top
    global auto
    auto=0
    top.destroy()

def initialize():#��ʼ������Ϊ�ĸ�����
    global chess
    chess[3][3].fill = 0
    chess[3][4].fill = 1
    chess[4][3].fill = 1
    chess[4][4].fill = 0

    chess[3][3].changecolor()
    chess[3][4].changecolor()
    chess[4][3].changecolor()
    chess[4][4].changecolor()

def main():
    global chess#ȫ�ֱ��� ���Ӷ���
    global root#ȫ�ֱ��� ������
    global step#�����Ĳ���
    global chessboard#���̶���
    global auto#�ж��Ƿ�Ϊ����ģʽ
    global top#�Ӵ��ڣ�ѡ��ģʽ��
    root=Tk()
    SelectMode()#ѡ��ģʽ
    step=1
    chessboard=ChessBoard(root)#����һ�����̶���
    chess=[]
    for i in range(8):
        line = []
        for j in range(8):
            line.append(Chess(chessboard.canvas,i,j,-1))#�����ӳ�ʼ��
        chess.append(line)
    initialize()

    root.mainloop()

main()
