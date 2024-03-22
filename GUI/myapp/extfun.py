from flet import *
def main(page:Page):
    # page.window_width=800


    #menu item
    menu = ['home','about','settings','contact']
    page_scren = Text(page.window_width,size=30)


    def opendrawer(e):
        if page.window_width < 380:
            page.overlay.append(drawer)
            drawer.offset = transform.Offset(0,0)
        else:
            closewindow()
        page.update()

    #Create collapse menu icon if size under 300
    collapse = Container(
        visible=False,
        content=IconButton(icon="menu",icon_color="white",on_click=opendrawer)

    )



    bar = AppBar(
        title=Text('Flet',size=30,color='white'),
        bgcolor='blue',
        actions=[
            Row()
        ]
    )
    #close sidebard right menu

    def closewindow(e):
        page.overlay.remove(drawer)
        page.update()


    # Create Side mebun if click menu icon


    drawer = Container(
        bgcolor="purple200",
        padding=10,
        margin=margin.only(left=20),
        width=page.window_width,
        height=page.window_height,
        offset=transform.Offset(-3,0),
        animate_offset=animation.Animation(300,"easeIn"),
        content = Column(
            [
                IconButton(icon='close',icon_color='red',on_click=closewindow)

            ]
        )
    )

    # #loop menu and show to actions bar
    for x in menu :
        bar.actions[0].controls.append(
            TextButton(x,
                       visible=True,
                       style=ButtonStyle(
                           color={
                               MaterialState.DEFAULT: 'white',
                                }
                            )
                        )
        ),
        drawer.content.controls.append(
            TextButton(x,
                       visible=True,
                       style=ButtonStyle(
                           color={
                               MaterialState.DEFAULT: 'white',
                           }
                       )
                       )

        )

    def changesize(e):
        page.window_width= int(e.control.value)
        page_scren.value = page.window_width
        page.update()



    # Create slider for change size
    slider_you = Slider(
        label="change size",
        value=int(page.window_width),
        min=200,
        max=800,
        on_change=changesize
    )


    page.add(
        bar,
        page_scren,
        slider_you
    )

    #Now check realtime if you resize window
    def check():
        while True:
            page_scren.value = page.window_width
            page_scren.update()
            if page.window_width < 380:
                for x in bar.actions[1].controls:
                    x.visible = False
                collapse.visible = True
                bar.update()
            else:
                for x in bar.actions[1].controls:
                    x.visible = True
                collapse.visible = False
                bar.update()
            page.update()

app(target=main)