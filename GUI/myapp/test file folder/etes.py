import flet as ft
import requests


update_event_name = ""
update_event_date = ""
update_event_time = ""
update_event_desc = ""
update_event_id   = ""
upcomingdata = []
def main(page):
    table = ft.DataTable(
        border=ft.border.all(2, "red"),
        show_bottom_border=True,
        # columns 里必须添加 DataColumn 类型的控件
        columns=[
            ft.DataColumn(ft.Text("Event Name")),
            ft.DataColumn(ft.Text("Event Owner")),
            ft.DataColumn(ft.Text("Event Category"), numeric=True),
            ft.DataColumn(ft.Text("Event Price"), numeric=True),
            ft.DataColumn(ft.Text("Event Start Date"), numeric=True),
            ft.DataColumn(ft.Text("Event End Date"), numeric=True),
            ft.DataColumn(ft.Text("Event Participation Limit"), numeric=True),
            ft.DataColumn(ft.Text("Event URL"), numeric=True),

        ],
        # rows 里必须添加 DataRow 类型的控件
        # DataRow

    )
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lv.controls.append(table)
    page.add(lv)

    # Logic below
    def get_current_event_data(e,update, data: list):
        global update_event_name, update_event_date, update_event_time, update_event_desc, update_event_id
        try:

            if len(data[0][f'{update}'][0]) > 0:
                # print(f"{update} Event ")
                update_event_name = data[0][f'{update}'][0]['eventName']
                dt_obj = data[0][f'{update}'][0]['eventStartDate']
                update_event_date, update_event_time = dt_obj.split('T')
                update_event_time = update_event_time.rstrip('Z')
                update_event_desc = data[0][f'{update}'][0]['eventDescription']
                update_event_id = data[0][f'{update}'][0]['_id']
                print(update_event_name)  # Comment out this after testing
                print(update_event_date)  # Comment out this after testing
                print(update_event_time)  # Comment out this after testing
                print(update_event_desc)  # Comment out this after testing
                print(update_event_id)  # Comment out this after testing
        except Exception as e:
            print(e)

    def check_event(e):
        global upcomingdata
        upcomingdata=[]
        try:
            response = requests.get('https://api.npoint.io/ac84ca141e388bf2bb9c')
            data = response.json()
            if len(data[0]['today'][0]) > 0:
                get_current_event_data(e,update="today", data=data)
                upcomingdata = data[0]['tomorrow'] + data[0]['upcoming']
            elif len(data[0]['tomorrow'][0]) > 0:
                get_current_event_data(e,update="tomorrow", data=data)
                upcomingdata = data[0]['upcoming']
            elif len(data[0]['upcoming'][0]) > 0:
                get_current_event_data(e,update="upcoming", data=data)
                upcomingdata = data[0]['upcoming'][1:]
        except Exception as e:
            print(e)
        button_clicked(e, upcomingdata)
    # Logic end here

    def button_clicked(e, data: list):
        print(data)
        table.visible = True
        table.rows.clear()
        for event in upcomingdata:
            print(event)
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(event["eventName"])),
                    ft.DataCell(ft.Text(event["eventOwner"])),
                    ft.DataCell(ft.Text(event["eventCategory"])),
                    ft.DataCell(ft.Text(event["price"])),
                    ft.DataCell(ft.Text(event["eventStartDate"].split('T')[0])),
                    ft.DataCell(ft.Text(event["eventEndDate"].split('T')[0])),
                    ft.DataCell(ft.Text(event["eventParticipationLimit"])),
                    ft.DataCell(ft.Text(event["_id"])),
                    ft.DataCell(ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD_ROUNDED,
                        url=event["_id"],
                    ))
                ]
            )
            table.rows.append(row)
        page.update()

    page.add(ft.ElevatedButton(text="添加一行数据", on_click=check_event, data=0))


ft.app(target=main)
