    canvas.create_oval(app.width//2 + 100,
    (app.height+120)//2 - 100, app.width//2 - 100, 
    (app.height+120)//2 + 100, outline = 'black', width = 8, fill = 'brown')
    #first eye
    canvas.create_oval((app.width-75)//2 + 15,
    (app.height+55)//2 - 15, (app.width-75)//2 - 15, 
    (app.height+55)//2 + 15, outline = 'black', fill = 'black')
    #second eye
    canvas.create_oval((app.width+75)//2 + 15,
    (app.height+55)//2 - 15, (app.width+75)//2 - 15, 
    (app.height+55)//2 + 15, outline = 'black', fill = 'black')
    #mouse circle
    canvas.create_oval(app.width//2 + 45,
    (app.height+180)//2 - 45, app.width//2 - 45, 
    (app.height+180)//2 + 45, outline = 'black',width = 5, fill = 'tan')
    #nose
    canvas.create_oval(app.width//2 + 15,
    (app.height+150)//2 - 15, app.width//2 - 15, 
    (app.height+150)//2 + 15, outline = 'black', fill = 'black')
    #mouth
    canvas.create_arc((app.width-20)//2 + 10,
    (app.height+210)//2 - 10, (app.width-20)//2 - 10, 
    (app.height+210)//2 + 10, outline = 'black', fill = 'black',style = ARC,
    extent = -180,width = 4)
    canvas.create_arc((app.width+20)//2 + 10,
    (app.height+210)//2 - 10, (app.width+20)//2 - 10, 
    (app.height+210)//2 + 10, outline = 'black', fill = 'black',style = ARC,
    extent = -180,width = 4)