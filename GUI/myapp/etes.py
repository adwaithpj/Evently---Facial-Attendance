import flet as ft


def main(page):
    table = ft.DataTable(
        border=ft.border.all(2, "red"),
        show_bottom_border=True,
        # columns 里必须添加 DataColumn 类型的控件
        columns=[
            ft.DataColumn(ft.Text("名字")),
            ft.DataColumn(ft.Text("电话")),
            ft.DataColumn(ft.Text("地址"), numeric=True),
        ],
        # rows 里必须添加 DataRow 类型的控件
        # DataRow
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("John")),
                    ft.DataCell(ft.Text("John")),
                    ft.DataCell(ft.Text("John")),
                ])
        ]
    )
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lv.controls.append(table)
    page.add(lv)

    def button_clicked(e):
        b = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("John")),
                ft.DataCell(ft.Text("John")),
                ft.DataCell(ft.Text("John")),
            ])

        table.rows.append(b)
        page.update()
        print("按钮被点击")

    page.add(ft.ElevatedButton(text="添加一行数据", on_click=button_clicked, data=0))


ft.app(target=main)