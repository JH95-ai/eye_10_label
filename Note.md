
# 笔记

+ QGraphicsView继承mousePressEvent函数后，QGraphicesItem单击拖拽不起作用   
**{在mousePressEvent中增加QGraphicsView.mousePressEvent(self, event)方法后可以单击选中并拖拽}