import flet as ft

# Define the LoginView function
def login_view(page: ft.Page):
    ref_username = ft.Ref[ft.TextField]()
    ref_password = ft.Ref[ft.TextField]()
    wrong_password = ft.Ref[str]("")  # Reference for the wrong password warning

    def login(e):
        entered_username = ref_username.current.value
        entered_password = ref_password.current.value

        # For demonstration purposes, check if password is "password"
        if entered_password != "password":
            wrong_password.current = "Incorrect password. Please try again."
            return

        print(entered_username)
        print(entered_password)
        print(page.width)
        page.go("/otp")

    # Define a variable to control image display based on screen size
    display_image = page.width >= 1200  # Change this threshold based on your requirements

    # Construct the login view
    login_page = ft.View(
        "/",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=0,
        controls=[
            ft.Row(
                wrap=False,
                spacing=1,
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="assets/svg/login_page.svg"
                        ),
                        visible=display_image,  # Only display the image on large screens
                    ),
                    ft.VerticalDivider(width=40, color="white"),
                    ft.Card(
                        elevation=0,
                        color="#ffffff",
                        surface_tint_color="#ffffff",
                        content=ft.Container(
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        alignment=ft.Alignment(-0.8, -0.5),
                                        content=ft.Image(
                                            src="assets/Logo/Logo.svg",
                                            width=247,
                                            height=57,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                        visible=not display_image,  # Hide logo on smaller screens
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    ft.Container(
                                        width=620,
                                        content=ft.Column(
                                            tight=True,
                                            spacing=0,
                                            alignment=ft.Alignment(-0.8, -0.5),
                                            controls=[
                                                ft.Text(
                                                    "Welcome Back",
                                                    font_family="DM Sans Regular",
                                                    size=32,
                                                ),
                                                ft.Text(
                                                    "Login to use the evently Application",
                                                    font_family="DM Sans Regular",
                                                    size=16,
                                                ),
                                            ]
                                        )
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    ft.TextField(ref=ref_username, label="Username", width=620, height=68, text_align="left"),
                                    ft.TextField(ref=ref_password, label="Password", password=True, can_reveal_password=True, width=620, height=68),
                                    ft.Text(
                                        ref=wrong_password,
                                        font_family="DM Sans Regular",
                                        size=14,
                                        color="red",
                                    ),
                                    ft.Row(
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=350,
                                        controls=[
                                            ft.Checkbox(label="Remember me", value=True,
                                                        on_change=lambda e: print("Remember me"),
                                                        label_style=ft.TextStyle(size=16, font_family="DM Sans Regular")),
                                            ft.Text(
                                                "Forgot Password?",
                                                font_family="DM Sans Regular",
                                                size=16,
                                                color="#2580B7",
                                            ),
                                        ]
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    ft.FilledTonalButton(
                                        style=ft.ButtonStyle(
                                            color='white',
                                            animation_duration= 100,
                                            bgcolor={
                                                ft.MaterialState.DEFAULT: "#57BAF5",
                                                ft.MaterialState.HOVERED: "#2580B7"
                                            },
                                            surface_tint_color="#FF5C00",
                                            elevation=0,
                                            shape={
                                                ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                                            },
                                        ),
                                        text="Login",
                                        on_click=login,
                                        width=620,
                                        height=68,
                                    ),
                                    ft.VerticalDivider(width=10, color="white"),
                                    ft.Row(
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                "Don't have an Account?",
                                                font_family="DM Sans Regular",
                                                size=16,
                                            ),
                                            ft.Text(
                                                "Register Here",
                                                font_family="DM Sans Regular",
                                                color="#2580B7",
                                                size=16,
                                            ),
                                        ]
                                    ),
                                    ft.VerticalDivider(width=100, color="white"),
                                ]
                            ),
                            padding=20,
                            margin=20,
                        ),
                        width=756,
                    )
                ]
            )
        ]
    )

    return login_page


# Define the OTPView function
def otp_view(page: ft.Page):
    # Define the OTP view here, similar to the LoginView

    return ft.View(
        "/otp",
        # Define the OTP view contents
    )


# Define the main function
# Define the main function
def main(page: ft.Page):
    # Define the route function to mimic flet-route behavior
    def route(url, view):
        return {"url": url, "view": view}

    app_routes = [
        route("/", login_view),
        route("/otp", otp_view),
    ]

    # Routing logic
    page.on("DOMContentLoaded", async def on_load():
        for route_ in app_routes:
            if page.route == route_["url"]:
                view = route_["view"](page)
                await ft.update(page, view))

    # Set up page properties
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    page.window_min_width = 1280
    page.window_max_width = 1920
    page.window_min_height = 720
    page.window_max_height = 1080
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "DM Sans regular": "assets/google_fonts/dmsans_static/DMSans-Regular.ttf",
        "DM Sans Bold": "assets/google_fonts/dmsans_static/DMSans-Bold.ttf",
        "DM Sans Italic": "assets/google_fonts/dmsans_static/DMSans-Italic.ttf",
        "DM Sans Bold Italic": "assets/google_fonts/dmsans_static/DMSans-BoldItalic.ttf",
        "DM Sans Medium": "assets/google_fonts/dmsans_static/DMSans-Medium.ttf",
        "DM Sans Medium Italic": "assets/google_fonts/dmsans_static/DMSans-MediumItalic.ttf",
        "DM Sans SemiBold": "assets/google_fonts/dmsans_static/DMSans-SemiBold.ttf",
        "DM Sans SemiBold Italic": "assets/google_fonts/dmsans_static/DMSans-SemiBoldItalic.ttf",
        "DM Sans Light": "assets/google_fonts/dmsans_static/DMSans-Light.ttf",
        "DM Sans Light Italic": "assets/google_fonts/dmsans_static/DMSans-LightItalic.ttf",
        "DM Sans ExtraLight": "assets/google_fonts/dmsans_static/DMSans-ExtraLight.ttf",
        "DM Sans ExtraLight Italic": "assets/google_fonts/dmsans_static/DMSans-ExtraLightItalic.ttf",
        "DM Sans Thin": "assets/google_fonts/dmsans_static/DMSans-Thin.ttf",
        "DM Sans Thin Italic": "assets/google_fonts/dmsans_static/DMSans-ThinItalic.ttf",
    }

    # Initial page load
    for route_ in app_routes:
        if page.route == route_["url"]:
            view = route_["view"](page)
            ft.update(page, view)

# Run the app
ft.app(target=main)
